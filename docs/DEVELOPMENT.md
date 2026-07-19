# Development workflow

This guide covers repository maintenance that does not require the private local dataset and does not execute the retained notebooks.

## Dataset-free validation environment

The validation scripts and their tests use only the Python standard library. Python 3.12 is recommended to match the recorded notebook metadata and the GitHub Actions environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m unittest discover -s tests -v
```

Installing `requirements.txt` is not necessary for documentation, policy, or validator changes. Those dependencies are needed only for a separately approved scientific environment that reads an independently obtained dataset.

## Required local checks

Run the checks from the repository root in this order:

```bash
git diff --check
python -m py_compile scripts/*.py tests/*.py
python -m unittest discover -s tests -v
python scripts/validate_notebook_integrity.py
python scripts/validate_dependency_declarations.py
python scripts/validate_public_repository.py
```

The dependency declaration check reads notebook JSON and import statements without importing scientific packages or executing cells.

## Notebook immutability review

Repository maintenance must leave the retained notebooks byte-for-byte unchanged. Before committing, confirm:

```bash
git diff --exit-code -- notebooks/
git status --short
```

If a notebook appears in the diff, stop. Do not clear outputs, normalize metadata, update execution counts, or rerun cells as part of a maintenance change.

## Review scope

Keep each commit focused and verify that its changed paths match its purpose. In particular:

- documentation changes must preserve recorded metrics and scientific limitations;
- validation changes must include a regression test for the behavior being changed;
- dependency changes must keep notebook imports and `requirements.txt` aligned;
- workflow changes must retain read-only permissions and dataset-free execution;
- no validation command may generate tracked reports, caches, data, figures, or model artifacts.

## Failure handling

Treat a failed safety check as evidence to investigate, not as a reason to remove or broadly bypass the check. Record the exact file and rule, add a minimal regression case, and preserve checks that protect private data and immutable scientific artifacts.
