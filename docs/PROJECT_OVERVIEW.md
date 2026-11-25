# Project overview

## Motivation

Pathology relies on examining tissue architecture and cellular morphology. Digitized whole-slide images are large, complex images, and computational methods can help organize image information for closer human inspection.

Project Patho explores an AI-assisted workflow that processes pathology images, produces spatially indexed model outputs, and visualizes those outputs in a review interface.

## Intended research direction

The project's broad direction is computational analysis of cancer-related tissue images. The repository's current implementation is best described as an exploratory inference and visualization pipeline.

The central engineering question represented by the current code is:

**Can an existing image model be applied to regions of a whole-slide image and its outputs be mapped back to slide coordinates in a reproducible, inspectable way?**

This is a pipeline question, not yet evidence that the model can accurately detect cancer in whole-slide images.

## System outline

1. **Input:** a whole-slide image (SVS in the documented workflow).
2. **Scale handling:** read scanner pixel-size metadata and map the slide to the model's expected physical scale. Research runs require a confirmed target scale.
3. **Sampling:** enumerate spatial supports and extract image context around each support.
4. **Filtering:** apply a heuristic tissue filter. This filter is not validated tissue segmentation and may omit relevant tissue.
5. **Inference:** load an existing saved Keras model and score batches of image patches.
6. **Artifacts:** write predictions, configuration, a manifest, and a dashboard-import JSON file.
7. **Review:** visualize raw scores, spatial summaries, and optional Grad-CAM attribution maps.

## What is implemented in the documented notebook

The latest notebook describes an inference-only workflow. It checks model input/output shapes, hashes the model and source slide, limits candidate processing, saves completed batches, records coverage, and labels the public sample run as a technical smoke test.

It does not call model training or claim that the public sample is a valid evaluation cohort.

## Scientific questions that still need answers

Before the project can support a diagnostic-performance claim, the research record needs to establish:

- What exact task and target label the model was trained to predict.
- Which dataset(s), institutions, tissue types, and patients were represented.
- How training, validation, and test data were separated, especially at the patient and slide level.
- Whether preprocessing and thresholds were selected without access to the test set.
- Whether the model was evaluated on an appropriate independent cohort.
- How performance compares with simple and clinically meaningful baselines.
- Whether performance is stable across relevant subgroups, scanners, and institutions.

## Intended use and safety boundary

The output is for exploratory research and human review only. It does not provide a diagnosis, calibrated clinical confidence, or a validated lesion map. A pathologist's assessment and appropriately designed validation remain necessary for any clinical claim.
