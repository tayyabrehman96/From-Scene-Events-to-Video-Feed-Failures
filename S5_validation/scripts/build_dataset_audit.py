#!/usr/bin/env python3
"""Write the academic dataset audit (catalogue, distribution, caveats)."""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "datasets"
AS_OF = "2026-08-31"
STATUS = "transcribed_from_manuscript"

CATALOGUE_FIELDS = [
    "dataset_id",
    "dataset_name",
    "citation_key",
    "year",
    "primary_tier",
    "multi_tier_flag",
    "task_family",
    "composition",
    "public_access",
    "n_train",
    "n_test",
    "split_unit",
    "official_split_named",
    "n_scenes_or_cameras",
    "n_anomaly_categories",
    "n_anomaly_events",
    "annotation_granularity",
    "resolution",
    "modality",
    "imaging_setting",
    "typical_evaluation_metric",
    "supervision_regimes_supported",
    "primary_anomaly_types",
    "source_description_verified",
    "verification_status",
    "notes",
]


def row(**kwargs) -> dict:
    rec = {k: "NR" for k in CATALOGUE_FIELDS}
    rec["source_description_verified"] = AS_OF
    rec["verification_status"] = STATUS
    rec["multi_tier_flag"] = "no"
    rec.update({k: v for k, v in kwargs.items() if v is not None})
    return rec


def catalogue() -> list[dict]:
    return [
        row(
            dataset_id="DS-T1-001",
            dataset_name="UCSD Ped1",
            citation_key="mahadevan2010anomaly",
            year="2010",
            primary_tier="1",
            task_family="behavioral_video_anomaly_detection",
            composition="real",
            public_access="yes",
            n_train="34",
            n_test="36",
            split_unit="video clips",
            official_split_named="yes",
            n_scenes_or_cameras="1",
            n_anomaly_categories="3",
            n_anomaly_events="NR",
            annotation_granularity="frame + pixel",
            resolution="158x238",
            modality="RGB (grayscale pedestrian walkway)",
            imaging_setting="fixed camera; single pedestrian walkway",
            typical_evaluation_metric="frame-level AUC; pixel-level localization where reported",
            supervision_regimes_supported="normal-only / one-class; self-supervised",
            primary_anomaly_types="Non-pedestrian entities (bicycles, carts) and unusual pedestrian motion",
            notes="Early canonical VAD benchmark. Limited scene diversity and a narrow anomaly definition. Many recent methods report Ped-family AUC > 97%, reducing remaining discriminative headroom.",
        ),
        row(
            dataset_id="DS-T1-002",
            dataset_name="UCSD Ped2",
            citation_key="mahadevan2010anomaly",
            year="2010",
            primary_tier="1",
            task_family="behavioral_video_anomaly_detection",
            composition="real",
            public_access="yes",
            n_train="16",
            n_test="12",
            split_unit="video clips",
            official_split_named="yes",
            n_scenes_or_cameras="1",
            n_anomaly_categories="3",
            n_anomaly_events="NR",
            annotation_granularity="frame + pixel",
            resolution="240x360",
            modality="RGB (grayscale pedestrian walkway)",
            imaging_setting="fixed camera; single pedestrian walkway",
            typical_evaluation_metric="frame-level micro-AUC",
            supervision_regimes_supported="normal-only / one-class; self-supervised",
            primary_anomaly_types="Non-pedestrian entities (bicycles, skateboarders)",
            notes="Most frequently reported single-scene normal-only benchmark in the comparison tables. Residual scores are compressed into a high AUC band (approximately 94–99% in later literature).",
        ),
        row(
            dataset_id="DS-T1-003",
            dataset_name="UMN",
            citation_key="mehran2009abnormal",
            year="2009",
            primary_tier="1",
            task_family="behavioral_video_anomaly_detection",
            composition="real",
            public_access="yes",
            n_train="NR",
            n_test="11",
            split_unit="video clips",
            official_split_named="NR",
            n_scenes_or_cameras="3",
            n_anomaly_categories="1",
            n_anomaly_events="NR",
            annotation_granularity="frame",
            resolution="320x240",
            modality="RGB",
            imaging_setting="indoor/outdoor crowd scenes",
            typical_evaluation_metric="frame-level AUC (study-specific protocols)",
            supervision_regimes_supported="normal-only / one-class",
            primary_anomaly_types="Crowd panic and escape",
            notes="Pre-2010 seminal corpus retained under IC5 as technical context. Not treated as a contemporary leaderboard.",
        ),
        row(
            dataset_id="DS-T1-004",
            dataset_name="CUHK Avenue",
            citation_key="lu2013abnormal",
            year="2013",
            primary_tier="1",
            task_family="behavioral_video_anomaly_detection",
            composition="real",
            public_access="yes",
            n_train="16",
            n_test="21",
            split_unit="videos",
            official_split_named="yes",
            n_scenes_or_cameras="1",
            n_anomaly_categories="5",
            n_anomaly_events="47",
            annotation_granularity="frame + pixel",
            resolution="360x640",
            modality="RGB",
            imaging_setting="campus avenue; variable pedestrian density",
            typical_evaluation_metric="frame-level AUC",
            supervision_regimes_supported="normal-only / one-class; self-supervised",
            primary_anomaly_types="Running, throwing objects, loitering, walking in unusual directions",
            notes="Perspective-dependent object size and variable density make it more challenging than UCSD. Widely used for unsupervised and self-supervised evaluation.",
        ),
        row(
            dataset_id="DS-T1-005",
            dataset_name="ShanghaiTech Campus",
            citation_key="luo2017revisit",
            year="2017",
            primary_tier="1",
            task_family="behavioral_video_anomaly_detection",
            composition="real",
            public_access="yes",
            n_train="330",
            n_test="107",
            split_unit="videos",
            official_split_named="yes",
            n_scenes_or_cameras="13",
            n_anomaly_categories="11",
            n_anomaly_events="130",
            annotation_granularity="frame",
            resolution="various",
            modality="RGB",
            imaging_setting="university campus; 13 camera locations",
            typical_evaluation_metric="frame-level AUC (normal-only and some weakly supervised protocols)",
            supervision_regimes_supported="normal-only; self-supervised; weakly supervised (selected methods)",
            primary_anomaly_types="Chasing, brawling, cycling in pedestrian zones, and related campus anomalies",
            notes="Event count (130) and category count (11) must not be conflated. Multi-scene design is the principal reason it remains informative after Ped2 saturation.",
        ),
        row(
            dataset_id="DS-T1-006",
            dataset_name="UCF-Crime",
            citation_key="sultani2018real",
            year="2018",
            primary_tier="1",
            task_family="weakly_supervised_video_anomaly_detection",
            composition="real",
            public_access="yes",
            n_train="1610",
            n_test="290",
            split_unit="untrimmed videos",
            official_split_named="yes",
            n_scenes_or_cameras="many",
            n_anomaly_categories="13",
            n_anomaly_events="NR",
            annotation_granularity="video-level (training); temporal test labels in the official protocol",
            resolution="various",
            modality="RGB",
            imaging_setting="untrimmed real-world surveillance; diverse viewpoints",
            typical_evaluation_metric="frame-level AUC under weak supervision",
            supervision_regimes_supported="video-level weakly supervised MIL",
            primary_anomaly_types="Abuse, arrest, arson, assault, burglary, explosion, fighting, road accidents, robbery, shooting, shoplifting, stealing, vandalism",
            notes="Standard split: 800 normal + 810 anomalous training videos and 290 test videos (1,900 total). Video-level tags and loose temporal boundaries introduce label noise. Contains arson/explosion labels but does not evaluate camera/feed failure or early-warning fire protocols.",
        ),
        row(
            dataset_id="DS-T1-007",
            dataset_name="Street Scene",
            citation_key="ramachandra2020street",
            year="2020",
            primary_tier="1",
            task_family="behavioral_video_anomaly_detection",
            composition="real",
            public_access="yes",
            n_train="46",
            n_test="35",
            split_unit="videos",
            official_split_named="yes",
            n_scenes_or_cameras="1",
            n_anomaly_categories="17",
            n_anomaly_events="NR",
            annotation_granularity="frame + bounding box",
            resolution="1280x720",
            modality="RGB",
            imaging_setting="urban street; single scene",
            typical_evaluation_metric="frame-level and spatial localization metrics (study-specific)",
            supervision_regimes_supported="normal-only / one-class",
            primary_anomaly_types="Jaywalking, loitering, vehicle anomalies",
            notes="Higher spatial resolution and bounding-box annotation relative to Ped2/Avenue. Single-scene design still limits cross-camera claims.",
        ),
        row(
            dataset_id="DS-T1-008",
            dataset_name="XD-Violence",
            citation_key="wu2020not",
            year="2020",
            primary_tier="1",
            task_family="weakly_supervised_multimodal_violence_detection",
            composition="real",
            public_access="yes",
            n_train="3954",
            n_test="800",
            split_unit="untrimmed videos",
            official_split_named="yes",
            n_scenes_or_cameras="many",
            n_anomaly_categories="6",
            n_anomaly_events="NR",
            annotation_granularity="video-level",
            resolution="various",
            modality="RGB + audio",
            imaging_setting="untrimmed video with audio track",
            typical_evaluation_metric="average precision (AP, %)",
            supervision_regimes_supported="video-level weakly supervised; multimodal fusion",
            primary_anomaly_types="Six violence categories (enumerated in the source paper; not listed individually in the review table)",
            notes="4,754 videos in total. Audio is part of the official corpus; RGB-only versus RGB+audio results are not interchangeable. Do not compare AP on XD-Violence with AUC on UCF-Crime.",
        ),
        row(
            dataset_id="DS-T1-009",
            dataset_name="ADOC",
            citation_key="doshi2022adoc",
            year="2020",
            primary_tier="3",
            multi_tier_flag="yes",
            task_family="mixed_scene_and_camera_tampering",
            composition="mixed",
            public_access="yes",
            n_train="NR",
            n_test="18",
            split_unit="videos",
            official_split_named="study-specific",
            n_scenes_or_cameras="1",
            n_anomaly_categories="5",
            n_anomaly_events="mixed",
            annotation_granularity="frame",
            resolution="VGA",
            modality="RGB",
            imaging_setting="university campus surveillance",
            typical_evaluation_metric="online / study-specific anomaly scoring",
            supervision_regimes_supported="online anomaly detection",
            primary_anomaly_types="Campus scene anomalies and camera tampering",
            notes="The most directly multi-tier public corpus in the review (scene anomalies plus camera tampering). Small, study-specific protocol; does not cover fire/smoke.",
        ),
        row(
            dataset_id="DS-T1-010",
            dataset_name="UBnormal",
            citation_key="acsintoae2022ubnormal",
            year="2022",
            primary_tier="1",
            task_family="behavioral_video_anomaly_detection",
            composition="synthetic",
            public_access="yes",
            n_train="268",
            n_test="211",
            split_unit="videos",
            official_split_named="yes",
            n_scenes_or_cameras="29",
            n_anomaly_categories="22",
            n_anomaly_events="NR",
            annotation_granularity="frame + pixel",
            resolution="720x1080",
            modality="RGB (virtual actors / rendered scenes)",
            imaging_setting="synthetic surveillance scenes",
            typical_evaluation_metric="frame-level AUC; pixel-level localization",
            supervision_regimes_supported="normal-only; open-set / virtual anomaly generation",
            primary_anomaly_types="Synthetically rendered behavioral anomalies with pixel masks",
            notes="Pixel-level masks that are impractical to obtain on real video. Synthetic composition must be stated when comparing with real-camera corpora.",
        ),
        row(
            dataset_id="DS-T1-011",
            dataset_name="NWPU Campus",
            citation_key="cao2023nwpu",
            year="2023",
            primary_tier="1",
            task_family="behavioral_video_anomaly_detection",
            composition="real",
            public_access="yes",
            n_train="305",
            n_test="148",
            split_unit="videos",
            official_split_named="yes",
            n_scenes_or_cameras="43",
            n_anomaly_categories="28",
            n_anomaly_events="NR",
            annotation_granularity="frame + bounding box",
            resolution="1080p",
            modality="RGB",
            imaging_setting="large-scale multi-scene campus",
            typical_evaluation_metric="frame-level and spatial metrics (study-specific)",
            supervision_regimes_supported="normal-only / weakly supervised (as used by citing studies)",
            primary_anomaly_types="Large-scale campus multi-scene anomalies",
            notes="Largest scene count among the tabulated VAD corpora (43 scenes). Protocol details beyond the review table remain NR pending source-page confirmation.",
        ),
        row(
            dataset_id="DS-T1-012",
            dataset_name="CHAD (Charlotte Anomaly Dataset)",
            citation_key="pazho2023chad",
            year="2023",
            primary_tier="1",
            task_family="behavioral_video_anomaly_detection",
            composition="real",
            public_access="yes",
            n_train="NR",
            n_test="NR",
            split_unit="NR",
            official_split_named="NR",
            n_scenes_or_cameras="4",
            n_anomaly_categories="6",
            n_anomaly_events="NR",
            annotation_granularity="frame + bounding box",
            resolution="HD",
            modality="RGB",
            imaging_setting="high-resolution multi-view",
            typical_evaluation_metric="NR in the review table",
            supervision_regimes_supported="NR",
            primary_anomaly_types="Diverse behavioral anomalies and normal activities",
            notes="Train/test counts are not stated in the review table and are recorded as NR rather than inferred.",
        ),
        row(
            dataset_id="DS-T2-001",
            dataset_name="Foggia surveillance fire",
            citation_key="foggia2015fire",
            year="2015",
            primary_tier="2",
            task_family="fire_smoke_classification",
            composition="real",
            public_access="yes",
            n_train="NR",
            n_test="NR",
            split_unit="videos",
            official_split_named="corpus-specific",
            n_scenes_or_cameras="NR",
            n_anomaly_categories="NR",
            n_anomaly_events="NR",
            annotation_granularity="video / image classification labels",
            resolution="NR",
            modality="RGB",
            imaging_setting="real-world surveillance cameras",
            typical_evaluation_metric="classification accuracy",
            supervision_regimes_supported="fully supervised classification",
            primary_anomaly_types="Fire and smoke",
            notes="62 videos. Early real-world surveillance fire corpus. Accuracy is dataset-specific and not comparable with detection mAP or segmentation mIoU.",
        ),
        row(
            dataset_id="DS-T2-002",
            dataset_name="BoWFire",
            citation_key="chino2015bowfire",
            year="2015",
            primary_tier="2",
            task_family="fire_classification_and_segmentation",
            composition="real",
            public_access="yes",
            n_train="NR",
            n_test="NR",
            split_unit="images",
            official_split_named="NR",
            n_scenes_or_cameras="NR",
            n_anomaly_categories="NR",
            n_anomaly_events="NR",
            annotation_granularity="classification + superpixel / segmentation",
            resolution="NR",
            modality="RGB",
            imaging_setting="web imagery",
            typical_evaluation_metric="classification accuracy; region overlap (study-specific)",
            supervision_regimes_supported="fully supervised",
            primary_anomaly_types="Fire (no smoke column in the review table)",
            notes="226 images. Superpixel-level fire annotation. Also appears as a FiSmo sub-collection and must not be double-counted as a separate aggregate.",
        ),
        row(
            dataset_id="DS-T2-003",
            dataset_name="FiSmo",
            citation_key="cazzolato2017fismo",
            year="2017",
            primary_tier="2",
            task_family="fire_smoke_classification_and_segmentation",
            composition="mixed",
            public_access="yes",
            n_train="NR",
            n_test="NR",
            split_unit="images / videos (sub-collections)",
            official_split_named="sub-collections reported separately",
            n_scenes_or_cameras="NR",
            n_anomaly_categories="NR",
            n_anomaly_events="NR",
            annotation_granularity="classification + segmentation (varies by sub-collection)",
            resolution="NR",
            modality="RGB",
            imaging_setting="mixed / web emergency-situation imagery",
            typical_evaluation_metric="sub-collection specific",
            supervision_regimes_supported="fully supervised",
            primary_anomaly_types="Fire and smoke",
            notes="Compilation of six sub-collections. Documented subsets: Flickr-Fire (2,000 images), BoWFire (226 images), SmokeBlock (1,666 images), plus annotated video subsets. Do not quote a single aggregate size.",
        ),
        row(
            dataset_id="DS-T2-004",
            dataset_name="FireNet",
            citation_key="jadon2019firenet",
            year="2019",
            primary_tier="2",
            task_family="fire_classification",
            composition="mixed",
            public_access="yes",
            n_train="NR",
            n_test="NR",
            split_unit="images",
            official_split_named="balanced binary set; split details NR",
            n_scenes_or_cameras="NR",
            n_anomaly_categories="2",
            n_anomaly_events="NR",
            annotation_granularity="image-level binary (fire / non-fire)",
            resolution="NR",
            modality="RGB",
            imaging_setting="indoor and outdoor mixed sources",
            typical_evaluation_metric="classification accuracy",
            supervision_regimes_supported="fully supervised; edge-oriented classifiers",
            primary_anomaly_types="Fire (binary; smoke not tabulated)",
            notes="Approximately 2,500 images, described as evenly divided. Preprint-associated corpus; the review records its accuracy for completeness and does not use it for state-of-the-art claims.",
        ),
        row(
            dataset_id="DS-T2-005",
            dataset_name="FLAME",
            citation_key="shamsoshoara2021aerial",
            year="2021",
            primary_tier="2",
            task_family="fire_smoke_classification_and_segmentation",
            composition="real",
            public_access="yes",
            n_train="NR",
            n_test="NR",
            split_unit="images and videos",
            official_split_named="NR",
            n_scenes_or_cameras="NR (UAV prescribed-burn sorties)",
            n_anomaly_categories="NR",
            n_anomaly_events="NR",
            annotation_granularity="frame-level binary + instance segmentation masks",
            resolution="NR",
            modality="RGB (aerial UAV)",
            imaging_setting="prescribed burns, Northern Arizona; aerial viewpoint",
            typical_evaluation_metric="classification labels; segmentation mIoU (e.g. Guan et al. 82.3% mIoU)",
            supervision_regimes_supported="fully supervised classification and segmentation",
            primary_anomaly_types="Fire and smoke",
            notes="2,003 images and 39 video sequences. Aerial masks are not comparable with ground-camera detection mAP.",
        ),
        row(
            dataset_id="DS-T2-006",
            dataset_name="D-Fire",
            citation_key="de2022dfire",
            year="2022",
            primary_tier="2",
            task_family="fire_smoke_detection",
            composition="mixed",
            public_access="yes",
            n_train="NR",
            n_test="NR",
            split_unit="images",
            official_split_named="NR",
            n_scenes_or_cameras="NR",
            n_anomaly_categories="NR",
            n_anomaly_events="NR",
            annotation_granularity="bounding box (detection)",
            resolution="NR",
            modality="RGB",
            imaging_setting="indoor, forest, and urban mixed environments",
            typical_evaluation_metric="detection AP/mAP at a study-specific IoU",
            supervision_regimes_supported="fully supervised object detection",
            primary_anomaly_types="Fire and smoke",
            notes="21,527 images. Addresses the single-environment limitation of earlier fire corpora. IoU threshold and official split remain NR in the review table.",
        ),
        row(
            dataset_id="DS-T2-007",
            dataset_name="FASDD",
            citation_key="wang2024fasdd",
            year="2024",
            primary_tier="2",
            task_family="fire_smoke_detection",
            composition="mixed",
            public_access="yes",
            n_train="NR",
            n_test="NR",
            split_unit="images",
            official_split_named="NR",
            n_scenes_or_cameras="NR",
            n_anomaly_categories="NR",
            n_anomaly_events="NR",
            annotation_granularity="bounding box for flame and smoke",
            resolution="NR",
            modality="RGB (remote sensing + ground)",
            imaging_setting="heterogeneous fire types, smoke densities, and environments",
            typical_evaluation_metric="detection AP/mAP (study-specific)",
            supervision_regimes_supported="fully supervised object detection",
            primary_anomaly_types="Fire and smoke",
            notes="Largest tabulated fire/smoke set (>120,000 images). Heterogeneity is the design goal; protocol-level comparability still requires matched splits and IoU.",
        ),
        row(
            dataset_id="DS-T3-001",
            dataset_name="Ribnick et al. tampering corpus",
            citation_key="ribnick2006realtime",
            year="2006",
            primary_tier="3",
            task_family="camera_tampering_detection",
            composition="real",
            public_access="partial",
            n_train="NR",
            n_test="NR",
            split_unit="videos",
            official_split_named="no public standard split",
            n_scenes_or_cameras="NR",
            n_anomaly_categories="NR",
            n_anomaly_events="30+",
            annotation_granularity="study-specific event labels",
            resolution="640x480",
            modality="RGB",
            imaging_setting="real demonstrations of physical tampering",
            typical_evaluation_metric="real-time detection; FAR not standardized",
            supervision_regimes_supported="handcrafted / DSP change detection",
            primary_anomaly_types="Spray; physical displacement",
            notes="40+ videos. Pre-2010 seminal context. Partial public access. Small study-specific collection.",
        ),
        row(
            dataset_id="DS-T3-002",
            dataset_name="UHCTD",
            citation_key="mantini2019uhctd",
            year="2019",
            primary_tier="3",
            task_family="camera_tampering_detection",
            composition="synthetic faults on real feeds",
            public_access="yes",
            n_train="NR",
            n_test="NR",
            split_unit="hours of video",
            official_split_named="protocol-specific",
            n_scenes_or_cameras="2",
            n_anomaly_categories="3",
            n_anomaly_events="synthetic",
            annotation_granularity="tampering-type labels on injected faults",
            resolution="NR",
            modality="RGB",
            imaging_setting="two real surveillance cameras; synthetic covered, defocused, and moved faults",
            typical_evaluation_metric="protocol-specific (classification / EER; FAR not a community standard)",
            supervision_regimes_supported="supervised baselines and feature time-series methods",
            primary_anomaly_types="Covered; defocused; moved",
            notes="Principal public camera-tampering benchmark in the review (>288 hours). Two-camera limitation and limited gradual-fault coverage are the main external-validity constraints.",
        ),
    ]


UCF_CATEGORIES = [
    "abuse",
    "arrest",
    "arson",
    "assault",
    "burglary",
    "explosion",
    "fighting",
    "road accidents",
    "robbery",
    "shooting",
    "shoplifting",
    "stealing",
    "vandalism",
]

FISMO_SUBSETS = [
    ("Flickr-Fire", "2000", "images", "fire"),
    ("BoWFire", "226", "images", "fire"),
    ("SmokeBlock", "1666", "images", "smoke"),
]


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def distribution(cat: list[dict]) -> list[dict]:
    rows = []

    def add(axis, level, n, note=""):
        rows.append(
            {
                "axis": axis,
                "level": level,
                "n_corpora": n,
                "share_of_catalogue": round(n / len(cat), 4),
                "note": note,
            }
        )

    add("catalogue", "unique_corpora", len(cat), "ADOC counted once (multi-tier)")
    by_tier = Counter(r["primary_tier"] for r in cat)
    add("primary_tier", "1_behavioral", by_tier["1"], "Principal evaluation tier; ADOC assigned to tier 3")
    add("primary_tier", "2_fire_smoke", by_tier["2"], "")
    add("primary_tier", "3_feed_integrity", by_tier["3"], "Includes ADOC and UHCTD and Ribnick")
    add("multi_tier_flag", "yes", sum(r["multi_tier_flag"] == "yes" for r in cat), "ADOC only in this catalogue")
    add("multi_tier_flag", "no", sum(r["multi_tier_flag"] == "no" for r in cat), "")
    by_pub = Counter(r["public_access"] for r in cat)
    for k in ("yes", "partial", "no"):
        if by_pub[k]:
            add("public_access", k, by_pub[k], "")
    by_comp = Counter(r["composition"] for r in cat)
    for k, n in sorted(by_comp.items()):
        add("composition", k, n, "")
    ann_groups = Counter()
    for r in cat:
        g = r["annotation_granularity"].split(";")[0]
        if "video-level" in g:
            key = "video_level"
        elif "pixel" in g:
            key = "frame_and_or_pixel"
        elif "bounding box" in g or "bbox" in g:
            key = "frame_and_or_box"
        elif "segmentation" in g or "superpixel" in g or "mask" in g:
            key = "segmentation_or_region"
        elif "classification" in g or "binary" in g:
            key = "image_or_video_classification"
        else:
            key = "other_or_study_specific"
        ann_groups[key] += 1
    for k, n in sorted(ann_groups.items()):
        add("annotation_family", k, n, "Coarse grouping of the annotation_granularity field")

    vad = [r for r in cat if r["primary_tier"] == "1" and r["dataset_name"] != "UMN"]
    def to_int(x):
        try:
            return int(str(x).replace(",", ""))
        except ValueError:
            return None

    train_sum = sum(to_int(r["n_train"]) or 0 for r in vad)
    test_sum = sum(to_int(r["n_test"]) or 0 for r in vad)
    n_train_known = sum(to_int(r["n_train"]) is not None for r in vad)
    n_test_known = sum(to_int(r["n_test"]) is not None for r in vad)
    rows.append(
        {
            "axis": "vad_split_volume",
            "level": "sum_n_train_where_numeric",
            "n_corpora": n_train_known,
            "share_of_catalogue": train_sum,
            "note": f"Sum of numeric train counts among tier-1 corpora excluding UMN; CHAD train is NR. Column share_of_catalogue holds the summed video/clip count ({train_sum}).",
        }
    )
    rows.append(
        {
            "axis": "vad_split_volume",
            "level": "sum_n_test_where_numeric",
            "n_corpora": n_test_known,
            "share_of_catalogue": test_sum,
            "note": f"Sum of numeric test counts among tier-1 corpora excluding UMN. Column share_of_catalogue holds the summed video/clip count ({test_sum}).",
        }
    )
    return rows


def caveats(cat: list[dict]) -> list[dict]:
    return [
        {
            "dataset_id": r["dataset_id"],
            "dataset_name": r["dataset_name"],
            "caveat_id": f"{r['dataset_id']}-C1",
            "caveat": r["notes"],
            "implication_for_comparison": (
                "Do not pool this corpus with a different task, metric, split, or modality without a qualified comparison."
            ),
        }
        for r in cat
    ]


def categories() -> list[dict]:
    rows = []
    for i, name in enumerate(UCF_CATEGORIES, 1):
        rows.append(
            {
                "dataset_name": "UCF-Crime",
                "citation_key": "sultani2018real",
                "category_index": i,
                "category_name": name,
                "tier_relevance": "1 (behavioral); arson and explosion are labels inside a weakly supervised crime corpus, not a fire-monitoring benchmark",
                "source": "manuscript UCF-Crime paragraph",
            }
        )
    for name, n, unit, phenomenon in FISMO_SUBSETS:
        rows.append(
            {
                "dataset_name": "FiSmo",
                "citation_key": "cazzolato2017fismo",
                "category_index": "",
                "category_name": f"sub-collection:{name}",
                "tier_relevance": f"2 ({phenomenon}); {n} {unit}",
                "source": "manuscript FiSmo paragraph",
            }
        )
    return rows


def dictionary() -> list[dict]:
    return [
        {"column": "dataset_id", "definition": "Stable identifier. T1/T2/T3 encodes the principal operational tier."},
        {"column": "primary_tier", "definition": "1 = behavioral/object interaction; 2 = fire/smoke hazard; 3 = camera/video-feed integrity. Multi-tier corpora receive one primary tier plus multi_tier_flag=yes."},
        {"column": "composition", "definition": "real | synthetic | mixed | synthetic faults on real feeds. Not inferred beyond the review text."},
        {"column": "public_access", "definition": "yes | partial | no. Partial means the originating study used a collection that is not fully redistributable."},
        {"column": "n_train / n_test", "definition": "Official split sizes in split_unit. NR if the review table does not state a number."},
        {"column": "official_split_named", "definition": "Whether a reusable named train/test partition is identified in the review."},
        {"column": "n_anomaly_events", "definition": "Count of anomalous events, distinct from n_anomaly_categories (see ShanghaiTech)."},
        {"column": "annotation_granularity", "definition": "What is labelled: video, frame, box, pixel, superpixel, or a combination."},
        {"column": "typical_evaluation_metric", "definition": "Metric family used on this corpus in the review. Not a licence to compare across families."},
        {"column": "NR", "definition": "Not reported in the manuscript tables or dataset-section prose. Not imputed."},
    ]


def main() -> None:
    cat = catalogue()
    write_csv(OUT / "dataset_catalogue.csv", CATALOGUE_FIELDS, cat)
    write_csv(
        OUT / "dataset_distribution.csv",
        ["axis", "level", "n_corpora", "share_of_catalogue", "note"],
        distribution(cat),
    )
    write_csv(
        OUT / "dataset_protocol_caveats.csv",
        ["dataset_id", "dataset_name", "caveat_id", "caveat", "implication_for_comparison"],
        caveats(cat),
    )
    write_csv(
        OUT / "dataset_categories_and_subsets.csv",
        ["dataset_name", "citation_key", "category_index", "category_name", "tier_relevance", "source"],
        categories(),
    )
    write_csv(OUT / "DATA_DICTIONARY.csv", ["column", "definition"], dictionary())
    print(f"Wrote {len(cat)} dataset catalogue rows to {OUT}")


if __name__ == "__main__":
    main()
