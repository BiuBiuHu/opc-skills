import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import sys
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('opc_sync', REPO / 'scripts/sync-local-skills.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class LocalSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='opc-sync-test-')
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name).resolve()
        self.source = self.work / 'source'
        self.source.mkdir()
        self.git(self.source, 'init', '-q', '-b', 'main')
        self.git(self.source, 'config', 'user.name', 'Fixture')
        self.git(self.source, 'config', 'user.email', 'fixture@invalid')
        self.payload = self.source / sync.PAYLOAD
        self.payload.mkdir(parents=True)
        self.entry = b'---\nname: opc-skills\ndescription: Fixture skill.\n---\n# Fixture\n'
        self.write('SKILL.md', self.entry)
        self.write('VERSION', b'1.0.0\n')
        self.write('references/rules.md', b'alpha\nbeta\ngamma\ndelta\n')
        self.write('scripts/run.sh', b'#!/bin/sh\nexit 0\n', 0o755)
        # Legacy checkout tests also need a root entry, as real root-skill repos have.
        for payload_file in self.payload.rglob('*'):
            if payload_file.is_file():
                target = self.source / payload_file.relative_to(self.payload)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(payload_file, target)
        self.initial = self.commit()
        self.root = self.work / 'profile'
        (self.root / '.agents/skills').mkdir(parents=True)
        self.state = self.root / '.local/state/opc-skills'
        self.primary = self.root / '.codex/skills/opc-skills'
        self.secondary = self.root / '.agents/skills/opc-skills'

    def git(self, repo, *args):
        return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.DEVNULL).decode().strip()

    def write(self, name, data, mode=0o644):
        p = self.payload / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        p.chmod(mode)

    def commit(self):
        self.git(self.source, 'add', '.')
        self.git(self.source, 'commit', '-qm', 'fixture')
        return self.git(self.source, 'rev-parse', 'HEAD')

    def apply(self, base=None):
        with sync.install_lock(self.state):
            return sync.install(self.root, self.source, self.state, base, True)

    def digests(self):
        return [sync.tree_digest(p) for p in (self.primary, self.secondary)]

    def test_fresh_install_updates_both_existing_surfaces(self):
        self.apply()
        self.assertEqual((self.primary / 'SKILL.md').read_bytes(), self.entry)
        self.assertEqual((self.secondary / 'VERSION').read_text().strip(), '1.0.0')
        self.assertFalse((self.root / '.cursor').exists())
        self.assertTrue((self.primary / 'scripts/run.sh').stat().st_mode & 0o111)
        self.assertEqual(sync.doctor(self.root, self.state, True)['status'], 'ok')

    def test_three_way_update_preserves_distinct_local_rules_and_unknown_files(self):
        self.apply()
        for p, first in [(self.primary, b'primary'), (self.secondary, b'secondary')]:
            (p / 'references/rules.md').write_bytes(first + b'\nbeta\ngamma\ndelta\n')
            (p / 'personal.txt').write_text('keep')
        self.write('references/rules.md', b'alpha\nbeta\ngamma\nnew-upstream\n')
        self.write('VERSION', b'1.0.1\n')
        self.commit()
        report = self.apply()
        for p, first in [(self.primary, b'primary'), (self.secondary, b'secondary')]:
            self.assertEqual((p / 'references/rules.md').read_bytes(), first + b'\nbeta\ngamma\nnew-upstream\n')
            self.assertEqual((p / 'personal.txt').read_text(), 'keep')
            self.assertEqual((p / 'VERSION').read_text().strip(), '1.0.1')
        self.assertTrue(Path(report['backups']).exists())
        self.assertEqual(sync.doctor(self.root, self.state, True)['status'], 'ok')

    def test_conflict_changes_neither_installation(self):
        self.apply()
        (self.secondary / 'references/rules.md').write_text('local rewrite\n')
        before = self.digests()
        self.write('references/rules.md', b'upstream rewrite\n')
        self.commit()
        with self.assertRaisesRegex(sync.SyncError, 'No installations changed'):
            self.apply()
        self.assertEqual(self.digests(), before)

    def test_unmanaged_copy_needs_explicit_base_and_then_keeps_local_edit(self):
        self.primary.mkdir(parents=True)
        (self.primary / 'SKILL.md').write_bytes(self.entry)
        (self.primary / 'VERSION').write_text('1.0.0\n')
        (self.primary / 'references').mkdir()
        (self.primary / 'references/rules.md').write_text('local\nbeta\ngamma\ndelta\n')
        before = sync.tree_digest(self.primary)
        with self.assertRaisesRegex(sync.SyncError, 'trusted baseline'):
            self.apply()
        self.assertEqual(sync.tree_digest(self.primary), before)
        self.apply(self.initial)
        self.assertTrue((self.primary / 'references/rules.md').read_text().startswith('local'))

    def test_corrupt_baseline_blocks_doctor_and_update(self):
        self.apply()
        meta = json.loads((self.primary / sync.META).read_text())
        (self.state / 'baselines' / meta['baseline'] / 'SKILL.md').write_text('corrupt')
        before = self.digests()
        with self.assertRaises(sync.SyncError):
            sync.doctor(self.root, self.state, True)
        with self.assertRaises(sync.SyncError):
            self.apply()
        self.assertEqual(self.digests(), before)

    def test_removed_upstream_file_and_local_delete_are_handled(self):
        self.apply()
        (self.payload / 'scripts/run.sh').unlink()
        (self.primary / 'references/rules.md').unlink()
        self.commit()
        self.apply()
        self.assertFalse((self.primary / 'references/rules.md').exists())
        self.assertFalse((self.primary / 'scripts/run.sh').exists())
        self.assertTrue((self.secondary / 'references/rules.md').exists())

    def test_upstream_delete_local_modify_is_a_conflict(self):
        self.apply()
        (self.primary / 'scripts/run.sh').write_text('local script')
        (self.payload / 'scripts/run.sh').unlink()
        self.commit()
        before = self.digests()
        with self.assertRaises(sync.SyncError):
            self.apply()
        self.assertEqual(self.digests(), before)

    def test_existing_alias_is_kept_and_unmanaged_symlink_is_rejected(self):
        self.secondary.symlink_to(self.primary, target_is_directory=True)
        self.apply()
        self.assertTrue(self.secondary.is_symlink())
        self.assertEqual(sync.doctor(self.root, self.state, True)['status'], 'ok')
        self.secondary.unlink()
        other = self.work / 'unrelated'
        other.mkdir()
        self.secondary.symlink_to(other, target_is_directory=True)
        with self.assertRaisesRegex(sync.SyncError, 'symlink'):
            self.apply()
        self.assertEqual(list(other.iterdir()), [])

    def test_clean_legacy_git_is_backed_up_but_dirty_one_is_not_overwritten(self):
        self.primary.parent.mkdir(parents=True)
        subprocess.run(['git', 'clone', '-q', str(self.source), str(self.primary)], check=True)
        report = self.apply()
        self.assertFalse((self.primary / '.git').exists())
        self.assertTrue((Path(report['backups']) / '0/.git').exists())
        shutil.rmtree(self.primary)
        subprocess.run(['git', 'clone', '-q', str(self.source), str(self.primary)], check=True)
        (self.primary / 'SKILL.md').write_text('dirty')
        with self.assertRaisesRegex(sync.SyncError, 'local changes'):
            self.apply()
        self.assertEqual((self.primary / 'SKILL.md').read_text(), 'dirty')

    def test_failure_on_second_swap_rolls_back_first(self):
        self.apply()
        before = self.digests()
        self.write('VERSION', b'2.0.0\n')
        self.commit()
        replace = os.replace
        def fail_second(src, dest):
            if Path(src).name.startswith('.opc-stage-') and Path(dest) == self.secondary:
                raise OSError('injected swap failure')
            return replace(src, dest)
        with patch.object(sync.os, 'replace', side_effect=fail_second):
            with self.assertRaisesRegex(OSError, 'injected'):
                self.apply()
        self.assertEqual(self.digests(), before)
        self.assertEqual(sync.doctor(self.root, self.state, True)['status'], 'ok')

    def test_lock_and_source_changes_block_before_installation(self):
        with sync.install_lock(self.state):
            with self.assertRaisesRegex(sync.SyncError, 'lock'):
                with sync.install_lock(self.state):
                    pass
        (self.source / 'SKILL.md').write_text('uncommitted')
        with self.assertRaisesRegex(sync.SyncError, 'local changes'):
            sync.source_repo(self.root, self.source)
        self.assertFalse(self.primary.exists())

    def test_bash_and_node_entrypoints_use_isolated_root(self):
        for name, command in [('bash', ['bash', str(REPO / 'scripts/install.sh')]),
                              ('node', ['node', str(REPO / 'bin/opc-skills.js')])]:
            isolated = self.work / name
            result = subprocess.run(command + ['install', '--root', str(isolated), '--source', str(self.source)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((isolated / '.codex/skills/opc-skills' / sync.META).exists())


    def test_source_cache_updates_offline_and_rejects_dirty_or_other_origin(self):
        with patch.object(sync, 'REPO_URL', str(self.source)):
            cache = sync.source_repo(self.root)
            self.write('VERSION', b'1.0.1\n')
            head = self.commit()
            self.assertEqual(self.git(sync.source_repo(self.root), 'rev-parse', 'HEAD'), head)
            (cache / 'local.txt').write_text('preserve')
            with self.assertRaisesRegex(sync.SyncError, 'local changes'):
                sync.source_repo(self.root)
            (cache / 'local.txt').unlink()
            self.git(cache, 'remote', 'set-url', 'origin', 'https://invalid.invalid/other.git')
            with self.assertRaisesRegex(sync.SyncError, 'another repository'):
                sync.source_repo(self.root)

    def test_payload_symlink_and_parent_symlink_are_rejected(self):
        (self.payload / 'references/escape.md').symlink_to('/etc/passwd')
        self.commit()
        with self.assertRaisesRegex(sync.SyncError, 'symlink'):
            self.apply()
        self.assertFalse(self.primary.exists())
        (self.payload / 'references/escape.md').unlink()
        self.commit()
        shutil.rmtree(self.secondary.parent)
        outside = self.work / 'outside'
        outside.mkdir()
        self.secondary.parent.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(sync.SyncError, 'parent crosses'):
            self.apply()
        self.assertEqual(list(outside.iterdir()), [])

    def test_snapshot_excludes_untracked_files_and_source_drift_is_detected(self):
        (self.payload / 'untracked.txt').write_text('must not ship')
        self.assertNotIn('untracked.txt', sync.snapshot(self.source)[1])
        (self.payload / 'untracked.txt').unlink()
        self.apply()
        meta = json.loads((self.secondary / sync.META).read_text())
        meta['sourceCommit'] = 'a' * 40
        (self.secondary / sync.META).write_text(json.dumps(meta))
        with self.assertRaisesRegex(sync.SyncError, 'drift'):
            sync.doctor(self.root, self.state, True)

    def test_invalid_local_entry_does_not_become_a_healthy_install(self):
        self.apply()
        (self.primary / 'SKILL.md').write_text('not a skill')
        before = self.digests()
        with self.assertRaisesRegex(sync.SyncError, 'frontmatter'):
            sync.doctor(self.root, self.state, True)
        with self.assertRaisesRegex(sync.SyncError, 'frontmatter'):
            self.apply()
        self.assertEqual(self.digests(), before)

    def test_curl_style_stdin_bootstrap_is_offline_and_isolated(self):
        helper = self.source / 'scripts/sync-local-skills.py'
        helper.parent.mkdir(exist_ok=True)
        shutil.copy2(REPO / 'scripts/sync-local-skills.py', helper)
        self.commit()
        mock_bin = self.work / 'mock-bin'
        mock_bin.mkdir()
        real_git = shutil.which('git')
        wrapper = mock_bin / 'git'
        wrapper.write_text('#!' + sys.executable + '\nimport os,sys\nargs=[%r if x==%r else x for x in sys.argv[1:]]\nos.execv(%r,[%r]+args)\n' % (str(self.source), sync.REPO_URL, real_git, real_git))
        wrapper.chmod(0o755)
        env = os.environ.copy()
        env['PATH'] = str(mock_bin) + os.pathsep + env['PATH']
        isolated = self.work / 'stdin-profile'
        result = subprocess.run(['bash', '-s', '--', 'install', '--root', str(isolated), '--source', str(self.source)], input=(REPO / 'scripts/install.sh').read_text(), env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((isolated / '.codex/skills/opc-skills' / sync.META).is_file())

    def test_report_write_failure_rolls_back_targets_and_previous_report(self):
        self.apply()
        before = self.digests()
        report = (self.state / 'last-install.json').read_bytes()
        self.write('VERSION', b'2.0.0\n')
        self.commit()
        replace = os.replace
        def fail_report(src, dest):
            if Path(dest) == self.state / 'last-install.json':
                raise OSError('injected report failure')
            return replace(src, dest)
        with patch.object(sync.os, 'replace', side_effect=fail_report):
            with self.assertRaisesRegex(OSError, 'report failure'):
                self.apply()
        self.assertEqual(self.digests(), before)
        self.assertEqual((self.state / 'last-install.json').read_bytes(), report)

if __name__ == '__main__':
    unittest.main()
