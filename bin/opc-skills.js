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
  install, update  Clone or fast-forward into ~/.codex/skills/opc-skills
  doctor           Print install paths, VERSION, git identity, and symlink health
  path             Print the primary Codex path
  help             Show this help
  version          Print this CLI version

If ~/.cursor/skills or ~/.claude/skills already exist, install also
symlinks there. Extra parent dirs are never created. git is required.
No editor config or secrets are read.

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

function runInstallSh(command) {
  if (!fs.existsSync(INSTALL_SH)) {
    fail(`install script not found at ${INSTALL_SH}`);
  }

  const result = spawnSync('bash', [INSTALL_SH, command], { stdio: 'inherit' });
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
if (args.length !== 1 || !allowed.has(command)) {
  process.stderr.write(`error: unknown command: ${args.join(' ')}\n\n`);
  printHelp();
  process.exit(1);
}

runInstallSh(command);
