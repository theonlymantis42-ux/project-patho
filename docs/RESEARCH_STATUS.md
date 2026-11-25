# Research status, limitations, and next steps

This is the current status based on the files in the repository. It separates code that runs from results that can be defended scientifically.

## What is implemented

- Colab workflows that load a saved H5 classifier and apply it to whole-slide images.
- OpenSlide image reading, pixel-scale checks, patch sampling, and bounded batch inference.
- A heuristic filter that skips some background supports.
- CSV, JSON manifest, and HTML review-report outputs.
- Score maps, spatial summaries, and optional Grad-CAM attribution maps.
- PCam and CAMELYON17-WILDS prediction and analysis artifacts.
- Exploratory analysis of patch-level discrimination, threshold errors, confidence, and variation across slides and patients.

These are software and analysis capabilities. They do not, by themselves, establish diagnostic performance.

## What the results currently show

The archived Paper 1 sample contains 2,000 CAMELYON17-WILDS patches from 9 patients and 10 slides. It reports ROC-AUC 0.953 and sensitivity 0.958 at a 0.50 threshold, but specificity is 0.668. The sample contains 337 false positives and 41 false negatives. More than half of the errors have predicted-class confidence of at least 0.90. Slide-level estimates vary substantially.

A separate 241,062-patch, center-coded result is stored in \`results.json\`. It reports different metrics at a different threshold and uses a different model/run record. It must not be merged with the Paper 1 sample.

See [Results](RESULTS.md) for the full numbers and interpretation limits.

## Issues that must be resolved

### 1. Two checkpoint histories

The whole-slide notebooks load \`my_cancer_model.h5\`. The recovered source audit describes a frozen ImageNet MobileNetV2 backbone with a small classification head. The training-history disclosure says that approximately 30,000 PCam test-designated images were passed to \`model.fit\` during development. The exact unique-image and epoch history was not reconstructed. Results from this checkpoint cannot be described as an independent PCam test.

A separate \`model.keras\` and November 11 manifest are also present. Do not assume it is the same architecture or training history as the H5 checkpoint.

### 2. Conflicting input-scaling records

The November 11 manifest records \`zero_to_one\` input scaling. The associated \`run.json\` records \`minus_one_to_one\`. Both refer to the same recorded trainer hash. The source trainer, checkpoint, and scoring code must be inspected to determine which preprocessing was actually used. Until then, the corresponding center-coded metrics are recorded results, not a fully reproducible final evaluation.

### 3. Pilot archive integrity

\`integrity_status.json\` records 4,000 pilot IDs, 506 saved-label conflicts against the pinned metadata, and \`final_evaluation_allowed: false\`. The older manuscript excludes the known pilot IDs from its sampled external analysis but also says the historical exposure inventory may be incomplete. The label conflicts need a documented resolution; they should not be silently overwritten.

### 4. Reproduction files are missing

The root \`reproduce_analysis.py\` expects \`plan.json\`, which is not present at the repository root. \`evaluate_internal_no_overlap.py\` imports \`prepare_pcam.py\` and checks for \`evaluate_internal.py\`; those files are also absent from the current root file set. There is no complete environment lockfile. A clean clone therefore cannot currently reproduce every reported result.

### 5. Evaluation scope

The main external sample contains 9 patients and 10 slides. Patient-cluster bootstrap intervals based on 9 clusters can be unstable. The sample is from one hospital split, does not represent clinical prevalence, and uses benchmark labels rather than new pathologist adjudication. Patch-level results do not establish patient-level diagnostic performance. The repository does not show prospective clinical testing or a pathologist-comparator study.

## Next steps, in order

1. **Resolve the November 11 preprocessing conflict.** Trace the trainer, model checkpoint, model lock, and scoring code. Record one verified preprocessing rule and regenerate predictions only if necessary.
2. **Separate the two checkpoints in the repository.** Add an explicit model card and immutable hashes for each checkpoint; state which notebook and analysis uses each one.
3. **Resolve the pilot metadata conflicts.** Audit the 506 label conflicts and document the complete known image-exposure list. Do not re-label or discard records without preserving the original files and explaining the correction.
4. **Restore the missing reproduction inputs.** Commit or link the required scripts and manifests, and add an environment specification with tested versions.
5. **Re-run a locked evaluation.** Freeze model, threshold, exclusions, split rules, and analysis code before opening the final evaluation set. Keep patient and slide identifiers in the analysis table and account for clustering.
6. **Expand external evaluation.** More independent patients, slides, and hospitals are needed before making broad generalization claims.
7. **Add expert review only with a defined protocol.** If pathologists review selected errors or regions, record who reviewed them, what information they saw, and how disagreements were handled. Do not describe informal feedback as a reader study.

## Claims this project does not currently support

The current repository does not establish that Project Patho diagnoses cancer, improves pathologist accuracy, detects disease earlier, reduces workload, or is ready for clinical use. It also does not show that the heatmap is a validated tumor segmentation. Those would require different studies and stronger evidence.

Negative and inconclusive findings belong in the research record. They are part of the project, not documentation to hide.
