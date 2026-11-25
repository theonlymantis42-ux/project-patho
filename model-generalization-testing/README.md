# Model Generalization Testing

This folder contains the patch-level experiments and the Paper 1 records. The goal of this work was to examine how a histopathology patch classifier behaved on benchmark data beyond its original development setting, and to look beyond one summary metric at errors, confidence, and variation between slides.

## Folder map

- **notebooks/** — the original patch-level analysis notebook.
- **manuscripts/** — Paper 1 protocol draft and archived manuscript files.
- [**Cases/**](Cases/) — raw false-positive and false-negative CSVs, separated by dataset and run.
- **results/figures/** — plots and exported figures.
- **results/tables/** — metrics, full prediction tables, slide summaries, and bootstrap outputs.
- **runs/2026-11-11/** — the separate Keras checkpoint, training record, and center-coded evaluation artifacts.
- **provenance/** — source audit, pilot exclusions/conflicts, and training-history disclosures.
- **scripts/** — analysis scripts and evaluation code.

## How to read the results

The archived 2,000-patch CAMELYON17-WILDS analysis is exploratory. It reports ROC-AUC of 0.953, but specificity at the fixed 0.50 threshold is 0.668; it also records 337 false positives and 41 false negatives. Its sample includes 9 patients and 10 slides, with considerable variation between slides.

The separate November 11 run is not a replication of that Paper 1 sample. It uses a different checkpoint and threshold, and its manifest/run record disagree about input scaling. Its metrics remain provisional until that discrepancy is resolved.

Read [the results guide](../docs/RESULTS.md) and [the research status](../docs/RESEARCH_STATUS.md) before using any number in a presentation or application. The CSVs preserve the recorded outputs; they do not independently validate the labels or evaluation design.
