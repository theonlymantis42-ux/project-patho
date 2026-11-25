# External performance and confidence calibration of a MobileNetV2 histopathology classifier on CAMELYON17 patches

## Abstract

**Purpose.** To characterize discrimination, threshold-dependent errors, calibration, and variation across patients and slides when an existing Project Patho classifier is applied to additional CAMELYON17-WILDS patches.

**Methods.** We evaluated one saved MobileNetV2-based model on 2,000 patches sampled reproducibly from the hospital-2 test split of a version-pinned CAMELYON17-WILDS mirror after excluding 4,000 documented pilot image IDs. Selection used a deterministic hash priority without class balancing. Images were scaled to [0,1], the decision threshold was fixed at 0.50, and weights were not updated. Uncertainty was estimated using 2,000 patient-cluster bootstrap replicates.

**Results.** The sample contained 986 positive and 1,014 negative patches from 9 patients and 10 slides. ROC-AUC was 0.953 (patient-cluster percentile interval, 0.891–0.968). Accuracy was 81.1%, sensitivity 95.8%, and specificity 66.8%. There were 337 false positives and 41 false negatives. Brier score was 0.155 and predicted-class confidence ECE was 0.130. Among 378 errors, 215 had confidence at least 0.90. Performance differed by slide; slide 26 had AUC 0.504 and sensitivity 31.3%, based on 16 positive patches.

**Interpretation.** In this exploratory sample, strong pooled discrimination coexisted with a substantial false-positive burden, high-confidence errors, and heterogeneous slide performance. These findings motivate further evaluation but do not establish a cross-dataset performance decrease, clinical readiness, or biological explanation of errors.

## 1 Introduction

PatchCamelyon (PCam) provides a tractable binary classification benchmark based on 96×96 histopathology patches [1]. CAMELYON17-WILDS offers a hospital-based setting for examining model behavior on a different benchmark source [2,5]. External assessment is relevant because classification performance can vary when data distributions differ, although identifying the cause of any difference requires more than an external result alone [5].

Discrimination, threshold-dependent classification, and probability calibration address different questions. A model may rank positive patches above negative patches while still producing many false positives at a particular threshold. Confidence calibration concerns whether stated confidence agrees with empirical correctness [6]. In histopathology, patches also occur within slides and patients, so a large patch count should not be mistaken for an equally large number of independent observations.

This study characterizes external discrimination, calibration, and patient- and slide-associated variation for one existing Project Patho model. We evaluated a reproducibly selected sample after removing documented pilot image IDs, retained the patient and slide hierarchy, and quantified confidence on errors. The study is explicitly exploratory. PCam test-designated images had been used for optimization during model development; consequently, this study makes no independent internal benchmark or internal-to-external performance-gap claim.

## 2 Materials and methods

### 2.1 Study design and provenance

This retrospective computational study evaluated one existing saved model. No training, fine-tuning, threshold optimization, or calibration fitting was performed during the reported external evaluation. The investigator reports developing the model using serial sets of approximately 10,000 PCam images, with nominal 8,000/2,000 partitions, and processing approximately 220,000 training-designated images. The investigator subsequently confirmed that approximately 30,000 test-designated images were also passed to model.fit, updating model parameters. These counts are investigator-reported approximations, not a reconstructed unique-image inventory. The exact sequence of sample use, total optimization epochs, and any overlap across successive batches could not be independently established from the retained notebook.

Accordingly, the PCam test-designated images are considered optimization data for this model. Previous PCam results are not used as independent testing evidence, and no generalization gap is calculated. The source model was my_cancer_model.h5; its SHA-256 digest is recorded in analysis_manifest.json. This disclosure distinguishes the reported development history from the file-verified architecture and the reproducible external inference run.

Earlier runs and their outputs were archived without modification. A source-metadata audit matched all 4,000 documented pilot image IDs and their hospital, patient, and slide fields. The first balanced pilot archive contained 506 label rows inconsistent with the current pinned mirror and 1,494 unique image IDs among 2,000 rows; conflicting saved labels were associated with identical pixel hashes. These observations concern that archive, not newly acquired labels. Its metrics are excluded from the present estimates. The supplied preprocessing code appears to reconstruct the workflow but does not establish which historical operation caused the discrepancy.

### 2.2 External source and sampling

Data were streamed from wltjr1007/Camelyon17-WILDS, test split, revision d784d5344ba6c967f83f9f3d9b2f1e2a4d6eb78f. The official WILDS implementation defines center 2 as the test hospital, and its binary patch task uses tumor in the central 32×32 region of a 96×96 image [2]. This run retained labels and hierarchy fields from the pinned mirror rather than independently relabeling histology.

After removing the union of 4,000 documented pilot image IDs, 81,054 metadata rows were eligible. Each eligible image ID received a SHA-256 priority from the exact string 20261024: followed by its decimal image ID; the 2,000 lowest priorities were selected. No class quotas, slide quotas, or outcome-based acceptance rules were applied. Selection covered the eligible benchmark pool, not the first 2,000 records in stream order. Sample composition reflects this benchmark and exclusion rule; it is not an estimate of clinical disease prevalence.

All selected IDs were unique and disjoint from the documented exclusion set. However, the researcher could not verify whether other images had previously been inspected. The sample is therefore new relative to documented archives, not certified historically untouched. Patch-level exclusions also do not create disjoint patients or slides from pilot development.

### 2.3 Model and inference

The saved model contains a frozen MobileNetV2 backbone [7], global average pooling, a 64-unit rectified-linear dense layer, and a one-unit sigmoid output. The model was loaded with compilation disabled for inference. RGB arrays were checked for shape 96×96×3, converted from uint8 to float32, and divided by 255.0. Prediction batch size was 32. A patch was predicted positive when cancer probability was at least 0.50. The model file hash was checked before and after inference and did not change.

No new ImageNet initialization or PCam retraining was conducted in this run. The recovered commented five-epoch training call is historical reference code, not proof of the actual training history.

### 2.4 Outcomes and calibration definitions

ROC-AUC summarizes pooled patch discrimination. Threshold-dependent outcomes include accuracy, sensitivity, specificity, balanced accuracy, precision, F1, and confusion-matrix counts. Brier score is the mean squared difference between positive-class probability and binary reference label.

For confidence ECE, predicted-class confidence was max(p, 1−p), correctness was the indicator that the thresholded prediction matched the label, and the interval [0,1] was partitioned into ten uniform bins. ECE was the bin-frequency-weighted absolute difference between mean confidence and empirical accuracy. The final bin included 1.0; other bins were left-closed and right-open. Separately, the reliability curve plots mean positive-class probability against observed positive fraction in ten uniform probability bins. These are distinct summaries and are labeled accordingly. Empty bins were omitted from plotted averages. Confidence levels 0.90 and 0.95 were used for descriptive error counts after inference, not model selection.

### 2.5 Hierarchy and uncertainty

Predictions retained image, hospital, patient, and slide identifiers. Patient- and slide-specific summaries were calculated from patches within each group; they are not patient-level diagnoses. ROC-AUC and sensitivity were undefined for groups without positive patches; analogous denominator rules were applied to other metrics.

We resampled the 9 observed patients with replacement 2,000 times using random seed 20261024. Every occurrence of a sampled patient contributed all of that patient's sampled slides and patches, preserving within-patient clustering. Metrics were recalculated for each replicate. The 2.5th and 97.5th percentiles form descriptive patient-cluster bootstrap intervals. All 2,000 replicates yielded defined values for the reported pooled metrics. These intervals are conditional on this model, hospital, and sample; with only 9 clusters, their coverage and stability require caution. They do not measure training-seed variability or generalization to new hospitals.

Leave-one-patient-out summaries were also calculated as a descriptive influence analysis. Omitting a patient does not retrain the model or alter its threshold. All analysis choices in this section beyond the recorded sampling/inference plan were made during exploratory analysis, not prospectively preregistered.

### 2.6 Software and reproducibility

The inference and analysis environment used TensorFlow 2.21.0, NumPy 2.1.3, pandas 2.2.3, scikit-learn 1.6.1, datasets 4.8.5, and Matplotlib 3.10.0. The saved package includes the prediction table, selected image IDs and reference labels, source revision, model and prediction hashes, analysis tables, bootstrap replicates, and figure exports. The sample size of 2,000 was chosen for a practical exploratory run; no prospective precision or power calculation was performed. The selection and inference settings were recorded before inference. Subgroup, uncertainty, and failure analyses were specified after the predictions were available, without changing the model or decision threshold. Reporting was informed by CLAIM 2024 [4].

## 3 Results

### 3.1 Cohort and pooled performance

The 2,000-patch cohort comprised 986 positive patches (49.3%) and 1,014 negative patches (50.7%) from 9 patients and 10 slides. The confusion matrix contained 945 true positives, 677 true negatives, 337 false positives, and 41 false negatives. Of negative patches, 33.2% were classified positive; of positive patches, 4.2% were classified negative.

**Table 1. Pooled patch metrics and descriptive 95% patient-cluster bootstrap intervals.** Rates are shown on a 0–1 scale. Intervals should not be interpreted as evidence of clinical performance.

| metric | estimate | ci_low | ci_high |
| --- | --- | --- | --- |
| roc_auc | 0.953 | 0.891 | 0.968 |
| accuracy | 0.811 | 0.671 | 0.883 |
| sensitivity | 0.958 | 0.867 | 0.973 |
| specificity | 0.668 | 0.626 | 0.715 |
| balanced_accuracy | 0.813 | 0.755 | 0.838 |
| precision | 0.737 | 0.290 | 0.877 |
| f1 | 0.833 | 0.435 | 0.920 |
| brier | 0.155 | 0.095 | 0.274 |
| confidence_ece_10_bins | 0.130 | 0.076 | 0.241 |

### 3.2 Slide composition and performance variation

Slide 28 contributed 810 patches, including 680 positive patches: 40.5% of the entire sample and 69.0% of positive patches. Pooled metrics therefore place substantial weight on this slide. Slide 26 had 90 patches, including 16 positives; its AUC was 0.504, sensitivity 0.313, and specificity 0.581. This is evidence of heterogeneous patch-level performance in the observed sample, not proof of a staining mechanism or patient characteristic causing failure. Slide 24 contained only 2 positive patches; its sensitivity estimate of 0.50 is especially unstable. Slides 20 and 21 contained no sampled positives, so their AUC and sensitivity are reported as undefined.

**Table 2. Per-slide sample composition and performance.** NA denotes an undefined metric. Small positive denominators must be considered when comparing slides.

| slide | n | positive | negative | roc_auc | sensitivity | specificity | accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 20 | 81 | 0 | 81 | NA | NA | 0.667 | 0.667 |
| 21 | 88 | 0 | 88 | NA | NA | 0.625 | 0.625 |
| 22 | 116 | 50 | 66 | 0.991 | 1.000 | 0.758 | 0.862 |
| 23 | 134 | 64 | 70 | 0.958 | 0.953 | 0.686 | 0.813 |
| 24 | 167 | 2 | 165 | 0.742 | 0.500 | 0.648 | 0.647 |
| 25 | 116 | 28 | 88 | 0.991 | 1.000 | 0.693 | 0.767 |
| 26 | 90 | 16 | 74 | 0.504 | 0.312 | 0.581 | 0.533 |
| 27 | 114 | 4 | 110 | 0.960 | 1.000 | 0.545 | 0.561 |
| 28 | 810 | 680 | 130 | 0.969 | 0.972 | 0.677 | 0.925 |
| 29 | 284 | 142 | 142 | 0.946 | 0.951 | 0.782 | 0.866 |

### 3.3 Calibration and confident errors

Mean predicted-class confidence was 0.941, compared with empirical accuracy of 0.811. Confidence averaged 0.958 on correct predictions and 0.866 on incorrect predictions. Of 378 errors, 215 (56.9%) had confidence at least 0.90 and 169 (44.7%) had confidence at least 0.95. Brier score was 0.155 and confidence ECE was 0.130. Together, these summaries show that high confidence did not reliably identify correct predictions in this sample. No internal calibration comparison was performed, so worsening under domain shift is not established.

### 3.4 Patient influence

When each observed patient was omitted in turn, pooled AUC ranged from 0.920 to 0.959 and accuracy from 0.734 to 0.828. These analyses describe sensitivity to patient composition rather than independent replication. Full values are provided in leave_one_patient_out.csv.

## 4 Discussion

The external results reveal distinct limitations of pooled discrimination, operating-point behavior, and confidence. Their interpretation depends on the patient and slide composition of the benchmark sample.

### 4.1 Interpretation of discrimination and errors

The model separated positive from negative patches well in the pooled sample, but its fixed operating point classified approximately one-third of reference-negative patches as positive. This combination is not contradictory: ROC-AUC evaluates ranking across thresholds, whereas specificity describes one selected threshold. The present study characterizes this operating point without optimizing it on external outcomes. The positive predictive value is also tied to the benchmark sample composition and should not be transferred directly to a clinical population.

High-confidence errors provide a second, distinct result. Confidence averaged 0.866 among incorrect predictions, and more than half of errors exceeded 0.90 confidence. These descriptive findings support measuring calibration and failure behavior alongside discrimination. They do not show that calibration worsened relative to PCam, since an independent internal comparator was unavailable. Temperature scaling, threshold selection, and adaptation were not performed; their benefits cannot be inferred from this study.

### 4.2 Patient and slide composition

The unequal distribution of positive patches is important to interpretation. Slide 28 supplied 69.0% of positive patches, and omitting its patient reduced pooled AUC to 0.920. In contrast, slide 26 showed weak discrimination and sensitivity. Such differences show that the pooled result does not describe every slide equally well. They do not establish whether staining, tissue morphology, artifact, or annotation uncertainty caused the variation. Patient- and slide-specific rates remain patch-level estimates, not patient diagnoses.

### 4.3 Limitations

The study evaluated one existing model at one benchmark hospital using 9 patients and 10 slides. Patient-cluster intervals account for within-patient patch dependence in resampling but are based on few clusters; their precision and coverage should be treated cautiously. They are conditional on the observed model and sample and do not capture independent-training-seed or new-hospital variability. The exploratory confidence intervals are descriptive; no multiplicity-adjusted subgroup hypothesis tests or claims of subgroup superiority were made. Several slides have very few positives, making their sensitivity and AUC estimates unstable.

The investigator-confirmed optimization on PCam test-designated images precludes treating earlier PCam testing as an independent internal benchmark. Exact historical training identities and optimization chronology were not fully recoverable. The external sample excludes all 4,000 documented pilot IDs, but completeness of earlier image exposure remains uncertain. It shares source patients and slides with pilot work, and it must not be described as an entirely untouched confirmatory test. Prior pilot results were available during model development, so the external hospital cannot be represented as historically unseen at the study-design level.

The source mirror was version-pinned, and saved pilot metadata were checked against it. Nevertheless, full image-by-image equivalence between the mirror and the original WILDS release has not been independently certified. The saved first balanced pilot archive contains confirmed source-label inconsistencies and duplicates; its results were excluded, and the cause was not established. Source labels were used as the reference standard for the present sample, without new pathological adjudication. Thus, label validity and possible artifacts cannot be independently assessed here.

The sampled benchmark distribution does not represent clinical prevalence, and image-patch classification does not constitute whole-slide staging, patient diagnosis, or a clinical workflow assessment. The study includes no prospective evaluation, clinical comparator, pathologist error adjudication, or evidence of clinical utility. No saliency-based biological interpretation is claimed. These limitations define the scope of the findings rather than being resolved by additional favorable patch samples.

## 5 Conclusion

In a 2,000-patch exploratory CAMELYON17 sample, an existing MobileNetV2-based classifier achieved pooled ROC-AUC of 0.953, while specificity at the fixed 0.50 threshold was 0.668. High-confidence errors and substantial slide-associated variation remained despite strong pooled discrimination. The results support reporting calibration, operating-point errors, and hierarchy-aware analyses together. Because development included PCam test-designated images and prior external exposure is incompletely reconstructed, the study supports a bounded external characterization of this model, not an independent internal-to-external comparison or a claim of clinical readiness.

## Data and code availability

The analysis uses publicly accessible benchmark data through a version-pinned mirror [3]. Study-specific selected IDs, predictions, metric tables, bootstrap replicates, software versions, source revision, and cryptographic hashes are retained in the accompanying analysis package. Dataset licensing and any public redistribution of images, model weights, and code require confirmation before release. No public code repository or public availability of the private analysis package is claimed.

## Figure legends

1. **ROC curve** (figures/01_ROC.png). Pooled patch discrimination for the existing model. The diagonal marks chance ranking; a high AUC does not imply adequate specificity at 0.50.
2. **Probability reliability** (figures/02_calibration.png). Mean positive-class probability versus positive fraction in ten uniform bins. Bin counts are supplied in probability_reliability_bins.csv; sparse bins warrant caution.
3. **Confusion matrix** (figures/03_confusion.png). Counts at the fixed threshold of 0.50; axes distinguish prediction and reference label.
4. **Confidence distribution** (figures/04_confidence.png). Separate within-group densities for correct and incorrect predictions. The curves are not scaled to group prevalence.
5. **Slide-specific rates** (figures/05_slide_rates.png). Sensitivity and specificity; missing bars indicate undefined rates where the corresponding class is absent.
6. **Slide composition** (figures/06_slide_composition.png). Positive and negative sampled patches by slide, showing unequal contributions to pooled estimates.

## References

1. Veeling BS, Linmans J, Winkens J, Cohen T, Welling M. Rotation Equivariant CNNs for Digital Pathology. 2018. arXiv:1806.03962. Dataset specification: https://github.com/basveeling/pcam

2. WILDS contributors. CAMELYON17 dataset implementation and official hospital split. https://github.com/p-lambda/wilds/blob/main/wilds/datasets/camelyon17_dataset.py

3. wltjr1007. Camelyon17-WILDS dataset mirror. Revision d784d5344ba6c967f83f9f3d9b2f1e2a4d6eb78f. https://huggingface.co/datasets/wltjr1007/Camelyon17-WILDS/tree/d784d5344ba6c967f83f9f3d9b2f1e2a4d6eb78f

4. Tejani AS, et al. Checklist for Artificial Intelligence in Medical Imaging (CLAIM): 2024 Update. Radiology: Artificial Intelligence. 2024;6:e240300. https://doi.org/10.1148/ryai.240300

5. Koh PW, Sagawa S, Marklund H, et al. WILDS: A Benchmark of in-the-Wild Distribution Shifts. Proceedings of the 38th International Conference on Machine Learning. PMLR. 2021;139:5637–5664. https://proceedings.mlr.press/v139/koh21a.html

6. Guo C, Pleiss G, Sun Y, Weinberger KQ. On Calibration of Modern Neural Networks. Proceedings of the 34th International Conference on Machine Learning. PMLR. 2017;70:1321–1330. https://proceedings.mlr.press/v70/guo17a.html

7. Sandler M, Howard A, Zhu M, Zhmoginov A, Chen LC. MobileNetV2: Inverted Residuals and Linear Bottlenecks. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition. 2018:4510–4520. https://openaccess.thecvf.com/content_cvpr_2018/html/Sandler_MobileNetV2_Inverted_Residuals_CVPR_2018_paper.html
