#!/usr/bin/env node
'use strict';

const { spawnSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

const PACKAGE_VERSION = require('../package.json').version;
const INSTALL_SH = path.join(__dirname, '..', 'scripts', 'install.sh');
const CURL_FALLBACK =
  'curl -fsSL https://raw.githubusercontent.com/BiuBiuHu/opc-skills/main/scripts/install.sh | bash';

const HELP = `opc-skills ${PACKAGE_VERSION}

Install, update, or diagnose the BiuBiuHu/opc-skills Codex skill.

Usage:
  npx opc-skills <command>

Commands:
  install, update  Update a verified source and synchronize skill installations
  doctor           Check source provenance, baselines, versions, and local overrides
  path             Print the primary Codex path
  help             Show this help
  version          Print this CLI version

Existing ~/.agents/skills, ~/.cursor/skills and ~/.claude/skills are synchronized.
Local edits are three-way merged; conflicts leave all installations unchanged.
Options: --root PATH, --source CLEAN_GIT_REPO, --base PRIOR_REF.
git and Python 3.9+ are required. No editor settings or credential stores are loaded.

This CLI wraps scripts/install.sh so curl|bash and npx stay aligned.

No-network / no-npm fallback:
  ${CURL_FALLBACK}
`;

function printHelp() {
  process.stdout.write(HELP);
}

function fail(message) {
  process.stderr.write(`error: ${message}\n`);
  process.exit(1);
}

function runInstallSh(command, options = []) {
  if (!fs.existsSync(INSTALL_SH)) {
    fail(`install script not found at ${INSTALL_SH}`);
  }

  const result = spawnSync('bash', [INSTALL_SH, command, ...options], { stdio: 'inherit' });
  if (result.error) {
    if (result.error.code === 'ENOENT') {
      process.stderr.write(
        'error: bash is required to run opc-skills install scripts.\n' +
          `\nfallback:\n  ${CURL_FALLBACK}\n`,
      );
      process.exit(1);
    }
    fail(result.error.message);
  }

  process.exit(result.status === null ? 1 : result.status);
}

const args = process.argv.slice(2);
const command = args[0];

if (args.length === 0) {
  printHelp();
  process.exit(0);
}

if (command === 'help' || command === '-h' || command === '--help') {
  printHelp();
  process.exit(0);
}

if (command === 'version' || command === '-v' || command === '--version') {
  process.stdout.write(`${PACKAGE_VERSION}\n`);
  process.exit(0);
}

const allowed = new Set(['install', 'update', 'doctor', 'path']);
if (!allowed.has(command)) {
  process.stderr.write(`error: unknown command: ${args.join(' ')}\n\n`);
  printHelp();
  process.exit(1);
}

runInstallSh(command, args.slice(1));
