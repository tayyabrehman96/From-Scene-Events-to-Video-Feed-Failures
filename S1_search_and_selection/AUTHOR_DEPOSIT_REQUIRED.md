# Author deposit still required (record-level screening files)

This folder contains the search specification and arithmetic that can be reconstructed from the submitted manuscript. The numerical selection and agreement values originated as provisional estimates/scenarios and are not verified by deposited source records:

- executable search strings
- eligibility (inclusion/exclusion) criteria
- PRISMA stage arithmetic
- screening and rater-file *schemas*
- evidence-freeze log

It does **not** invent 16,482 bibliographic export rows or 13,905 independent title/abstract decisions. Those files exist only if the original search ledger and the two screeners' decision sheets are copied here.

## Files the authors must still place in this repository

| Missing source file | Where to put it | Why reviewers need it |
| --- | --- | --- |
| Raw database exports (RIS/CSV/BibTeX) for IEEE, ACM, Scopus, WoS, Scholar | `raw_exports/` | Recompute identification counts |
| Deduplication log (DOI pass, title–author–year pass, manual residuals) | `screening/deduplication_log.csv` | Recompute “removed before screening” |
| Independent screener A title/abstract decisions | `screening/title_abstract_screener_A.csv` | Recompute κ, PABAK, AC1 |
| Independent screener B title/abstract decisions | `screening/title_abstract_screener_B.csv` | Same |
| Independent screener A full-text decisions | `screening/fulltext_screener_A.csv` | Same at full text |
| Independent screener B full-text decisions | `screening/fulltext_screener_B.csv` | Same |
| Consensus inclusion list (N5) with primary tier | `screening/included_studies_N5.csv` | Verify 616 and 441/122/53 |
| Independent D1–D5 ratings (both raters + consensus) | `../S3_extraction/appraisal_independent_ratings.csv` | Verify 132 × 5 = 660 items |

Column requirements are in `11_screening_ledger_schema.csv` and `12_independent_screener_schema.csv`.

The updated article currently presents the PRISMA, agreement, tier-allocation, and appraisal aggregates as review results, but the available package history identifies them as proposed estimates or internally consistent scenarios. Accordingly, these rows use `verification_status = provisional_author_verification_required`. They must be replaced from the original records before submission; a non-recomputability disclaimer alone is insufficient.
