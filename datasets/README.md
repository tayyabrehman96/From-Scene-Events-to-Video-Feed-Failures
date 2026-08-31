# Dataset audit

This folder is the **dataset audit** that accompanies Supplementary Material S4. It records, for every benchmark or study-specific corpus tabulated in the review, the fields declared in the manuscript:

> official split, public-access status, real/synthetic/mixed composition, number of cameras or scenes where available, annotation level, known protocol caveats, and the date on which the source description was last verified. Cells that cannot be established from the primary source are marked **NR** rather than inferred.

The package does **not** redistribute video, images, or weights. It documents *which* public corpora the review used and *how* they differ, so that a reader can audit comparability claims without treating heterogeneous benchmarks as a single leaderboard.

## Files

| File | Contents |
| --- | --- |
| [`dataset_catalogue.csv`](dataset_catalogue.csv) | One row per unique corpus (21 datasets). Master audit. |
| [`dataset_distribution.csv`](dataset_distribution.csv) | Counts and shares by primary tier, manuscript-table membership, tier dedication, public access, composition, and annotation family; summed VAD train/test volume where numeric |
| [`dataset_protocol_caveats.csv`](dataset_protocol_caveats.csv) | Per-corpus comparison caveats |
| [`dataset_categories_and_subsets.csv`](dataset_categories_and_subsets.csv) | UCF-Crime’s 13 named categories; FiSmo sub-collections that must not be aggregated |
| [`DATA_DICTIONARY.csv`](DATA_DICTIONARY.csv) | Column definitions |

## Operational tiers

| Tier | Operational family | Corpora in this catalogue (primary assignment) |
| --- | --- | --- |
| 1 | Behavioural / object-interaction video anomaly detection | UCSD Ped1/Ped2, UMN, CUHK Avenue, ShanghaiTech, UCF-Crime, Street Scene, XD-Violence, UBnormal, NWPU Campus, CHAD |
| 2 | Physical hazard (fire / smoke) | Foggia, BoWFire, FiSmo, FireNet, FLAME, D-Fire, FASDD |
| 3 | Camera / video-feed integrity | Ribnick tampering corpus, UHCTD; **ADOC** (primary tier 3, also scene anomalies) |

ADOC is the only tabulated corpus that jointly evaluates scene anomalies and camera tampering. It is counted once (`multi_tier_flag = yes`). UCF-Crime contains arson and explosion *labels* but is not a fire-monitoring or feed-integrity benchmark.

Two counting axes are retained explicitly. Under mutually exclusive `primary_tier`, ADOC is assigned to Tier 3, giving 11/7/3 unique corpora. Under `manuscript_table_membership`, ADOC appears in both the behavioural and feed-integrity dataset tables, giving 12/7/3 table memberships. These memberships overlap and therefore must not be summed as unique datasets. The `tier_dedicated_corpora` axis reproduces the manuscript's 11/7/1 dedicated-corpus counts.

## How to read distribution

`dataset_distribution.csv` is the intended summary for reviewers:

- **primary_tier** — infrastructure asymmetry: behavioral VAD has many reusable public splits; fire/smoke is intermediate; feed integrity is sparse (UHCTD plus small or partial collections).
- **manuscript_table_membership** — reproduces the 12/7/3 counts in the dataset tables; ADOC is counted in two tables.
- **tier_dedicated_corpora** — distinguishes reusable tier-specific corpora from mixed or study-specific collections (11/7/1).
- **composition** — real versus synthetic versus mixed. UBnormal is synthetic; UHCTD injects synthetic faults onto real feeds; several fire sets are mixed web/ground/remote-sensing imagery.
- **annotation_family** — video-level weak labels (UCF-Crime, XD-Violence) are not interchangeable with frame+pixel Ped2/Avenue masks or with fire detection boxes / segmentation masks.
- **vad_split_volume** — sums of *numeric* train and test clip/video counts on tier-1 rows excluding UMN. CHAD train/test remain NR and are omitted from the sum. The `share_of_catalogue` column on those two rows holds the **summed count**, not a proportion.

## Comparability rule (aligned with the manuscript)

A result on one row of the catalogue supports a **direct** comparison with another row only when task, supervision regime, split, modality, pretraining, metric implementation, and post-processing are sufficiently aligned. Any single mismatch requires a qualified comparison. In particular:

- Do not rank Ped2/Avenue/ShanghaiTech frame-AUC against UCF-Crime frame-AUC or XD-Violence AP.
- Do not rank fire classification accuracy against detection mAP or segmentation mIoU.
- Do not treat two-camera UHCTD protocols as a community FAR standard.
- Do not merge FiSmo sub-collections into one size statistic.

## Verification

`source_description_verified` is the package date. Values are transcribed from the review’s dataset tables and dataset-section prose. Where the manuscript is silent, the cell is **NR**. Official host URLs and licence texts are not invented here; retrieve them from the cited publications.

Last generated: 2026-08-31.
