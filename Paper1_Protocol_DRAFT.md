# Paper 1 protocol — preflight draft, NOT LOCKED

Question: How does a PCam-only classifier generalize to CAMELYON17 hospital 2, and how do discrimination, calibration, and errors vary?
H1 discrimination decreases externally; H2 calibration worsens; H3 patient/slide performance varies; H4 high-confidence errors occur.

## Fixed study boundaries from the agreed plan
- Existing model and all existing runs are pilots only. Originals remain unchanged; snapshot checksums are recorded.
- Fresh ImageNet MobileNetV2 backbone, global average pooling, Dense(64, ReLU), Dense(1, sigmoid), 96x96 RGB inputs.
- Input scaling image/255.0 as specified in the prior plan. Do not silently substitute MobileNetV2 preprocessing.
- Horizontal/vertical flips and moderate rotation; exact rotation must be specified before lock.
- Official PCam train 262144 and validation 32768; no test data in training or tuning.
- Five independent seeds; identical architecture and training settings; fresh model for every seed.
- Freeze weights and all selection rules before internal and external evaluation. Default threshold 0.50.
- Official PCam test 32768 for final internal evaluation; no iterative test-driven changes.
- External: all eligible CAMELYON17-WILDS hospital-2 test patches after exclusion; retain natural distribution among eligible patches.
- Exclude every previously inspected patch; do not rebalance final external data.
- Preserve image, hospital, patient, and slide IDs in every prediction row.
- Primary outcome external ROC-AUC. Also report accuracy, sensitivity, specificity, balanced accuracy, precision, F1, confusion matrix, Brier, ECE, reliability curves, and confidence on correct/incorrect predictions.
- Report per-seed values, mean, SD, range, and generalization gaps with explicitly defined signs.
- Patient/slide analyses; AUC undefined for one-class groups. Clustered 95% bootstrap CIs with limitations for small cluster counts.
- Error analysis and limited illustrative Grad-CAM only after model and dataset lock.
- No CAMELYON17 training, tuning, calibration, threshold selection, stain-normalization intervention, or architecture changes based on external results.

## Outstanding before protocol lock
1. Verify source extraction code and image_id semantics against original WILDS metadata. Current union has 4000 unique IDs from 6000 saved pilot rows; completeness is unverified.
2. Account for slide-22 experiments and any other previously inspected images. Reconstruct missing IDs or explicitly resolve exclusion coverage before proceeding.
3. Obtain official PCam files and CAMELYON17 metadata/data; verify provenance, split counts, hashes, and upstream dataset definitions.
4. Specify backbone freeze/fine-tuning schedule, optimizer, learning rate, epochs, batch size, checkpoint rule, exact augmentation, five seeds, ECE definition/bins, bootstrap unit/count/seed, undefined-metric handling, and error-example selection rules BEFORE training/final testing.
5. Audit prior PCam test exposure and disclose that official test data were used in pilot development. Fresh retraining alone does not make previously used test data historically untouched; resolve the internal evaluation claim before lock.

Status: Preflight only. No training or final test access has occurred in this notebook.
