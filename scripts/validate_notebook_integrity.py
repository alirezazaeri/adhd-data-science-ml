#!/usr/bin/env python3
"""Validate the JSON structure and approved hashes of the tracked notebooks."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "NOTEBOOK_INTEGRITY.md"
EXPECTED_NOTEBOOKS = {
    "notebooks/1_data_eploration.ipynb",
    "notebooks/2_modeling.ipynb",
}
TABLE_ROW = re.compile(
    r"^\| `(?P<path>notebooks/[^`]+\.ipynb)` \| `(?P<digest>[0-9a-f]{64})` \|$"
)


def load_manifest() -> dict[str, str]:
    """Read the notebook hash table from the public integrity document."""
    entries: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        match = TABLE_ROW.match(line)
        if match:
            entries[match.group("path")] = match.group("digest")

    if set(entries) != EXPECTED_NOTEBOOKS:
        missing = sorted(EXPECTED_NOTEBOOKS - set(entries))
        extra = sorted(set(entries) - EXPECTED_NOTEBOOKS)
        raise ValueError(f"Notebook manifest mismatch; missing={missing}, extra={extra}")
    return entries


def sha256(path: Path) -> str:
    """Return the SHA-256 digest without modifying the file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_notebook(relative_path: str, expected_hash: str) -> None:
    """Check that one notebook is valid JSON and has the approved digest."""
    path = ROOT / relative_path
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)

    actual_hash = sha256(path)
    if actual_hash != expected_hash:
        raise ValueError(f"Hash mismatch: {relative_path}")
    print(f"OK: {relative_path}")


def main() -> int:
    try:
        for notebook, expected_hash in sorted(load_manifest().items()):
            validate_notebook(notebook, expected_hash)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Notebook integrity validation failed: {exc}", file=sys.stderr)
        return 1

    print("Notebook integrity validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
