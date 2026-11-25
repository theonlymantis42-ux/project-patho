# Project Patho — start here

The repository is now organized around the two main parts of the project.

## Read the research overview

1. [README](README.md) — project summary and repository map.
2. [Project overview](docs/PROJECT_OVERVIEW.md) — the research question and scope.
3. [Architecture](docs/ARCHITECTURE.md) — patch classifier and whole-slide workflow diagrams.
4. [Data and model record](docs/DATA_AND_MODEL.md) — dataset provenance and checkpoint histories.
5. [Results](docs/RESULTS.md) — the separate experiments and their limits.
6. [Reproduction guide](docs/REPRODUCING.md) — Colab setup and missing dependencies.
7. [Research status](docs/RESEARCH_STATUS.md) — unresolved issues and next steps.

## Browse the work

- **Model Generalization Testing:** model-generalization-testing/
  - Start with its README, then open Cases/ for false-positive and false-negative records.
  - Figures, metrics, manuscripts, model provenance, and scripts are grouped in their own subfolders.
- **Whole-Slide Processing Model Testing:** whole-slide-processing-model-testing/
  - Start with its README, then open notebooks/ for the slide-processing workflows.
- **Project notes:** project-notes/ contains the retained run-log document.

The older Paper 1 analysis is exploratory, not clinical validation. The November 11 model run is kept separate because its saved manifest and run record disagree about input scaling. The notebooks load models from private Drive locations; they do not train models by themselves.
