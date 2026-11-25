# Cases

These are the exported case tables from specific model-evaluation runs. They are tabular records, not a gallery of tissue images. Each row identifies a source index, reference label, model output, predicted label, and error type.

## Collections

- **CAMELYON17_External_Test/** — false positives and false negatives from the archived 2,000-patch Paper 1 sample.
- **CAMELYON17_External_Test_Run_2/** — false positives and false negatives from a separate 2,000-image run. Its metrics file is stored under results/tables.
- **PCam_Validation/** — the false-positive export available for the PCam validation analysis. No matching false-negative CSV was present in the repository.

Do not combine cases across folders. They come from different runs and do not necessarily share the same checkpoint, threshold, or sampling procedure.

The CSVs have been moved without changing their contents. Source image access and image-level context are not included in these tables.
