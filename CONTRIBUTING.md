# Contributing

Contributions that improve documentation, validation, accessibility, or reproducibility are welcome when they preserve the repository's data and responsible-use boundaries.

## Never contribute sensitive or restricted material

Do not include or attach:

- raw, processed, merged, training, or held-out participant data;
- sample participant rows or screenshots containing records;
- copied WiDS Datathon 2025 files or restricted data-dictionary content;
- credentials, tokens, private keys, configuration secrets, or local personal paths;
- notebook checkpoints, CatBoost state, model artifacts, archives, or generated exports containing restricted data.

Use synthetic data only when a maintainer has explicitly approved the example and it cannot be mistaken for competition data.

## Notebook preservation

The two tracked notebooks preserve owner-approved historical code, Markdown, metadata, execution counts, and outputs. Do not edit, execute, reformat, rename, clear, or regenerate them without explicit maintainer approval for a separate scientific revision.

Before submitting a change, run:

```bash
python scripts/validate_notebook_integrity.py
python scripts/validate_public_repository.py
git diff --check
```

## Public wording

Describe this work as experimental predictive modelling of a recorded outcome. Do not introduce claims of diagnosis, clinical validity, NHS affiliation, GDPR compliance, treatment value, deployment readiness, causation, fairness certification, or bias elimination.

Keep limitations near performance, subgroup, and interpretability claims. Follow [Responsible use](RESPONSIBLE_USE.md), the [model card](MODEL_CARD.md), and [Fairness and bias](docs/FAIRNESS_AND_BIAS.md).

## Change quality

- Keep commits coherent and limited to one reviewable purpose.
- Explain the reason for the change and its validation in the pull request.
- Check relative Markdown links and GitHub-template syntax.
- Preserve the official dataset links and non-redistribution language.
- Do not change retained metrics or scientific results without explicit maintainer approval and evidence.

## Security and privacy reports

Do not open a public issue containing participant data, credentials, restricted content, or sensitive local paths. Follow [Security](SECURITY.md) for a safe contact route and provide only the minimum non-sensitive information needed to describe the concern.
