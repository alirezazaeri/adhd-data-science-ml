# Methodology

## Scope

This document describes the retained workflow at aggregate level. It does not change, rerun, or reinterpret the owner-approved notebooks and results.

The task predicts the recorded binary `ADHD_Outcome` label for experimental evaluation. Prediction is not diagnosis, and the workflow has not been clinically or externally validated.

## Data modalities

The WiDS Datathon 2025 competition files used by the workflow contain:

- a functional-connectome matrix with 19,900 upper-triangle connections derived from 200 brain regions;
- recorded outcome labels;
- psychometric and questionnaire measures in Metadata A;
- demographic and collection-context fields in Metadata B.

The complete cohort contains 1,213 participants. Participant-level values are not distributed or reproduced in this repository.

## Participant split

The data-preparation notebook creates an 80/20 participant-level split:

| Split | Participants |
|---|---:|
| Training | 970 |
| Held-out | 243 |

The split uses random state 42 and stratification over the combination of the recorded outcome and binary sex fields. The verified participant-ID sets do not overlap.

## Preprocessing and feature construction

### Metadata A

Missing values in Metadata A are handled with iterative imputation fitted from the training split. Mutual-information feature selection then retains ten psychometric/questionnaire predictors using the training outcome.

### Metadata B

Recorded categorical fields are encoded using the training split, and mutual-information selection retains five Metadata B predictors. In the retained modelling representation, categorical codes are treated numerically rather than one-hot encoded; CatBoost was not supplied explicit categorical-feature metadata.

### Functional connectivity

The 19,900 connectome values are reduced to 30 components using RBF Kernel PCA fitted on the training split and applied to the held-out split.

### Final merge

The selected feature groups are merged by the coded participant identifier:

| Feature group | Retained predictors |
|---|---:|
| Metadata A | 10 |
| Metadata B | 5 |
| Kernel PCA components | 30 |
| **Total** | **45** |

The coded participant identifier, outcome, and binary sex field are removed before model fitting. The sex field is retained separately for the exploratory subgroup comparison.

## Model training and selection

Four classifiers are evaluated:

- Logistic Regression;
- Random Forest;
- Gradient Boosting;
- CatBoost.

Each model uses `GridSearchCV` with five folds and positive-class F1 as the scoring metric. The retained best settings and reported scores remain exactly as saved in the modelling notebook.

## Evaluation and interpretation

The four tuned models are compared on the same 243-participant held-out split using accuracy, positive-class precision, positive-class recall, and positive-class F1. Gradient Boosting has the strongest recorded held-out F1, while CatBoost has the strongest recorded CV F1.

The workflow also retains:

- a confusion matrix and precision-recall curve for Gradient Boosting;
- exploratory performance comparisons across the recorded binary sex groups;
- SHAP feature-attribution output for model interpretation.

SHAP values are model-specific associations, not causal or biological evidence.

## Methodological limitations

### Preprocessing outside CV folds

Imputation, feature selection, encoding, Kernel PCA, and relevant scaling steps were fitted on the complete training split before the internal GridSearchCV folds. They were not refitted independently within every fold. Information from each fold's validation portion can therefore influence the representation used during tuning, making recorded CV scores potentially optimistic.

### Held-out-set reuse

The held-out split was reused for four-model comparison, model choice, subgroup analysis, and SHAP interpretation. It is an experimental held-out set, not an untouched external test set. No nested CV was performed.

### Criterion overlap

Some symptom and questionnaire predictors may overlap conceptually with the recorded outcome criteria. Predictive performance therefore does not establish an independent biomarker or mechanism.

### Proxy and site risks

Demographic, race, site, scan-location, enrolment-year, behavioural, and collection-context variables may encode proxy information or site-specific effects. The retained workflow does not isolate these influences.

### Missing validation layers

No external cohort, independent site, prospective sample, calibration study, confidence intervals, significance tests, or threshold analysis was included. These omissions limit generalisation and prevent clinical, deployment, or fairness claims.

See [Evaluation](EVALUATION.md), [Fairness and bias](FAIRNESS_AND_BIAS.md), and [Responsible use](../RESPONSIBLE_USE.md) for the interpretation boundaries.
