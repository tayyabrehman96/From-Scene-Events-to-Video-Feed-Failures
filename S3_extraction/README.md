# S3 — Core primary-evidence extraction

`core_primary_evidence.csv` contains every unique study that appears in the manuscript comparison / SOTA tables, with tier, training regime, scoring mechanism, representation, datasets, metrics, result summary, manuscript table IDs, and appraisal-flag notes taken from the text (for example VadCLIP backbone confound).

This is **not** yet the working total of 132 independently coded core studies. Remaining rows must be added from the original extraction sheet. D1–D5 cells are `author_verification_required` until the independent rating files are deposited into `appraisal_independent_ratings.csv` using `appraisal_ratings_template.csv`.

Ratings: **L** low concern, **S** some concerns, **H** high concern. No composite score is computed; no study is excluded on the basis of a rating.
