# Reproducibility

## Historical environment

Notebook metadata records Python 3.12.7. The exact installed versions of the project dependencies were not preserved, so `requirements.txt` is intentionally an unpinned human-readable dependency list rather than a verified environment lock.

Do not treat a successful installation from that file as proof of byte-for-byte or metric-for-metric reproducibility. A future lock or constraints file should be generated only after the notebooks have been validated in a clean, approved environment; versions must not be guessed from current releases.

## Required local setup

1. Obtain WiDS Datathon 2025 from the official Kaggle competition and accept the provider terms.
2. Place the four required files under `data/` as described in [Dataset setup](DATASET_SETUP.md).
3. Create a compatible Python environment and install `requirements.txt`.
4. Launch Jupyter with `notebooks/` as the working directory so the recorded relative paths `../data/`, `../processed_data/`, and `../final_data/` resolve correctly.

Participant-level files remain local and ignored throughout the workflow.

## Notebook order

1. `notebooks/1_data_eploration.ipynb` prepares the processed and merged local data.
2. `notebooks/2_modeling.ipynb` fits, tunes, evaluates, and interprets the four classifiers.

The filename `1_data_eploration.ipynb` is intentionally preserved because renaming would change the approved historical notebook state.

## Randomness and saved state

- Random state 42 is used where recorded for the participant split and several model-related operations.
- At least one exploratory plotting sample is unseeded, so that display may differ between executions.
- Execution counts are preserved in their historical, non-sequential order; they are not evidence that a fresh top-to-bottom run was completed in the published state.
- No fitted model artifacts are included. Reproducing fitted estimators requires full local retraining.
- Existing notebook outputs are historical retained results, not outputs regenerated during publication preparation.

## Integrity checks

The approved notebook hashes are published in [Notebook integrity](NOTEBOOK_INTEGRITY.md). The notebooks must remain byte-for-byte unchanged unless a maintainer explicitly approves a separate scientific revision.

JSON and hash validation do not execute cells and do not establish that current package releases reproduce the retained outputs.

## Known reproducibility limits

- Exact dependency versions and a verified environment lock are unavailable.
- The restricted dataset is not redistributed and must be obtained independently.
- No trained model files are saved.
- The notebooks contain historical execution-count disorder.
- Preprocessing and feature selection occur before the internal GridSearchCV folds, so a rerun preserves a known CV-design limitation rather than producing leakage-isolated validation.
- Hardware, low-level numerical libraries, and current dependency behaviour may affect a fresh run.

Reproduction is therefore best understood as rerunning the documented experimental workflow under compatible conditions, not as a guarantee of identical outputs.
