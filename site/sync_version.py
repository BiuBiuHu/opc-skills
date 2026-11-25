#!/usr/bin/env python3
"""Write the repo VERSION into the marketing site so the badge cannot go stale."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
VERSION_FILE = ROOT / "VERSION"
VERSION_SPAN = re.compile(
    r"(<([^>\s]+)([^>]*\s)?data-opc-version(\s[^>]*)?>)(.*?)(</\2>)",
    re.S,
)


def read_version() -> str:
    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    if not version:
        raise SystemExit("VERSION is empty")
    return version


def replace_version(html: str, version: str) -> str:
    def repl(match: re.Match[str]) -> str:
        return f"{match.group(1)}{version}{match.group(6)}"

    updated, count = VERSION_SPAN.subn(repl, html)
    if count == 0:
        raise SystemExit("no data-opc-version markers found")
    return updated


def main() -> int:
    version = read_version()
    (SITE / "version.txt").write_text(version + "\n", encoding="utf-8")
    for path in (SITE / "index.html", SITE / "zh" / "index.html"):
        path.write_text(replace_version(path.read_text(encoding="utf-8"), version), encoding="utf-8")
        print(f"synced {path.relative_to(ROOT)} -> v{version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
