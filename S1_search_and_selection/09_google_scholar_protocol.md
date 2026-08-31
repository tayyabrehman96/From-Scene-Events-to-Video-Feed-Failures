# S1 — Google Scholar supplementary-discovery protocol

Google Scholar is **not** a fielded bibliographic database. Boolean interpretation, ranking, and the result set are less reproducible than IEEE Xplore, ACM DL, Scopus, or Web of Science. The review therefore uses it only as a supplementary discovery source.

## Predeclared rules (from the manuscript)

| Rule | Specification |
| --- | --- |
| Role | Gap filling and citation discovery, not a primary identification source |
| Date handling | Search dates recorded separately from the fielded-database freeze |
| Screening rule | Records are screened only down to a predeclared maximum rank |
| Deduplication | Scholar hits are merged into the master record set after DOI then title–author–year deduplication |
| Inclusion | Same eligibility criteria as Table 3 / `06_eligibility_inclusion_exclusion.csv` |
| Reporting | Query string, execution date, interface, maximum screened rank, and unique-after-dedup count are required fields |

## Author deposit still required

The working PRISMA identification cell (`Google Scholar (supplementary) = 2,142`) is a **provisional author-review value**. Deposit the original Scholar query log here:

- exact phrase queries as executed
- date/time and interface (web UI vs API)
- maximum rank screened per query
- export or screening sheet of unique records retained after deduplication

Until that log is deposited, reviewers can audit the *protocol* but cannot recompute the Scholar identification count from source.
