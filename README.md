# Project Patho

I built Project Patho to study patch-level histopathology classification and to make model outputs easier to inspect in the context of a whole-slide image.

The repository has two related but separate parts:

1. **Model Generalization Testing** — experiments on how saved classifiers behave across PCam and CAMELYON17-WILDS data, including false-positive and false-negative analysis.
2. **Whole-Slide Processing Model Testing** — Colab notebooks that apply a saved model to a whole-slide image and map patch scores back to slide coordinates.

The project is exploratory. It does not provide a validated diagnosis or a clinically validated tumor map.

## Start here

- [Project overview](docs/PROJECT_OVERVIEW.md) — what the project is trying to study.
- [Architecture](docs/ARCHITECTURE.md) — how the patch classifier and whole-slide workflow fit together.
- [Data and model record](docs/DATA_AND_MODEL.md) — dataset provenance and the two checkpoint histories.
- [Results](docs/RESULTS.md) — the metrics in the repository and what can and cannot be concluded.
- [Reproduction guide](docs/REPRODUCING.md) — how to run the Colab notebooks and what is still missing.
- [Research status](docs/RESEARCH_STATUS.md) — unresolved issues and work needed before stronger claims are justified.
- [References](docs/REFERENCES.md) — dataset, model, visualization, and reporting sources.

## Repository layout

[**Model Generalization Testing**](model-generalization-testing/) contains the patch-classification experiments and Paper 1 records:

- **notebooks/** — the patch-level analysis notebook.
- **manuscripts/** — the Paper 1 protocol draft and archived manuscript files.
- **Cases/** — separate false-positive and false-negative CSVs, grouped by dataset/run.
- **results/** — figures, metrics, prediction tables, and patient/slide analyses.
- **runs/2026-11-11/** — the separate November 11 training and evaluation record.
- **provenance/** and **scripts/** — integrity records, model-history disclosures, and analysis code.

[**Whole-Slide Processing Model Testing**](whole-slide-processing-model-testing/) contains the Paper 2 / whole-slide workflow:

- **notebooks/** — the standard review notebook, the Grad-CAM version, and the bounded Colab processing notebook.
- **models/** — the older H5 checkpoint used by those notebooks.
- **runs/** — a legacy patch-coordinate prediction table. Its original run manifest is not present in the repository.

[**project-notes/**](project-notes/) holds a legacy run-log document whose contents have not been assigned to either experiment. [**docs/**](docs/) contains the project-wide documentation.

## What the current results say

The archived Paper 1 analysis covers 2,000 CAMELYON17-WILDS patches from 9 patients and 10 slides. It reports ROC-AUC of 0.953, sensitivity of 0.958, and specificity of 0.668 at a 0.50 threshold. There were 337 false positives and 41 false negatives. More than half of the errors had predicted-class confidence of at least 0.90.

That result is useful partly because it shows why AUC alone is not enough: high pooled discrimination coexisted with a substantial false-positive burden, slide-to-slide variation, and confident mistakes. The sample is exploratory and does not establish clinical performance.

A separate center-coded evaluation and a second 2,000-image metrics file are also present. They are documented separately because their model/run records and supporting methods are not interchangeable. One newer run has conflicting input-scaling metadata; see [Results](docs/RESULTS.md).

## Important limitations

The older H5 model's development history includes use of PCam test-designated images in model fitting, so its PCam test results cannot be presented as an independent internal benchmark. The repository also contains a separate newer run whose manifest and run record disagree about whether inputs were scaled to [0, 1] or [-1, 1]. Some analysis scripts also refer to files that are not in a clean clone.

Those issues are documented rather than glossed over. Until they are resolved, the stored results should be described as exploratory, not as final independent validation.

## Running the notebooks

See [Reproduction guide](docs/REPRODUCING.md). The notebooks load a saved model from private Google Drive; they do not train it. Use only de-identified slides that you are authorized to process. The public CMU skin slide in the bounded notebook is for technical testing, not cancer-detection evaluation.

## Intended use

Project Patho is a research prototype. Model scores are not calibrated diagnostic probabilities, candidate regions are not confirmed lesions, and Grad-CAM maps are not tumor segmentations. The software is not intended for clinical decision-making.
