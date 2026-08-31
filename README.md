# From Scene Events to Video-Feed Failures — replication package (S1–S5)

Public, versioned supplementary materials for the systematic review *From Scene Events to Video-Feed Failures*. This repository is the Data-availability and Code-availability location cited in the manuscript:

<https://github.com/tayyabrehman96/From-Scene-Events-to-Video-Feed-Failures>

It is written for **researchers** who want to reuse the search specification, tables, and figure data, and for **reviewers** who need to audit PRISMA claims, inclusion/exclusion rules, numerical provenance, and validation checks.

## Package map

| Supplement | Contents | Folder |
| --- | --- | --- |
| **S1** | Database query families, executable Boolean strings, evidence-freeze log, eligibility (inclusion/exclusion) criteria, PRISMA flow CSV, full-text exclusion counts, screening schemas, Google Scholar and deduplication protocols | [`S1_search_and_selection/`](S1_search_and_selection/) |
| **S2** | Bibliographic citation inventory (machine-readable CSV + BibTeX) | [`S2_citation_inventory/`](S2_citation_inventory/) |
| **S3** | Core primary-evidence extraction table transcribed from manuscript comparison tables, plus the five-dimension appraisal instrument and a ratings template | [`S3_extraction/`](S3_extraction/) |
| **S4** | Performance-provenance table linking every reproduced numerical cell to its citation key; figure source CSVs; per-table CSV dumps | [`S4_performance_provenance/`](S4_performance_provenance/) |
| **S5** | Validation and table-generation scripts, data dictionary, checksums, amendment log, audit report | [`S5_validation/`](S5_validation/) |

Manuscript source, bibliography, and figure PNGs are in [`manuscript/`](manuscript/) (LaTeX at repository root is the compiling submission copy).

## Inclusion / exclusion CSVs

| File | What it is |
| --- | --- |
| [`S1_search_and_selection/06_eligibility_inclusion_exclusion.csv`](S1_search_and_selection/06_eligibility_inclusion_exclusion.csv) | IC1–IC5 and EC1–EC5 (the decision rules) |
| [`S1_search_and_selection/07_prisma_flow.csv`](S1_search_and_selection/07_prisma_flow.csv) | Identification → inclusion counts |
| [`S1_search_and_selection/08_fulltext_exclusions_by_criterion.csv`](S1_search_and_selection/08_fulltext_exclusions_by_criterion.csv) | EC1–EC5 tallies |
| [`S1_search_and_selection/screening/inclusion_exclusion_counts.csv`](S1_search_and_selection/screening/inclusion_exclusion_counts.csv) | Same PRISMA counts in the screening folder |
| [`S1_search_and_selection/screening/ic3_surveillance_transfer_examples.csv`](S1_search_and_selection/screening/ic3_surveillance_transfer_examples.csv) | Auditable IC3 include/exclude examples |

Record-level screening decisions (one row per identified record) are **not invented**. Schemas and a deposit checklist are in [`S1_search_and_selection/AUTHOR_DEPOSIT_REQUIRED.md`](S1_search_and_selection/AUTHOR_DEPOSIT_REQUIRED.md).

## Figure source data

| Figure | Source CSV |
| --- | --- |
| PRISMA flow (`fig:prisma`) | [`S4_performance_provenance/figure_source_data/fig_prisma_flow.csv`](S4_performance_provenance/figure_source_data/fig_prisma_flow.csv) |
| Included studies by primary tier (`fig:tax_a`) | [`S4_performance_provenance/figure_source_data/fig2a_anomaly_tier_counts.csv`](S4_performance_provenance/figure_source_data/fig2a_anomaly_tier_counts.csv) |
| Temporal-reasoning heatmap (`fig:temporal_validation`) | [`S4_performance_provenance/figure_source_data/fig_temporal_reasoning_suitability.csv`](S4_performance_provenance/figure_source_data/fig_temporal_reasoning_suitability.csv) |

Schematic figures (framework, methods overview, foundation-model diagram, comparability tree, deployment architecture) have no numerical source table; they are listed in [`S4_performance_provenance/figure_manifest.csv`](S4_performance_provenance/figure_manifest.csv).

## Verification status

Every quantitative CSV has a `verification_status` (or equivalent) column:

- `transcribed_from_manuscript` — copied from `main.tex` / `references.bib` / deposited figures
- `working_author_review` — internally consistent PRISMA / agreement / tier-allocation working values; **must be replaced from the original ledger before treating the manuscript as a finished systematic review**
- `author_verification_required` — D1–D5 ratings and PDF page confirmation of transcribed numbers

The manuscript switch `\provisionalnumberstrue` matches this status.

## Reproduce the tables and run the audit

Python 3.10+; standard library only.

```bash
python S5_validation/scripts/build_replication_tables.py
python S5_validation/scripts/validate_package.py
```

Expected validation outcome at this deposit: **PASS** with warnings that (i) S3 row count is the table-extracted core set, not yet 132 independently coded studies, (ii) D1–D5 ratings are still templates, and (iii) any citation keys used in tables but missing from the `.bib` file are listed.

## What this package does *not* do

The S5 scripts validate **review data**. They do not retrain detection models or download third-party video datasets.

## Licence

Data and documentation: [CC BY 4.0](LICENSE). Scripts: MIT (see `LICENSE`).
