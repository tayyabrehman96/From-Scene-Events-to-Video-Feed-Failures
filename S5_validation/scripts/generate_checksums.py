#!/usr/bin/env python3
"""Recompute SHA-256 checksums for every tracked package file."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "S5_validation" / "checksums.sha256"
SKIP_DIRS = {".git", "__pycache__", "_github_clone", "manuscript"}
SKIP_NAMES = {
    "main.tex",
    "main.bbl",
    "main.pdf",
    "references.bib",
    "README_BEFORE_SUBMISSION.md",
    "PDF_PREFLIGHT.txt",
    "PRISMA_PROVISIONAL_NUMBERS_FOR_REVIEW.csv",
    "checksums.sha256",
}
SKIP_SUFFIXES = {".png"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    files = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name in SKIP_NAMES:
            continue
        if p.suffix.lower() in SKIP_SUFFIXES:
            continue
        files.append(p)
    lines = []
    for p in sorted(files, key=lambda x: x.relative_to(ROOT).as_posix()):
        lines.append(f"{sha256_file(p)}  {p.relative_to(ROOT).as_posix()}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} checksums to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
