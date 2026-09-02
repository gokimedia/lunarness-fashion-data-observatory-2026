"""Command-line interface for ``lunarness-fashion-data``."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, List, Optional, Sequence

from . import __version__
from .core import (
    format_record_value,
    get_citation,
    get_record,
    list_records,
    list_sources,
    list_topics,
    search_records,
    validate_dataset,
)


def _write_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def _print_records(records: List[dict]) -> None:
    if not records:
        print("No records found.")
        return
    print("id\ttopic\tperiod\tentity\tvalue")
    for record in records:
        print(
            "\t".join(
                str(value)
                for value in (
                    record["id"],
                    record["topic"],
                    record["period"],
                    record["entity"],
                    format_record_value(record),
                )
            )
        )


def _print_record(record: dict) -> None:
    labels = (
        ("ID", "id"),
        ("Topic", "topic"),
        ("Entity", "entity"),
        ("Geography", "geography"),
        ("Period", "period"),
    )
    for label, key in labels:
        print(f"{label}: {record[key]}")
    print(f"Value: {format_record_value(record)}")
    if record.get("derivation"):
        print(f"Derivation: {record['derivation']}")
    if record.get("caveat"):
        print(f"Caveat: {record['caveat']}")
    print(f"Source: {record['source']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lunarness-fashion-data",
        description="Query and validate the Lunarness Fashion Data Observatory 2026 dataset.",
        epilog="Canonical source: https://lunarness.com/pages/fashion-statistics-observatory",
    )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List dataset records.")
    list_parser.add_argument("--topic")
    list_parser.add_argument("--json", action="store_true")

    get_parser = subparsers.add_parser("get", help="Get one record by ID.")
    get_parser.add_argument("record_id")
    get_parser.add_argument("--json", action="store_true")

    search_parser = subparsers.add_parser("search", help="Search descriptive record fields.")
    search_parser.add_argument("query", nargs="+")
    search_parser.add_argument("--json", action="store_true")

    topics_parser = subparsers.add_parser("topics", help="List unique topics.")
    topics_parser.add_argument("--json", action="store_true")

    sources_parser = subparsers.add_parser("sources", help="List source URLs and record IDs.")
    sources_parser.add_argument("--json", action="store_true")

    validate_parser = subparsers.add_parser("validate", help="Validate the bundled release.")
    validate_parser.add_argument("--json", action="store_true")

    subparsers.add_parser("citation", help="Print the preferred dataset citation.")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "list":
        records = list_records(args.topic)
        _write_json(records) if args.json else _print_records(records)
        return 0
    if args.command == "get":
        record = get_record(args.record_id)
        if record is None:
            print(f"Unknown record id: {args.record_id}.", file=sys.stderr)
            return 1
        _write_json(record) if args.json else _print_record(record)
        return 0
    if args.command == "search":
        records = search_records(" ".join(args.query))
        _write_json(records) if args.json else _print_records(records)
        return 0
    if args.command == "topics":
        topics = list_topics()
        _write_json(topics) if args.json else print("\n".join(topics))
        return 0
    if args.command == "sources":
        sources = list_sources()
        if args.json:
            _write_json(sources)
        else:
            for source in sources:
                print(f"{source['url']}\n  {', '.join(source['record_ids'])}")
        return 0
    if args.command == "validate":
        result = validate_dataset()
        if args.json:
            _write_json(result)
        else:
            print("Dataset is valid." if result["valid"] else "Dataset is invalid.")
            stats = result["stats"]
            print(
                f"Records: {stats['records']}; topics: {stats['topics']}; "
                f"sources: {stats['sources']}."
            )
            for error in result["errors"]:
                print(f"ERROR: {error}", file=sys.stderr)
            for warning in result["warnings"]:
                print(f"WARNING: {warning}", file=sys.stderr)
        return 0 if result["valid"] else 1
    if args.command == "citation":
        print(get_citation())
        return 0
    return 2
