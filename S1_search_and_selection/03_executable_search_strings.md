# S1 — Executable database search strings

These strings are transcribed from manuscript Appendix A (`app:search_strings`) so that a reviewer can re-execute the fielded searches. Field codes and date filters are shown as applied. Concept blocks correspond to the four query families in `01_query_families.csv`.

**Evidence freeze:** 30 June 2026.  
**Covered window:** January 2010 – 30 June 2026.  
**Initial search:** April 2025. **Update search:** June 2026.

## Scopus (`TITLE-ABS-KEY`)

```
TITLE-ABS-KEY(
 ("video anomaly detection" OR "abnormal event" OR "anomalous event"
  OR "violence detection" OR loitering OR "fall detection"
  OR "crowd anomaly" OR "traffic anomaly" OR "abandoned object")
 OR ( (fire OR flame OR smoke OR wildfire OR haze) W/5
      (detection OR classification OR segmentation OR "early warning") )
 OR ( ("camera tampering" OR "camera anomaly" OR "lens occlusion"
       OR "defocus" OR "frozen stream" OR "frame loss"
       OR "signal corruption" OR "no-reference image quality") )
)
AND ( surveillance OR CCTV OR "closed-circuit" OR monitoring
      OR "traffic camera" )
AND ( "deep learning" OR CNN OR RNN OR autoencoder OR transformer
      OR "vision-language" OR "foundation model" OR "self-supervised"
      OR "multiple instance" OR diffusion OR "state-space" OR Mamba )
AND PUBYEAR > 2009 AND PUBYEAR < 2027
AND ( LIMIT-TO(DOCTYPE,"ar") OR LIMIT-TO(DOCTYPE,"cp") )
AND ( LIMIT-TO(LANGUAGE,"English") )
```

## Web of Science Core Collection (Topic field `TS`)

```
TS=( ("video anomaly detection" OR "abnormal event" OR "anomalous event"
      OR "violence detection" OR loitering OR "fall detection"
      OR "crowd anomaly" OR "traffic anomaly" OR "abandoned object"
      OR (fire OR flame OR smoke OR wildfire) NEAR/5
         (detection OR classification OR segmentation)
      OR "camera tampering" OR "camera anomaly" OR "lens occlusion"
      OR "frozen stream" OR "frame loss" OR "no-reference image quality") )
AND TS=( surveillance OR CCTV OR "closed-circuit" OR monitoring )
Refined by: Document Types = (ARTICLE OR PROCEEDINGS PAPER)
            Languages = (ENGLISH)
Timespan = 2010-01-01 to 2026-06-30
```

## IEEE Xplore (Command Search; metadata + abstract)

```
( "All Metadata":"video anomaly detection" OR "abnormal event"
  OR "violence detection" OR "crowd anomaly" OR "abandoned object"
  OR "fire detection" OR "smoke detection" OR "camera tampering"
  OR "camera anomaly" OR "frozen stream" OR "frame loss" )
AND ( "All Metadata":surveillance OR CCTV OR monitoring )
AND ( "All Metadata":"deep learning" OR CNN OR transformer
      OR autoencoder OR "vision-language" OR "self-supervised"
      OR "multiple instance" )
Filters: Year 2010-2026; Content Type: Conferences, Journals
```

## ACM Digital Library (Advanced Search; title/abstract/keywords)

```
[[Title: "video anomaly detection"] OR [Abstract: "abnormal event"]
 OR [Keywords: "violence detection"] OR [Abstract: "fire detection"]
 OR [Abstract: "smoke detection"] OR [Abstract: "camera tampering"]]
AND [[Abstract: surveillance] OR [Abstract: CCTV]
     OR [Abstract: monitoring]]
AND [Publication Date: (01/01/2010 TO 06/30/2026)]
```

## Official proceedings (non-Boolean)

WACV 2026 and CVPR 2026 open-access proceedings available before the freeze were screened title-by-title against the same vocabulary. Main / Findings / workshop designation is a required per-item field. Findings papers are not treated as equivalent to main-conference papers.

## Google Scholar

Google Scholar was used only as supplementary discovery. Non-fielded phrase queries, maximum screened rank, and the inclusion/deduplication rule belong in `09_google_scholar_protocol.md` and must be completed from the original search log (see `AUTHOR_DEPOSIT_REQUIRED.md`).
