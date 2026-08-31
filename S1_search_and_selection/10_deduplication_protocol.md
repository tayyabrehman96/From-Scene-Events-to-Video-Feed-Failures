# S1 — Deduplication protocol

Two automated passes plus a manual residual pass, as specified in the manuscript (Section 2.2).

## Pass 1 — DOI match

Records with an identical DOI are collapsed to a single master record. The retained copy prefers, in order: journal version over conference version when they report the same experiment; otherwise the earlier dated export.

## Pass 2 — Normalised title + first-author surname + year

Normalisation: lowercase; strip punctuation; collapse whitespace; remove trailing subtitle after `:` only when the remainder is an identical stem. Match on normalised title AND first-author surname AND publication year.

## Pass 3 — Manual residual near-matches

Human review of remaining near-duplicates, including:

- preprint / journal pairs
- conference / journal extensions of the same experiment (EC2)
- records with missing DOI but overlapping titles

Each removal is logged with `removal_reason` in the deduplication ledger schema (`11_screening_ledger_schema.csv`).

## What is **not** collapsed

Incremental but eligible studies are not excluded merely because the methodological contribution is small. Overlapping publications are consolidated only when they report the same underlying experiment or when a later journal article supersedes an earlier conference version.
