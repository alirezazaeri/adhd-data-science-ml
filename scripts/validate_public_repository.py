#!/usr/bin/env python3
"""Run dataset-free checks for the public repository tree."""

from __future__ import annotations

import fnmatch
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
DATA_DIRECTORIES = ("data", "processed_data", "final_data")
ALLOWED_DATA_FILES = {
    f"{directory}/{filename}"
    for directory in DATA_DIRECTORIES
    for filename in (".gitkeep", "README.md")
}
FORBIDDEN_DATA_SUFFIXES = {
    ".csv",
    ".feather",
    ".parquet",
    ".sav",
    ".tsv",
    ".xls",
    ".xlsx",
}
FORBIDDEN_ARTIFACT_SUFFIXES = {
    ".7z",
    ".cbm",
    ".h5",
    ".joblib",
    ".onnx",
    ".p12",
    ".pem",
    ".pfx",
    ".pickle",
    ".pkl",
    ".pt",
    ".tar",
    ".zip",
}
SECRET_FILENAMES = {
    ".env",
    "credentials.json",
    "kaggle.json",
    "secrets.json",
}
INTERNAL_REPORT_PATTERNS = (
    "*audit-report*.md",
    "*cleanup-report*.md",
    "*publishing-report*.md",
    "*readiness-audit*.md",
    "*security-report*.md",
    "*task-report*.md",
    "*validation-report*.md",
)
PRIVATE_PATH_MARKERS = (
    re.compile(r"/Users/[^/\s]+/"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
)
PROCESS_MARKERS = (
    "academic project",
    "future repository",
    "private preparation",
    "repository preparation",
    "student project",
)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\((?P<target>[^)]+)\)")
REQUIREMENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*(?:\[[A-Za-z0-9_,.-]+\])?(?:\s*[<>=!~].*)?$")


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def check_tracked_boundaries(files: list[str]) -> list[str]:
    errors: list[str] = []
    for relative in files:
        path = Path(relative)
        lower_name = path.name.lower()
        suffix = path.suffix.lower()

        if path.parts and path.parts[0] in DATA_DIRECTORIES and relative not in ALLOWED_DATA_FILES:
            errors.append(f"Unexpected tracked data-directory file: {relative}")
        if suffix in FORBIDDEN_DATA_SUFFIXES:
            errors.append(f"Forbidden tracked dataset format: {relative}")
        if suffix in FORBIDDEN_ARTIFACT_SUFFIXES or relative.endswith((".tar.gz", ".service-account.json")):
            errors.append(f"Forbidden tracked artifact format: {relative}")
        if lower_name in SECRET_FILENAMES or lower_name.endswith("service-account.json"):
            errors.append(f"Forbidden tracked credential filename: {relative}")
        if any(fnmatch.fnmatch(lower_name, pattern) for pattern in INTERNAL_REPORT_PATTERNS):
            errors.append(f"Forbidden tracked internal-report filename: {relative}")
        if relative.startswith(("docs/reports/", "reports/private/", "private_reports/")):
            errors.append(f"Forbidden tracked internal-report path: {relative}")
        if ".ipynb_checkpoints" in path.parts or "catboost_info" in path.parts:
            errors.append(f"Forbidden tracked generated state: {relative}")
    return errors


def clean_link_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    target = target.split(maxsplit=1)[0]
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    return target or None


def check_markdown(files: list[str]) -> list[str]:
    errors: list[str] = []
    for relative in files:
        if not relative.lower().endswith(".md"):
            continue
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()

        for marker in PROCESS_MARKERS:
            if marker in lowered:
                errors.append(f"Private or academic workflow wording in: {relative}")
        for pattern in PRIVATE_PATH_MARKERS:
            if pattern.search(text):
                errors.append(f"Personal absolute path in: {relative}")

        for match in MARKDOWN_LINK.finditer(text):
            target = clean_link_target(match.group("target"))
            if target is None:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"Relative link escapes repository in {relative}: {target}")
                continue
            if not resolved.exists():
                errors.append(f"Broken relative link in {relative}: {target}")
    return errors


def check_requirements(files: list[str]) -> list[str]:
    errors: list[str] = []
    for relative in files:
        if not fnmatch.fnmatch(Path(relative).name, "requirements*.txt"):
            continue
        for line_number, raw_line in enumerate((ROOT / relative).read_text(encoding="utf-8").splitlines(), 1):
            line = raw_line.split("#", 1)[0].strip()
            if line and not REQUIREMENT.fullmatch(line):
                errors.append(f"Unsupported requirement syntax: {relative}:{line_number}")
    return errors


def main() -> int:
    try:
        files = tracked_files()
        errors = [
            *check_tracked_boundaries(files),
            *check_markdown(files),
            *check_requirements(files),
        ]
    except (OSError, UnicodeError, subprocess.SubprocessError) as exc:
        print(f"Repository validation could not complete: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in sorted(set(errors)):
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Public repository validation passed for {len(files)} tracked files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
