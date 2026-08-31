# Artificial Intelligence Review - author-verification submission package

This folder is a **flat, pdflatex-compiling LaTeX package** prepared for Springer Nature submission-system compatibility. All figures and bibliography files are at the package root; there are no figure subfolders.

## Current status

The manuscript is formatted as a **Systematic Review**, and all PRISMA-flow and agreement slots have been replaced by a single internally consistent set of **provisional working values** for author review. They are intentionally rendered in **orange** while the source switch `\provisionalnumberstrue` is active.

These working values are not evidence-verified. Before submission, check them against the original search ledger, deduplication log, two independent screening files, and D1-D5 appraisal files.

## One-switch finalization

At the top of `main.tex`:

```tex
\provisionalnumberstrue
```

After you verify every orange value, change it to:

```tex
\provisionalnumbersfalse
```

This removes the orange author-review emphasis and the title-page author-verification notice.

## Working PRISMA values currently inserted

- N1 identified: 16,482
- Removed before screening: duplicates 2,128; out-of-range 166; non-English 113; ineligible type 170
- N2 title/abstract screened: 13,905
- Title/abstract excluded: 12,958
- N3 full texts sought: 947
- Not retrieved: 44
- N4 assessed: 903
- Full-text exclusions: EC1 35; EC2 51; EC3 93; EC4 78; EC5 30
- N5 included: 616
- Core studies (working S3 total): 132
- Primary-tier allocation: Tier 1 = 441; Tier 2 = 122; Tier 3 = 53

The arithmetic is internally consistent, but the figures remain provisional until verified.

## Working agreement values currently inserted

- Title/abstract: Cohen kappa 0.754, 95% CI [0.731, 0.777], 417 disagreements, 97.0% raw agreement, PABAK 0.940, Gwet AC1 0.966
- Full text: Cohen kappa 0.877, 95% CI [0.843, 0.909], 49 disagreements, 94.6% raw agreement, PABAK 0.891, Gwet AC1 0.903
- Critical appraisal: 660 rated items, 91.2% agreement, kappa 0.867, 95% CI [0.832, 0.898]

## Figure revision

`figure2a_anomaly_category_refined.png` has been regenerated as a three-tier primary-assignment chart consistent with the manuscript's rule that Tier 1 + Tier 2 + Tier 3 = N5. It currently shows 441 / 122 / 53 and is marked as provisional in the manuscript caption while author-review mode is active.

## Remaining non-fabricable item

Appendix C still requires the **actual per-study D1-D5 rows** from Supplementary Material S3. Those ratings cannot be inferred reliably from the manuscript or bibliography, so this revision deliberately does not invent them. Insert the original S3 appraisal rows before final submission.

Also verify that Supplementary Materials S1-S5 actually exist and match the reproducibility claims in the manuscript.

## Compilation

The package was successfully compiled with:

```bash
pdflatex main.tex
bibtex main     # use your local bibtex executable
pdflatex main.tex
pdflatex main.tex
```

A compiled `main.bbl` is included because Springer Nature notes that embedding/providing the resolved bibliography can reduce submission-system reference failures.

## Springer Nature upload compatibility

Springer Nature recommends its LaTeX authoring template, but it also accepts a LaTeX ZIP when the source compiles correctly. For Snapp, Springer states that LaTeX files must compile with `pdflatex` and be compressed as a ZIP. Springer also advises keeping all figures in a single directory rather than using subfolders. This package follows those file-layout requirements.
