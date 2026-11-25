# Project Patho — start here

This repository contains two related but separate kinds of work: patch-classification experiments and whole-slide inference/review tools.

Read the current documentation in this order:

1. [README](README.md) — a short description of the project and its current limits.
2. [Project overview](docs/PROJECT_OVERVIEW.md) — the research question and the two parts of the project.
3. [Architecture](docs/ARCHITECTURE.md) — how the patch classifier and whole-slide workflow fit together.
4. [Data and model record](docs/DATA_AND_MODEL.md) — datasets, checkpoints, and provenance.
5. [Results](docs/RESULTS.md) — the metrics in the repository and what can and cannot be concluded.
6. [Reproduction guide](docs/REPRODUCING.md) — notebook setup and missing dependencies.
7. [Research status](docs/RESEARCH_STATUS.md) — the issues that need to be resolved next.

The older Paper 1 manuscript is an archived exploratory analysis, not a clinical validation study. The protocol draft is explicitly not locked. The root result files include separate runs; do not combine their metrics.

The whole-slide notebooks load an existing H5 checkpoint from private Google Drive. They do not train the model. Use only de-identified slides you are authorized to process.

The project currently has unresolved model-provenance and preprocessing issues. They are called out in the documentation because they affect how the results should be interpreted.
