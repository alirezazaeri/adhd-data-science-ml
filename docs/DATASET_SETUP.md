# Dataset setup

This repository does not distribute data. The notebooks use the **WiDS Datathon 2025** competition data, which users must obtain independently from the official provider.

## Official access

1. Sign in to a Kaggle account.
2. Open the [WiDS Datathon 2025 competition](https://www.kaggle.com/competitions/widsdatathon2025/).
3. Review and accept the competition rules.
4. Download the training files from the competition [data page](https://www.kaggle.com/competitions/widsdatathon2025/data), using the updated `TRAIN_NEW` materials where presented.

Dataset access, use, storage, and any downstream sharing remain subject to the official competition and upstream-provider terms. Cite the dataset as **WiDS Datathon 2025**.

## Required local files

Preserve the filenames expected by the notebooks:

```text
data/
├── FUNCTIONAL_CONNECTOME_MATRICES.csv
├── LABELS.xlsx
├── METADATA_A.xlsx
└── METADATA_B.xlsx
```

Place these files in `data/` at the repository root. Do not rename them.

Running the data-preparation notebook creates participant-level files under:

```text
processed_data/
final_data/
```

All participant-level files in these three directories are ignored by Git. Only each directory's public `README.md` and `.gitkeep` placeholder are intended to be tracked.

## Non-redistribution boundary

- This repository provides no data mirror, archive, sample rows, participant extracts, or copied competition files.
- Do not commit or contribute raw, processed, merged, training, or held-out participant data.
- Do not reproduce restricted data-dictionary content in issues, pull requests, documentation, or code comments.
- Users are responsible for confirming that their access, storage, processing, and use comply with the provider's current terms.

The repository's software licence does not grant rights to the competition data or upstream datasets.
