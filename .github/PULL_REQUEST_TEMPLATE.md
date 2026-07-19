## Summary

Describe the public change and why it is needed.

## Validation

List the dataset-free checks performed.

## Safety checklist

- [ ] No participant-level raw, processed, merged, training, or held-out data is included.
- [ ] No copied competition files, sample participant rows, or restricted data-dictionary content is included.
- [ ] No credentials, secret filenames, sensitive screenshots, or personal local paths are included.
- [ ] The preserved notebooks, metadata, execution counts, and outputs are unchanged.
- [ ] Existing retained metrics, subgroup outputs, SHAP outputs, and PNG files are unchanged.
- [ ] Medical, causal, deployment, NHS, GDPR, and fairness claims follow the repository's responsible-use boundaries.
- [ ] Relative Markdown links and GitHub templates were validated.
- [ ] `python scripts/validate_notebook_integrity.py` passes.
- [ ] `python scripts/validate_public_repository.py` passes.
- [ ] `git diff --check` passes.

Do not attach participant records, competition data, credentials, restricted content, or sensitive local information to this pull request.
