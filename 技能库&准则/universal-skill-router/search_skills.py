#!/usr/bin/env python3
"""Search catalog metadata and print the best skill entry points."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CATALOG = REPO / "catalog" / "skills.json"
TIER_BONUS = {
    "maintained": 8,
    "router": 7,
    "community": 5,
    "tool-bundled": 4,
    "bundled": 3,
    "variant": 0,
}


def normalize(text: str) -> str:
    return text.casefold().replace("_", "-")


def query_terms(query: str) -> list[str]:
    query = normalize(query)
    terms = re.findall(r"[a-z0-9][a-z0-9.+#/-]*|[\u3400-\u9fff]+", query)
    expanded: list[str] = []
    for term in terms:
        expanded.append(term)
        if re.fullmatch(r"[\u3400-\u9fff]{4,}", term):
            expanded.extend(term[index : index + 2] for index in range(len(term) - 1))
    return list(dict.fromkeys(expanded))


def score(record: dict[str, object], terms: list[str], full_query: str) -> int:
    name = normalize(str(record["name"]))
    description = normalize(str(record["description"]))
    path = normalize(str(record["path"]))
    category = normalize(str(record["category"]))
    total = TIER_BONUS.get(str(record["tier"]), 0)
    if full_query and full_query in f"{name} {description} {path}":
        total += 25
    for term in terms:
        if term == name:
            total += 30
        elif term in name:
            total += 14
        if term in description:
            total += 6
        if term in path:
            total += 4
        if term in category:
            total += 2
    return total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="domain, deliverable, method, or risk keywords")
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--category")
    parser.add_argument("--include-variants", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not CATALOG.is_file():
        raise SystemExit("catalog missing; run: python scripts/build_catalog.py")
    records = json.loads(CATALOG.read_text(encoding="utf-8"))["skills"]
    terms = query_terms(args.query)
    full_query = normalize(args.query.strip())
    ranked = []
    for record in records:
        if not args.include_variants and record["tier"] == "variant":
            continue
        if args.category and record["category"] != args.category:
            continue
        relevance = score(record, terms, full_query)
        if relevance > TIER_BONUS.get(str(record["tier"]), 0):
            ranked.append((relevance, record))
    ranked.sort(key=lambda item: (-item[0], str(item[1]["name"]), str(item[1]["path"])))
    selected = [dict(record, score=relevance) for relevance, record in ranked[: max(args.limit, 0)]]

    if args.as_json:
        print(json.dumps(selected, ensure_ascii=False, indent=2))
        return
    if not selected:
        print("No matching skills. Try broader or bilingual keywords.")
        return
    for record in selected:
        description = str(record["description"])
        if len(description) > 140:
            description = description[:137] + "..."
        print(f"[{record['score']:>3}] {record['name']}  ({record['category']}, {record['tier']})")
        print(f"      {record['path']}")
        if description:
            print(f"      {description}")


if __name__ == "__main__":
    main()
