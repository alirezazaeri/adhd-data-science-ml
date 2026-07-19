"""Regression tests for notebook structure and hash validation."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts import validate_notebook_integrity as validator


class NotebookIntegrityTests(unittest.TestCase):
    def test_loads_exact_manifest_entries(self) -> None:
        digest = "a" * 64
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "manifest.md"
            manifest.write_text(f"| `notebooks/example.ipynb` | `{digest}` |\n", encoding="utf-8")

            entries = validator.load_manifest(manifest, {"notebooks/example.ipynb"})

            self.assertEqual(entries, {"notebooks/example.ipynb": digest})

    def test_rejects_missing_or_extra_manifest_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "manifest.md"
            manifest.write_text("No notebook hashes here.\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "missing=.*example"):
                validator.load_manifest(manifest, {"notebooks/example.ipynb"})

    def test_accepts_valid_json_with_matching_hash(self) -> None:
        content = json.dumps({"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}).encode()
        digest = hashlib.sha256(content).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "notebooks" / "example.ipynb"
            path.parent.mkdir()
            path.write_bytes(content)

            validator.validate_notebook("notebooks/example.ipynb", digest, root)

    def test_rejects_hash_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "notebooks" / "example.ipynb"
            path.parent.mkdir()
            path.write_text("{}", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Hash mismatch"):
                validator.validate_notebook("notebooks/example.ipynb", "0" * 64, root)

    def test_rejects_invalid_notebook_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "notebooks" / "example.ipynb"
            path.parent.mkdir()
            path.write_text("not json", encoding="utf-8")

            with self.assertRaises(json.JSONDecodeError):
                validator.validate_notebook("notebooks/example.ipynb", "0" * 64, root)


if __name__ == "__main__":
    unittest.main()
