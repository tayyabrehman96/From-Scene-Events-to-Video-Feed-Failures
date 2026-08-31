# Optional LitStudy interoperability

This package uses an optional interoperability script based on
[LitStudy](https://github.com/NLeSC/litstudy), version 1.0.6. LitStudy provides
uniform import of CSV, RIS, and BibTeX metadata; identifier-aware set
operations; descriptive bibliometric statistics; citation/co-authorship
networks; and exploratory topic modelling.

## Scope in this replication package

### Reproducible S3 evidence map

`scripts/build_litstudy_evidence_map.py` applies LitStudy's NMF and nonlinear
embedding functions to the 52 studies in `S3_extraction/core_primary_evidence.csv`.
The corpus combines bibliographic titles with deposited structured descriptors
(tier, training regime, scoring mechanism, representation, modality, and
datasets); no generated abstracts are used. It writes document-topic weights,
embedding coordinates, topic terms, and fixed parameters to `topic_model/`,
plus two local PNGs used by the manuscript.

This is an exploratory visualization of the table-extracted evidence subset.
It is not a topic model of the provisional 616-study set, and cluster size or
distance must not be interpreted as literature prevalence, effect size, or
study quality.

### Optional raw-export metadata audit

`scripts/litstudy_metadata_audit.py` uses only the metadata-ingestion and
`DocumentSet` union capabilities to:

1. load deposited CSV, RIS, and BibTeX source exports;
2. combine source collections using DOI/identifier/title matching;
3. report records loaded per file;
4. write year and venue distributions; and
5. report how many duplicate records the union collapsed.

These outputs are **secondary audit artefacts**. The authoritative review
process remains the S1 raw exports, explicit two-pass deduplication log,
independent screening decisions, and consensus ledger. LitStudy is not used to
infer eligibility, appraisal ratings, anomaly tiers, or performance values.

The adapter was added during replication-package preparation. It must not be
described as the software that generated the original PRISMA counts unless the
authors rerun the deposited source exports, compare the output against the
original ledger, and record that amendment.

## Installation and use

Core S5 validation has no third-party dependency. Install LitStudy only for
this optional audit:

```bash
python -m pip install -r S5_validation/requirements-litstudy.txt
python S5_validation/scripts/litstudy_metadata_audit.py
```

By default, the script reads `S1_search_and_selection/raw_exports/` and writes
to `S1_search_and_selection/screening/litstudy_audit/`. It exits without
creating results when no source exports have been deposited.

An alternative input is accepted:

```bash
python S5_validation/scripts/litstudy_metadata_audit.py \
  --input path/to/exports \
  --output path/to/audit
```

## Features deliberately not used as primary evidence

- Topic modelling and embeddings are exploratory and sensitive to abstract
  availability, preprocessing, stop words, topic count, and random state.
- Citation and co-citation networks are incomplete when databases expose only
  citation counts rather than reference lists.
- Scopus enrichment requires institutional access and an Elsevier API key.
- Automated annotations cannot replace independent human eligibility
  decisions under the declared IC1–IC5/EC1–EC5 criteria.

## Citation and licence

LitStudy is distributed under the Apache License 2.0. If this optional adapter
is used, cite:

> Heldens, S., Sclocco, A., Dreuning, H., van Werkhoven, B., Hijma, P.,
> Maassen, J., & van Nieuwpoort, R. V. (2022). litstudy: A Python package for
> literature reviews. *SoftwareX*, 20, 101207.
> https://doi.org/10.1016/j.softx.2022.101207

No LitStudy source code is copied into this repository; the adapter calls its
public Python API.
