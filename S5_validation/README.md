# S5 — Validation scripts, dictionary, checksums, amendment log, audit

| File | Purpose |
| --- | --- |
| `scripts/build_replication_tables.py` | Regenerates S1–S4 CSVs from the manuscript-derived tables |
| `scripts/build_dataset_audit.py` | Regenerates `datasets/` catalogue, distribution, caveats, and category lists |
| `scripts/build_comparability_audit.py` | Regenerates the 43 result cells, 903 pairwise decisions, sensitivity summary, and descriptive regression checks |
| `scripts/build_litstudy_evidence_map.py` | Regenerates the six-topic landscape and word clouds from titles plus structured descriptors for the 52 extended S3 studies |
| `scripts/validate_package.py` | Structural + PRISMA-arithmetic + dataset + comparability audit |
| `scripts/generate_checksums.py` | Rewrites `checksums.sha256` |
| `scripts/litstudy_metadata_audit.py` | Optional CSV/RIS/BibTeX import, identifier-aware union, and descriptive metadata audit |
| `requirements-litstudy.txt` | Pinned dependency for the optional LitStudy audit only |
| `LITSTUDY_INTEROPERABILITY.md` | Scope, limitations, citation, and reproducible usage |
| `data_dictionary.csv` | Column definitions |
| `package_manifest.csv` | Version and row counts |
| `checksums.sha256` | SHA-256 of every deposited file except this checksum file |
| `AMENDMENT_LOG.md` | Dated changes |
| `audit_report.md` | Last automated audit |

The `comparability/` folder is the machine-readable source for the article's formal audit: 43 result cells, 903 unordered pairs, 54 C3-comparable pairs (6.0%), 19 classes, largest class 6. It also contains C1–C3 sensitivity results and the Ped2/UCF-Crime/XD-Violence descriptive OLS checks.

The `topic_model/` folder contains the document-topic weights, two-dimensional coordinates, topic terms, manually readable labels, and fixed analysis parameters behind the article's exploratory LitStudy figure. This title-and-descriptor analysis covers 52 table-extracted studies only; it is not a model of the provisional 616-study set and is not used to estimate topic prevalence.

```bash
python S5_validation/scripts/build_replication_tables.py
python S5_validation/scripts/build_dataset_audit.py
python S5_validation/scripts/build_comparability_audit.py
python S5_validation/scripts/build_litstudy_evidence_map.py
python S5_validation/scripts/validate_package.py
python S5_validation/scripts/generate_checksums.py
```

Core validation uses the Python standard library only. For the optional
LitStudy interoperability audit:

```bash
python -m pip install -r S5_validation/requirements-litstudy.txt
python S5_validation/scripts/litstudy_metadata_audit.py
```

This optional adapter does not make inclusion/exclusion decisions and must not
be represented as the tool that generated the original PRISMA counts.
