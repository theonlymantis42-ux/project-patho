# Project Patho

I built Project Patho to study patch-level histopathology classification and to make model outputs easier to inspect in the context of a whole-slide image.

The repository has two related but separate parts:

1. **Patch-classification experiments:** PCam development records, CAMELYON17-WILDS evaluations, prediction files, calibration and error analyses, and manuscript drafts.
2. **Whole-slide review tools:** Colab notebooks that load a saved classifier, process an SVS/NDPI/pyramidal TIFF slide, and display patch scores in a browser report.

The project is exploratory. It does not provide a validated diagnosis or a clinically validated tumor map.

## Start here

- [Project overview](docs/PROJECT_OVERVIEW.md) — what the project is trying to study.
- [Architecture](docs/ARCHITECTURE.md) — diagrams of the classifier and whole-slide workflow.
- [Data and model record](docs/DATA_AND_MODEL.md) — dataset provenance and the two separate checkpoint histories.
- [Results](docs/RESULTS.md) — reported metrics, with each run kept separate.
- [Reproduction guide](docs/REPRODUCING.md) — how to run the Colab notebooks and what is still missing.
- [Research status and next steps](docs/RESEARCH_STATUS.md) — unresolved issues and the work needed before stronger claims are justified.
- [References](docs/REFERENCES.md) — original dataset, model, visualization, and reporting sources.

## What the current results say

The archived Paper 1 analysis covers 2,000 CAMELYON17-WILDS patches from 9 patients and 10 slides. It reports ROC-AUC of 0.953, sensitivity of 0.958, and specificity of 0.668 at a 0.50 threshold. There were 337 false positives and 41 false negatives. More than half of the errors had predicted-class confidence of at least 0.90.

That result is useful partly because it shows why AUC alone is not enough: high pooled discrimination coexisted with a substantial false-positive burden, slide-to-slide variation, and confident mistakes. The sample is exploratory and does not establish clinical performance.

A separate center-coded evaluation and a second 2,000-image metrics file are also present. They are documented separately because their model/run records and supporting methods are not interchangeable. One newer run has conflicting input-scaling metadata; see [Results](docs/RESULTS.md).

## Main files

| File | What it is |
| --- | --- |
| `Project_Patho_Process_and_Review.ipynb` | Full-grid whole-slide inference and browser review notebook |
| `Project_Patho_Paper2_Colab_Processing.ipynb` | Separate bounded Colab workflow; default public slide is a technical smoke test |
| `my_cancer_model.h5` | Older checkpoint loaded by the whole-slide notebooks |
| `model.keras` | Separate checkpoint associated with the November 11 training/evaluation records |
| `Paper1_Manuscript_BACKUP_before_training-history_update.md` | Archived exploratory manuscript; read with the limitations in the current docs |
| `Paper1_Protocol_DRAFT.md` | Earlier protocol draft, not a locked protocol |
| `results.json`, `summary.json`, and CSV files | Stored evaluation artifacts; see [Results](docs/RESULTS.md) before interpreting them |

## Important limitations

The older H5 model's development history includes use of PCam test-designated images in model fitting, so its PCam test results cannot be presented as an independent internal benchmark. The repository also contains a separate newer run whose manifest and run record disagree about whether inputs were scaled to [0, 1] or [-1, 1]. In addition, some analysis scripts refer to files that are not in a clean clone.

Those issues are documented rather than glossed over. Until they are resolved, the stored results should be described as exploratory, not as final independent validation.

## Running the notebooks

See [Reproduction guide](docs/REPRODUCING.md). The notebooks load a saved model from private Google Drive; they do not train it. Use only de-identified slides that you are authorized to process. The public CMU skin slide in the bounded notebook is for technical testing, not cancer-detection evaluation.

## Intended use

Project Patho is a research prototype. Model scores are not calibrated diagnostic probabilities, candidate regions are not confirmed lesions, and Grad-CAM maps are not tumor segmentations. The software is not intended for clinical decision-making.
