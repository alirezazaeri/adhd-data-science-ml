"""Tests for dataset-free notebook dependency declaration checks."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts import validate_dependency_declarations as validator


class DependencyDeclarationTests(unittest.TestCase):
    def test_loads_normalized_requirement_names(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "requirements.txt"
            path.write_text("scikit_learn>=1\nPandas\n# comment\n", encoding="utf-8")

            self.assertEqual(validator.load_requirements(path), {"scikit-learn", "pandas"})

    def test_extracts_imports_from_code_cells_only(self) -> None:
        notebook = {
            "cells": [
                {"cell_type": "markdown", "source": ["import hidden\n"]},
                {"cell_type": "code", "source": ["import pandas as pd\n", "from sklearn.model_selection import train_test_split\n"]},
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "notebook.ipynb"
            path.write_text(json.dumps(notebook), encoding="utf-8")

            self.assertEqual(validator.extract_notebook_imports(path), {"pandas", "sklearn"})

    def test_accepts_declared_import_aliases_and_standard_library(self) -> None:
        imports = {"IPython", "os", "pandas", "sklearn"}
        requirements = {"ipython", "pandas", "scikit-learn"}

        self.assertEqual(validator.missing_declarations(imports, requirements), set())

    def test_reports_undeclared_third_party_import(self) -> None:
        missing = validator.missing_declarations({"pandas", "shap"}, {"pandas"})

        self.assertEqual(missing, {"shap"})

    def test_requires_mapping_for_new_requirement(self) -> None:
        with self.assertRaisesRegex(ValueError, "new-package"):
            validator.declared_imports({"new-package"})


if __name__ == "__main__":
    unittest.main()
