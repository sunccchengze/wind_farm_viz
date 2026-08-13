#!/usr/bin/env python3
"""Validate catalog integrity, import provenance, and repository size policy."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "AGENTS.md",
    "SKILL.md",
    "catalog/sources.lock.json",
    "catalog/import-report.json",
    "catalog/skills.json",
    "governance/CONSTITUTION.md",
    "governance/QUALITY_GATES.md",
    "skills/human-writing/SKILL.md",
    "skills/victor-design/SKILL.md",
    "skills/openwiki/SKILL.md",
    "skills/screencoder/SKILL.md",
    "tools/openwiki/package.json",
    "tools/openwiki/LICENSE",
    "tools/screencoder/README.md",
    "tools/screencoder/UPSTREAM.md",
    "tools/screencoder/LICENSE",
]
COMMUNITY_PRUNED_EXTENSIONS = {
    ".zip", ".tar", ".gz", ".7z", ".rar", ".mp4", ".mov", ".avi",
    ".gif", ".psd", ".pptx", ".docx", ".pdf", ".ttf", ".woff",
    ".woff2", ".png", ".jpg", ".jpeg", ".webp", ".icns", ".mp3",
}
MAX_FILES = 10_000
MAX_BYTES = 128 * 1024 * 1024
MAX_COMMUNITY_FILE_BYTES = 500_000


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []

    for relative in REQUIRED:
        if not (REPO / relative).is_file():
            fail(errors, f"missing required file: {relative}")

    lock_path = REPO / "catalog/sources.lock.json"
    report_path = REPO / "catalog/import-report.json"
    catalog_path = REPO / "catalog/skills.json"
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    for source in lock["aggregateSources"] + lock["directSources"]:
        if not re.fullmatch(r"[0-9a-f]{40}", source.get("commit", "")):
            fail(errors, f"invalid pinned commit for source {source.get('id')}")
    for source in lock["directSources"]:
        installed = REPO / source["installedAt"]
        if not installed.exists():
            fail(errors, f"direct source is not installed: {source['id']} -> {installed}")

    report = json.loads(report_path.read_text(encoding="utf-8"))
    report_records = report["canonical"] + report["variants"]
    for record in report_records:
        output = REPO / record["outputPath"]
        if not output.is_file():
            fail(errors, f"imported skill missing: {record['outputPath']}")
            continue
        if sha256(output) != record["sha256"]:
            fail(errors, f"imported skill hash mismatch: {record['outputPath']}")
        if set(Path(record["sourcePath"]).parts) & {"test", "tests", "fixtures"}:
            fail(errors, f"test fixture was imported as a skill: {record['sourcePath']}")

    expected_report_count = report["counts"]["canonicalSkills"] + report["counts"]["variantSkills"]
    if len(report_records) != expected_report_count:
        fail(errors, "import report counts do not match its records")

    community_root = REPO / "skills/community"
    for path in community_root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.casefold() in COMMUNITY_PRUNED_EXTENSIONS:
            fail(errors, f"pruned media/archive present in community import: {path.relative_to(REPO)}")
        if path.stat().st_size > MAX_COMMUNITY_FILE_BYTES:
            fail(errors, f"oversized community file: {path.relative_to(REPO)}")

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    discovered = [
        path for path in REPO.rglob("SKILL.md")
        if ".git" not in path.relative_to(REPO).parts and "node_modules" not in path.relative_to(REPO).parts
    ]
    if catalog["count"] != len(catalog["skills"]) or catalog["count"] != len(discovered):
        fail(errors, f"catalog is stale: catalog={catalog['count']} discovered={len(discovered)}")
    for record in catalog["skills"]:
        path = REPO / record["path"]
        if not path.is_file() or sha256(path) != record["sha256"]:
            fail(errors, f"catalog hash/path mismatch: {record['path']}")

    missing_licenses = [name for name, value in report["licenses"].items() if value is None]
    if missing_licenses:
        warnings.append(
            "aggregate collections without a discoverable collection-level license: "
            + ", ".join(sorted(missing_licenses))
        )

    files = [
        path for path in REPO.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(REPO).parts and "node_modules" not in path.relative_to(REPO).parts
    ]
    total_bytes = sum(path.stat().st_size for path in files)
    if len(files) > MAX_FILES:
        fail(errors, f"repository file policy exceeded: {len(files)} > {MAX_FILES}")
    if total_bytes > MAX_BYTES:
        fail(errors, f"repository byte policy exceeded: {total_bytes} > {MAX_BYTES}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(
        f"Validated {len(discovered)} skills, {len(report_records)} imported bodies, "
        f"{len(files)} files, {total_bytes / (1024 * 1024):.1f} MiB."
    )
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
