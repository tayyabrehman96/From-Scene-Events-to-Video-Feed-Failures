# From Scene Events to Video-Feed Failures

**Versioned replication package (Supplementary Materials S1–S5)** for the systematic review of visual anomaly detection in surveillance, spanning behavioural and object-interaction events, physical hazards (fire and smoke), and camera / video-feed integrity failures.

| | |
| --- | --- |
| **Repository** | https://github.com/tayyabrehman96/From-Scene-Events-to-Video-Feed-Failures |
| **Package version** | 0.2.0 (2026-08-31) |
| **Evidence window** | January 2010 – 30 June 2026 (seminal pre-2010 exceptions under IC5) |
| **Initial search / update / freeze** | April 2025 / June 2026 / **30 June 2026** |
| **Licence** | Data and documentation: [CC BY 4.0](LICENSE). Scripts: MIT (same file). |

This is the location named in the manuscript **Data availability** and **Code availability** statements. It is intended for **journal reviewers**, **information specialists checking PRISMA-S**, and **researchers** who need machine-readable tables, search strings, dataset metadata, and numerical provenance.

---

## 1. What this repository is

A structured, citable deposit of the review’s *methods and evidence objects*, not a model zoo and not a copy of the article PDF.

| Included | Not included |
| --- | --- |
| Executable database search strings and freeze log (S1) | Manuscript `main.tex`, `.bib`, figure PNGs, or compiled PDF |
| Eligibility (inclusion/exclusion) rules and PRISMA-stage counts (S1) | Raw RIS/CSV exports of the ~16k identification set (drop zone provided) |
| Bibliographic inventory of 176 cited items (S2) | Third-party surveillance video, images, or pretrained weights |
| A 43-cell consolidated evidence table and aggregate appraisal results (S3) | Independent screener decision sheets (schema provided; files not deposited) |
| Principal-table and extended numerical provenance (S4) | Row-level D1–D5 appraisal ratings (aggregate results only) |
| Dataset audit: 21 corpora, splits, access, composition, caveats | Retraining scripts for detection models |
| Validation scripts, data dictionary, SHA-256 checksums (S5) | A claimed meta-analysis (the review is a structured / SWiM synthesis) |

The S5 scripts **validate the review data**. They do not reproduce underlying detectors.

---

## 2. How to use the package (by role)

**Journal reviewer or editor.** Start here, in this order:

1. This file (scope, status flags, what is still provisional).
2. [`S1_search_and_selection/AUTHOR_DEPOSIT_REQUIRED.md`](S1_search_and_selection/AUTHOR_DEPOSIT_REQUIRED.md) — honest gap list.
3. [`S1_search_and_selection/03_executable_search_strings.md`](S1_search_and_selection/03_executable_search_strings.md) — re-runnable Boolean strings.
4. [`S1_search_and_selection/06_eligibility_inclusion_exclusion.csv`](S1_search_and_selection/06_eligibility_inclusion_exclusion.csv) and [`07_prisma_flow.csv`](S1_search_and_selection/07_prisma_flow.csv).
5. [`datasets/dataset_catalogue.csv`](datasets/dataset_catalogue.csv) and [`datasets/dataset_distribution.csv`](datasets/dataset_distribution.csv).
6. [`S4_performance_provenance/performance_provenance.csv`](S4_performance_provenance/performance_provenance.csv).
7. Run `python S5_validation/scripts/validate_package.py` (standard library only).

**Researcher reusing the search.** Copy the four query families and the fielded strings for Scopus, Web of Science, IEEE Xplore, and ACM DL. Google Scholar is supplementary only; see [`09_google_scholar_protocol.md`](S1_search_and_selection/09_google_scholar_protocol.md).

**Researcher comparing methods or datasets.** Do not treat S4 as a leaderboard. Use the dataset catalogue and protocol caveats first, then the provenance table, which records training regime, representation, scoring mechanism, and whether a row is the *canonical* consolidated value or a repeated local table.

---

## 3. Review questions (context for the files)

The synthesis is organised around six questions. Files in this repository are the audit trail for those questions, not a substitute for the narrative in the article.

| ID | Question (condensed) | Principal machine-readable support |
| --- | --- | --- |
| RQ1 | Which behavioural, hazard, and feed-integrity anomalies are studied? | [`datasets/`](datasets/), S3 `primary_tier` |
| RQ2 | Which supervision, scoring, and representation families are used? | S3 extraction columns; S4 provenance |
| RQ3 | Datasets, metrics, protocols, and where comparison is invalid | Dataset audit; S4 `metric` / `dataset` |
| RQ4 | Evidence for or against cross-tier transfer of mechanisms | S3 flags; dataset caveats; heatmap source CSV |
| RQ5 | Deployment, latency, robustness, explanation reporting | S3 `deployment_reporting` (often NR) |
| RQ6 | Consequential evidence gaps | Distribution by tier; UHCTD/ADOC sparsity notes |

Pooling is **not** performed: there is no common estimand across tiers or supervision regimes, benchmark papers typically lack sampling variances, and canonical splits are reused.

---

## 4. Repository layout

```
.
├── README.md                          ← this description
├── LICENSE
├── CITATION.cff
├── S1_search_and_selection/           ← Supplementary S1
├── S2_citation_inventory/             ← Supplementary S2
├── S3_extraction/                     ← Supplementary S3
├── S4_performance_provenance/         ← Supplementary S4 (numbers and figures)
├── datasets/                          ← S4 dataset audit (expanded)
└── S5_validation/                     ← Supplementary S5
```

### S1 — Search specification, freeze log, inclusion / exclusion

Folder: [`S1_search_and_selection/`](S1_search_and_selection/)

The search used **four query families** so that fire/smoke and feed-integrity papers that never use the phrase *anomaly detection* are not systematically missed: (QF1) behavioural VAD; (QF2) physical hazards; (QF3) camera/feed integrity; (QF4) cross-cutting 2025–2026 vocabulary (foundation models, Mamba, open-vocabulary, edge deployment).

Sources: IEEE Xplore, ACM Digital Library, Scopus, Web of Science Core Collection, Google Scholar (supplementary), citation tracking, and official WACV/CVPR 2026 proceedings available before the freeze. CVPR 2026 Findings papers are recorded separately and are **not** treated as equivalent to main-conference papers.

| File | Description |
| --- | --- |
| [`01_query_families.csv`](S1_search_and_selection/01_query_families.csv) | Concept blocks and representative terms |
| [`03_executable_search_strings.md`](S1_search_and_selection/03_executable_search_strings.md) | Fielded Boolean strings (Scopus `TITLE-ABS-KEY`, WoS `TS`, IEEE Command Search, ACM advanced search) |
| [`04_evidence_freeze_log.csv`](S1_search_and_selection/04_evidence_freeze_log.csv) | Coverage start, initial search, update search, freeze |
| [`05_search_reporting_minimum_fields.csv`](S1_search_and_selection/05_search_reporting_minimum_fields.csv) | PRISMA-S minimum fields per source |
| [`06_eligibility_inclusion_exclusion.csv`](S1_search_and_selection/06_eligibility_inclusion_exclusion.csv) | **IC1–IC5** and **EC1–EC5** (the decision rules) |
| [`07_prisma_flow.csv`](S1_search_and_selection/07_prisma_flow.csv) | Identification through inclusion, with arithmetic formulae |
| [`08_fulltext_exclusions_by_criterion.csv`](S1_search_and_selection/08_fulltext_exclusions_by_criterion.csv) | Eligibility-stage EC1–EC5 tallies |
| [`09_google_scholar_protocol.md`](S1_search_and_selection/09_google_scholar_protocol.md) | Why Scholar is not a primary identification source |
| [`10_deduplication_protocol.md`](S1_search_and_selection/10_deduplication_protocol.md) | DOI pass, then normalised title + first-author + year, then manual residuals |
| [`11_screening_ledger_schema.csv`](S1_search_and_selection/11_screening_ledger_schema.csv) | Required columns for a future record-level ledger |
| [`12_independent_screener_schema.csv`](S1_search_and_selection/12_independent_screener_schema.csv) | Required columns for both independent raters |
| [`screening/`](S1_search_and_selection/screening/) | Stage counts, working agreement statistics, IC3 include/exclude examples |
| [`raw_exports/`](S1_search_and_selection/raw_exports/) | Empty drop zone for publisher metadata exports (no PDFs) |

**Reported PRISMA arithmetic** (all identities pass; values are not independently recomputable until the original ledger is deposited):

| Slot | *n* | Formula |
| --- | --- | --- |
| N1 identified | 16,482 | Sum of six source rows |
| Removed before screening | 2,577 | Duplicates 2,128 + date 166 + language 113 + type 170 |
| N2 title/abstract screened | 13,905 | N1 − 2,577 |
| Title/abstract excluded | 12,958 | Working value |
| N3 full texts sought | 947 | N2 − 12,958 |
| Not retrieved | 44 | Working value |
| N4 assessed | 903 | N3 − 44 |
| Full-text excluded | 287 | EC1 35 + EC2 51 + EC3 93 + EC4 78 + EC5 30 |
| **N5 included** | **616** | N4 − 287 |
| Primary-tier allocation | 441 / 122 / 53 | Must sum to N5 (multi-category studies counted once) |
| Core appraisal set | 132 | Aggregate appraisal results are reported; the row-level matrix is not distributed |

Deduplication is two automated passes plus manual residual review. Incremental eligible studies are not dropped merely because the contribution is small; conference/journal pairs are collapsed only when they report the same experiment.

### S2 — Bibliographic citation inventory

Folder: [`S2_citation_inventory/`](S2_citation_inventory/)

| File | Description |
| --- | --- |
| [`citation_inventory.csv`](S2_citation_inventory/citation_inventory.csv) | **176** cited items: key, type, year, authors, title, venue, DOI, and a heuristic `role_in_review` (primary study, dataset, positioning review, reporting standard, background) |

The inventory is the machine-readable bibliography. It is **not** the list of 616 included studies (N5). The article bibliography is the smaller set of items cited in support of specific claims; N5 is every record that passed full-text eligibility. Those two quantities must not be conflated.

Native BibTeX is omitted from this public repository by design (the replication package is data and scripts, not the manuscript source).

### S3 — Core primary-evidence extraction and appraisal instrument

Folder: [`S3_extraction/`](S3_extraction/)

| File | Description |
| --- | --- |
| [`consolidated_performance_evidence.csv`](S3_extraction/consolidated_performance_evidence.csv) | The **43 result cells** in the two principal numerical tables, with benchmark, metric, value, supervision, modality, representation, scoring mechanism, and unavailable protocol coordinates marked `NR` |
| [`core_primary_evidence.csv`](S3_extraction/core_primary_evidence.csv) | Extended **52-study** extraction of the manuscript's comparison and SOTA tables |
| [`appraisal_instrument.csv`](S3_extraction/appraisal_instrument.csv) | Five diagnostic dimensions **D1–D5** (transparency, split integrity, metric validity, comparison fairness, external validity), with low- and high-concern anchors |
| [`appraisal_aggregate.csv`](S3_extraction/appraisal_aggregate.csv) | Reported aggregate: 132 studies, 660 ratings, 91.2% agreement, κ = 0.867 (95% CI [0.832, 0.898]); explicitly marked not independently recomputable |
| [`appraisal_ratings_template.csv`](S3_extraction/appraisal_ratings_template.csv) | Empty L / S / H grid for consensus ratings — **not filled with invented scores** |

Ratings are **L** (low concern), **S** (some concerns), **H** (high concern). No composite quality score is computed. No study is excluded on the basis of a rating. The aggregate appraisal result is a review result; without the row-level matrix it cannot be independently recomputed from this repository.

### S4 — Numerical provenance and figure source data

Folder: [`S4_performance_provenance/`](S4_performance_provenance/)

| File | Description |
| --- | --- |
| [`principal_table_provenance.csv`](S4_performance_provenance/principal_table_provenance.csv) | **43** rows covering every result cell in the two principal consolidated tables |
| [`performance_provenance.csv`](S4_performance_provenance/performance_provenance.csv) | Extended **137-row** provenance table covering principal and repeated local manuscript tables |
| [`figure_source_data/`](S4_performance_provenance/figure_source_data/) | Machine-readable values behind data-bearing figures |
| [`manuscript_tables/`](S4_performance_provenance/manuscript_tables/) | Per-table CSV dumps (reconstruction, prediction, weakly supervised, datasets, …) |
| [`figure_manifest.csv`](S4_performance_provenance/figure_manifest.csv) | Which figures are data vs schematic |

| Figure (manuscript) | Source CSV |
| --- | --- |
| PRISMA flow | [`figure_source_data/fig_prisma_flow.csv`](S4_performance_provenance/figure_source_data/fig_prisma_flow.csv) |
| Included studies by primary tier (441 / 122 / 53) | [`figure_source_data/fig2a_anomaly_tier_counts.csv`](S4_performance_provenance/figure_source_data/fig2a_anomaly_tier_counts.csv) |
| Temporal-reasoning mechanism × tier | [`figure_source_data/fig_temporal_reasoning_suitability.csv`](S4_performance_provenance/figure_source_data/fig_temporal_reasoning_suitability.csv) |

`page_confirmation` remains `author_verification_required` until each number is checked against the cited PDF page. Shared rows (for example MemAE on Ped2) appear in more than one local table; the canonical value is the consolidated comparison.

### Dataset audit (expanded S4)

Folder: [`datasets/`](datasets/)

Academic catalogue of every benchmark or study-specific corpus **tabulated** in the review. Video is not redistributed.

| File | Description |
| --- | --- |
| [`dataset_catalogue.csv`](datasets/dataset_catalogue.csv) | **21** unique corpora: split sizes, public access, real/synthetic/mixed composition, scenes or cameras, annotation granularity, modality, typical metric, supervision regimes, and notes |
| [`dataset_distribution.csv`](datasets/dataset_distribution.csv) | Counts and shares by tier, access, composition, annotation family; summed VAD train/test volume where numeric |
| [`dataset_protocol_caveats.csv`](datasets/dataset_protocol_caveats.csv) | Why that corpus cannot be used as a global leaderboard row |
| [`dataset_categories_and_subsets.csv`](datasets/dataset_categories_and_subsets.csv) | UCF-Crime’s 13 named categories; FiSmo sub-collections that must not be aggregated |
| [`DATA_DICTIONARY.csv`](datasets/DATA_DICTIONARY.csv) | Column definitions |

**Distribution of the 21 tabulated corpora** (primary-tier assignment; ADOC counted once as multi-tier, primary tier 3):

| Axis | Breakdown |
| --- | --- |
| Primary tier | Behavioural 11 · Fire/smoke 7 · Feed integrity 3 |
| Public access | Yes 20 · Partial 1 (Ribnick et al.) |
| Composition | Real 14 · Mixed 5 · Synthetic 1 (UBnormal) · Synthetic faults on real feeds 1 (UHCTD) |
| VAD split volume (numeric tier-1 rows, excluding UMN; CHAD remains NR) | Train 6,579 · Test 1,660 clips/videos |

Comparability constraints encoded in the audit: Ped2/Avenue/ShanghaiTech frame-AUC is not ranked against UCF-Crime AUC or XD-Violence AP; fire classification accuracy is not ranked against detection mAP or segmentation mIoU; UHCTD is a two-camera protocol, not a community false-alarm-rate standard; FiSmo subsets are not one aggregate *n*.

Cells the manuscript does not state are **NR**, not imputed.

### S5 — Validation, dictionary, checksums, amendment log

Folder: [`S5_validation/`](S5_validation/)

| File | Description |
| --- | --- |
| [`scripts/build_replication_tables.py`](S5_validation/scripts/build_replication_tables.py) | Regenerates S1–S4 CSVs from the deposited table specifications |
| [`scripts/build_dataset_audit.py`](S5_validation/scripts/build_dataset_audit.py) | Regenerates `datasets/` |
| [`scripts/build_comparability_audit.py`](S5_validation/scripts/build_comparability_audit.py) | Regenerates the 43-cell, 903-pair comparability audit, sensitivity analysis, and descriptive regression checks |
| [`scripts/validate_package.py`](S5_validation/scripts/validate_package.py) | Required-file check, six PRISMA identities, duplicate keys, Figure 2a vs N5, dataset integrity, and 43/903/54 comparability assertions |
| [`scripts/generate_checksums.py`](S5_validation/scripts/generate_checksums.py) | SHA-256 over package files (excludes local manuscript source) |
| [`scripts/litstudy_metadata_audit.py`](S5_validation/scripts/litstudy_metadata_audit.py) | Optional CSV/RIS/BibTeX ingestion, identifier-aware union, and year/venue/deduplication summaries using LitStudy |
| [`LITSTUDY_INTEROPERABILITY.md`](S5_validation/LITSTUDY_INTEROPERABILITY.md) | Exact scope, limitations, installation, and citation for the optional interoperability layer |
| [`data_dictionary.csv`](S5_validation/data_dictionary.csv) | Cross-supplement column definitions |
| [`checksums.sha256`](S5_validation/checksums.sha256) | Integrity manifest |
| [`AMENDMENT_LOG.md`](S5_validation/AMENDMENT_LOG.md) | Dated changes |
| [`audit_report.md`](S5_validation/audit_report.md) | Last automated audit |

Python 3.10 or later; **standard library only**.

```bash
python S5_validation/scripts/build_replication_tables.py
python S5_validation/scripts/build_dataset_audit.py
python S5_validation/scripts/build_comparability_audit.py
python S5_validation/scripts/validate_package.py
python S5_validation/scripts/generate_checksums.py
```

The generated S5 audit contains **43 result cells**, all **903 unordered pairs**, and **54 directly comparable pairs** under the recorded C3 coordinates (6.0%; 19 classes; largest class 6). It also reproduces the manuscript's Ped2, UCF-Crime, and XD-Violence descriptive trend statistics.

### Optional repository-only LitStudy interoperability

The package can import deposited CSV, RIS, and BibTeX exports through
[LitStudy](https://github.com/NLeSC/litstudy), combine collections with its
identifier-aware `DocumentSet` union, and generate descriptive year, venue,
and duplicate-collapse summaries:

```bash
python -m pip install -r S5_validation/requirements-litstudy.txt
python S5_validation/scripts/litstudy_metadata_audit.py
```

This adapter is a **post hoc repository aid and is not cited as part of the updated manuscript methodology**. It does not infer
eligibility, replace the declared DOI/title-author-year deduplication ledger,
or establish the reported PRISMA counts. Topic models and bibliographic
networks are also treated as exploratory because their completeness depends
on abstract and reference-list coverage.

---

## 5. Verification-status vocabulary

Every quantitative table uses one of:

| Status | Meaning |
| --- | --- |
| `transcribed_from_manuscript` | Copied from the article’s tables, dataset section, or bibliography |
| `reported_review_result_not_independently_recomputable` | Reported in the updated article, but the raw export, paired decision, or row-level rating matrix required for independent recomputation is not deposited |
| `author_verification_required` | D1–D5 consensus ratings; PDF page confirmation of transcribed numbers |

This vocabulary matches the updated article's explicit boundary between distributed numerical analyses and review results whose record-level source files are not included.

---

## 6. What still must be deposited (not fabricated here)

See [`S1_search_and_selection/AUTHOR_DEPOSIT_REQUIRED.md`](S1_search_and_selection/AUTHOR_DEPOSIT_REQUIRED.md).

| Missing object | Why a reviewer needs it |
| --- | --- |
| Raw database exports (IEEE, ACM, Scopus, WoS, Scholar, proceedings) | Recompute identification counts |
| Deduplication log | Recompute “removed before screening” |
| Independent title/abstract and full-text decisions (both screeners) | Recompute κ, PABAK, Gwet AC1 |
| Consensus N5 list with primary tier | Verify 616 and 441 / 122 / 53 |
| Remaining S3 rows and independent D1–D5 ratings | Verify 132 × 5 = 660 appraisal items |

Until those files are present, PRISMA identification counts and agreement statistics are **working values**, not ledger-verified results.

---

## 7. Citation

Please cite the systematic review. This repository may additionally be cited as a dataset via [`CITATION.cff`](CITATION.cff).

---

## 8. Related reporting standards

The article maps PRISMA 2020, PRISMA-S, and SWiM items internally. This package supports that mapping by exposing search strings, eligibility rules, flow counts, extraction fields, and dataset protocol variables. PROSPERO was not used (out of scope for this evidence type). Any later public protocol deposit should be labelled **retrospective**.
