#!/usr/bin/env python3
"""Synchronize the canonical root frontend into the standalone website mirror."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEBSITE = ROOT / "website"

# Only browser/runtime files belong in the mirror. Source work happens in ROOT.
MIRROR_FILES = (
    "index.html",
    "admin.html",
    "favicon.svg",
    "css/styles.css",
    "css/admin.css",
    "js/core.js",
    "js/puzzle-modes.js",
    "js/race.js",
    "js/submissions.js",
    "js/library.js",
    "js/app.js",
    "js/i18n.js",
    "puzzles_embedded.js",
    "netto_translations_en.js",
    "netto_frontend_puzzles.js",
    "netto_race_sets.js",
    "netto_race_pool.js",
    "netto_breinkrakers.js",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differing_files() -> list[str]:
    different: list[str] = []
    for relative in MIRROR_FILES:
        source = ROOT / relative
        target = WEBSITE / relative
        if not source.is_file():
            raise FileNotFoundError(f"Canonical file is missing: {source}")
        if not target.is_file() or digest(source) != digest(target):
            different.append(relative)
    return different


def sync() -> list[str]:
    changed = differing_files()
    for relative in changed:
        source = ROOT / relative
        target = WEBSITE / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report drift without changing files",
    )
    args = parser.parse_args()

    changed = differing_files() if args.check else sync()
    if changed:
        action = "Out of sync" if args.check else "Synchronized"
        print(f"{action}: {', '.join(changed)}")
        return 1 if args.check else 0

    print("website/ is identical to the canonical frontend.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
