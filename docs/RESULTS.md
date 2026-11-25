# Results currently recorded

This page reports what is in the repository. It does not combine separate runs or treat an exploratory result as clinical evidence.

## 1. Archived Paper 1 external sample

The archived manuscript analyzes 2,000 patches from the CAMELYON17-WILDS hospital-2 test split. The sample contains 986 positive and 1,014 negative patches from 9 patients and 10 slides. The decision threshold was 0.50.

| Metric | Recorded estimate | Descriptive 95% patient-cluster interval |
| --- | ---: | ---: |
| ROC-AUC | 0.953 | 0.891–0.968 |
| Accuracy | 0.811 | 0.671–0.883 |
| Sensitivity | 0.958 | 0.867–0.973 |
| Specificity | 0.668 | 0.626–0.715 |
| Balanced accuracy | 0.813 | 0.755–0.838 |
| Precision | 0.737 | 0.290–0.877 |
| F1 | 0.833 | 0.435–0.920 |
| Brier score | 0.155 | 0.095–0.274 |
| Confidence ECE, 10 bins | 0.130 | 0.076–0.241 |

The confusion matrix contains 945 true positives, 677 true negatives, 337 false positives, and 41 false negatives. At this threshold, 33.2% of sampled negative patches were called positive. The high sensitivity therefore came with a substantial false-positive burden.

The pooled result also hides variation between slides. Slide 26 had an AUC of 0.504 and sensitivity of 0.312 on 90 sampled patches, only 16 of which were positive. Slide 28 contributed 810 patches, 40.5% of the full sample. This uneven composition affects the pooled estimate.

The confidence analysis found 378 errors. Of those, 215 (56.9%) had predicted-class confidence of at least 0.90, and 169 (44.7%) were at least 0.95. Mean confidence was 0.941 while accuracy was 0.811. The result is a warning against interpreting the model's raw output as trustworthy confidence.

The intervals resample patients, not individual patches, but they are based on only 9 patient clusters. They are descriptive and can be unstable.

### How to interpret this analysis

This is an exploratory characterization of one existing model on one sampled benchmark cohort. The manuscript documents that test-designated PCam images had previously been used with `model.fit` during development of the older checkpoint. It therefore makes no independent PCam benchmark claim and does not calculate a PCam-to-CAMELYON17 generalization gap.

The 2,000 selected patches were new relative to the 4,000 documented pilot image IDs excluded during sampling. However, the manuscript says earlier image exposure may be incomplete and that the sample shares source patients and slides with pilot work. It is not a historically untouched confirmatory test. Labels came from the pinned dataset source rather than fresh pathologist adjudication.

## 2. Separate CAMELYON17 Run 2 metrics file

The repository also contains `CAMELYON17_External_Test_Run_2_metrics.csv`, which reports a second 2,000-image result:

| Metric | Value in CSV |
| --- | ---: |
| Accuracy | 0.8065 |
| Precision | 0.7299 |
| Sensitivity / recall | 0.9730 |
| Specificity | 0.6400 |
| F1 | 0.8341 |
| ROC-AUC | 0.9557 |
| Brier score | 0.1608 |
| ECE | 0.1333 |

The CSV reports 973 true positives, 640 true negatives, 360 false positives, and 27 false negatives. The repository does not currently provide a matching protocol, sample composition, threshold definition, or uncertainty analysis for this file. It should not be described as a replication of the Paper 1 sample or merged with the table above.

## 3. Separate center-coded WILDS result

The separate `results.json` artifact records an evaluation at threshold 0.1767316 across 241,062 patches, 30 slides, and 24 case groups. It reports centers 0, 1, and 4:

| Center code | Patches | Slides | Case groups | ROC-AUC | Sensitivity | Specificity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 59,436 | 10 | 7 | 0.9138 | 0.7131 | 0.9268 |
| 1 | 34,904 | 10 | 8 | 0.8892 | 0.6595 | 0.9133 |
| 4 | 146,722 | 10 | 9 | 0.8116 | 0.7976 | 0.6203 |
| Pooled, descriptive | 241,062 | 30 | 24 | 0.8405 | 0.7568 | 0.7383 |

The pooled average precision is 0.8575 and the Brier score is 0.1940. The result file describes case-group bootstrap intervals using 2,000 resamples. The intervals are wide in places, especially for center 4, where the AUC interval is 0.550–0.977. These estimates are conditional on this model and the recorded sample; they do not establish performance at new hospitals.

This analysis is not ready to be presented as a fully reproducible final evaluation. The associated November 11 manifest says the model input was scaled to [0, 1], but the run record says [-1, 1]. That conflict needs to be resolved against the actual trainer, checkpoint, and scoring code. The result metadata also says undocumented earlier exposure cannot be ruled out.

## 4. PCam test summary stored separately

The root `summary.json` reports 32,734 PCam test rows, with pooled ROC-AUC 0.8860, sensitivity 0.8983, and specificity 0.6454. It is a separate stored summary, not a substitute for a verified clean benchmark. Its linkage to the checkpoint and preprocessing configuration must be checked alongside the scaling mismatch described above.

## Bottom line

The repository contains useful exploratory results, including a detailed error and confidence analysis. It does not yet support a clean claim of independent validation, clinical accuracy, or readiness for diagnostic use. The next step is to reconcile the model/run records and make each result reproducible from its exact inputs and code.
