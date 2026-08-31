#!/usr/bin/env python3
"""Validate the S1–S5 replication package. Exit 0 if structural checks pass."""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
S1 = ROOT / "S1_search_and_selection"
S2 = ROOT / "S2_citation_inventory"
S3 = ROOT / "S3_extraction"
S4 = ROOT / "S4_performance_provenance"
S5 = ROOT / "S5_validation"

REQUIRED = [
    S1 / "01_query_families.csv",
    S1 / "03_executable_search_strings.md",
    S1 / "04_evidence_freeze_log.csv",
    S1 / "06_eligibility_inclusion_exclusion.csv",
    S1 / "07_prisma_flow.csv",
    S1 / "08_fulltext_exclusions_by_criterion.csv",
    S1 / "screening" / "inclusion_exclusion_counts.csv",
    S2 / "citation_inventory.csv",
    S3 / "core_primary_evidence.csv",
    S3 / "appraisal_instrument.csv",
    S4 / "performance_provenance.csv",
    S4 / "figure_source_data" / "fig2a_anomaly_tier_counts.csv",
    S4 / "figure_source_data" / "fig_prisma_flow.csv",
    S5 / "data_dictionary.csv",
    S5 / "checksums.sha256",
    S5 / "AMENDMENT_LOG.md",
]


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def prisma_map() -> dict[str, int]:
    out = {}
    for row in read_csv(S1 / "07_prisma_flow.csv"):
        out[row["item"]] = int(float(row["n"]))
    return out


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for path in REQUIRED:
        if not path.exists():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1

    p = prisma_map()
    source_items = [
        "IEEE Xplore",
        "ACM Digital Library",
        "Scopus",
        "Web of Science Core Collection",
        "Google Scholar (supplementary)",
        "Citation tracking + 2026 proceedings",
    ]
    source_sum = sum(p[i] for i in source_items)
    if source_sum != p["N1_total_identified"]:
        errors.append(f"N1 {p['N1_total_identified']} != source sum {source_sum}")
    if p["removed_total"] != p["duplicates"] + p["out_of_range_date"] + p["non_english"] + p["ineligible_document_type"]:
        errors.append("removed_total does not equal the four pre-screen reasons")
    if p["N2_title_abstract_screened"] != p["N1_total_identified"] - p["removed_total"]:
        errors.append("N2 arithmetic failed")
    if p["N3_full_texts_sought"] != p["N2_title_abstract_screened"] - p["title_abstract_excluded"]:
        errors.append("N3 arithmetic failed")
    if p["N4_full_text_assessed"] != p["N3_full_texts_sought"] - p["reports_not_retrieved"]:
        errors.append("N4 arithmetic failed")
    ec_sum = sum(p[f"full_text_excluded_{c}"] for c in ["EC1", "EC2", "EC3", "EC4", "EC5"])
    if p["N5_studies_included"] != p["N4_full_text_assessed"] - ec_sum:
        errors.append("N5 arithmetic failed")
    tier_sum = p["tier1_behavioural_primary"] + p["tier2_hazard_primary"] + p["tier3_feed_integrity_primary"]
    if tier_sum != p["N5_studies_included"]:
        errors.append(f"tier sum {tier_sum} != N5 {p['N5_studies_included']}")

    fig2 = read_csv(S4 / "figure_source_data" / "fig2a_anomaly_tier_counts.csv")
    fig2_sum = sum(int(r["n_included_primary"]) for r in fig2)
    if fig2_sum != p["N5_studies_included"]:
        errors.append(f"Figure 2a sum {fig2_sum} != N5 {p['N5_studies_included']}")

    s2 = read_csv(S2 / "citation_inventory.csv")
    keys = [r["citation_key"] for r in s2]
    dup = [k for k, n in {k: keys.count(k) for k in keys}.items() if keys.count(k) > 1]
    # unique check
    seen = set()
    dups = set()
    for k in keys:
        if k in seen:
            dups.add(k)
        seen.add(k)
    if dups:
        errors.append(f"duplicate S2 citation keys: {sorted(dups)}")

    s3 = read_csv(S3 / "core_primary_evidence.csv")
    s3_keys = {r["citation_key"] for r in s3}
    missing_s2 = sorted(s3_keys - set(keys))
    if missing_s2:
        warnings.append(f"S3 keys not in S2 bibliography: {missing_s2}")

    s4 = read_csv(S4 / "performance_provenance.csv")
    missing_s4 = sorted({r["citation_key"] for r in s4} - set(keys))
    if missing_s4:
        warnings.append(f"S4 keys not in S2 bibliography: {missing_s4}")

    if len(s3) != int(p["core_studies_S3"]):
        warnings.append(
            f"S3 extracted rows={len(s3)} but working core_studies_S3={p['core_studies_S3']}. "
            "Deposit the remaining extraction rows before claiming 132 core studies."
        )

    pending = sum(
        1
        for r in s3
        if r.get("appraisal_D1") == "author_verification_required"
    )
    if pending:
        warnings.append(f"{pending} S3 rows still lack D1–D5 ratings")

    print("S2 rows:", len(s2))
    print("S3 rows:", len(s3))
    print("S4 rows:", len(s4))
    print("N1 / N5 / tiers:", p["N1_total_identified"], p["N5_studies_included"], tier_sum)
    if warnings:
        print("WARNINGS")
        for w in warnings:
            print(" -", w)
    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
