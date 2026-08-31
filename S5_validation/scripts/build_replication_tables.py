#!/usr/bin/env python3
"""Build machine-readable S1–S5 tables from the manuscript evidence.

This script does not invent record-level screening decisions or D1–D5 ratings.
It transcribes search protocol, bibliography, comparison-table numbers, and
figure-source datasets that are present in the submitted manuscript package.
"""
from __future__ import annotations

import csv
import hashlib
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BIB = ROOT / "references.bib"
S1 = ROOT / "S1_search_and_selection"
S2 = ROOT / "S2_citation_inventory"
S3 = ROOT / "S3_extraction"
S4 = ROOT / "S4_performance_provenance"
S4F = S4 / "figure_source_data"
S4T = S4 / "manuscript_tables"
S5 = ROOT / "S5_validation"

PACKAGE_VERSION = "0.3.1"
AS_OF = date(2026, 8, 31).isoformat()
STATUS_PROVISIONAL = "provisional_author_verification_required"
# Compatibility name used throughout the table builders; values are provisional.
STATUS_REPORTED = STATUS_PROVISIONAL
STATUS_TRANSCRIBED = "transcribed_from_manuscript"
STATUS_PENDING = "author_verification_required"
CHECKSUM_SKIP_DIRS = {".git", "__pycache__", "_github_clone", "manuscript"}
CHECKSUM_SKIP_NAMES = {
    "main.tex",
    "main.bbl",
    "main.pdf",
    "references.bib",
    "README_BEFORE_SUBMISSION.md",
    "PDF_PREFLIGHT.txt",
    "PRISMA_PROVISIONAL_NUMBERS_FOR_REVIEW.csv",
    "checksums.sha256",
    "audit_report.md",
}
CHECKSUM_SKIP_SUFFIXES = {
    ".aux",
    ".bcf",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".lof",
    ".log",
    ".lot",
    ".nav",
    ".out",
    ".pdf",
    ".png",
    ".snm",
    ".toc",
    ".vrb",
    ".xml",
}


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})


def parse_bib(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    entries = []
    for m in re.finditer(
        r"@(\w+)\s*\{\s*([^,]+)\s*,(.*?)(?=\n@|\Z)",
        text,
        flags=re.S,
    ):
        etype, key, body = m.group(1), m.group(2).strip(), m.group(3)
        fields = {}
        for fm in re.finditer(
            r"(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"[^\"]*\")",
            body,
            flags=re.S,
        ):
            raw = fm.group(2).strip()
            if raw.startswith("{") and raw.endswith("}"):
                raw = raw[1:-1]
            elif raw.startswith('"') and raw.endswith('"'):
                raw = raw[1:-1]
            fields[fm.group(1).lower()] = re.sub(r"\s+", " ", raw).strip()
        title = fields.get("title", "")
        title_l = title.lower()
        role = classify_role(etype, title_l, fields)
        entries.append(
            {
                "citation_key": key,
                "entry_type": etype.lower(),
                "year": fields.get("year", ""),
                "author": fields.get("author", ""),
                "title": title,
                "journal": fields.get("journal", ""),
                "booktitle": fields.get("booktitle", ""),
                "volume": fields.get("volume", ""),
                "number": fields.get("number", ""),
                "pages": fields.get("pages", ""),
                "publisher": fields.get("publisher", ""),
                "doi": fields.get("doi", ""),
                "url": fields.get("url", ""),
                "role_in_review": role,
                "verification_status": STATUS_TRANSCRIBED,
            }
        )
    return entries


def classify_role(etype: str, title_l: str, fields: dict) -> str:
    if "litstudy" in title_l:
        return "review_software"
    if any(
        w in title_l
        for w in (
            "review",
            "survey",
            "systematic",
            "a comprehensive",
            "state-of-the-art",
        )
    ) and "dataset" not in title_l:
        if "prisma" in title_l or "swim" in title_l or "reporting" in title_l:
            return "reporting_standard"
        return "positioning_review"
    if any(
        w in title_l
        for w in (
            "dataset",
            "benchmark",
            "corpus",
            "ucsd",
            "uhctd",
            "flame",
            "fasdd",
            "d-fire",
            "street scene",
            "ubnormal",
            "chad",
        )
    ):
        return "dataset_or_benchmark"
    if any(
        w in title_l
        for w in (
            "prisma",
            "guidelines",
            "kappa",
            "agreement",
            "bias",
            "meta-analy",
        )
    ):
        return "methods_or_reporting"
    if etype.lower() in {"article", "inproceedings"}:
        return "primary_or_comparative_study"
    return "background_or_other"


def s1_tables() -> None:
    write_csv(
        S1 / "01_query_families.csv",
        [
            "query_family_id",
            "query_family",
            "core_concepts",
            "representative_terms",
            "source",
        ],
        [
            {
                "query_family_id": "QF1",
                "query_family": "Behavioral VAD",
                "core_concepts": "anomaly task + surveillance context + learning method",
                "representative_terms": (
                    "video anomaly detection; abnormal event; violence; loitering; "
                    "fall; crowd; traffic; abandoned object; CNN; RNN; autoencoder; "
                    "MIL; self-supervised; transformer"
                ),
                "source": "tab:query_families",
            },
            {
                "query_family_id": "QF2",
                "query_family": "Physical hazards",
                "core_concepts": "fire/smoke phenomenon + visual monitoring + learning method",
                "representative_terms": (
                    "fire; flame; smoke; haze; early warning; wildfire; CCTV; "
                    "video surveillance; classification; detection; segmentation; transformer"
                ),
                "source": "tab:query_families",
            },
            {
                "query_family_id": "QF3",
                "query_family": "Feed integrity",
                "core_concepts": "camera/feed failure + surveillance context",
                "representative_terms": (
                    "camera tampering; blocked lens; occlusion; blur; defocus; "
                    "displacement; frozen stream; frame loss; signal corruption; "
                    "no-reference image quality"
                ),
                "source": "tab:query_families",
            },
            {
                "query_family_id": "QF4",
                "query_family": "Cross-cutting update",
                "core_concepts": "recent representation/evaluation/deployment terms",
                "representative_terms": (
                    "foundation model; vision-language model; multimodal LLM; CLIP; "
                    "open-vocabulary; state-space model; Mamba; event-centric evaluation; "
                    "edge deployment"
                ),
                "source": "tab:query_families",
            },
        ],
    )

    write_csv(
        S1 / "05_search_reporting_minimum_fields.csv",
        [
            "source",
            "interface_fields",
            "search_families",
            "date_handling",
            "archived_reproducibility_record",
        ],
        [
            {
                "source": "IEEE Xplore",
                "interface_fields": "Command Search; metadata/abstract terms",
                "search_families": "Behavioral, hazard, feed-integrity, cross-cutting",
                "date_handling": "2010--30 June 2026",
                "archived_reproducibility_record": (
                    "Exact Boolean syntax, filters, execution window, export-format specification"
                ),
            },
            {
                "source": "ACM Digital Library",
                "interface_fields": "Advanced Search; title/abstract/keywords",
                "search_families": "Same four families",
                "date_handling": "2010--30 June 2026",
                "archived_reproducibility_record": "Exact syntax and interface notes",
            },
            {
                "source": "Scopus",
                "interface_fields": "TITLE-ABS-KEY",
                "search_families": "Same four families",
                "date_handling": "2010--30 June 2026",
                "archived_reproducibility_record": (
                    "Fielded syntax, source-type and language filters"
                ),
            },
            {
                "source": "Web of Science Core Collection",
                "interface_fields": "Topic field (TS)",
                "search_families": "Same four families",
                "date_handling": "2010--30 June 2026",
                "archived_reproducibility_record": "Fielded syntax, index coverage and filters",
            },
            {
                "source": "Google Scholar",
                "interface_fields": "Phrase/keyword discovery queries",
                "search_families": "Gap filling and citation discovery",
                "date_handling": "Search dates recorded separately",
                "archived_reproducibility_record": (
                    "Query, maximum screened rank, inclusion rule, deduplication rule"
                ),
            },
            {
                "source": "Official proceedings",
                "interface_fields": "WACV/CVPR open-access repositories",
                "search_families": "2025--2026 update vocabulary",
                "date_handling": "Evidence freeze: 30 June 2026",
                "archived_reproducibility_record": (
                    "Proceedings pages checked, study status, main/findings/workshop designation"
                ),
            },
        ],
    )

    write_csv(
        S1 / "04_evidence_freeze_log.csv",
        [
            "event_id",
            "event",
            "date",
            "description",
            "verification_status",
        ],
        [
            {
                "event_id": "EF1",
                "event": "Coverage start",
                "date": "2010-01-01",
                "description": "Lower bound of the eligible publication window (IC5), with pre-2010 seminal exceptions.",
                "verification_status": STATUS_TRANSCRIBED,
            },
            {
                "event_id": "EF2",
                "event": "Initial search",
                "date": "2025-04",
                "description": "First execution of the four query families across fielded databases plus Scholar.",
                "verification_status": STATUS_TRANSCRIBED,
            },
            {
                "event_id": "EF3",
                "event": "Update search",
                "date": "2026-06",
                "description": "Update search including official WACV 2026 and CVPR 2026 proceedings.",
                "verification_status": STATUS_TRANSCRIBED,
            },
            {
                "event_id": "EF4",
                "event": "Evidence freeze",
                "date": "2026-06-30",
                "description": "Hard freeze. No later record is eligible as quantitative benchmark evidence.",
                "verification_status": STATUS_TRANSCRIBED,
            },
            {
                "event_id": "EF5",
                "event": "Coverage end",
                "date": "2026-06-30",
                "description": "Upper bound of the eligible publication window (IC5).",
                "verification_status": STATUS_TRANSCRIBED,
            },
        ],
    )

    write_csv(
        S1 / "06_eligibility_inclusion_exclusion.csv",
        [
            "criterion_id",
            "polarity",
            "criterion_text",
            "prisma_stage_applied",
            "source",
        ],
        [
            {
                "criterion_id": "IC1",
                "polarity": "inclusion",
                "criterion_text": (
                    "Peer-reviewed journal or conference paper; accepted 2025--2026 "
                    "main-conference, findings, and workshop papers were eligible but "
                    "their publication category was recorded separately."
                ),
                "prisma_stage_applied": "title_abstract_and_full_text",
                "source": "tab:eligibility",
            },
            {
                "criterion_id": "IC2",
                "polarity": "inclusion",
                "criterion_text": (
                    "Proposes, evaluates, or critically benchmarks a computational method "
                    "for scene anomaly detection, visual hazard recognition, or camera/video-feed integrity."
                ),
                "prisma_stage_applied": "title_abstract_and_full_text",
                "source": "tab:eligibility",
            },
            {
                "criterion_id": "IC3",
                "polarity": "inclusion",
                "criterion_text": (
                    "Targets surveillance, traffic monitoring, public-space monitoring, "
                    "industrial monitoring, or a fixed-camera setting whose sensing conditions, "
                    "anomaly definition, and evaluation outputs transfer directly to surveillance feed monitoring."
                ),
                "prisma_stage_applied": "title_abstract_and_full_text",
                "source": "tab:eligibility",
            },
            {
                "criterion_id": "IC4",
                "polarity": "inclusion",
                "criterion_text": (
                    "Reports quantitative evaluation on a public benchmark or a sufficiently "
                    "described study-specific evaluation corpus."
                ),
                "prisma_stage_applied": "full_text",
                "source": "tab:eligibility",
            },
            {
                "criterion_id": "IC5",
                "polarity": "inclusion",
                "criterion_text": (
                    "Falls within January 2010--June 2026, except seminal pre-2010 datasets "
                    "or methods required for technical context."
                ),
                "prisma_stage_applied": "pre_screening_and_full_text",
                "source": "tab:eligibility",
            },
            {
                "criterion_id": "EC1",
                "polarity": "exclusion",
                "criterion_text": "Non-English publication or inaccessible full text.",
                "prisma_stage_applied": "pre_screening_or_eligibility",
                "source": "tab:eligibility",
            },
            {
                "criterion_id": "EC2",
                "polarity": "exclusion",
                "criterion_text": (
                    "Duplicate report, extended abstract, or a conference version superseded "
                    "by a substantially overlapping journal extension."
                ),
                "prisma_stage_applied": "eligibility",
                "source": "tab:eligibility",
            },
            {
                "criterion_id": "EC3",
                "polarity": "exclusion",
                "criterion_text": (
                    "Non-visual-only work, medical/industrial inspection without a surveillance "
                    "transfer argument, or generic anomaly detection without relevant evaluation."
                ),
                "prisma_stage_applied": "eligibility",
                "source": "tab:eligibility",
            },
            {
                "criterion_id": "EC4",
                "polarity": "exclusion",
                "criterion_text": (
                    "No quantitative evaluation, inadequate description of data/splits, or "
                    "results that cannot be associated with a defined task and metric."
                ),
                "prisma_stage_applied": "eligibility",
                "source": "tab:eligibility",
            },
            {
                "criterion_id": "EC5",
                "polarity": "exclusion",
                "criterion_text": (
                    "Review papers used only for positioning, not as primary experimental evidence."
                ),
                "prisma_stage_applied": "eligibility",
                "source": "tab:eligibility",
            },
        ],
    )

    # Representative IC3 audit examples from the manuscript.
    write_csv(
        S1 / "screening" / "ic3_surveillance_transfer_examples.csv",
        ["decision", "example", "criterion", "source"],
        [
            {
                "decision": "included",
                "example": (
                    "A fixed-camera traffic-monitoring fire detector whose sensing conditions match CCTV"
                ),
                "criterion": "IC3",
                "source": "sec:study_selection",
            },
            {
                "decision": "excluded",
                "example": (
                    "An industrial-inspection method (MVTec-style) with no surveillance-transfer argument"
                ),
                "criterion": "EC3",
                "source": "sec:study_selection",
            },
            {
                "decision": "excluded",
                "example": "A medical video-anomaly method with no surveillance transfer",
                "criterion": "EC3",
                "source": "sec:study_selection",
            },
        ],
    )

    prisma_id = [
        ("IEEE Xplore", 3214),
        ("ACM Digital Library", 1987),
        ("Scopus", 4568),
        ("Web of Science Core Collection", 3511),
        ("Google Scholar (supplementary)", 2142),
        ("Citation tracking + 2026 proceedings", 1060),
    ]
    n1 = sum(v for _, v in prisma_id)
    dup, oor, ne, inel = 2128, 166, 113, 170
    removed = dup + oor + ne + inel
    n2 = n1 - removed
    ta_ex = 12958
    n3 = n2 - ta_ex
    not_ret = 44
    n4 = n3 - not_ret
    ecs = [("EC1", 35), ("EC2", 51), ("EC3", 93), ("EC4", 78), ("EC5", 30)]
    n5 = n4 - sum(v for _, v in ecs)
    core = 132
    t1, t2, t3 = 441, 122, 53

    prisma_rows = []
    for src, val in prisma_id:
        prisma_rows.append(
            {
                "stage": "identification",
                "item": src,
                "n": val,
                "formula": "provisional estimate; source export not deposited",
                "verification_status": STATUS_REPORTED,
            }
        )
    prisma_rows.extend(
        [
            {
                "stage": "identification",
                "item": "N1_total_identified",
                "n": n1,
                "formula": "sum of source rows",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "removed_before_screening",
                "item": "duplicates",
                "n": dup,
                "formula": "provisional estimate",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "removed_before_screening",
                "item": "out_of_range_date",
                "n": oor,
                "formula": "provisional estimate",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "removed_before_screening",
                "item": "non_english",
                "n": ne,
                "formula": "provisional estimate",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "removed_before_screening",
                "item": "ineligible_document_type",
                "n": inel,
                "formula": "provisional estimate",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "removed_before_screening",
                "item": "removed_total",
                "n": removed,
                "formula": "2128+166+113+170",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "screening",
                "item": "N2_title_abstract_screened",
                "n": n2,
                "formula": "N1 - removed_total",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "screening",
                "item": "title_abstract_excluded",
                "n": ta_ex,
                "formula": "provisional estimate",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "screening",
                "item": "N3_full_texts_sought",
                "n": n3,
                "formula": "N2 - title_abstract_excluded",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "eligibility",
                "item": "reports_not_retrieved",
                "n": not_ret,
                "formula": "provisional estimate",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "eligibility",
                "item": "N4_full_text_assessed",
                "n": n4,
                "formula": "N3 - not_retrieved",
                "verification_status": STATUS_REPORTED,
            },
        ]
    )
    for cid, val in ecs:
        prisma_rows.append(
            {
                "stage": "eligibility",
                "item": f"full_text_excluded_{cid}",
                "n": val,
                "formula": "provisional estimate; see 06_eligibility_inclusion_exclusion.csv",
                "verification_status": STATUS_REPORTED,
            }
        )
    prisma_rows.extend(
        [
            {
                "stage": "included",
                "item": "N5_studies_included",
                "n": n5,
                "formula": "N4 - sum(EC1..EC5)",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "included",
                "item": "core_studies_S3",
                "n": core,
                "formula": "provisional estimate; source extraction not deposited",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "included",
                "item": "tier1_behavioural_primary",
                "n": t1,
                "formula": "primary-tier allocation; T1+T2+T3 must equal N5",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "included",
                "item": "tier2_hazard_primary",
                "n": t2,
                "formula": "primary-tier allocation",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "included",
                "item": "tier3_feed_integrity_primary",
                "n": t3,
                "formula": "primary-tier allocation",
                "verification_status": STATUS_REPORTED,
            },
        ]
    )
    write_csv(
        S1 / "07_prisma_flow.csv",
        ["stage", "item", "n", "formula", "verification_status"],
        prisma_rows,
    )
    write_csv(
        S1 / "screening" / "inclusion_exclusion_counts.csv",
        ["stage", "item", "n", "formula", "verification_status"],
        prisma_rows,
    )
    write_csv(
        S1 / "08_fulltext_exclusions_by_criterion.csv",
        ["criterion_id", "n_excluded", "criterion_text", "verification_status"],
        [
            {
                "criterion_id": cid,
                "n_excluded": val,
                "criterion_text": next(
                    r["criterion_text"]
                    for r in [
                        {
                            "criterion_id": "EC1",
                            "criterion_text": "Non-English publication or inaccessible full text.",
                        },
                        {
                            "criterion_id": "EC2",
                            "criterion_text": (
                                "Duplicate report, extended abstract, or a conference version "
                                "superseded by a substantially overlapping journal extension."
                            ),
                        },
                        {
                            "criterion_id": "EC3",
                            "criterion_text": "No surveillance transfer.",
                        },
                        {
                            "criterion_id": "EC4",
                            "criterion_text": "No quantitative evaluation / inadequate data description.",
                        },
                        {
                            "criterion_id": "EC5",
                            "criterion_text": "Review paper used only for positioning.",
                        },
                    ]
                    if r["criterion_id"] == cid
                ),
                "verification_status": STATUS_REPORTED,
            }
            for cid, val in ecs
        ],
    )

    write_csv(
        S1 / "screening" / "agreement_provisional_values.csv",
        [
            "stage",
            "statistic",
            "value",
            "notes",
            "verification_status",
        ],
        [
            {
                "stage": "title_abstract",
                "statistic": "cohen_kappa",
                "value": "0.754",
                "notes": "provisional scenario; paired decisions not deposited",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "title_abstract",
                "statistic": "kappa_95ci",
                "value": "[0.731, 0.777]",
                "notes": "provisional scenario; source matrix not deposited",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "title_abstract",
                "statistic": "disagreements",
                "value": "417",
                "notes": "provisional scenario; directional split not deposited",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "title_abstract",
                "statistic": "raw_agreement_pct",
                "value": "97.0",
                "notes": "provisional scenario; source matrix not deposited",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "title_abstract",
                "statistic": "pabak",
                "value": "0.940",
                "notes": "2*raw_agreement-1",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "title_abstract",
                "statistic": "gwet_ac1",
                "value": "0.966",
                "notes": "provisional scenario; source matrix not deposited",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "full_text",
                "statistic": "cohen_kappa",
                "value": "0.877",
                "notes": "provisional scenario; paired decisions not deposited",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "full_text",
                "statistic": "kappa_95ci",
                "value": "[0.843, 0.909]",
                "notes": "provisional scenario; source matrix not deposited",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "full_text",
                "statistic": "disagreements",
                "value": "49",
                "notes": "provisional scenario; directional split not deposited",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "full_text",
                "statistic": "raw_agreement_pct",
                "value": "94.6",
                "notes": "provisional scenario; source matrix not deposited",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "full_text",
                "statistic": "pabak",
                "value": "0.891",
                "notes": "2*raw_agreement-1",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "full_text",
                "statistic": "gwet_ac1",
                "value": "0.903",
                "notes": "provisional scenario; source matrix not deposited",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "appraisal",
                "statistic": "n_rated_items",
                "value": "660",
                "notes": "132 core studies x 5 dimensions",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "appraisal",
                "statistic": "observed_agreement_pct",
                "value": "91.2",
                "notes": "provisional scenario; row-level ratings not deposited",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "appraisal",
                "statistic": "cohen_kappa_unweighted",
                "value": "0.867",
                "notes": "provisional scenario; source matrix not deposited",
                "verification_status": STATUS_REPORTED,
            },
            {
                "stage": "appraisal",
                "statistic": "kappa_95ci",
                "value": "[0.832, 0.898]",
                "notes": "provisional scenario; source matrix not deposited",
                "verification_status": STATUS_REPORTED,
            },
        ],
    )

    write_csv(
        S1 / "11_screening_ledger_schema.csv",
        [
            "column",
            "required",
            "description",
            "allowed_values",
        ],
        [
            {"column": "record_id", "required": "yes", "description": "Stable unique ID", "allowed_values": "string"},
            {"column": "source", "required": "yes", "description": "Database or supplementary source", "allowed_values": "IEEE|ACM|Scopus|WoS|Scholar|citation_tracking|proceedings"},
            {"column": "query_family_id", "required": "yes", "description": "QF1–QF4 or mixed", "allowed_values": "QF1|QF2|QF3|QF4|mixed"},
            {"column": "title", "required": "yes", "description": "Record title", "allowed_values": "string"},
            {"column": "authors", "required": "yes", "description": "Author string", "allowed_values": "string"},
            {"column": "year", "required": "yes", "description": "Publication year", "allowed_values": "integer or NR"},
            {"column": "doi", "required": "no", "description": "DOI if present", "allowed_values": "string"},
            {"column": "stage", "required": "yes", "description": "Last completed PRISMA stage", "allowed_values": "identified|removed_before_screening|title_abstract|full_text|included"},
            {"column": "decision", "required": "yes", "description": "Consensus decision", "allowed_values": "include|exclude|not_retrieved"},
            {"column": "exclusion_criterion", "required": "if exclude", "description": "Single primary exclusion code", "allowed_values": "EC1|EC2|EC3|EC4|EC5|duplicate|out_of_range|non_english|ineligible_type"},
            {"column": "primary_tier", "required": "if include", "description": "Principal evaluation tier", "allowed_values": "1|2|3"},
            {"column": "multi_category_flag", "required": "if include", "description": "Spans more than one tier", "allowed_values": "yes|no"},
            {"column": "publication_category", "required": "yes", "description": "Venue class", "allowed_values": "journal|main_conference|findings|workshop|preprint"},
        ],
    )
    write_csv(
        S1 / "12_independent_screener_schema.csv",
        ["column", "required", "description", "allowed_values"],
        [
            {"column": "record_id", "required": "yes", "description": "Must match screening ledger", "allowed_values": "string"},
            {"column": "screener_id", "required": "yes", "description": "Rater identity", "allowed_values": "A|B"},
            {"column": "stage", "required": "yes", "description": "Screening stage", "allowed_values": "title_abstract|full_text"},
            {"column": "decision", "required": "yes", "description": "Independent decision before consensus", "allowed_values": "include|exclude|unsure"},
            {"column": "exclusion_criterion", "required": "if exclude", "description": "Rater-assigned criterion", "allowed_values": "EC1|EC2|EC3|EC4|EC5|other"},
            {"column": "notes", "required": "no", "description": "Free text", "allowed_values": "string"},
        ],
    )


def performance_tables() -> dict[str, list[dict]]:
    """Canonical and local manuscript tables used for S3/S4."""
    dash = ""
    consolidated = [
        # method, year, key, regime, ped2, avenue, shtech, ucf, xd, repr, scoring, table, canonical
        ("Conv-AE", 2016, "hasan2016learning", "Normal-only", "85.0", "80.0", "60.9", dash, dash, "ConvAE", "Reconstruction", "tab:consolidated_performance", True),
        ("Frame-Pred", 2018, "liu2018future", "Normal-only", "95.4", "85.1", "72.8", dash, dash, "U-Net + GAN", "Prediction", "tab:consolidated_performance", True),
        ("MemAE", 2019, "gong2019memorizing", "Normal-only", "94.1", "83.3", "71.2", dash, dash, "AE + memory", "Reconstruction", "tab:consolidated_performance", True),
        ("MNAD", 2020, "park2020learning", "Normal-only", "97.0", "88.5", "70.5", dash, dash, "AE + memory", "Recon. + prediction", "tab:consolidated_performance", True),
        ("Georgescu et al.", 2021, "georgescu2021anomaly", "Self-supervised", "97.8", "89.3", "82.7", dash, dash, "Multi-task CNN", "Pretext discrepancy", "tab:consolidated_performance", True),
        ("SSMTL++v1", 2023, "barbalau2023ssmtl", "Self-supervised", dash, "93.7", "82.9", dash, dash, "Multi-task + CvT/pretexts", "Pretext discrepancy", "tab:consolidated_performance", True),
        ("SSMTL++v2", 2023, "barbalau2023ssmtl", "Self-supervised", dash, "91.6", "83.8", dash, dash, "Alternative multi-task configuration", "Pretext discrepancy", "tab:consolidated_performance", True),
        ("STG-NF", 2023, "hirschorn2023normalizing", "Normal-only / pose", dash, dash, "85.9", dash, dash, "Pose + normalizing flow", "Density", "tab:consolidated_performance", True),
        ("FPDM", 2023, "yan2023feature", "Normal-only", dash, "90.1", "78.6", dash, dash, "Feature diffusion", "Prediction/reconstruction", "tab:consolidated_performance", True),
        ("HSC", 2023, "sun2023hierarchical", "Normal-only semantic contrast", "98.1", "93.7", "83.4", dash, dash, "Semantic parsing + AE/memory", "Reconstruction + contrastive", "tab:consolidated_performance", True),
        ("MIL-Rank", 2018, "sultani2018real", "Video-level weak supervision", dash, dash, dash, "75.4", dash, "C3D", "MIL ranking", "tab:weak_foundation_performance", True),
        ("RTFM", 2021, "tian2021weakly", "Video-level weak supervision", dash, dash, "97.2", "84.3", "77.8", "I3D", "Feature magnitude", "tab:weak_foundation_performance", True),
        ("Wu & Liu", 2021, "wu2021causal", "Video-level weak supervision", dash, dash, dash, "84.9", "75.9", "I3D", "Causal temporal relation", "tab:weak_foundation_performance", True),
        ("MGFN", 2023, "chen2023mgfn", "Video-level weak supervision", dash, dash, dash, "86.7", "80.1", "I3D", "Multi-granularity MIL", "tab:weak_foundation_performance", True),
        ("UR-DMU (RGB)", 2023, "zhou2023dmu", "Video-level weak supervision", dash, dash, dash, "87.0", "81.7", "I3D", "Uncertainty-regulated dual memory", "tab:weak_foundation_performance", True),
        ("UR-DMU (RGB+audio)", 2023, "zhou2023dmu", "Video-level weak supervision", dash, dash, dash, dash, "81.8", "I3D + VGGish", "Modality ablation", "tab:weak_foundation_performance", True),
        ("SGTTD", 2024, "wu2022self", "Video-level weak supervision", dash, dash, "97.3", "85.1", dash, "Temporal transformer", "Weak temporal discrimination", "tab:weak_foundation_performance", True),
        ("VadCLIP", 2024, "wu2024vadclip", "Video labels + frozen CLIP", dash, dash, dash, "88.0", "84.5", "CLIP ViT-B/16", "Vision-language alignment", "tab:weak_foundation_performance", True),
        ("PEL4VAD", 2024, "zhang2024pel4vad", "Video labels + CLIP prompt features", dash, dash, "98.1", "86.8", "85.6", "I3D + CLIP prompts", "Prompt-enhanced context learning", "tab:weak_foundation_performance", True),
    ]

    reconstruction = [
        ("Conv-AE", 2016, "hasan2016learning", "Normal-only", "85.0", "80.0", "60.9", dash, dash, "ConvAE", "Reconstruction", "tab:reconstruction_methods", False),
        ("Stacked RNN", 2017, "luo2017revisit", "Unsupervised", "92.2", "81.7", "68.0", dash, dash, "AE + sparse coding", "Reconstruction", "tab:reconstruction_methods", False),
        ("ConvLSTM-AE", 2017, "chong2017abnormal", "Unsupervised", "88.1", "77.0", dash, dash, dash, "ConvLSTM-AE", "Reconstruction", "tab:reconstruction_methods", False),
        ("MemAE", 2019, "gong2019memorizing", "Unsupervised", "94.1", "83.3", "71.2", dash, dash, "AE + memory", "Reconstruction", "tab:reconstruction_methods", False),
        ("AnoPCN", 2019, "ye2019anopcn", "Unsupervised", "96.8", "86.2", "73.6", dash, dash, "AE + prediction", "Reconstruction", "tab:reconstruction_methods", False),
        ("MNAD", 2020, "park2020learning", "Unsupervised", "97.0", "88.5", "70.5", dash, dash, "AE + memory + pred.", "Reconstruction", "tab:reconstruction_methods", False),
        ("FPDM", 2023, "yan2023feature", "Unsupervised", dash, "90.1", "78.6", dash, dash, "Feature Diffusion", "Prediction/reconstruction", "tab:reconstruction_methods", False),
    ]
    prediction = [
        ("Frame-Pred", 2018, "liu2018future", "Normal-only", "95.4", "85.1", "72.8", dash, dash, "U-Net + GAN", "Prediction", "tab:prediction_methods", False),
        ("Morais et al.", 2019, "morais2019learning", "Normal-only / pose", dash, "88.3", "75.4", dash, dash, "MPED-RNN", "Prediction", "tab:prediction_methods", False),
        ("BMAN", 2020, "lee2019bman", "Normal-only", "96.6", "90.0", "76.2", dash, dash, "BiDirectional", "Prediction", "tab:prediction_methods", False),
        ("CT-D2GAN", 2021, "feng2021ct", "Normal-only", "97.2", "85.9", "77.7", dash, dash, "Conv-Transf + D2GAN", "Prediction", "tab:prediction_methods", False),
        ("Hybrid Flow", 2021, "liu2021hybrid", "Normal-only", "96.3", "85.8", "73.2", dash, dash, "MemAE + flow pred.", "Prediction", "tab:prediction_methods", False),
        ("CR-BPN", 2022, "chen2022comprehensive", "Normal-only", "98.3", "90.3", "78.1", dash, dash, "Bi-prediction net", "Prediction", "tab:prediction_methods", False),
        ("STENet", 2024, "wang2024stenet", "Normal-only", "98.1", "89.7", "76.8", dash, dash, "Spatiotemporal enhance", "Prediction", "tab:prediction_methods", False),
    ]
    weakly = [
        ("MIL-Rank", 2018, "sultani2018real", "Video-level weak supervision", dash, dash, dash, "75.4", dash, "C3D / I3D", "MIL ranking", "tab:weakly_methods", False),
        ("GCN-Anomaly", 2019, "zhong2019graph", "Video-level weak supervision", dash, dash, "84.4", "82.1", dash, "TSN + GCN", "Graph MIL", "tab:weakly_methods", False),
        ("Wu et al. (XD-Violence)", 2020, "wu2020not", "Video-level weak supervision", dash, dash, dash, "82.4", "78.6", "I3D + VGGish", "HL-Net", "tab:weakly_methods", False),
        ("RTFM", 2021, "tian2021weakly", "Video-level weak supervision", dash, dash, "97.2", "84.3", "77.8", "I3D", "Feature magnitude", "tab:weakly_methods", False),
        ("MIST", 2021, "feng2021mist", "Video-level weak supervision", dash, dash, "94.8", "82.3", dash, "I3D", "Multi-instance self-training", "tab:weakly_methods", False),
        ("MGFN", 2023, "chen2023mgfn", "Video-level weak supervision", dash, dash, dash, "86.7", "80.1", "I3D", "Multi-granularity MIL", "tab:weakly_methods", False),
        ("UR-DMU (RGB)", 2023, "zhou2023dmu", "Video-level weak supervision", dash, dash, dash, "87.0", "81.7", "I3D", "Uncertainty-regulated dual memory", "tab:weakly_methods", False),
        ("UR-DMU (RGB+audio)", 2023, "zhou2023dmu", "Video-level weak supervision", dash, dash, dash, dash, "81.8", "I3D + VGGish", "Modality ablation", "tab:weakly_methods", False),
        ("PEL4VAD", 2024, "zhang2024pel4vad", "Video labels + CLIP prompt features", dash, dash, "98.1", "86.8", "85.6", "I3D + CLIP prompt features", "Prompt-enhanced context learning", "tab:weakly_methods", False),
    ]
    ssl = [
        ("Georgescu et al.", 2021, "georgescu2021anomaly", "Self-supervised", "97.8", "89.3", "82.7", dash, dash, "Multi-task CNN", "Pretext discrepancy", "tab:self_supervised_methods", False),
        ("Jigsaw", 2022, "wang2022video_jigsaw", "Self-supervised", "96.8", "87.5", "75.2", dash, dash, "Spatiotemporal jigsaw", "Pretext discrepancy", "tab:self_supervised_methods", False),
        ("Cho et al.", 2023, "cho2023look", "Self-supervised", "97.6", "89.8", "79.3", dash, dash, "Contrastive temporal neighbors", "Contrastive", "tab:self_supervised_methods", False),
        ("SSMTL++v1", 2023, "barbalau2023ssmtl", "Self-supervised", dash, "93.7", "82.9", dash, dash, "Multi-task + CvT", "Pretext discrepancy", "tab:self_supervised_methods", False),
        ("SSMTL++v2", 2023, "barbalau2023ssmtl", "Self-supervised", dash, "91.6", "83.8", dash, dash, "Alternative configuration", "Pretext discrepancy", "tab:self_supervised_methods", False),
        ("HSC", 2023, "sun2023hierarchical", "Normal-only semantic contrast", "98.1", "93.7", "83.4", dash, dash, "Semantic parsing + AE/memory", "Reconstruction + contrastive", "tab:self_supervised_methods", False),
    ]
    transformer = [
        ("CT-D2GAN", 2021, "feng2021ct", "Normal-only", "97.2", "85.9", "77.7", dash, dash, "CNN + Transformer hybrid", "Prediction", "tab:transformer_methods", False),
        ("TEVAD", 2023, "chen2024tevad", "Video-level weak supervision", dash, dash, dash, "84.9", dash, "Caption-augmented MIL", "MIL + language", "tab:transformer_methods", False),
        ("SGTTD", 2024, "wu2022self", "Video-level weak supervision", dash, dash, "97.3", "85.1", dash, "Self-guided temporal transformer", "Weak temporal discrimination", "tab:transformer_methods", False),
    ]
    foundation = [
        ("LAVAD", 2024, "zanella2024harnessing", "Training-free", dash, dash, dash, "78.1", dash, "CLIP ViT-L/14", "Prompt similarity", "tab:foundation_methods", False),
        ("VadCLIP", 2024, "wu2024vadclip", "Video labels + frozen CLIP", dash, dash, dash, "88.0", "84.5", "CLIP ViT-B/16", "Vision-language alignment", "tab:foundation_methods", False),
        ("PEL4VAD", 2024, "zhang2024pel4vad", "Video labels + CLIP prompt features", dash, dash, "98.1", "86.8", "85.6", "I3D + CLIP prompt features", "Prompt-enhanced context learning", "tab:foundation_methods", False),
        ("HAWK", 2024, "tang2024hawk", "Instruction tuning", dash, dash, dash, "NR", "NR", "VideoLLaMA", "Open-world description", "tab:foundation_methods", False),
        ("Follow the Rules", 2024, "yang2024follow", "Rule induction / verification", dash, dash, dash, "80.3", dash, "LLM/VLM rule pipeline", "Rule violation", "tab:foundation_methods", False),
        ("AnyAnomaly", 2026, "ahn2026anyanomaly", "Training-free customizable VQA", dash, dash, dash, "NR", "NR", "LVLM", "User-defined concepts", "tab:foundation_methods", False),
        ("ASK-HINT", 2026, "zou2026askhint", "Training-free action-centric prompting", dash, dash, dash, "NR", "NR", "Frozen VLM", "Prompt similarity", "tab:foundation_methods", False),
        ("LAVIDA", 2026, "dai2026lavida", "Pseudo-anomaly; no real VAD training data", dash, dash, dash, "NR", "NR", "MLLM", "Zero-shot frame/pixel", "tab:foundation_methods", False),
        ("Alert-CLIP", 2026, "zhu2026alertclip", "Representation tuning", dash, dash, dash, "NR", "NR", "CLIP", "Multi-level alignment", "tab:foundation_methods", False),
    ]

    cols = [
        "method",
        "year",
        "citation_key",
        "training_regime",
        "ped2_auc",
        "avenue_auc",
        "shtech_auc",
        "ucf_crime_auc",
        "xd_violence_ap",
        "representation",
        "scoring_mechanism",
        "manuscript_table",
        "canonical_for_s4",
    ]
    named = {
        "consolidated_normal": [dict(zip(cols, r[:-1] + (str(r[-1]).lower(),))) for r in [(*x[:-1], x[-1]) for x in consolidated if x[11] == "tab:consolidated_performance"]],
        "consolidated_weak": [dict(zip(cols, (*x[:-1], str(x[-1]).lower()))) for x in consolidated if x[11] == "tab:weak_foundation_performance"],
        "reconstruction": [dict(zip(cols, (*x[:-1], str(x[-1]).lower()))) for x in reconstruction],
        "prediction": [dict(zip(cols, (*x[:-1], str(x[-1]).lower()))) for x in prediction],
        "weakly": [dict(zip(cols, (*x[:-1], str(x[-1]).lower()))) for x in weakly],
        "ssl": [dict(zip(cols, (*x[:-1], str(x[-1]).lower()))) for x in ssl],
        "transformer": [dict(zip(cols, (*x[:-1], str(x[-1]).lower()))) for x in transformer],
        "foundation": [dict(zip(cols, (*x[:-1], str(x[-1]).lower()))) for x in foundation],
    }
    # Fix canonical flag encoding
    def pack(rows):
        out = []
        for x in rows:
            d = {
                "method": x[0],
                "year": x[1],
                "citation_key": x[2],
                "training_regime": x[3],
                "ped2_auc": x[4],
                "avenue_auc": x[5],
                "shtech_auc": x[6],
                "ucf_crime_auc": x[7],
                "xd_violence_ap": x[8],
                "representation": x[9],
                "scoring_mechanism": x[10],
                "manuscript_table": x[11],
                "canonical_for_s4": "yes" if x[12] else "no",
            }
            out.append(d)
        return out

    return {
        "consolidated_normal": pack([x for x in consolidated if x[11] == "tab:consolidated_performance"]),
        "consolidated_weak": pack([x for x in consolidated if x[11] == "tab:weak_foundation_performance"]),
        "reconstruction": pack(reconstruction),
        "prediction": pack(prediction),
        "weakly": pack(weakly),
        "ssl": pack(ssl),
        "transformer": pack(transformer),
        "foundation": pack(foundation),
        "all_perf": pack(
            consolidated + reconstruction + prediction + weakly + ssl + transformer + foundation
        ),
    }


def fire_camera_tables() -> tuple[list[dict], list[dict], list[dict]]:
    fire_cls = [
        {
            "year": 2015,
            "study": "Foggia et al.",
            "citation_key": "foggia2015fire",
            "architecture": "Multi-expert CNN",
            "evaluation_corpus": "Surveillance videos",
            "metric": "accuracy",
            "value": "93.5",
            "task": "classification",
            "primary_tier": "2",
            "note": "Early real-time video fire classifier; corpus-specific protocol",
            "manuscript_table": "tab:sota_fire_classification",
        },
        {
            "year": 2019,
            "study": "Muhammad et al.",
            "citation_key": "muhammad2019efficient",
            "architecture": "Fine-tuned SqueezeNet",
            "evaluation_corpus": "Custom CCTV",
            "metric": "accuracy",
            "value": "94.5",
            "task": "classification",
            "primary_tier": "2",
            "note": "Lightweight surveillance-oriented model",
            "manuscript_table": "tab:sota_fire_classification",
        },
        {
            "year": 2019,
            "study": "FireNet",
            "citation_key": "jadon2019firenet",
            "architecture": "Compact CNN",
            "evaluation_corpus": "FireNet",
            "metric": "accuracy",
            "value": "95.2",
            "task": "classification",
            "primary_tier": "2",
            "note": "Preprint-only; not used for SOTA claims",
            "manuscript_table": "tab:sota_fire_classification",
        },
        {
            "year": 2022,
            "study": "Huang / Chen et al.",
            "citation_key": "chen2022fire",
            "architecture": "Wavelet + CNN",
            "evaluation_corpus": "Benchmark image and video sets",
            "metric": "accuracy",
            "value": "96.8",
            "task": "classification",
            "primary_tier": "2",
            "note": "Spectral features reduce some fire-like false alarms",
            "manuscript_table": "tab:sota_fire_classification",
        },
    ]
    fire_det = [
        {
            "year": 2022,
            "study": "Guan et al.",
            "citation_key": "guan2022improved",
            "architecture": "Mask R-CNN variant",
            "evaluation_corpus": "FLAME",
            "metric": "mIoU",
            "value": "82.3",
            "task": "segmentation",
            "primary_tier": "2",
            "note": "Aerial fire masks; not comparable with detection mAP",
            "manuscript_table": "tab:sota_fire_detection",
        },
        {
            "year": 2023,
            "study": "Niu et al.",
            "citation_key": "niu2023improved",
            "architecture": "YOLOv5 + infrared",
            "evaluation_corpus": "UAV infrared corpus",
            "metric": "mAP",
            "value": "89.2",
            "task": "detection",
            "primary_tier": "2",
            "note": "Modality-specific UAV setting",
            "manuscript_table": "tab:sota_fire_detection",
        },
        {
            "year": 2024,
            "study": "Park and Lee",
            "citation_key": "park2024wildfire",
            "architecture": "YOLOv8 and RT-DETR with augmentation",
            "evaluation_corpus": "Wildfire corpus",
            "metric": "mAP",
            "value": "91.0",
            "task": "detection",
            "primary_tier": "2",
            "note": "Reported best configuration; split and IoU threshold are study-specific",
            "manuscript_table": "tab:sota_fire_detection",
        },
        {
            "year": 2024,
            "study": "Gao et al.",
            "citation_key": "gao2024twostage",
            "architecture": "Two-stage deep model",
            "evaluation_corpus": "Heritage buildings",
            "metric": "F1",
            "value": "93.1",
            "task": "detection and classification",
            "primary_tier": "2",
            "note": "Domain-specific indoor early-fire setting",
            "manuscript_table": "tab:sota_fire_detection",
        },
    ]
    camera = [
        {
            "year": 2006,
            "study": "Ribnick et al.",
            "citation_key": "ribnick2006realtime",
            "method": "Low-level CV + DSP",
            "faults": "Spray, displacement",
            "corpus": "Custom",
            "real_or_synthetic": "Real demonstrations",
            "latency_far": "Real-time; FAR not standardized",
            "limitation": "Small study-specific collection",
            "primary_tier": "3",
            "manuscript_table": "tab:sota_camera",
        },
        {
            "year": 2017,
            "study": "Mantini and Shah",
            "citation_key": "mantini2017signal",
            "method": "Signal-detection and time-series features",
            "faults": "Occlusion, displacement, defocus",
            "corpus": "Custom",
            "real_or_synthetic": "Mixed",
            "latency_far": "EER and decision delay in the study protocol",
            "limitation": "Camera-specific baseline assumptions",
            "primary_tier": "3",
            "manuscript_table": "tab:sota_camera",
        },
        {
            "year": 2019,
            "study": "Mantini and Shah (UHCTD)",
            "citation_key": "mantini2019uhctd",
            "method": "CNN and feature baselines with UHCTD",
            "faults": "Covered, defocused, moved",
            "corpus": "UHCTD",
            "real_or_synthetic": "Synthetic faults on real feeds",
            "latency_far": "Protocol-specific",
            "limitation": "Two-camera benchmark; limited gradual faults",
            "primary_tier": "3",
            "manuscript_table": "tab:sota_camera",
        },
        {
            "year": 2020,
            "study": "ADOC",
            "citation_key": "doshi2022adoc",
            "method": "Online anomaly detection",
            "faults": "Scene + camera tampering",
            "corpus": "Campus video",
            "real_or_synthetic": "Mixed",
            "latency_far": "Online protocol",
            "limitation": "Small mixed-tier corpus",
            "primary_tier": "3",
            "manuscript_table": "tab:sota_camera",
        },
        {
            "year": 2023,
            "study": "Mantini and Shah (feature survey)",
            "citation_key": "mantini2023feature_survey",
            "method": "Multi-feature time-series analysis",
            "faults": "Multiple tampering types",
            "corpus": "Real surveillance",
            "real_or_synthetic": "Mixed",
            "latency_far": "Study-specific",
            "limitation": "No common false-alarm-rate standard",
            "primary_tier": "3",
            "manuscript_table": "tab:sota_camera",
        },
    ]
    return fire_cls, fire_det, camera


def dataset_tables() -> tuple[list[dict], list[dict], list[dict]]:
    vad = [
        ["UCSD Ped1", "mahadevan2010anomaly", 2010, "34", "36", "1", "3", "Frame + pixel", "158x238", "Non-pedestrian entities (bikes, carts)", "1"],
        ["UCSD Ped2", "mahadevan2010anomaly", 2010, "16", "12", "1", "3", "Frame + pixel", "240x360", "Non-pedestrian entities (bikes, skaters)", "1"],
        ["UMN", "mehran2009abnormal", 2009, "", "11", "3", "1", "Frame", "320x240", "Crowd panic and escape", "1"],
        ["CUHK Avenue", "lu2013abnormal", 2013, "16", "21", "1", "5", "Frame + pixel", "360x640", "Running, throwing, loitering", "1"],
        ["ShanghaiTech", "luo2017revisit", 2017, "330", "107", "13", "11", "Frame", "Various", "Chasing, brawling, cycling", "1"],
        ["UCF-Crime", "sultani2018real", 2018, "1610", "290", "Many", "13", "Video-level", "Various", "13 real-world crime categories", "1"],
        ["Street Scene", "ramachandra2020street", 2020, "46", "35", "1", "17", "Frame + bbox", "1280x720", "Jaywalking, loitering, vehicle anomalies", "1"],
        ["XD-Violence", "wu2020not", 2020, "3954", "800", "Many", "6", "Video-level", "Various", "Violence with audio track", "1"],
        ["ADOC", "doshi2022adoc", 2020, "", "18", "1", "5", "Frame", "VGA", "Campus anomalies + camera tampering", "1+3"],
        ["UBnormal", "acsintoae2022ubnormal", 2022, "268", "211", "29", "22", "Frame + pixel", "720x1080", "Synthetic scenes with pixel masks", "1"],
        ["NWPU Campus", "cao2023nwpu", 2023, "305", "148", "43", "28", "Frame + bbox", "1080p", "Large-scale campus multi-scene", "1"],
        ["CHAD", "pazho2023chad", 2023, "", "", "4", "6", "Frame + bbox", "HD", "High-resolution multi-view", "1"],
    ]
    keys = [
        "dataset",
        "citation_key",
        "year",
        "train",
        "test",
        "scenes",
        "n_categories",
        "annotation",
        "resolution",
        "primary_anomaly_types",
        "primary_tier",
    ]
    vad_rows = [dict(zip(keys, r)) for r in vad]
    fire = [
        {
            "dataset": "Foggia",
            "citation_key": "foggia2015fire",
            "year": 2015,
            "size": "62 videos",
            "fire": "yes",
            "smoke": "yes",
            "type": "Cls",
            "source": "Surveillance",
            "feature": "Early real-world surveillance fire dataset",
            "primary_tier": "2",
        },
        {
            "dataset": "BoWFire",
            "citation_key": "chino2015bowfire",
            "year": 2015,
            "size": "226 images",
            "fire": "yes",
            "smoke": "no",
            "type": "Cls + Seg",
            "source": "Web",
            "feature": "Superpixel-level fire annotation",
            "primary_tier": "2",
        },
        {
            "dataset": "FireNet",
            "citation_key": "jadon2019firenet",
            "year": 2019,
            "size": "~2500 images",
            "fire": "yes",
            "smoke": "no",
            "type": "Cls",
            "source": "Mixed",
            "feature": "Balanced binary fire/non-fire",
            "primary_tier": "2",
        },
        {
            "dataset": "FiSmo",
            "citation_key": "cazzolato2017fismo",
            "year": 2017,
            "size": "6 sub-collections",
            "fire": "yes",
            "smoke": "yes",
            "type": "Cls + Seg",
            "source": "Mixed / web",
            "feature": "Compilation of emergency-situation fire and smoke sets",
            "primary_tier": "2",
        },
        {
            "dataset": "FLAME",
            "citation_key": "shamsoshoara2021aerial",
            "year": 2021,
            "size": "2003 img + 39 vid",
            "fire": "yes",
            "smoke": "yes",
            "type": "Cls + Seg",
            "source": "UAV aerial",
            "feature": "Aerial perspective with instance masks",
            "primary_tier": "2",
        },
        {
            "dataset": "D-Fire",
            "citation_key": "de2022dfire",
            "year": 2022,
            "size": "21527 images",
            "fire": "yes",
            "smoke": "yes",
            "type": "Det",
            "source": "Mixed",
            "feature": "Multi-environment bounding boxes",
            "primary_tier": "2",
        },
        {
            "dataset": "FASDD",
            "citation_key": "wang2024fasdd",
            "year": 2024,
            "size": "120000+ images",
            "fire": "yes",
            "smoke": "yes",
            "type": "Det",
            "source": "Remote sensing + ground",
            "feature": "Largest heterogeneous fire/smoke set",
            "primary_tier": "2",
        },
    ]
    cam = [
        {
            "dataset": "Ribnick et al. corpus",
            "citation_key": "ribnick2006realtime",
            "year": 2006,
            "videos": "40+",
            "anomaly_events": "30+",
            "resolution": "640x480",
            "anomaly_types": "Spray, physical displacement",
            "public": "Partial",
            "primary_tier": "3",
        },
        {
            "dataset": "UHCTD",
            "citation_key": "mantini2019uhctd",
            "year": 2019,
            "videos": "288 h (2 cams)",
            "anomaly_events": "Synthetic",
            "resolution": "NR",
            "anomaly_types": "Covered, defocused, moved",
            "public": "Yes",
            "primary_tier": "3",
        },
        {
            "dataset": "ADOC",
            "citation_key": "doshi2022adoc",
            "year": 2020,
            "videos": "18",
            "anomaly_events": "Mixed",
            "resolution": "VGA",
            "anomaly_types": "Camera tampering + scene anomalies",
            "public": "Yes",
            "primary_tier": "1+3",
        },
    ]
    return vad_rows, fire, cam


APPRAISAL_FLAGS = {
    "wu2024vadclip": "pretraining/backbone confound vs C3D MIL baseline; do not attribute 88.0 vs 75.4 solely to weak supervision",
    "zhang2024pel4vad": "pretraining/backbone confound (I3D + CLIP prompts)",
    "jadon2019firenet": "preprint-only; not used for comparative or SOTA claims",
    "barbalau2023ssmtl": "retain v1 and v2 separately; do not mix best Avenue with best ShanghaiTech",
    "zhou2023dmu": "single 2023 AAAI method; RGB vs RGB+audio XD-Violence gap is 81.66 vs 81.77 in the source",
    "ahn2026anyanomaly": "2026 paper; emerging direction only; not used for benchmark leadership",
    "zou2026askhint": "2026 paper; emerging direction only",
    "dai2026lavida": "2026 paper; emerging direction only",
    "zhu2026alertclip": "2026 paper; emerging direction only",
}


def build_s3(perf: dict, fire_cls, fire_det, camera) -> list[dict]:
    rows_by_key = {}

    def upsert(key, **kwargs):
        rec = rows_by_key.setdefault(
            key,
            {
                "citation_key": key,
                "method_or_study": "",
                "year": "",
                "primary_tier": "",
                "multi_category_flag": "no",
                "training_regime": "",
                "scoring_mechanism": "",
                "representation": "",
                "modality": "RGB",
                "datasets": "",
                "metric": "",
                "result_summary": "",
                "deployment_reporting": "NR",
                "publication_category": "peer_reviewed",
                "manuscript_tables": "",
                "appraisal_D1": STATUS_PENDING,
                "appraisal_D2": STATUS_PENDING,
                "appraisal_D3": STATUS_PENDING,
                "appraisal_D4": STATUS_PENDING,
                "appraisal_D5": STATUS_PENDING,
                "appraisal_flag": APPRAISAL_FLAGS.get(key, ""),
                "verification_status": STATUS_TRANSCRIBED,
            },
        )
        overwrite = {"primary_tier", "method_or_study", "year"}
        for k, v in kwargs.items():
            if k == "manuscript_tables":
                existing = [x for x in rec["manuscript_tables"].split(";") if x]
                if v and v not in existing:
                    existing.append(v)
                rec["manuscript_tables"] = ";".join(existing)
            elif k == "datasets":
                existing = [x for x in rec["datasets"].split(";") if x]
                for part in str(v).split(";"):
                    if part and part not in existing:
                        existing.append(part)
                rec["datasets"] = ";".join(existing)
            elif k == "result_summary":
                existing = [x for x in rec["result_summary"].split(" | ") if x]
                for part in str(v).split(" | "):
                    if part and part not in existing:
                        existing.append(part)
                rec["result_summary"] = " | ".join(existing)
            elif k in overwrite and v:
                rec[k] = v
            elif v and not rec.get(k):
                rec[k] = v
            elif k in rec and v:
                rec[k] = rec[k] or v

    for r in perf["all_perf"]:
        ds = []
        summary = []
        for name, col, metric in (
            ("Ped2", "ped2_auc", "frame AUC"),
            ("Avenue", "avenue_auc", "frame AUC"),
            ("ShanghaiTech", "shtech_auc", "frame AUC"),
            ("UCF-Crime", "ucf_crime_auc", "frame AUC"),
            ("XD-Violence", "xd_violence_ap", "AP"),
        ):
            val = r[col]
            if val and val not in {"NR", "--"}:
                ds.append(name)
                summary.append(f"{name} {metric}={val}")
        modality = "RGB+audio" if "audio" in r["method"].lower() or "VGGish" in r["representation"] else "RGB"
        upsert(
            r["citation_key"],
            method_or_study=r["method"],
            year=r["year"],
            primary_tier="1",
            training_regime=r["training_regime"],
            scoring_mechanism=r["scoring_mechanism"],
            representation=r["representation"],
            modality=modality,
            datasets=";".join(ds),
            metric="frame-level AUC unless XD-Violence AP",
            result_summary=" | ".join(summary),
            manuscript_tables=r["manuscript_table"],
        )

    for r in fire_cls + fire_det:
        upsert(
            r["citation_key"],
            method_or_study=r["study"],
            year=r["year"],
            primary_tier="2",
            training_regime="task-specific supervised",
            scoring_mechanism=r["task"],
            representation=r["architecture"],
            datasets=r["evaluation_corpus"],
            metric=r["metric"],
            result_summary=f"{r['metric']}={r['value']}",
            manuscript_tables=r["manuscript_table"],
        )
    for r in camera:
        upsert(
            r["citation_key"],
            method_or_study=r["study"],
            year=r["year"],
            primary_tier="3",
            training_regime="study-specific",
            scoring_mechanism="change-point / quality / CNN baseline",
            representation=r["method"],
            datasets=r["corpus"],
            metric="study-specific (EER/FAR/latency)",
            result_summary=r["latency_far"],
            manuscript_tables=r["manuscript_table"],
        )
    if "doshi2022adoc" in rows_by_key:
        rows_by_key["doshi2022adoc"]["multi_category_flag"] = "yes"
        rows_by_key["doshi2022adoc"]["primary_tier"] = "3"
    return sorted(rows_by_key.values(), key=lambda r: (str(r["year"]), r["citation_key"]))


def flatten_provenance(perf, fire_cls, fire_det) -> list[dict]:
    rows = []
    pid = 1

    def add(**kwargs):
        nonlocal pid
        rec = {
            "provenance_id": f"P{pid:04d}",
            "verification_status": STATUS_TRANSCRIBED,
            "page_confirmation": STATUS_PENDING,
        }
        rec.update(kwargs)
        rows.append(rec)
        pid += 1

    metric_map = [
        ("ped2_auc", "UCSD Ped2", "frame-level AUC (%)"),
        ("avenue_auc", "CUHK Avenue", "frame-level AUC (%)"),
        ("shtech_auc", "ShanghaiTech", "frame-level AUC (%)"),
        ("ucf_crime_auc", "UCF-Crime", "frame-level AUC (%)"),
        ("xd_violence_ap", "XD-Violence", "AP (%)"),
    ]
    seen_canonical = set()
    for r in perf["all_perf"]:
        for col, dataset, metric in metric_map:
            val = r[col]
            if not val or val in {"NR", "--"}:
                continue
            key = (r["citation_key"], dataset, metric, val, r["method"])
            canonical = r["canonical_for_s4"] == "yes"
            if canonical:
                seen_canonical.add((r["citation_key"], dataset, val))
            add(
                manuscript_table=r["manuscript_table"],
                method=r["method"],
                citation_key=r["citation_key"],
                year=r["year"],
                dataset=dataset,
                metric=metric,
                value=val,
                training_regime=r["training_regime"],
                representation=r["representation"],
                scoring_mechanism=r["scoring_mechanism"],
                immediate_source=f"cited study {r['citation_key']}",
                canonical_table=r["canonical_for_s4"],
                note="Repeated local table row" if r["canonical_for_s4"] == "no" else "Canonical consolidated comparison",
            )
    for r in fire_cls + fire_det:
        add(
            manuscript_table=r["manuscript_table"],
            method=r["study"],
            citation_key=r["citation_key"],
            year=r["year"],
            dataset=r["evaluation_corpus"],
            metric=r["metric"],
            value=r["value"],
            training_regime="task-specific supervised",
            representation=r["architecture"],
            scoring_mechanism=r["task"],
            immediate_source=f"cited study {r['citation_key']}",
            canonical_table="no",
            note=(
                f"Extended fire/hazard table; outside the 43-cell principal "
                f"consolidated comparison. {r['note']}"
            ).strip(),
        )
    return rows


def figure_sources() -> None:
    write_csv(
        S4F / "fig_prisma_flow.csv",
        ["slot", "label", "n", "verification_status"],
        [
            {"slot": "id_ieee", "label": "IEEE Xplore", "n": 3214, "verification_status": STATUS_REPORTED},
            {"slot": "id_acm", "label": "ACM Digital Library", "n": 1987, "verification_status": STATUS_REPORTED},
            {"slot": "id_scopus", "label": "Scopus", "n": 4568, "verification_status": STATUS_REPORTED},
            {"slot": "id_wos", "label": "Web of Science", "n": 3511, "verification_status": STATUS_REPORTED},
            {"slot": "id_scholar", "label": "Google Scholar (supplementary)", "n": 2142, "verification_status": STATUS_REPORTED},
            {"slot": "id_other", "label": "Citation tracking + 2026 proceedings", "n": 1060, "verification_status": STATUS_REPORTED},
            {"slot": "N1", "label": "Total identified", "n": 16482, "verification_status": STATUS_REPORTED},
            {"slot": "dup", "label": "Duplicates removed", "n": 2128, "verification_status": STATUS_REPORTED},
            {"slot": "oor", "label": "Out-of-range date", "n": 166, "verification_status": STATUS_REPORTED},
            {"slot": "lang", "label": "Non-English", "n": 113, "verification_status": STATUS_REPORTED},
            {"slot": "type", "label": "Ineligible document type", "n": 170, "verification_status": STATUS_REPORTED},
            {"slot": "N2", "label": "Title/abstract screened", "n": 13905, "verification_status": STATUS_REPORTED},
            {"slot": "ta_ex", "label": "Title/abstract excluded", "n": 12958, "verification_status": STATUS_REPORTED},
            {"slot": "N3", "label": "Full texts sought", "n": 947, "verification_status": STATUS_REPORTED},
            {"slot": "not_ret", "label": "Not retrieved", "n": 44, "verification_status": STATUS_REPORTED},
            {"slot": "N4", "label": "Full text assessed", "n": 903, "verification_status": STATUS_REPORTED},
            {"slot": "EC1", "label": "EC1 excluded", "n": 35, "verification_status": STATUS_REPORTED},
            {"slot": "EC2", "label": "EC2 excluded", "n": 51, "verification_status": STATUS_REPORTED},
            {"slot": "EC3", "label": "EC3 excluded", "n": 93, "verification_status": STATUS_REPORTED},
            {"slot": "EC4", "label": "EC4 excluded", "n": 78, "verification_status": STATUS_REPORTED},
            {"slot": "EC5", "label": "EC5 excluded", "n": 30, "verification_status": STATUS_REPORTED},
            {"slot": "N5", "label": "Studies included", "n": 616, "verification_status": STATUS_REPORTED},
            {"slot": "S3_core", "label": "Core studies in S3", "n": 132, "verification_status": STATUS_REPORTED},
        ],
    )
    write_csv(
        S4F / "fig2a_anomaly_tier_counts.csv",
        ["tier_id", "tier_name", "n_included_primary", "share_of_N5", "verification_status", "note"],
        [
            {
                "tier_id": "1",
                "tier_name": "Behavioural / object interaction",
                "n_included_primary": 441,
                "share_of_N5": round(441 / 616, 4),
                "verification_status": STATUS_REPORTED,
                "note": "Primary-tier assignment; multi-category studies counted once",
            },
            {
                "tier_id": "2",
                "tier_name": "Physical hazard (fire/smoke)",
                "n_included_primary": 122,
                "share_of_N5": round(122 / 616, 4),
                "verification_status": STATUS_REPORTED,
                "note": "Primary-tier assignment; multi-category studies counted once",
            },
            {
                "tier_id": "3",
                "tier_name": "Camera / video-feed integrity",
                "n_included_primary": 53,
                "share_of_N5": round(53 / 616, 4),
                "verification_status": STATUS_REPORTED,
                "note": "Primary-tier assignment; multi-category studies counted once",
            },
        ],
    )
    write_csv(
        S4F / "fig_temporal_reasoning_suitability.csv",
        [
            "mechanism",
            "tier1_person_scene",
            "tier2_fire_smoke",
            "tier3_camera_feed",
            "source_figure",
            "note",
        ],
        [
            {
                "mechanism": "Implicit temporal (3D conv/RNN)",
                "tier1_person_scene": "High",
                "tier2_fire_smoke": "Moderate",
                "tier3_camera_feed": "Low",
                "source_figure": "figure_reasoning_tier_heatmap.png",
                "note": "Transcribed from the deposited figure. Manuscript caption describes a mechanism-cue-validation matrix; the image is a relative-suitability heatmap.",
            },
            {
                "mechanism": "Temporal attention (Transformer)",
                "tier1_person_scene": "High",
                "tier2_fire_smoke": "Moderate",
                "tier3_camera_feed": "Low",
                "source_figure": "figure_reasoning_tier_heatmap.png",
                "note": "",
            },
            {
                "mechanism": "Causal temporal convolution",
                "tier1_person_scene": "High",
                "tier2_fire_smoke": "Low",
                "tier3_camera_feed": "Moderate",
                "source_figure": "figure_reasoning_tier_heatmap.png",
                "note": "",
            },
            {
                "mechanism": "Spatio-temporal graphs",
                "tier1_person_scene": "High",
                "tier2_fire_smoke": "Low",
                "tier3_camera_feed": "Low",
                "source_figure": "figure_reasoning_tier_heatmap.png",
                "note": "",
            },
            {
                "mechanism": "Scene graphs + symbolic rules",
                "tier1_person_scene": "High",
                "tier2_fire_smoke": "Low",
                "tier3_camera_feed": "Moderate",
                "source_figure": "figure_reasoning_tier_heatmap.png",
                "note": "",
            },
            {
                "mechanism": "LLM rule induction",
                "tier1_person_scene": "Moderate",
                "tier2_fire_smoke": "Low",
                "tier3_camera_feed": "Low",
                "source_figure": "figure_reasoning_tier_heatmap.png",
                "note": "",
            },
            {
                "mechanism": "Temporal logic (LTL/STL)",
                "tier1_person_scene": "Moderate",
                "tier2_fire_smoke": "Low",
                "tier3_camera_feed": "High",
                "source_figure": "figure_reasoning_tier_heatmap.png",
                "note": "",
            },
        ],
    )
    write_csv(
        S4 / "figure_manifest.csv",
        [
            "figure_file",
            "manuscript_label",
            "kind",
            "source_data_file",
            "notes",
        ],
        [
            {
                "figure_file": "figure2a_anomaly_category_refined.png",
                "manuscript_label": "fig:tax_a / fig:taxonomy_tree panel a",
                "kind": "data",
                "source_data_file": "S4_performance_provenance/figure_source_data/fig2a_anomaly_tier_counts.csv",
                "notes": "Provisional primary-tier counts 441 / 122 / 53 summing to N5=616",
            },
            {
                "figure_file": "figure2a_anomaly_category_revised.png",
                "manuscript_label": "superseded working copy of panel a",
                "kind": "data",
                "source_data_file": "S4_performance_provenance/figure_source_data/fig2a_anomaly_tier_counts.csv",
                "notes": "Byte-identical working copy retained for audit; prefer the refined filename in the manuscript",
            },
            {
                "figure_file": "figure_reasoning_tier_heatmap.png",
                "manuscript_label": "fig:temporal_validation",
                "kind": "data",
                "source_data_file": "S4_performance_provenance/figure_source_data/fig_temporal_reasoning_suitability.csv",
                "notes": "Transcribed High/Moderate/Low cells from the deposited PNG",
            },
            {
                "figure_file": "(TikZ in main.tex)",
                "manuscript_label": "fig:prisma",
                "kind": "data",
                "source_data_file": "S4_performance_provenance/figure_source_data/fig_prisma_flow.csv",
                "notes": "PRISMA flow is drawn in TikZ from provisional counts",
            },
            {
                "figure_file": "litstudy_evidence_topic_landscape.png",
                "manuscript_label": "fig:litstudy_topics panel a",
                "kind": "data",
                "source_data_file": "S5_validation/topic_model/document_topics.csv",
                "notes": "Exploratory nonlinear map of 52 table-extracted S3 studies; not the provisional N5 set",
            },
            {
                "figure_file": "litstudy_evidence_topic_clouds.png",
                "manuscript_label": "fig:litstudy_topics panel b",
                "kind": "data",
                "source_data_file": "S5_validation/topic_model/topic_terms.csv",
                "notes": "Six NMF topics from titles and deposited S3 descriptors; no generated abstracts",
            },
            {
                "figure_file": "framework_diagram.png",
                "manuscript_label": "fig:framework",
                "kind": "schematic",
                "source_data_file": "",
                "notes": "Conceptual diagram; no numerical source table",
            },
            {
                "figure_file": "methods_overview.png",
                "manuscript_label": "fig:methods_overview",
                "kind": "schematic",
                "source_data_file": "",
                "notes": "Conceptual diagram; no numerical source table",
            },
            {
                "figure_file": "foundation_model_diagram.png",
                "manuscript_label": "fig:foundation_model_diagram",
                "kind": "schematic",
                "source_data_file": "",
                "notes": "Conceptual diagram; no numerical source table",
            },
            {
                "figure_file": "Protocol Comparability Decision Tree.png",
                "manuscript_label": "fig:comparability_tree",
                "kind": "schematic",
                "source_data_file": "",
                "notes": "Decision procedure; no numerical source table",
            },
            {
                "figure_file": "Deployment-oriented modular surveillance architecture.png",
                "manuscript_label": "fig:modular_deployment",
                "kind": "schematic",
                "source_data_file": "",
                "notes": "Proposed architecture; no numerical source table",
            },
        ],
    )


def data_dictionary() -> None:
    rows = [
        ("S1", "07_prisma_flow.csv", "n", "integer", "Count at a PRISMA slot"),
        ("S1", "07_prisma_flow.csv", "verification_status", "enum", "provisional_author_verification_required | transcribed_from_manuscript | author_verification_required"),
        ("S1", "06_eligibility_inclusion_exclusion.csv", "criterion_id", "string", "IC1–IC5 or EC1–EC5"),
        ("S2", "citation_inventory.csv", "citation_key", "string", "BibTeX key used in main.tex"),
        ("S2", "citation_inventory.csv", "role_in_review", "enum", "Heuristic role label from title/type; not a substitute for S3 coding"),
        ("S3", "core_primary_evidence.csv", "primary_tier", "enum", "1 behavioural, 2 hazard, 3 feed integrity"),
        ("S3", "core_primary_evidence.csv", "appraisal_D1", "enum", "L | S | H | author_verification_required"),
        ("S3", "consolidated_performance_evidence.csv", "result_id", "string", "Stable ID for one principal-table result cell"),
        ("S3", "appraisal_aggregate.csv", "recomputable_from_package", "enum", "Whether the statistic can be recalculated from deposited row-level data"),
        ("S4", "performance_provenance.csv", "canonical_table", "enum", "yes = use this value as the manuscript canonical number"),
        ("S4", "principal_table_provenance.csv", "result_id", "string", "Links the 43 principal result cells to the comparability audit"),
        ("S4", "performance_provenance.csv", "page_confirmation", "enum", "author must confirm the value against the cited PDF page"),
        ("S4", "figure_source_data/fig2a_anomaly_tier_counts.csv", "n_included_primary", "integer", "Primary-tier count; must sum to N5"),
        ("S5", "comparability/pairwise_comparability.csv", "comparable_C3", "boolean", "Agreement on benchmark, metric, supervision regime, and modality"),
        ("S5", "comparability/comparability_summary.csv", "comparability_density", "number", "Direct edges divided by all unordered pairs"),
        ("S5", "comparability/descriptive_regression_checks.csv", "ols_slope_points_per_year", "number", "Descriptive OLS slope; not a methodological effect"),
        ("S5", "topic_model/document_topics.csv", "dominant_topic", "integer", "Highest-weight NMF topic for one of the 52 table-extracted S3 studies"),
        ("S5", "topic_model/document_topics.csv", "embedding_x", "number", "First nonlinear embedding coordinate; distance is not an effect size"),
        ("S5", "topic_model/topic_terms.csv", "top_terms", "string", "Ten highest-weight tokens for the topic, semicolon separated"),
        ("S5", "topic_model/analysis_metadata.csv", "value", "string", "Fixed LitStudy model settings and interpretive boundary"),
    ]
    write_csv(
        S5 / "data_dictionary.csv",
        ["supplement", "file", "column", "type", "definition"],
        [{"supplement": a, "file": b, "column": c, "type": d, "definition": e} for a, b, c, d, e in rows],
    )


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def is_package_file(path: Path) -> bool:
    if any(part in CHECKSUM_SKIP_DIRS for part in path.parts):
        return False
    if path.name in CHECKSUM_SKIP_NAMES:
        return False
    if path.suffix.lower() in CHECKSUM_SKIP_SUFFIXES:
        return False
    return True


def write_checksums_and_audit(extra_notes: list[str]) -> None:
    files = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if not is_package_file(p):
            continue
        rel = p.relative_to(ROOT).as_posix()
        files.append((rel, sha256_file(p), p.stat().st_size))
    files.sort()
    lines = [f"{digest}  {rel}" for rel, digest, _ in files]
    (S5 / "checksums.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")

    n_s3 = sum(1 for _ in (S3 / "core_primary_evidence.csv").open(encoding="utf-8")) - 1
    n_s4 = sum(1 for _ in (S4 / "performance_provenance.csv").open(encoding="utf-8")) - 1
    n_s2 = sum(1 for _ in (S2 / "citation_inventory.csv").open(encoding="utf-8")) - 1
    report = f"""# S5 audit report

- Package version: {PACKAGE_VERSION}
- Audit date: {AS_OF}
- Files checksummed: {len(files)}
- S2 citation inventory rows: {n_s2}
- S3 core-evidence rows extracted from manuscript tables: {n_s3}
- S4 provenance rows: {n_s4}

## Automatic checks

The validation script `scripts/validate_package.py` re-runs these tests:

1. Required S1–S5 files exist.
2. PRISMA arithmetic: source rows sum to N1; N1 minus pre-screen removals equals N2; N2 minus title/abstract exclusions equals N3; N3 minus not-retrieved equals N4; N4 minus EC1–EC5 equals N5; Tier1+Tier2+Tier3 equals N5.
3. No duplicate `citation_key` in S2.
4. Every S4 `citation_key` with a numerical value exists in S2 or is flagged.
5. Figure 2a counts sum to N5.
6. The formal comparability audit contains 43 result cells, 903 pairwise rows, and 54 C3-comparable edges (6.0%; 19 classes; largest class 6).
7. The LitStudy evidence map contains one document-topic row per extended S3 study and exactly six topics.

## Author-verification gaps (not failures of this deposit)

{chr(10).join('- ' + n for n in extra_notes)}

## How a reviewer should use this package

1. Read `README.md` and `S1_search_and_selection/AUTHOR_DEPOSIT_REQUIRED.md`.
2. Re-execute the Boolean strings in `S1_search_and_selection/03_executable_search_strings.md` if checking search reproducibility.
3. Treat `verification_status = provisional_author_verification_required` as an unsupported proposed value that must be replaced from original source records before submission.
4. Use `S4_performance_provenance/principal_table_provenance.csv` for the 43 formal-analysis cells and `performance_provenance.csv` for the extended manuscript tables.
5. Treat `S5_validation/topic_model/` as an exploratory visualization of 52 table-extracted studies, not as evidence about the provisional N5 corpus.
6. Run `python S5_validation/scripts/validate_package.py`.
"""
    (S5 / "audit_report.md").write_text(report, encoding="utf-8")
    write_csv(
        S5 / "package_manifest.csv",
        ["key", "value"],
        [
            {"key": "package_version", "value": PACKAGE_VERSION},
            {"key": "audit_date", "value": AS_OF},
            {"key": "n_checksummed_files", "value": str(len(files))},
            {"key": "n_s2_rows", "value": str(n_s2)},
            {"key": "n_s3_rows", "value": str(n_s3)},
            {"key": "n_s4_rows", "value": str(n_s4)},
            {
                "key": "github",
                "value": "https://github.com/tayyabrehman96/From-Scene-Events-to-Video-Feed-Failures",
            },
        ],
    )


def main() -> None:
    s1_tables()
    if BIB.exists():
        bib = parse_bib(BIB)
        write_csv(
            S2 / "citation_inventory.csv",
            [
                "citation_key",
                "entry_type",
                "year",
                "author",
                "title",
                "journal",
                "booktitle",
                "volume",
                "number",
                "pages",
                "publisher",
                "doi",
                "url",
                "role_in_review",
                "verification_status",
            ],
            bib,
        )
    else:
        bib = list(csv.DictReader((S2 / "citation_inventory.csv").open(encoding="utf-8")))

    perf = performance_tables()
    fire_cls, fire_det, camera = fire_camera_tables()
    vad_ds, fire_ds, cam_ds = dataset_tables()

    for name, rows in perf.items():
        if name == "all_perf":
            continue
        write_csv(
            S4T / f"{name}.csv",
            list(rows[0].keys()),
            rows,
        )
    write_csv(S4T / "fire_classification.csv", list(fire_cls[0].keys()), fire_cls)
    write_csv(S4T / "fire_detection.csv", list(fire_det[0].keys()), fire_det)
    write_csv(S4T / "camera_integrity.csv", list(camera[0].keys()), camera)
    write_csv(S4T / "datasets_vad.csv", list(vad_ds[0].keys()), vad_ds)
    write_csv(S4T / "datasets_fire.csv", list(fire_ds[0].keys()), fire_ds)
    write_csv(S4T / "datasets_camera.csv", list(cam_ds[0].keys()), cam_ds)

    s3 = build_s3(perf, fire_cls, fire_det, camera)
    write_csv(
        S3 / "core_primary_evidence.csv",
        list(s3[0].keys()),
        s3,
    )
    write_csv(
        S3 / "appraisal_instrument.csv",
        ["dimension_id", "dimension", "signalling_question", "low_concern", "high_concern"],
        [
            {
                "dimension_id": "D1",
                "dimension": "Experimental transparency",
                "signalling_question": "Are preprocessing, hyperparameters, training schedule, and feature extractor described in sufficient detail to permit reimplementation?",
                "low_concern": "All four described; code or configuration released",
                "high_concern": "Backbone or training schedule unstated; no code",
            },
            {
                "dimension_id": "D2",
                "dimension": "Dataset and split integrity",
                "signalling_question": "Are train/validation/test separation, leakage controls, and annotation assumptions stated and defensible?",
                "low_concern": "Standard split used and named; leakage controls stated",
                "high_concern": "Split undocumented, self-defined without release, or test data used for model selection",
            },
            {
                "dimension_id": "D3",
                "dimension": "Metric validity",
                "signalling_question": "Do metric granularity and implementation match the task, and is threshold or operating-point selection disclosed?",
                "low_concern": "Metric matches task; thresholds and aggregation stated",
                "high_concern": "Frame-level metric reported for an event-level claim; threshold selected on test data",
            },
            {
                "dimension_id": "D4",
                "dimension": "Comparison fairness",
                "signalling_question": "Are supervision regime, backbone, pretraining source, modality, and evaluation code comparable to the baselines, or explicitly qualified where they are not?",
                "low_concern": "Baselines rerun under a common implementation, or differences stated",
                "high_concern": "Headline gain confounded with backbone or pretraining change presented as a paradigm result",
            },
            {
                "dimension_id": "D5",
                "dimension": "External validity",
                "signalling_question": "Is there evidence beyond a single in-distribution test split—cross-scene or cross-dataset testing, robustness analysis, released weights, or deployment measurement?",
                "low_concern": "Cross-dataset or cross-camera evaluation reported",
                "high_concern": "Single dataset, single split, no robustness or deployment evidence",
            },
        ],
    )
    write_csv(
        S3 / "appraisal_ratings_template.csv",
        [
            "citation_key",
            "method_or_study",
            "primary_tier",
            "D1",
            "D2",
            "D3",
            "D4",
            "D5",
            "rater",
            "note",
        ],
        [
            {
                "citation_key": r["citation_key"],
                "method_or_study": r["method_or_study"],
                "primary_tier": r["primary_tier"],
                "D1": STATUS_PENDING,
                "D2": STATUS_PENDING,
                "D3": STATUS_PENDING,
                "D4": STATUS_PENDING,
                "D5": STATUS_PENDING,
                "rater": "consensus",
                "note": "Insert L/S/H from the original independent rating files. Do not invent ratings.",
            }
            for r in s3
        ],
    )

    prov = flatten_provenance(perf, fire_cls, fire_det)
    write_csv(
        S4 / "performance_provenance.csv",
        list(prov[0].keys()),
        prov,
    )
    figure_sources()
    data_dictionary()

    notes = [
        f"The extended S3 table contains {len(s3)} unique studies; the proposed 132-study core total has no deposited source extraction and requires author verification.",
        "The appraisal agreement aggregates originated from a provisional scenario; row-level D1–D5 ratings are absent and an empty schema is provided.",
        "Raw database exports and both screeners' independent decision files are not in this deposit.",
        "PRISMA identification, screening, tier-allocation, and agreement numbers are provisional estimates without deposited source records and must not be presented as verified review results.",
        "S4 page_confirmation remains author_verification_required until each number is checked against the cited PDF.",
    ]
    write_checksums_and_audit(notes)
    print(f"Built package: S2={len(bib)} S3={len(s3)} S4={len(prov)}")


if __name__ == "__main__":
    main()
