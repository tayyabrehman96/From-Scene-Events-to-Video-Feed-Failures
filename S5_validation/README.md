# S5 — Validation scripts, dictionary, checksums, amendment log, audit

| File | Purpose |
| --- | --- |
| `scripts/build_replication_tables.py` | Regenerates S1–S4 CSVs from the manuscript-derived tables |
| `scripts/build_dataset_audit.py` | Regenerates `datasets/` catalogue, distribution, caveats, and category lists |
| `scripts/validate_package.py` | Structural + PRISMA-arithmetic + dataset-catalogue audit |
| `scripts/generate_checksums.py` | Rewrites `checksums.sha256` |
| `data_dictionary.csv` | Column definitions |
| `package_manifest.csv` | Version and row counts |
| `checksums.sha256` | SHA-256 of every deposited file except this checksum file |
| `AMENDMENT_LOG.md` | Dated changes |
| `audit_report.md` | Last automated audit |

```bash
python S5_validation/scripts/build_replication_tables.py
python S5_validation/scripts/build_dataset_audit.py
python S5_validation/scripts/validate_package.py
python S5_validation/scripts/generate_checksums.py
```
