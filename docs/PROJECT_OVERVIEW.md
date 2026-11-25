# Project overview

I built Project Patho to explore two connected problems in computational pathology: how patch classifiers behave on pathology images from a different dataset or hospital, and how their patch-level outputs can be mapped back onto a whole-slide image for review.

The repository contains experiments, saved checkpoints, evaluation artifacts, and two Colab notebooks. It is not a single finished application or one unified experiment. Some records describe an older H5 checkpoint; a separate November 2026 run uses a Keras checkpoint and its own manifest. Their results and training histories must remain separate.

## The research question

The most developed analysis asks how an existing pathology patch classifier behaves on CAMELYON17-WILDS data, particularly when performance is considered alongside false positives, false negatives, confidence calibration, and variation across slides and patients.

That question is narrower than asking whether AI can diagnose cancer. The current evidence concerns patch-level classification on benchmark data. It does not establish patient-level diagnosis, clinical utility, or performance in a hospital workflow.

## Two parts of the project

**Patch-level experiments.** The repository contains PCam development records, CAMELYON17-WILDS evaluation artifacts, prediction tables, error lists, calibration outputs, and manuscript drafts. The archived Paper 1 analysis is exploratory and has important limits, including prior use of PCam test-designated images during development of the older checkpoint.

**Whole-slide review.** The Colab notebooks load an existing H5 model, read a whole-slide image using OpenSlide, sample image context, run patch inference, and map scores back to slide coordinates. A browser report displays the score map and optional Grad-CAM attribution. This is an inference and visualization workflow; it does not train a model or generate a validated slide diagnosis.

See [Architecture](ARCHITECTURE.md) for the two workflows, [Data and model record](DATA_AND_MODEL.md) for checkpoint and dataset provenance, and [Results](RESULTS.md) for the separate analyses currently represented in the repository.

## Current state

The code can process slides and produce review artifacts. The repository also contains exploratory benchmark results. However, there are unresolved issues in the model history and run metadata. In particular, the November 11 manifest and run record disagree about the input scaling used for a newer checkpoint. Some analysis scripts also reference files that are not present in a clean clone.

Those gaps matter. The results are documented with their caveats rather than presented as independent validation. The next work is to reconcile the model records, restore the missing reproduction inputs, and repeat only the analyses that can be tied to a verified checkpoint and protocol.

## Intended use

Project Patho is for research and software development. Its outputs are not medical advice, a diagnosis, or a substitute for review by a qualified pathologist.