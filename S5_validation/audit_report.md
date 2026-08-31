# S5 audit report

- Package version: 0.1.0-author-verification
- Audit date: 2026-08-31
- Files checksummed: 56
- S2 citation inventory rows: 176
- S3 core-evidence rows extracted from manuscript tables: 52
- S4 provenance rows: 137

## Automatic checks

The validation script `scripts/validate_package.py` re-runs these tests:

1. Required S1–S5 files exist.
2. PRISMA arithmetic: source rows sum to N1; N1 minus pre-screen removals equals N2; N2 minus title/abstract exclusions equals N3; N3 minus not-retrieved equals N4; N4 minus EC1–EC5 equals N5; Tier1+Tier2+Tier3 equals N5.
3. No duplicate `citation_key` in S2.
4. Every S4 `citation_key` with a numerical value exists in S2 or is flagged.
5. Figure 2a counts sum to N5.

## Author-verification gaps (not failures of this deposit)

- S3 currently contains 52 unique studies extracted from manuscript comparison tables, not the working total of 132 core studies.
- Per-study D1–D5 ratings are not fabricated; templates are provided.
- Raw database exports and both screeners' independent decision files are not in this deposit.
- PRISMA identification, screening, and agreement numbers are working_author_review values.
- S4 page_confirmation remains author_verification_required until each number is checked against the cited PDF.

## How a reviewer should use this package

1. Read `README.md` and `S1_search_and_selection/AUTHOR_DEPOSIT_REQUIRED.md`.
2. Re-execute the Boolean strings in `S1_search_and_selection/03_executable_search_strings.md` if checking search reproducibility.
3. Treat `verification_status = working_author_review` cells as unverified until the raw exports and rater files are deposited.
4. Use `S4_performance_provenance/performance_provenance.csv` to trace every transcribed manuscript number to a citation key.
5. Run `python S5_validation/scripts/validate_package.py`.
