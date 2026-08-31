#!/usr/bin/env python3
"""Generate the 43-cell comparability, pairwise, sensitivity, and trend audits."""
from __future__ import annotations

import csv
import itertools
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "S4_performance_provenance" / "manuscript_tables"
OUT = ROOT / "S5_validation" / "comparability"
S3 = ROOT / "S3_extraction"
S4 = ROOT / "S4_performance_provenance"

DATASETS = [
    ("ped2_auc", "UCSD Ped2", "frame-level micro-AUC (%)"),
    ("avenue_auc", "CUHK Avenue", "frame-level micro-AUC (%)"),
    ("shtech_auc", "ShanghaiTech", "frame-level AUC (%)"),
    ("ucf_crime_auc", "UCF-Crime", "frame-level AUC (%)"),
    ("xd_violence_ap", "XD-Violence", "average precision (%)"),
]


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def supervision_code(table: str, method: str) -> str:
    if table == "normal":
        if method == "HSC":
            return "normal-only semantic contrast"
        if method == "STG-NF":
            return "normal-only pose"
        row = method
        if row in {"Georgescu et al.", "SSMTL++v1", "SSMTL++v2"}:
            return "self-supervised"
        return "normal-only"
    if method == "VadCLIP":
        return "video labels + CLIP pretraining"
    if method == "PEL4VAD":
        return "video labels + CLIP prompt features"
    return "video labels"


def modality_code(method: str) -> str:
    return "RGB+audio" if method == "UR-DMU (RGB+audio)" else "RGB"


def build_cells() -> list[dict]:
    cells = []
    for table, filename in (
        ("normal", "consolidated_normal.csv"),
        ("weak", "consolidated_weak.csv"),
    ):
        for row in read_csv(TABLES / filename):
            for column, dataset, metric in DATASETS:
                value = row.get(column, "").strip()
                if not value or value == "NR":
                    continue
                cells.append(
                    {
                        "result_id": f"R{len(cells) + 1:02d}",
                        "source_table": (
                            "tab:consolidated_performance"
                            if table == "normal"
                            else "tab:weak_foundation_performance"
                        ),
                        "method": row["method"],
                        "citation_key": row["citation_key"],
                        "year": row["year"],
                        "benchmark": dataset,
                        "metric": metric,
                        "value": value,
                        "task_formulation": (
                            "normality-based VAD"
                            if table == "normal"
                            else "weakly supervised VAD"
                        ),
                        "supervision_regime": supervision_code(table, row["method"]),
                        "input_modality": modality_code(row["method"]),
                        "train_test_split": "NR",
                        "pretraining_source": (
                            "CLIP"
                            if row["method"] in {"VadCLIP", "PEL4VAD"}
                            else "NR"
                        ),
                        "metric_implementation": "as reported by cited study",
                        "test_time_postprocessing": "NR",
                        "representation": row["representation"],
                        "scoring_mechanism": row["scoring_mechanism"],
                        "verification_status": "transcribed_from_manuscript",
                    }
                )
    return cells


def class_key(row: dict, level: str) -> tuple:
    key = (row["benchmark"], row["metric"])
    if level in {"C2", "C3"}:
        key += (row["supervision_regime"],)
    if level == "C3":
        key += (row["input_modality"],)
    return key


def group_summary(cells: list[dict], subset: str, level: str) -> dict:
    selected = [
        row
        for row in cells
        if subset == "combined"
        or (subset == "normal" and row["source_table"] == "tab:consolidated_performance")
        or (
            subset == "weak"
            and row["source_table"] == "tab:weak_foundation_performance"
        )
    ]
    counts = Counter(class_key(row, level) for row in selected)
    edges = sum(n * (n - 1) // 2 for n in counts.values())
    possible = len(selected) * (len(selected) - 1) // 2
    return {
        "subset": subset,
        "coordinate_set": level,
        "coordinates": {
            "C1": "benchmark + metric",
            "C2": "benchmark + metric + supervision regime",
            "C3": "benchmark + metric + supervision regime + input modality",
        }[level],
        "n_result_cells": len(selected),
        "n_possible_pairs": possible,
        "n_comparable_pairs": edges,
        "comparability_density": f"{edges / possible:.6f}",
        "comparability_density_pct": f"{100 * edges / possible:.1f}",
        "n_classes": len(counts),
        "largest_class": max(counts.values()),
    }


def build_pairs(cells: list[dict]) -> list[dict]:
    pairs = []
    for index, (a, b) in enumerate(itertools.combinations(cells, 2), 1):
        same_benchmark = a["benchmark"] == b["benchmark"]
        same_metric = a["metric"] == b["metric"]
        same_supervision = a["supervision_regime"] == b["supervision_regime"]
        same_modality = a["input_modality"] == b["input_modality"]
        mismatches = [
            name
            for name, same in (
                ("benchmark", same_benchmark),
                ("metric", same_metric),
                ("supervision_regime", same_supervision),
                ("input_modality", same_modality),
            )
            if not same
        ]
        pairs.append(
            {
                "pair_id": f"P{index:03d}",
                "result_a": a["result_id"],
                "result_b": b["result_id"],
                "method_a": a["method"],
                "method_b": b["method"],
                "benchmark_a": a["benchmark"],
                "benchmark_b": b["benchmark"],
                "same_benchmark": str(same_benchmark).lower(),
                "same_metric": str(same_metric).lower(),
                "same_supervision": str(same_supervision).lower(),
                "same_modality": str(same_modality).lower(),
                "comparable_C1": str(same_benchmark and same_metric).lower(),
                "comparable_C2": str(
                    same_benchmark and same_metric and same_supervision
                ).lower(),
                "comparable_C3": str(
                    same_benchmark
                    and same_metric
                    and same_supervision
                    and same_modality
                ).lower(),
                "mismatched_recorded_coordinates": ";".join(mismatches),
                "unresolved_coordinates": (
                    "train_test_split;pretraining_source;"
                    "metric_implementation;test_time_postprocessing"
                ),
            }
        )
    return pairs


def ols(rows: list[dict], benchmark: str) -> dict:
    selected = [
        row
        for row in rows
        if row["benchmark"] == benchmark and int(row["year"]) >= 2020
    ]
    x = [float(row["year"]) for row in selected]
    y = [float(row["value"]) for row in selected]
    xbar = sum(x) / len(x)
    ybar = sum(y) / len(y)
    sxx = sum((v - xbar) ** 2 for v in x)
    slope = sum((a - xbar) * (b - ybar) for a, b in zip(x, y)) / sxx
    intercept = ybar - slope * xbar
    fitted = [intercept + slope * v for v in x]
    ss_res = sum((actual - fit) ** 2 for actual, fit in zip(y, fitted))
    ss_tot = sum((actual - ybar) ** 2 for actual in y)
    r2 = 1 - ss_res / ss_tot
    return {
        "benchmark": benchmark,
        "metric": selected[0]["metric"],
        "year_min": min(int(v) for v in x),
        "year_max": max(int(v) for v in x),
        "n": len(y),
        "minimum": f"{min(y):.1f}",
        "maximum": f"{max(y):.1f}",
        "spread": f"{max(y) - min(y):.1f}",
        "headroom_to_100": f"{100 - max(y):.1f}",
        "ols_slope_points_per_year": f"{slope:.2f}",
        "r_squared": f"{r2:.2f}",
        "interpretation": (
            "Descriptive fit to heterogeneous literature-reported values; "
            "not a methodological effect and not suitable for extrapolation."
        ),
    }


def appraisal_aggregate() -> list[dict]:
    return [
        {
            "statistic": "core_primary_studies",
            "value": "132",
            "basis": "reported review result",
            "recomputable_from_package": "no",
        },
        {
            "statistic": "rated_items",
            "value": "660",
            "basis": "132 studies x 5 dimensions",
            "recomputable_from_package": "no",
        },
        {
            "statistic": "observed_agreement_pct",
            "value": "91.2",
            "basis": "reported aggregate",
            "recomputable_from_package": "no",
        },
        {
            "statistic": "unweighted_cohen_kappa",
            "value": "0.867",
            "basis": "reported aggregate",
            "recomputable_from_package": "no",
        },
        {
            "statistic": "kappa_95ci",
            "value": "[0.832, 0.898]",
            "basis": "reported aggregate",
            "recomputable_from_package": "no",
        },
        {
            "statistic": "rating_scale",
            "value": "L | S | H",
            "basis": "D1-D5 appraisal instrument",
            "recomputable_from_package": "instrument only",
        },
    ]


def main() -> None:
    cells = build_cells()
    pairs = build_pairs(cells)
    sensitivity = [
        group_summary(cells, subset, level)
        for level in ("C1", "C2", "C3")
        for subset in ("normal", "weak", "combined")
    ]
    c3_summary = [row for row in sensitivity if row["coordinate_set"] == "C3"]
    trends = [ols(cells, name) for name in ("UCSD Ped2", "UCF-Crime", "XD-Violence")]

    write_csv(OUT / "result_cells.csv", list(cells[0]), cells)
    write_csv(OUT / "pairwise_comparability.csv", list(pairs[0]), pairs)
    write_csv(OUT / "comparability_summary.csv", list(c3_summary[0]), c3_summary)
    write_csv(OUT / "comparability_sensitivity.csv", list(sensitivity[0]), sensitivity)
    write_csv(OUT / "descriptive_regression_checks.csv", list(trends[0]), trends)
    write_csv(
        S3 / "consolidated_performance_evidence.csv", list(cells[0]), cells
    )
    write_csv(
        S3 / "appraisal_aggregate.csv",
        ["statistic", "value", "basis", "recomputable_from_package"],
        appraisal_aggregate(),
    )
    write_csv(
        S4 / "principal_table_provenance.csv",
        [
            "result_id",
            "source_table",
            "method",
            "citation_key",
            "year",
            "benchmark",
            "metric",
            "value",
            "verification_status",
        ],
        cells,
    )
    print(
        f"Built comparability audit: {len(cells)} cells, {len(pairs)} pairs, "
        f"{sum(row['comparable_C3'] == 'true' for row in pairs)} C3 edges."
    )


if __name__ == "__main__":
    main()
