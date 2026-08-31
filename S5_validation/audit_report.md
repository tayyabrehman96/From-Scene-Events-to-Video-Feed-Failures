# S5 audit report

- Package version: 0.2.1
- Audit date: 2026-08-31
- Files checksummed: 74
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
6. The formal comparability audit contains 43 result cells, 903 pairwise rows, and 54 C3-comparable edges (6.0%; 19 classes; largest class 6).

## Author-verification gaps (not failures of this deposit)

- The extended S3 table contains 52 unique studies; the proposed 132-study core total has no deposited source extraction and requires author verification.
- The appraisal agreement aggregates originated from a provisional scenario; row-level D1–D5 ratings are absent and an empty schema is provided.
- Raw database exports and both screeners' independent decision files are not in this deposit.
- PRISMA identification, screening, tier-allocation, and agreement numbers are provisional estimates without deposited source records and must not be presented as verified review results.
- S4 page_confirmation remains author_verification_required until each number is checked against the cited PDF.

## How a reviewer should use this package

1. Read `README.md` and `S1_search_and_selection/AUTHOR_DEPOSIT_REQUIRED.md`.
2. Re-execute the Boolean strings in `S1_search_and_selection/03_executable_search_strings.md` if checking search reproducibility.
3. Treat `verification_status = provisional_author_verification_required` as an unsupported proposed value that must be replaced from original source records before submission.
4. Use `S4_performance_provenance/principal_table_provenance.csv` for the 43 formal-analysis cells and `performance_provenance.csv` for the extended manuscript tables.
5. Run `python S5_validation/scripts/validate_package.py`.
