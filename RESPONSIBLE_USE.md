# Responsible use

## Status

This repository documents **experimental predictive modelling of a recorded binary outcome**. It does not diagnose ADHD and is not a clinical tool, medical device, screening system, or healthcare decision-support system. The work has not been clinically validated and has no documented NHS affiliation.

The project does not provide medical advice, treatment guidance, or a substitute for assessment by a qualified clinician. It does not establish GDPR compliance or approval under any healthcare, data-protection, or medical-device framework.

## Prohibited uses

Do not use this project or its recorded results for:

- diagnosis, screening, triage, treatment, or clinical risk assessment;
- insurance, education access, employment, benefits, or eligibility decisions;
- decisions about an identifiable person;
- automated or human-in-the-loop high-stakes decisions;
- claims that a biological, demographic, behavioural, or imaging feature causes ADHD;
- claims that a model is fair, unbiased, clinically valid, deployable, or suitable for healthcare.

## Evidence boundaries

The recorded results are conditional on one dataset, one participant split, the retained preprocessing choices, and the historical evaluation design.

- **Class imbalance and errors:** class 1 is the majority class. Positive-class recall is high, while class-0 recall is substantially weaker. Aggregate F1 can obscure this error asymmetry.
- **Validation design:** preprocessing and feature selection were completed before the internal GridSearchCV folds. The recorded CV scores may therefore be optimistic.
- **Held-out reuse:** the same held-out split was used for comparison of four tuned models, model selection, subgroup evaluation, and interpretation. It is not an untouched external test set.
- **No clinical or external validation:** no independent clinical, site-held-out, prospective, or external cohort validation was performed.
- **No calibration or threshold study:** probability calibration, decision-curve analysis, and threshold selection were not part of the retained workflow.

## Fairness and subgroup limitations

The recorded binary-sex subgroup comparisons are exploratory. The subgroup sizes are unequal, class-specific groups are smaller, and no confidence intervals or significance tests were calculated. Equalized odds, demographic parity, calibration parity, intersectional analysis, and broad race or site evaluation were not performed.

These comparisons are not fairness certification and do not establish that bias is absent. Demographic, collection-site, scan-location, enrolment-year, behavioural, and questionnaire variables may encode proxy information or reflect structural differences in data collection.

## Interpretation limitations

- Symptom and questionnaire predictors may overlap conceptually with the recorded outcome criteria, which can inflate apparent predictive usefulness without demonstrating an independent marker.
- SHAP values describe how the fitted model assigned contributions within the recorded feature representation. They do not establish biological importance, clinical mechanism, or causation.
- Site and acquisition differences may limit generalisation beyond the recorded dataset.
- Model associations should not be interpreted as stable properties of individuals or populations.

## Immutable historical notebooks

The notebooks preserve their owner-approved historical state. Any stronger wording retained inside them is historical experimental narrative. It must not be interpreted as evidence of diagnosis, clinical usefulness, NHS affiliation, deployment readiness, regulatory or GDPR compliance, treatment value, fairness certification, or bias elimination.

Use the narrower boundaries in this document, the [model card](MODEL_CARD.md), and the [fairness and bias statement](docs/FAIRNESS_AND_BIAS.md) when interpreting the repository.
