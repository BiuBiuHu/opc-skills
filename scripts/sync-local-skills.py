#!/usr/bin/env python3
"""Synchronize committed skill payloads; retain local edits using verified baselines."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid
from urllib.parse import urlsplit

REPO_URL = 'https://github.com/BiuBiuHu/opc-skills.git'
PAYLOAD = 'plugins/opc-skills/skills/opc-skills/'
META = '.opc-install.json'


class SyncError(Exception):
    pass


def git(repo, *args):
    p = subprocess.run(['git', '-C', str(repo), *args], capture_output=True)
    if p.returncode:
        raise SyncError('Git operation failed; check repository, ref, and connectivity.')
    return p.stdout


def sha(data):
    return hashlib.sha256(data).hexdigest()


def relative(name):
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or not p.parts or str(p) != name or name == META:
        raise SyncError('Unsafe payload path.')
    return p


def normalized_origin(value):
    value = value.strip().rstrip('/')
    if value.startswith('ssh://'):
        parsed = urlsplit(value)
        value = 'https://' + (parsed.hostname or '') + parsed.path
    else:
        value = re.sub(r'^[^@/]+@([^/:]+):', r'https://\1/', value)
    return value.removesuffix('.git')


def clean_repo(path):
    if Path(git(path, 'rev-parse', '--show-toplevel').decode().strip()).resolve() != path.resolve():
        raise SyncError('Source must be the repository root.')
    if git(path, 'status', '--porcelain').strip():
        raise SyncError('Source has local changes; preserve and commit them before updating.')


def snapshot(repo, ref='HEAD'):
    commit = git(repo, 'rev-parse', '--verify', '--end-of-options', ref + '^{commit}').decode().strip()
    entries = git(repo, 'ls-tree', '-rz', commit).split(b'\0')
    items = []
    for entry in entries:
        if not entry:
            continue
        info, raw = entry.split(b'\t', 1)
        mode, kind, obj = info.decode().split()
        name = raw.decode('utf-8')
        items.append((name, mode, kind, obj))
    bundled = any(name == PAYLOAD + 'SKILL.md' for name, *_ in items)
    files = {}
    for name, mode, kind, obj in items:
        if bundled:
            if not name.startswith(PAYLOAD):
                continue
            rel = name[len(PAYLOAD):]
        else:
            rel = name
            if not (rel in ('SKILL.md', 'VERSION', 'LICENSE') or
                    rel.startswith(('agents/', 'references/', 'templates/')) or
                    rel in ('scripts/start_rnd.sh', 'scripts/check_release_integrity.sh',
                            'scripts/check_project_coupling.sh', 'scripts/prepare_post_release_content.sh',
                            'docs/subagent-optimization-plan.md', 'docs/subagent-runtime-invocation-design.md')):
                continue
        relative(rel)
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise SyncError('Payload contains a symlink, submodule, or unsupported file.')
        files[rel] = (git(repo, 'cat-file', 'blob', obj), 0o755 if mode == '100755' else 0o644)
    if not {'SKILL.md', 'VERSION'} <= files.keys():
        raise SyncError('Source lacks a skill entry or VERSION.')
    validate_entry(files['SKILL.md'][0])
    return commit, files


def validate_entry(data):
    m = re.match(rb'^---\n(.*?)\n---(?:\n|$)', data, re.S)
    if not m or not re.search(rb'''(?m)^name:\s*['\"]?opc-skills['\"]?\s*$''', m.group(1)):
        raise SyncError('Invalid opc-skills entry frontmatter.')


def manifest(files):
    return {name: {'sha256': sha(data), 'mode': mode}
            for name, (data, mode) in sorted(files.items())}


def write_file(path, data, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    path.chmod(mode)


def atomic_json(path, value):
    with tempfile.NamedTemporaryFile(prefix='.opc-report-', dir=path.parent, delete=False) as f:
        temp = Path(f.name)
        f.write((json.dumps(value, indent=2) + '\n').encode())
    try:
        temp.chmod(0o600)
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def baseline_id(files):
    return sha(json.dumps(manifest(files), sort_keys=True).encode())


def save_baseline(state, files):
    ident = baseline_id(files)
    root = state / 'baselines' / ident
    if not root.exists():
        root.mkdir(parents=True)
        for name, (data, mode) in files.items():
            write_file(root / name, data, mode)
    # Verify immutable content even if this baseline was stored by an earlier run.
    for name, (data, _) in files.items():
        if not (root / name).is_file() or (root / name).read_bytes() != data:
            raise SyncError('Stored baseline is corrupt; restore it before updating.')
    return ident


def load_baseline(target, state):
    try:
        if (target / META).is_symlink():
            raise SyncError('Installation metadata must not be a symlink.')
        meta = json.loads((target / META).read_text())
        if meta['format'] != 1 or not re.fullmatch('[a-f0-9]{64}', meta['baseline']):
            raise ValueError()
        if not re.fullmatch('[a-f0-9]{40,64}', meta['sourceCommit']):
            raise ValueError()
        files = {}
        for name, item in meta['files'].items():
            relative(name)
            data = (state / 'baselines' / meta['baseline'] / name).read_bytes()
            if sha(data) != item['sha256'] or item['mode'] not in (0o644, 0o755):
                raise ValueError()
            files[name] = (data, item['mode'])
        if not {'SKILL.md', 'VERSION'} <= files.keys() or baseline_id(files) != meta['baseline']:
            raise ValueError()
        return meta, files
    except (KeyError, ValueError, OSError, TypeError, AttributeError):
        raise SyncError('Missing or invalid baseline/provenance; restore it, do not guess from VERSION.')


def read_local(root, name):
    relative(name)
    path = root / name
    for ancestor in [path, *path.parents]:
        if ancestor == root.parent:
            break
        if ancestor.is_symlink():
            raise SyncError('A managed payload path crosses a local symlink: ' + name)
    if not path.exists():
        return None
    if not path.is_file():
        raise SyncError('A payload file is shadowed by a directory: ' + name)
    return path.read_bytes(), stat.S_IMODE(path.stat().st_mode)


def merge_value(old, local, incoming):
    # Absence is meaningful: preserve local deletion unless upstream also changed it.
    if local == old:
        return incoming
    if incoming == old or local == incoming:
        return local
    if old is None or local is None or incoming is None:
        raise SyncError('delete/modify or independent-add conflict')
    od, om = old
    ld, lm = local
    nd, nm = incoming
    if ld == od:
        data = nd
    elif nd == od or ld == nd:
        data = ld
    else:
        if any(b'\0' in d for d in (od, ld, nd)):
            raise SyncError('binary conflict')
        with tempfile.TemporaryDirectory(prefix='opc-merge-') as temp:
            p = Path(temp)
            for name, data in [('local', ld), ('base', od), ('incoming', nd)]:
                (p / name).write_bytes(data)
            result = subprocess.run(['git', 'merge-file', '-p', str(p / 'local'),
                                     str(p / 'base'), str(p / 'incoming')], capture_output=True)
        if result.returncode:
            raise SyncError('content conflict')
        data = result.stdout
    if lm != om and nm != om and lm != nm:
        raise SyncError('mode conflict')
    return data, lm if lm != om else nm


def tree_digest(root):
    if not root.exists():
        return None
    h = hashlib.sha256()
    for path in sorted(root.rglob('*')):
        # Git internals can update automatically; legacy dirty state is checked separately.
        rel = path.relative_to(root)
        if '.git' in rel.parts:
            continue
        h.update(str(rel).encode())
        if path.is_symlink():
            h.update(b'L' + os.readlink(path).encode())
        elif path.is_file():
            h.update(b'F' + path.read_bytes() + str(stat.S_IMODE(path.stat().st_mode)).encode())
        else:
            h.update(b'D')
    return h.hexdigest()


def targets(root, explicit_root=False):
    primary = root / '.codex/skills/opc-skills'
    if not explicit_root and os.environ.get('CODEX_HOME'):
        primary = Path(os.environ['CODEX_HOME']).expanduser().resolve() / 'skills/opc-skills'
    paths = [primary]
    for name in ['.agents', '.cursor', '.claude']:
        parent = root / name / 'skills'
        if parent.is_dir():
            paths.append(parent / 'opc-skills')
    aliases = []
    result = []
    for p in paths:
        for parent in p.parents:
            if parent == root or parent == Path('/'):
                break
            if parent.is_symlink():
                raise SyncError('Installation parent crosses an unmanaged symlink.')
        if p.is_symlink():
            if p != primary and p.resolve() == primary.resolve():
                aliases.append(p)
                continue
            raise SyncError('Unmanaged installation symlink; preserve it and select a dedicated --root.')
        result.append(p)
    return result, aliases


def source_repo(root, source=None):
    if source:
        p = Path(source).expanduser().resolve()
        clean_repo(p)
        return p
    p = root / '.local/share/opc-skills/source'
    if p.exists():
        clean_repo(p)
        if normalized_origin(git(p, 'remote', 'get-url', 'origin').decode()) != normalized_origin(REPO_URL):
            raise SyncError('Source cache belongs to another repository; refusing to modify it.')
        git(p, 'fetch', 'origin', 'main')
        git(p, 'switch', 'main')
        git(p, 'merge', '--ff-only', 'origin/main')
    else:
        p.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(['git', 'clone', '--branch', 'main', REPO_URL, str(p)], capture_output=True)
        if result.returncode:
            raise SyncError('Cannot clone source cache; existing installations were not changed.')
    return p


@contextmanager
def install_lock(state):
    state.mkdir(parents=True, exist_ok=True)
    state.chmod(0o700)
    path = state / 'install.lock'
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise SyncError('Another installation is active or left a lock; inspect it before retrying.')
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        yield
    finally:
        path.unlink(missing_ok=True)


def legacy_base(target, source, base):
    if (target / '.git').exists():
        if not (target / '.git').is_dir():
            raise SyncError('Linked Git worktree cannot be converted automatically.')
        clean_repo(target)
        origin = normalized_origin(git(target, 'remote', 'get-url', 'origin').decode())
        if origin not in (normalized_origin(REPO_URL), normalized_origin(str(source.resolve()))):
            raise SyncError('Legacy checkout belongs to another repository.')
        if len(re.findall(b'^worktree ', git(target, 'worktree', 'list', '--porcelain'), re.M)) != 1:
            raise SyncError('Legacy checkout has other worktrees; preserve it and use a dedicated --root.')
        return snapshot(target)[1]
    if base:
        return snapshot(source, base)[1]
    raise SyncError('Unmanaged copy has no trusted baseline. Review its prior commit and use --base REF; it will be backed up and three-way merged.')


def install(root, source, state, base=None, explicit_root=False):
    commit, incoming = snapshot(source)
    dests, aliases = targets(root, explicit_root)
    plans = []
    conflicts = []
    for dest in dests:
        if dest.exists() and not dest.is_dir():
            raise SyncError('Installation path is not a directory.')
        if (dest / META).is_file():
            _, old = load_baseline(dest, state)
        elif dest.exists() and any(dest.iterdir()):
            old = legacy_base(dest, source, base)
        else:
            old = {}
        values = {}
        for name in old.keys() | incoming.keys():
            try:
                values[name] = merge_value(old.get(name), read_local(dest, name), incoming.get(name))
            except SyncError as e:
                conflicts.append(str(dest) + ': ' + name + ' (' + str(e) + ')')
        plans.append({'dest': dest, 'values': values, 'before': tree_digest(dest)})
    if conflicts:
        # Do not emit file contents or apply one target while another is blocked.
        raise SyncError('No installations changed. Resolve conflicts first:\n' + '\n'.join(conflicts))
    ident = save_baseline(state, incoming)
    meta = {'format': 1, 'sourceCommit': commit, 'baseline': ident,
            'version': incoming['VERSION'][0].decode().strip(), 'files': manifest(incoming)}
    run = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    backup_root = state / 'backups' / run
    staged = []
    swapped = []
    try:
        for index, plan in enumerate(plans):
            dest = plan['dest']
            dest.parent.mkdir(parents=True, exist_ok=True)
            stage = Path(tempfile.mkdtemp(prefix='.opc-stage-', dir=dest.parent))
            plan['stage'] = stage
            staged.append(stage)
            if dest.exists():
                shutil.copytree(dest, stage, dirs_exist_ok=True, symlinks=True,
                                ignore=lambda directory, names: ['.git'] if Path(directory) == dest and '.git' in names else [])
                backup = backup_root / str(index)
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(dest, backup, symlinks=True)
            for name, value in plan['values'].items():
                if value is None:
                    (stage / name).unlink(missing_ok=True)
                else:
                    write_file(stage / name, *value)
            write_file(stage / META, (json.dumps(meta, indent=2) + '\n').encode(), 0o600)
            if not (stage / 'SKILL.md').is_file() or not (stage / 'VERSION').is_file():
                raise SyncError('Local deletion removed a required entry; resolve it first.')
            validate_entry((stage / 'SKILL.md').read_bytes())
        if backup_root.exists():
            recovery = {'sourceCommit': commit, 'targets': {str(i): str(p['dest']) for i, p in enumerate(plans)}}
            write_file(backup_root / 'manifest.json', (json.dumps(recovery, indent=2) + '\n').encode(), 0o600)
        # Detect edits while preparing the transaction, before the first replacement.
        for plan in plans:
            if tree_digest(plan['dest']) != plan['before']:
                raise SyncError('Installation changed concurrently; no update applied.')
        for plan in plans:
            dest = plan['dest']
            previous = dest.with_name('.opc-previous-' + uuid.uuid4().hex)
            if dest.exists():
                os.replace(dest, previous)
            try:
                os.replace(plan['stage'], dest)
            except BaseException:
                if previous.exists():
                    os.replace(previous, dest)
                raise
            swapped.append((dest, previous))
        for plan in plans:
            if json.loads((plan['dest'] / META).read_text()) != meta:
                raise SyncError('Post-install provenance check failed.')
        report = {'sourceCommit': commit, 'version': meta['version'],
                  'targets': [p['dest'].as_posix() for p in plans], 'aliases': [str(p) for p in aliases],
                  'backups': str(backup_root) if backup_root.exists() else None}
        atomic_json(state / 'last-install.json', report)
    except BaseException:
        for dest, previous in reversed(swapped):
            shutil.rmtree(dest)
            if previous.exists():
                os.replace(previous, dest)
        raise
    finally:
        for stage in staged:
            if stage.exists():
                shutil.rmtree(stage)
    for _, previous in swapped:
        if previous.exists():
            shutil.rmtree(previous)
    return report


def doctor(root, state, explicit_root=False):
    dests, aliases = targets(root, explicit_root)
    rows = []
    heads = set()
    for dest in dests:
        if not dest.exists():
            raise SyncError('Installation missing: ' + str(dest))
        meta, old = load_baseline(dest, state)
        if not (dest / 'SKILL.md').is_file() or (dest / 'VERSION').read_text().strip() != meta['version']:
            raise SyncError('Entry/version does not match installation provenance.')
        validate_entry((dest / 'SKILL.md').read_bytes())
        overrides = [n for n, value in old.items() if read_local(dest, n) != value]
        rows.append({'path': str(dest), 'sourceCommit': meta['sourceCommit'],
                     'version': meta['version'], 'localOverrides': overrides})
        heads.add((meta['sourceCommit'], meta['baseline'], meta['version']))
    if len(heads) != 1:
        raise SyncError('Installation source/version drift; synchronize before using both copies.')
    return {'status': 'ok', 'installations': rows, 'aliases': [str(p) for p in aliases]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['install', 'update', 'doctor', 'path'], nargs='?', default='install')
    parser.add_argument('--root', type=Path, help='Installation home/prefix; isolates every path for tests or a separate profile.')
    parser.add_argument('--source', type=Path, help='Use a clean local Git source instead of fetching main.')
    parser.add_argument('--base', help='Explicit prior source ref for first adoption of an unmanaged copy.')
    args = parser.parse_args()
    root = (args.root or Path.home()).expanduser().resolve()
    if root == Path('/'):
        raise SyncError('Use a dedicated installation home.')
    state = root / '.local/state/opc-skills'
    if args.command == 'path':
        print(targets(root, args.root is not None)[0][0])
    elif args.command == 'doctor':
        print(json.dumps(doctor(root, state, args.root is not None), indent=2))
    else:
        with install_lock(state):
            repo = source_repo(root, args.source)
            result = install(root, repo, state, args.base, args.root is not None)
        print(json.dumps(result, indent=2))
        print('opc-skills is ready for the next turn. Local overrides and backups are retained.')


if __name__ == '__main__':
    try:
        if sys.version_info < (3, 9):
            raise SyncError('Python 3.9 or later is required.')
        main()
    except (SyncError, OSError) as e:
        print('error: ' + str(e), file=sys.stderr)
        sys.exit(1)
