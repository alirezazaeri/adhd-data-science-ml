# Evaluation

## Retained model results

The values below are transcribed from the owner-approved modelling notebook. They were not recalculated. `CV F1` is the best positive-class F1 recorded by five-fold `GridSearchCV`; the remaining columns are positive-class metrics on the 243-participant experimental held-out split.

| Model | CV F1 | Held-out accuracy | Held-out precision | Held-out recall | Held-out F1 |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8513 | 0.802 | 0.805 | 0.940 | 0.867 |
| Random Forest | 0.8494 | 0.807 | 0.803 | 0.952 | 0.871 |
| Gradient Boosting | 0.8514 | 0.815 | 0.808 | 0.958 | 0.877 |
| CatBoost | 0.8532 | 0.811 | 0.807 | 0.952 | 0.874 |

Gradient Boosting has the strongest recorded held-out F1 (0.877). CatBoost has the strongest recorded CV F1 (0.8532). The differences are narrow and were not accompanied by confidence intervals or statistical significance tests, so the table does not establish a meaningful performance separation beyond the recorded split.

## Error interpretation

The complete cohort contains 382 class-0 and 831 class-1 participants. The held-out split contains 76 class-0 and 167 class-1 participants. Optimization used positive-class F1, and all four models record high class-1 recall. Class-0 recall is substantially lower in the retained classification outputs.

Accuracy and positive-class F1 should therefore not be read as balanced performance across both classes. The recorded Gradient Boosting confusion matrix provides the most direct aggregate view of this asymmetry.

## Validation boundaries

- Preprocessing and feature construction were completed on the full training split before the internal CV folds. Recorded CV values may be optimistic.
- The held-out split was used for evaluation of all four tuned models, comparison, subgroup analysis, and interpretation. It is not an untouched external test set.
- No nested cross-validation, external validation, independent site validation, or prospective evaluation was performed.
- No confidence intervals, significance tests, balanced-accuracy comparison, Matthews correlation coefficient analysis, or formal model-ranking uncertainty was reported.
- No probability-calibration, calibration-parity, threshold-selection, or decision-curve analysis was performed.

These results support description of a retained experiment only. They do not support diagnosis, clinical use, healthcare deployment, fairness certification, or performance claims beyond the recorded data and design.
