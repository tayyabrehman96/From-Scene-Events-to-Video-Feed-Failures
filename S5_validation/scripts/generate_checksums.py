#!/usr/bin/env python3
"""Recompute SHA-256 checksums for every tracked package file."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "S5_validation" / "checksums.sha256"
SKIP = {".git", "__pycache__", "_github_clone"}


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
        if any(part in SKIP for part in p.parts):
            continue
        if p.name == "checksums.sha256":
            continue
        files.append(p)
    lines = []
    for p in sorted(files, key=lambda x: x.relative_to(ROOT).as_posix()):
        lines.append(f"{sha256_file(p)}  {p.relative_to(ROOT).as_posix()}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} checksums to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
