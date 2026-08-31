# S3 — Core primary-evidence extraction

`consolidated_performance_evidence.csv` contains the 43 method × benchmark result cells in the article's two principal numerical tables. It records the benchmark, metric, value, supervision regime, modality, representation, scoring mechanism, and the protocol coordinates available for the comparability audit. Unreported split, pretraining, implementation, and post-processing fields are marked `NR`, not inferred.

`core_primary_evidence.csv` is a broader 52-study extraction of all manuscript comparison / SOTA tables. `appraisal_aggregate.csv` records the article's aggregate appraisal results for 132 core studies (660 D1–D5 ratings, 91.2% agreement, κ = 0.867, 95% CI [0.832, 0.898]). The row-level rating matrix is not distributed, so those aggregates are explicitly marked not independently recomputable.

Ratings: **L** low concern, **S** some concerns, **H** high concern. No composite score is computed; no study is excluded on the basis of a rating. `appraisal_ratings_template.csv` provides a schema only and contains no invented ratings.
