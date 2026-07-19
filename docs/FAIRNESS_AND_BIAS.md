# Fairness and bias

## Exploratory scope

The retained fairness-related work is an exploratory comparison of model performance across the dataset's recorded binary sex field. It is not a comprehensive fairness assessment, certification, or demonstration that bias has been removed.

The 243-participant held-out split contains 160 participants in one recorded sex group and 83 in the other. Class-specific subgroup sizes are smaller: class 0 contains 43 and 33 participants, while class 1 contains 117 and 50. Unequal and small subgroup sizes make point estimates unstable and limit comparison.

## What was evaluated

The notebook records subgroup classification reports and class-specific precision, recall, and F1 comparisons for Logistic Regression, Random Forest, Gradient Boosting, and CatBoost. These are descriptive results from the reused held-out split.

The class-0 comparisons show an important weakness: recall for class 0 is low across the recorded models and groups. Strong class-1 recall or overall F1 does not resolve that error pattern.

## What was not evaluated

The retained workflow does not include:

- confidence intervals or statistical tests for subgroup differences;
- equalized-odds or equal-opportunity analysis;
- demographic-parity analysis;
- subgroup calibration or calibration-parity analysis;
- threshold sensitivity by subgroup;
- intersectional analysis;
- comprehensive race, ethnicity, age, site, or socioeconomic evaluation;
- external replication of subgroup findings.

The held-out set was also used for model comparison and interpretation, so it is not an independent fairness-validation cohort.

## Sources of potential bias

- **Representation:** the recorded groups and outcome classes are unequal in size.
- **Measurement:** questionnaire and symptom variables may overlap the outcome construct or reflect differential measurement.
- **Proxy features:** demographic, race, site, scan-location, enrolment-year, behavioural, and collection-context variables may encode protected or structural information indirectly.
- **Site and acquisition effects:** collection and imaging differences may be mistaken for generalisable patterns.
- **Model selection:** positive-class F1 was the tuning target, which does not directly protect class-0 or subgroup performance.
- **Evaluation reuse:** using one held-out split for several analytical purposes increases the risk of overinterpreting observed differences.

## Interpretation boundary

Do not label any evaluated model as the "fairest" model. Do not claim equal performance, bias elimination, universal fairness, or suitability for decisions about individuals. The subgroup results are descriptive signals that motivate better evaluation with larger samples, prespecified fairness criteria, uncertainty estimates, intersectional analysis, calibration, and external validation.

See [Responsible use](../RESPONSIBLE_USE.md) for prohibited high-stakes uses.
