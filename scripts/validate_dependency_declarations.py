#!/usr/bin/env python3
"""Verify that tracked notebook imports are declared without executing notebooks."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "requirements.txt"
NOTEBOOKS = (
    ROOT / "notebooks" / "1_data_eploration.ipynb",
    ROOT / "notebooks" / "2_modeling.ipynb",
)
IMPORT_LINE = re.compile(
    r"^\s*(?:from\s+(?P<from_module>[A-Za-z_]\w*)|import\s+(?P<import_module>[A-Za-z_]\w*))",
    re.MULTILINE,
)
REQUIREMENT_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*")
DISTRIBUTION_IMPORTS = {
    "catboost": {"catboost"},
    "ipython": {"IPython"},
    "matplotlib": {"matplotlib"},
    "notebook": {"notebook"},
    "numpy": {"numpy"},
    "openpyxl": {"openpyxl"},
    "pandas": {"pandas"},
    "scikit-learn": {"sklearn"},
    "seaborn": {"seaborn"},
    "shap": {"shap"},
}


def canonical_distribution(name: str) -> str:
    """Normalize a distribution name using Python packaging conventions."""
    return re.sub(r"[-_.]+", "-", name).lower()


def load_requirements(path: Path) -> set[str]:
    """Read declared top-level distributions from a requirements file."""
    requirements: set[str] = set()
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        match = REQUIREMENT_NAME.match(line)
        if match is None:
            raise ValueError(f"Could not parse requirement at {path}:{line_number}")
        requirements.add(canonical_distribution(match.group()))
    return requirements


def extract_notebook_imports(path: Path) -> set[str]:
    """Return top-level import names from code cells without executing the notebook."""
    notebook = json.loads(path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        for match in IMPORT_LINE.finditer(source):
            imports.add(match.group("from_module") or match.group("import_module"))
    return imports


def declared_imports(requirements: set[str]) -> set[str]:
    """Resolve declared distributions to the import names they provide."""
    unknown = sorted(requirements - set(DISTRIBUTION_IMPORTS))
    if unknown:
        raise ValueError(f"Add import-name mappings for requirements: {', '.join(unknown)}")
    return set().union(*(DISTRIBUTION_IMPORTS[name] for name in requirements))


def missing_declarations(imports: set[str], requirements: set[str]) -> set[str]:
    """Return third-party imports not supplied by a declared distribution."""
    third_party = imports - sys.stdlib_module_names
    return third_party - declared_imports(requirements)


def main() -> int:
    try:
        requirements = load_requirements(REQUIREMENTS)
        imports = set().union(*(extract_notebook_imports(path) for path in NOTEBOOKS))
        missing = sorted(missing_declarations(imports, requirements))
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Dependency declaration validation failed: {exc}", file=sys.stderr)
        return 1

    if missing:
        print(
            f"Dependency declaration validation failed; undeclared imports: {', '.join(missing)}",
            file=sys.stderr,
        )
        return 1

    checked = ", ".join(sorted(imports - sys.stdlib_module_names))
    print(f"Dependency declarations cover notebook imports: {checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
