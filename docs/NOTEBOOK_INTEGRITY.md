# Notebook integrity

The two notebooks preserve an owner-approved historical state, including their code, Markdown, metadata, execution counts, and retained outputs. These SHA-256 hashes provide a byte-level integrity check:

| Notebook | SHA-256 |
|---|---|
| `notebooks/1_data_eploration.ipynb` | `ae2eb113d9d8a0d58f78f48509483112827dcedef0962e66a27d08d8965414c1` |
| `notebooks/2_modeling.ipynb` | `096963a93264f9b19e1ea9e282e8ff5b7e037cf40fd709333470234a7090df25` |

Validate the files without executing them:

```bash
python scripts/validate_notebook_integrity.py
```

The check confirms valid JSON and exact byte hashes. It does not execute cells, verify current dependency compatibility, or independently validate the scientific results.

Any hash mismatch requires maintainer review. Do not normalize, reformat, repair, clear, or replace a notebook to make the check pass.
