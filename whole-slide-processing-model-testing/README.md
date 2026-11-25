# Whole-Slide Processing Model Testing

This folder contains the Paper 2 / whole-slide inference and review tools. The notebooks load the existing H5 checkpoint, sample regions from a whole-slide image, run patch-level inference, and map the resulting scores back to slide coordinates.

## Folder map

- **notebooks/** — three related Colab workflows.
- **models/my_cancer_model.h5** — the older checkpoint loaded by the whole-slide notebooks.
- **runs/legacy_predictions.csv** — an existing patch-coordinate prediction export. The original slide/run manifest was not present alongside it, so it is retained as an unlinked legacy artifact rather than presented as a reproducible run.

## Which notebook should I open?

- **Project_Patho_Process_and_Review.ipynb** — full-grid processing and browser review report.
- **Project_Patho_Stitched_GradCAM.ipynb** — the review workflow with optional stitched Grad-CAM attribution maps.
- **Project_Patho_Paper2_Colab_Processing.ipynb** — a bounded processing workflow. Its default public CMU skin slide is a technical smoke test, not a cancer-detection evaluation.

The notebooks expect the model in the private Drive project folder at Pathology_Project/my_cancer_model.h5. Moving the checkpoint in GitHub does not change that Drive path. When setting up a new Colab session, put the file at the expected Drive location or update MODEL_PATH in the notebook.

The slide outputs are for exploratory research and human review. Patch scores are not calibrated diagnostic probabilities, candidate regions are not confirmed lesions, and Grad-CAM is not tumor segmentation. Keep the original slide available for native-resolution review.
