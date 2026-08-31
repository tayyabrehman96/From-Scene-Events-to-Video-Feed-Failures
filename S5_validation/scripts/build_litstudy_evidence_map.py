#!/usr/bin/env python3
"""Build an exploratory LitStudy map of the 52 table-extracted S3 studies.

The analysis uses publication titles plus existing structured S3 descriptors.
It does not represent the provisional 616-study included set and does not use
synthetic abstracts.
"""
from __future__ import annotations

import csv
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud

import litstudy

ROOT = Path(__file__).resolve().parents[2]
S2 = ROOT / "S2_citation_inventory" / "citation_inventory.csv"
S3 = ROOT / "S3_extraction" / "core_primary_evidence.csv"
OUT = ROOT / "S5_validation" / "topic_model"
MAP_PNG = ROOT / "litstudy_evidence_topic_landscape.png"
CLOUD_PNG = ROOT / "litstudy_evidence_topic_clouds.png"

SEED = 42
NUM_TOPICS = 6
TOPIC_LABELS = [
    "Weakly supervised VAD",
    "Supervised hazard recognition",
    "Reconstruction and memory",
    "Prediction and feature dynamics",
    "Camera/feed integrity diagnostics",
    "Language-guided VAD",
]
TIER_LABELS = {
    "1": "tier_behavioral",
    "2": "tier_hazard",
    "3": "tier_feed_integrity",
}
GENERIC_WORDS = [
    "based",
    "using",
    "method",
    "methods",
    "approach",
    "study",
    "detection",
    "anomaly",
    "video",
]
DISPLAY_FILTER_WORDS = {"tier", "task", "specific", "level", "multi"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def descriptor(row: dict[str, str]) -> str:
    values = [
        TIER_LABELS.get(row["primary_tier"], "tier_not_reported"),
        row["training_regime"],
        row["scoring_mechanism"],
        row["representation"],
        row["modality"],
        row["datasets"],
    ]
    return " ".join(value for value in values if value and value != "NR")


def build_documents(s2: dict[str, dict], s3: list[dict]):
    normalized = []
    for row in s3:
        citation = s2.get(row["citation_key"], {})
        normalized.append(
            {
                "citation_key": row["citation_key"],
                "title": citation.get("title") or row["method_or_study"],
                "authors": citation.get("author", ""),
                "year": row["year"],
                "descriptor": descriptor(row),
            }
        )

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False,
        encoding="utf-8",
        newline="",
    ) as handle:
        fields = ["citation_key", "title", "authors", "year", "descriptor"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(normalized)
        temporary = Path(handle.name)

    try:
        docs = litstudy.load_csv(
            str(temporary),
            title_field="title",
            authors_field="authors",
            abstract_field="descriptor",
            date_field="year",
        )
    finally:
        temporary.unlink(missing_ok=True)
    return normalized, docs


def main() -> None:
    citation_rows = read_csv(S2)
    citations = {row["citation_key"]: row for row in citation_rows}
    evidence_rows = read_csv(S3)
    normalized, docs = build_documents(citations, evidence_rows)

    corpus = litstudy.build_corpus(
        docs,
        min_docs=2,
        max_docs_ratio=0.9,
        remove_words=GENERIC_WORDS,
        ngram_threshold=0.8,
    )
    model = litstudy.train_nmf_model(
        corpus,
        NUM_TOPICS,
        seed=SEED,
        max_iter=500,
    )
    layout = np.asarray(
        litstudy.calculate_embedding(
            corpus,
            svd_dims=min(30, len(corpus.dictionary) - 1),
            perplexity=15,
            seed=SEED,
        )
    )
    dominant = np.asarray(model.best_topic_for_documents(), dtype=int)
    weights = np.asarray(model.doc2topic)

    document_rows = []
    for index, row in enumerate(normalized):
        topic_id = int(dominant[index])
        output = {
            "document_id": f"D{index + 1:02d}",
            "citation_key": row["citation_key"],
            "title": row["title"],
            "year": row["year"],
            "dominant_topic": topic_id + 1,
            "topic_label": TOPIC_LABELS[topic_id],
            "topic_weight": f"{weights[index, topic_id]:.6f}",
            "embedding_x": f"{layout[index, 0]:.6f}",
            "embedding_y": f"{layout[index, 1]:.6f}",
        }
        for topic_index in range(NUM_TOPICS):
            output[f"topic_{topic_index + 1}_weight"] = (
                f"{weights[index, topic_index]:.6f}"
            )
        document_rows.append(output)

    topic_rows = []
    for topic_id, label in enumerate(TOPIC_LABELS):
        weighted_terms = [
            (term, weight)
            for term, weight in model.best_token_weights_for_topic(topic_id, limit=15)
            if weight > 1e-8
        ]
        members = int(np.sum(dominant == topic_id))
        topic_rows.append(
            {
                "topic_id": topic_id + 1,
                "topic_label": label,
                "n_documents": members,
                "top_terms": "; ".join(term for term, _ in weighted_terms),
                "top_term_weights": "; ".join(
                    f"{weight:.6f}" for _, weight in weighted_terms
                ),
                "label_basis": (
                    "Author-readable label assigned from top-weighted terms "
                    "and strongest-loading documents"
                ),
            }
        )

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUT / "document_topics.csv", list(document_rows[0]), document_rows)
    write_csv(OUT / "topic_terms.csv", list(topic_rows[0]), topic_rows)
    write_csv(
        OUT / "analysis_metadata.csv",
        ["field", "value"],
        [
            {"field": "software", "value": "LitStudy 1.0.6"},
            {"field": "model", "value": "non-negative matrix factorization"},
            {"field": "input_scope", "value": "52 table-extracted S3 studies"},
            {
                "field": "text_input",
                "value": (
                    "bibliographic title plus deposited S3 tier, training, "
                    "scoring, representation, modality, and dataset descriptors"
                ),
            },
            {"field": "abstracts_used", "value": "no"},
            {"field": "num_topics", "value": str(NUM_TOPICS)},
            {"field": "random_seed", "value": str(SEED)},
            {"field": "minimum_document_frequency", "value": "2"},
            {"field": "maximum_document_ratio", "value": "0.9"},
            {"field": "embedding", "value": "LitStudy nonlinear 2D embedding"},
            {"field": "maximum_reported_nonzero_terms_per_topic", "value": "15"},
            {
                "field": "term_profile_display",
                "value": (
                    "word cloud plus eight ranked terms with within-topic "
                    "weights normalized to the highest-weight term"
                ),
            },
            {
                "field": "interpretive_limit",
                "value": (
                    "Exploratory map of the table-extracted subset; not the "
                    "provisional 616-study included set and not prevalence evidence"
                ),
            },
        ],
    )

    colors = plt.get_cmap("tab10")(np.arange(NUM_TOPICS))
    fig, ax = plt.subplots(figsize=(12.5, 8.3), constrained_layout=True)
    for topic_id, label in enumerate(TOPIC_LABELS):
        mask = dominant == topic_id
        ax.scatter(
            layout[mask, 0],
            layout[mask, 1],
            s=65,
            color=colors[topic_id],
            alpha=0.82,
            edgecolor="white",
            linewidth=0.6,
            label=f"T{topic_id + 1}: {label} (n={int(mask.sum())})",
        )
        if np.any(mask):
            center = layout[mask].mean(axis=0)
            ax.annotate(
                f"T{topic_id + 1}\n{label}",
                center,
                ha="center",
                va="center",
                fontsize=8.5,
                fontweight="bold",
                bbox={
                    "boxstyle": "round,pad=0.28",
                    "facecolor": "white",
                    "edgecolor": colors[topic_id],
                    "alpha": 0.92,
                },
            )
    ax.set_title(
        "Exploratory topical landscape of table-extracted surveillance evidence",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xlabel("Nonlinear embedding dimension 1")
    ax.set_ylabel("Nonlinear embedding dimension 2")
    ax.grid(alpha=0.16, linewidth=0.6)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=False)
    fig.savefig(MAP_PNG, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    fig = plt.figure(figsize=(14, 10.6), constrained_layout=True)
    outer = fig.add_gridspec(3, 2, hspace=0.15, wspace=0.10)
    for topic_id in range(NUM_TOPICS):
        row, column = divmod(topic_id, 2)
        panel = outer[row, column].subgridspec(
            2,
            2,
            height_ratios=[0.16, 0.84],
            width_ratios=[0.58, 0.42],
            hspace=0.02,
            wspace=0.04,
        )
        title_ax = fig.add_subplot(panel[0, :])
        cloud_ax = fig.add_subplot(panel[1, 0])
        rank_ax = fig.add_subplot(panel[1, 1])
        raw_frequencies = {
            term.replace("_", " "): weight
            for term, weight in model.best_token_weights_for_topic(
                topic_id, limit=50
            )
            if not term.startswith("tier_")
            and term not in DISPLAY_FILTER_WORDS
        }
        maximum = max(raw_frequencies.values())
        frequencies = {
            term: weight
            for term, weight in raw_frequencies.items()
            if weight >= maximum * 0.01
        }
        topic_mass = 100 * weights[:, topic_id].sum() / weights.sum()
        members = int(np.sum(dominant == topic_id))
        title_ax.text(
            0.0,
            0.55,
            f"T{topic_id + 1}  {TOPIC_LABELS[topic_id]}",
            fontsize=11,
            fontweight="bold",
            color=colors[topic_id],
            va="center",
        )
        title_ax.text(
            1.0,
            0.55,
            f"dominant documents: {members}  |  topic mass: {topic_mass:.1f}%",
            fontsize=8.5,
            color="#4a4a4a",
            ha="right",
            va="center",
        )
        title_ax.axhline(0.05, color=colors[topic_id], linewidth=1.2, alpha=0.75)
        title_ax.axis("off")

        rgb = tuple(int(channel * 255) for channel in colors[topic_id, :3])
        cloud = WordCloud(
            width=1100,
            height=520,
            max_words=28,
            max_font_size=92,
            min_font_size=9,
            prefer_horizontal=0.92,
            relative_scaling=0.45,
            collocations=False,
            background_color="white",
            random_state=SEED,
            color_func=lambda *args, **kwargs: (
                f"rgb({rgb[0]},{rgb[1]},{rgb[2]})"
            ),
        ).generate_from_frequencies(frequencies)
        cloud_ax.imshow(cloud, interpolation="bilinear")
        cloud_ax.axis("off")

        ranked = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)[:8]
        labels = [term for term, _ in ranked][::-1]
        relative_weights = [100 * value / maximum for _, value in ranked][::-1]
        y = np.arange(len(labels))
        rank_ax.barh(
            y,
            relative_weights,
            color=colors[topic_id],
            alpha=0.78,
            height=0.62,
        )
        rank_ax.set_yticks(y, labels, fontsize=7.4)
        rank_ax.set_xlim(0, 108)
        rank_ax.set_xlabel("relative NMF weight", fontsize=7.2)
        rank_ax.tick_params(axis="x", labelsize=6.8)
        rank_ax.grid(axis="x", alpha=0.16, linewidth=0.5)
        rank_ax.spines[["top", "right", "left"]].set_visible(False)
        for ypos, value in zip(y, relative_weights):
            rank_ax.text(
                min(value + 2, 102),
                ypos,
                f"{value:.0f}",
                va="center",
                fontsize=6.6,
                color="#333333",
            )
    fig.suptitle(
        "Term structure of the six title-and-descriptor NMF topics",
        fontsize=15,
        fontweight="bold",
    )
    fig.savefig(CLOUD_PNG, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(
        f"Built LitStudy map for {len(docs)} S3 studies and {NUM_TOPICS} topics.\n"
        f"Data: {OUT.relative_to(ROOT)}\n"
        f"Figures: {MAP_PNG.name}, {CLOUD_PNG.name}"
    )


if __name__ == "__main__":
    main()
