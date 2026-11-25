# Research status and evidence gaps

This document distinguishes implementation evidence from scientific evidence. It should be updated whenever the project changes.

## Demonstrated by the latest documented notebook

- An existing saved Keras model can be loaded for inference.
- The notebook checks for a 96 × 96 RGB input and a single sigmoid-style output.
- Whole-slide image reading is performed with OpenSlide.
- The workflow samples spatial supports, applies a heuristic tissue filter, and batches inference.
- It writes prediction CSVs and run metadata, including model/source hashes and coverage information.
- It can export data for a browser-based review interface.
- The default public CMU skin slide is labeled as a technical smoke test, not a cancer-detection evaluation.

These are implementation capabilities. They are not evidence of diagnostic performance.

## Not established by the repository record reviewed for this documentation

The current repository record does not yet provide a sufficiently clear, auditable account of:

- The complete provenance and licensing of every dataset and label.
- The model architecture, training procedure, training cohort, and checkpoint provenance.
- Patient-level and slide-level data splits.
- A prespecified evaluation protocol and decision threshold.
- Independent test-set performance with confidence intervals.
- External validation across institutions, scanners, or tissue domains.
- A comparison against meaningful baselines.
- A pathologist-reviewed error analysis.

Do not fill these gaps with estimates or inferred results. Add evidence and citations before changing these statements.

## Required evidence table

| Item | Current documentation status | Evidence needed |
|---|---|---|
| Research objective | Broadly described | One precise, testable research question |
| Dataset provenance | Incomplete | Dataset name/version, access terms, labels, inclusion criteria |
| Model provenance | Incomplete | Architecture, checkpoint origin, training data, preprocessing |
| Data separation | Not established | Patient-/slide-level split manifest and leakage checks |
| Evaluation | Not established | Prespecified metrics, baselines, confidence intervals |
| External generalization | Not established | Independent cohort and domain-shift analysis |
| Human review | Not established | Defined pathologist review protocol, if performed |
| Reproducibility | Partially implemented | Environment file, exact commands, versioned inputs |

## Reporting rules

- Report denominators and exclusions alongside every metric.
- Keep patient-level separation explicit; patch-level random splits can produce misleading results when patches from the same patient or slide cross partitions.
- Do not describe a technical smoke test as model validation.
- Do not call raw model scores confidence unless calibration has been evaluated.
- Do not call Grad-CAM a segmentation or explanation of causal reasoning.
- Distinguish exploratory results, held-out internal evaluation, and independent external validation.
- Report negative and inconclusive findings.

## Next documentation steps

1. Add a dataset card for each dataset actually used.
2. Add a model card documenting checkpoint origin and intended input domain.
3. Add a reproducible environment specification and exact run instructions.
4. Add a split manifest that does not expose patient identifiers.
5. Add an evaluation report only after the protocol and results can be independently checked.
