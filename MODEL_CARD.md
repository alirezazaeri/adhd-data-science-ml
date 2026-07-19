# Model card

## Model details

This repository retains an experimental comparison of four binary classifiers:

- Logistic Regression;
- Random Forest;
- Gradient Boosting;
- CatBoost.

The intended technical task is prediction of the recorded binary `ADHD_Outcome` label for experimental evaluation. The work is not a diagnostic model, clinical tool, screening system, or healthcare-ready system.

## Data

The workflow uses **WiDS Datathon 2025** data obtained from the official [Kaggle competition](https://www.kaggle.com/competitions/widsdatathon2025/). The complete labeled cohort contains 1,213 participants:

| Aggregate | Value |
|---|---:|
| Class 0 | 382 |
| Class 1 | 831 |
| Training split | 970 |
| Experimental held-out split | 243 |
| Final predictors | 45 |

The participant-level dataset is not distributed. Access and use remain subject to the competition and upstream-provider terms.

## Inputs and preprocessing

The 45 fitted predictors combine:

- 10 imputed and mutual-information-selected Metadata A features;
- 5 encoded and mutual-information-selected Metadata B features;
- 30 RBF Kernel PCA components derived from 19,900 connectome features.

The coded participant identifier, outcome, and recorded binary sex field are excluded from model fitting. The sex field is retained separately for exploratory subgroup evaluation.

## Training and validation design

The participant-level split uses random state 42 and outcome-by-recorded-sex stratification. All four models are tuned with five-fold `GridSearchCV` scored by positive-class F1, then evaluated on the same 243-participant held-out split.

Preprocessing, feature selection, Kernel PCA, and relevant scaling were fitted on the complete training split before the GridSearchCV folds rather than independently inside each fold. Recorded CV scores may therefore be optimistic.

The held-out split was reused for four-model comparison, model choice, subgroup analysis, and SHAP interpretation. It is not an untouched external test set.

## Retained performance

These values are preserved from the approved modelling notebook and were not recalculated:

| Model | CV F1 | Held-out accuracy | Held-out precision | Held-out recall | Held-out F1 |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8513 | 0.802 | 0.805 | 0.940 | 0.867 |
| Random Forest | 0.8494 | 0.807 | 0.803 | 0.952 | 0.871 |
| Gradient Boosting | 0.8514 | 0.815 | 0.808 | 0.958 | 0.877 |
| CatBoost | 0.8532 | 0.811 | 0.807 | 0.952 | 0.874 |

Gradient Boosting has the strongest recorded held-out F1 (0.877). CatBoost has the strongest recorded CV F1 (0.8532). The differences are narrow and were not tested for statistical significance.

## Limitations

- Class 1 is the majority class; class-0 recall is substantially weaker than class-1 recall.
- Optimization focused on positive-class F1.
- No confidence intervals, formal model-comparison tests, calibration, threshold analysis, or decision-curve analysis were performed.
- No nested CV, external cohort, independent site, prospective, or clinical validation was performed.
- The binary-sex subgroup analysis is exploratory, uses unequal groups, and lacks uncertainty estimates or formal fairness criteria.
- Questionnaire and symptom features may overlap the outcome criteria.
- Demographic, race, site, scan-location, enrolment-year, and collection-context variables may act as proxies or encode confounding.
- SHAP output is model-specific association, not causal, biological, or clinical evidence.

## Intended uses

- Review of an historical experimental data-science workflow.
- Technical review of multimodal preprocessing, classifier comparison, evaluation limitations, and responsible machine-learning documentation.
- Reproducibility investigation by users who independently obtain authorised dataset access.

## Prohibited uses

Do not use the models or results for diagnosis, screening, treatment, clinical triage, insurance, education access, employment, benefits, or any decision about an identifiable person. Do not represent the models as clinically valid, fair, unbiased, diagnostic, deployable, healthcare-ready, causally explanatory, NHS-affiliated, or GDPR-compliant.

## Fairness statement

The recorded subgroup work is not fairness certification and does not establish bias elimination. See [Fairness and bias](docs/FAIRNESS_AND_BIAS.md).

## Data and licence boundaries

The repository's MIT licence applies only to original public code and documentation. It does not license WiDS Datathon 2025 data, upstream datasets, participant-level raw/processed/final files, restricted data-dictionary content, third-party dependencies, or external trademarks.

See [Dataset setup](docs/DATASET_SETUP.md) and [Responsible use](RESPONSIBLE_USE.md).
