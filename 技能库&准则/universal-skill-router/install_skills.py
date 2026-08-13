#!/usr/bin/env python3
"""Copy selected canonical skill packages into another Agent skill directory."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CATALOG = REPO / "catalog" / "skills.json"
TIER_RANK = {"maintained": 0, "router": 1, "community": 2, "tool-bundled": 3, "bundled": 4, "variant": 9}


def normalize(name: str) -> str:
    name = name.casefold().strip().replace("_", "-")
    return re.sub(r"-+", "-", re.sub(r"\s+", "-", name))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", action="append", required=True, help="exact catalog skill name; repeatable")
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--force", action="store_true", help="replace an existing target package")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not CATALOG.is_file():
        raise SystemExit("catalog missing; run: python scripts/build_catalog.py")
    records = json.loads(CATALOG.read_text(encoding="utf-8"))["skills"]

    selected = []
    for requested in args.name:
        wanted = normalize(requested)
        matches = [record for record in records if record["name"] == wanted and record["tier"] != "variant"]
        if not matches:
            raise SystemExit(f"canonical skill not found: {requested}")
        matches.sort(key=lambda record: (TIER_RANK.get(str(record["tier"]), 8), str(record["path"])))
        selected.append(matches[0])

    target_root = args.target.expanduser().resolve()
    for record in selected:
        skill_file = REPO / str(record["path"])
        source_package = skill_file.parent
        destination = target_root / normalize(str(record["name"]))
        print(f"{record['name']}: {source_package} -> {destination}")
        if args.dry_run:
            continue
        target_root.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            if not args.force:
                raise SystemExit(f"target exists (use --force): {destination}")
            shutil.rmtree(destination)
        # The repository router is a single root file; installing it must not
        # copy this entire repository into the target.
        if skill_file == REPO / "SKILL.md":
            destination.mkdir(parents=True)
            shutil.copy2(skill_file, destination / "SKILL.md")
        else:
            shutil.copytree(source_package, destination)


if __name__ == "__main__":
    main()
