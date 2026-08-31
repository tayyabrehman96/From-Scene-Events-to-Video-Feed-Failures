#!/usr/bin/env python3
"""Optional LitStudy interoperability audit for deposited bibliographic exports.

This script is deliberately secondary to the authoritative S1 screening ledger.
It imports CSV, RIS, and BibTeX metadata, combines source collections using
LitStudy's identifier-aware DocumentSet union, and writes descriptive audit
tables. It does not make inclusion/exclusion decisions.
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "S1_search_and_selection" / "raw_exports"
DEFAULT_OUTPUT = ROOT / "S1_search_and_selection" / "screening" / "litstudy_audit"
SUPPORTED = {".csv", ".ris", ".bib", ".bibtex"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Import deposited bibliographic metadata with LitStudy and write "
            "source, year, and deduplication audit tables."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="File or directory containing CSV, RIS, or BibTeX metadata exports.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Directory for generated audit CSVs.",
    )
    return parser.parse_args()


def discover(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix.lower() in SUPPORTED else []
    if not path.exists():
        return []
    return sorted(
        p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED
    )


def load_document_set(litstudy, path: Path):
    suffix = path.suffix.lower()
    if suffix == ".ris":
        return litstudy.load_ris_file(str(path))
    if suffix in {".bib", ".bibtex"}:
        return litstudy.load_bibtex(str(path))
    return litstudy.load_csv(
        str(path),
        title_field="title",
        authors_field="authors",
        abstract_field="abstract",
        date_field="year",
        source_field="venue",
        doi_field="doi",
    )


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    files = discover(args.input)
    if not files:
        print(
            f"No CSV/RIS/BibTeX exports found under {args.input}. "
            "Deposit the original metadata exports before running this audit."
        )
        return 0

    try:
        import litstudy
    except ImportError:
        print(
            "LitStudy is not installed. Run "
            "'python -m pip install -r S5_validation/requirements-litstudy.txt'.",
            file=sys.stderr,
        )
        return 2

    combined = None
    manifest = []
    total_loaded = 0
    for path in files:
        docs = load_document_set(litstudy, path)
        count = len(docs)
        total_loaded += count
        manifest.append(
            {
                "file": path.relative_to(ROOT).as_posix()
                if path.is_relative_to(ROOT)
                else str(path),
                "format": path.suffix.lower().lstrip("."),
                "records_loaded": count,
            }
        )
        combined = docs if combined is None else combined | docs

    unique_count = len(combined)
    manifest.append(
        {
            "file": "ALL_SOURCES",
            "format": "identifier-aware union",
            "records_loaded": unique_count,
        }
    )

    years = Counter(
        str(doc.publication_year) if doc.publication_year is not None else "NR"
        for doc in combined
    )
    sources = Counter(doc.publication_source or "NR" for doc in combined)

    write_csv(
        args.output / "source_manifest.csv",
        ["file", "format", "records_loaded"],
        manifest,
    )
    write_csv(
        args.output / "year_distribution.csv",
        ["publication_year", "n_records"],
        [
            {"publication_year": year, "n_records": count}
            for year, count in sorted(years.items())
        ],
    )
    write_csv(
        args.output / "venue_distribution.csv",
        ["publication_source", "n_records"],
        [
            {"publication_source": source, "n_records": count}
            for source, count in sorted(
                sources.items(), key=lambda item: (-item[1], item[0])
            )
        ],
    )
    write_csv(
        args.output / "deduplication_summary.csv",
        ["records_loaded_across_files", "unique_after_union", "duplicates_collapsed"],
        [
            {
                "records_loaded_across_files": total_loaded,
                "unique_after_union": unique_count,
                "duplicates_collapsed": total_loaded - unique_count,
            }
        ],
    )

    print(
        f"LitStudy audit complete: {total_loaded} loaded records, "
        f"{unique_count} unique after identifier-aware union."
    )
    print(f"Outputs: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
