# Data and model record

This page separates the datasets and checkpoints that appear in the repository. They have different histories and should not be combined into one model narrative.

## Datasets

| Dataset or source | How it appears in the project | What is recorded | Important qualification |
| --- | --- | --- | --- |
| PatchCamelyon (PCam) | Development data in the November 11 run manifest | 262,144 training rows and 32,768 validation rows; the manifest records source-slide counts and image hashes | The manifest says slide identity is known but biological patient separation is not verified |
| CAMELYON17-WILDS | External patch evaluation in the archived Paper 1 analysis | A 2,000-patch sample from the hospital-2 test split; 9 patients and 10 slides | The sample is exploratory. It shares source patients/slides with pilot work, and earlier exposure cannot be ruled out completely |
| CAMELYON17-WILDS center-coded result | Separate evaluation artifact in `results.json` | 241,062 patches across centers coded 0, 1, and 4; 30 slides and 24 case groups | This is a separate run from the 2,000-patch Paper 1 sample; see the preprocessing discrepancy below |

### PCam development split recorded in the November 11 manifest

The file `zero_to_one_20261111.json` records:

- **Training:** 262,144 rows, 131,072 positive labels, 216 source slides, and 220,025 unique RGB hashes.
- **Validation:** 32,768 rows, 16,369 positive labels, 54 source slides, and 28,108 unique RGB hashes.

The manifest records publisher-checksummed HDF5 label files and a comparison with central-region tumor metadata. It does not establish biological patient-level separation. The duplicate/hash counts should remain visible rather than being silently treated as unique independent specimens.

### CAMELYON17-WILDS Paper 1 sample

The archived manuscript describes a reproducibly selected sample from the hospital-2 test split of a version-pinned mirror. It records 81,054 eligible metadata rows after removing 4,000 documented pilot image IDs, then selects 2,000 IDs by deterministic SHA-256 priority. The selected sample contains 986 positive patches and 1,014 negative patches from 9 patients and 10 slides.

The label source is the pinned dataset mirror, not new pathologist adjudication. The manuscript explicitly notes that the sample is new relative to the documented exclusion list, not certified historically untouched. Prior work involved the same source patients and slides.

## Checkpoints and architecture

### `whole-slide-processing-model-testing/models/my_cancer_model.h5` — older checkpoint

The recovered source audit describes this model as:

- 96 × 96 RGB input.
- Pixel values converted from uint8 to float32 and divided by 255.
- Frozen ImageNet MobileNetV2 backbone.
- Global average pooling.
- Dense layer with 64 ReLU units.
- One-unit sigmoid output.

This architecture is attributed to the recovered source, not independently reconstructed from a complete training record. The whole-slide Colab notebooks load this file for inference; they do not train it.

The training-history disclosure records that approximately 30,000 images designated for the PCam test split were passed to `model.fit` during development. The counts are investigator-reported approximations, and a complete unique-image/epoch history was not recovered. For that reason, PCam test results for this older checkpoint must not be described as an independent internal benchmark.

### `model-generalization-testing/runs/2026-11-11/model.keras` — separate November 11 run

A second checkpoint appears alongside `zero_to_one_20261111.json`, `run.json`, and `results.json`. The manifest records ImageNet initialization, five epochs, batch size 64, learning rate 0.001, seed 20261111, and a target sensitivity of 0.95.

There is an unresolved conflict: the manifest says input scaling was **zero-to-one**, while `run.json` for the same recorded run says **minus-one-to-one**. The trainer hash is recorded in both metadata sources, so this is not a harmless naming difference. The source code, saved checkpoint, and scoring manifest need to be checked together before the associated metrics are treated as reproducible.

The manifest does not provide enough directly auditable detail here to attribute the older MobileNetV2 architecture to this checkpoint. The two model files are therefore documented separately.

## Data handling

The whole-slide notebooks expect the model and authorized slide files in the investigator's private Google Drive. Do not upload identifiable patient information or protected health information to this repository or to a third-party runtime. Only use de-identified material that you are authorized to process in the chosen environment.

Dataset names and public benchmark labels do not, by themselves, establish that every local copy or derived file is licensed for redistribution. Check the upstream terms before sharing data or model artifacts publicly.
