# Raw bibliographic exports

Place one file (or one folder) per source and execution window:

```
ieee_xplore_2025-04.csv
ieee_xplore_2026-06.csv
acm_dl_2025-04.csv
acm_dl_2026-06.csv
scopus_2025-04.csv
scopus_2026-06.csv
wos_2025-04.csv
wos_2026-06.csv
google_scholar_2025-04.csv
google_scholar_2026-06.csv
citation_tracking.csv
wacv2026_proceedings.csv
cvpr2026_proceedings.csv
```

Minimum columns: `source`, `query_family`, `execution_date`, `title`, `authors`, `year`, `doi`, `venue`, `document_type`, `language`, `url`.

Do not commit publisher PDFs. Export metadata only.

## Optional LitStudy audit

CSV, RIS, and BibTeX exports in this folder can be loaded by:

```bash
python -m pip install -r S5_validation/requirements-litstudy.txt
python S5_validation/scripts/litstudy_metadata_audit.py
```

For normalized CSV files, the adapter maps `title`, `authors`, `abstract`,
`year`, `venue`, and `doi` explicitly. It writes only secondary metadata
summaries; the source exports and human screening ledger remain authoritative.
