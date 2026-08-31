# S4 — Numerical performance provenance and figure source data

`performance_provenance.csv` is one row per manuscript numerical cell (method × dataset × metric). `canonical_table = yes` marks the consolidated tables that the manuscript treats as the source of truth when the same number is repeated locally for reading convenience.

`page_confirmation = author_verification_required` until each value is checked against the cited PDF page.

Figure source CSVs are in `figure_source_data/`. Per-table dumps of the manuscript comparison tables are in `manuscript_tables/`. The **dataset audit** (catalogue, distribution by tier/access/composition, protocol caveats, named categories) is in [`../datasets/`](../datasets/). See `figure_manifest.csv` for the mapping from PNG / TikZ figures to source CSVs.
