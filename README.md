# Project Patho

**An exploratory computational pathology project**

Project Patho is a research and engineering prototype exploring how machine-learning outputs can be applied to digitized pathology images and presented as spatial maps for human review.

> **Current status:** Work in progress. This repository does not establish clinical validity, diagnostic accuracy, or readiness for clinical use. Model scores are not calibrated diagnostic confidence, and highlighted regions are not confirmed lesions.

## Start here

If you are new to the project, read these in order:

1. **[Project overview](docs/PROJECT_OVERVIEW.md)** — the motivation, intended question, system outline, and current limitations.
2. **The Colab slide-processing notebook** — the current documented inference workflow. It loads an existing saved model; it does not train or fine-tune that model.
3. **[Research status and evidence gaps](docs/RESEARCH_STATUS.md)** — what the repository currently demonstrates, what is not yet demonstrated, and what must be documented before making research claims.

## What the current workflow does

The latest documented Colab workflow:

- Loads an existing Keras model from the investigator's Google Drive.
- Checks the model's expected input and output shapes.
- Reads a whole-slide image using OpenSlide.
- Samples image supports and applies a heuristic tissue filter.
- Runs inference in bounded batches and writes prediction checkpoints.
- Exports a run configuration, manifest, CSV predictions, and a JSON payload for a browser-based review interface.
- Can optionally generate and display Grad-CAM attribution maps.

The default public-slide run is explicitly a **technical smoke test**. The included CMU-1-Small-Region example is a skin reference slide used to check processing and display plumbing; it is not a lymph-node evaluation set and must not be used as evidence of cancer-detection performance.

## Important interpretation limits

- A patch score is a model output, not a calibrated probability of disease.
- A thresholded patch is a candidate for review, not a confirmed diagnosis or lesion.
- Spatial averages and connected regions are exploratory visual summaries.
- Grad-CAM is an attribution visualization, not a tumor segmentation mask or proof that the model reasons correctly.
- A technically successful run does not establish generalization to a new scanner, institution, tissue type, or patient population.
- Partial slide coverage must not be described as a whole-slide assessment.

## Reproducibility and data handling

The notebook records run configuration and provenance information, including source-slide and model hashes, preprocessing details, scan coverage, and software versions. Slide files and the saved model are expected to remain in the investigator's controlled storage rather than being committed to this repository.

Do not commit identifiable patient information, protected health information, or any slide data unless the required permissions and de-identification have been confirmed. Use only data that may lawfully and ethically be used for the stated research purpose.

## What this repository does not claim

Project Patho is not a clinical decision-support product. It has not been established here as a validated diagnostic system, a replacement for pathologists, or a tool that improves patient outcomes. Those claims would require appropriately designed, independently evaluated evidence.

## Development priorities

1. Make the dataset, labels, patient-level split, and evaluation protocol explicit.
2. Document the model's origin, training data, preprocessing, and intended input domain.
3. Separate technical pipeline checks from scientific evaluation.
4. Report patient-/slide-level metrics with uncertainty and clearly defined baselines when a valid evaluation exists.
5. Test external generalization before making claims beyond the development data.
6. Keep limitations and failed experiments visible rather than presenting only favorable examples.

See [Research status and evidence gaps](docs/RESEARCH_STATUS.md) for the current documentation checklist.
