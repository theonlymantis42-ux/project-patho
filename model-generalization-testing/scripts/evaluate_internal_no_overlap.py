"""Score official PCam test once with the locked clean-run model and threshold."""

import argparse
import csv
import hashlib
import json
from pathlib import Path

import h5py
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

from prepare_pcam import check_separation, digest, prepare_split, write_json


def summarize(labels, scores, threshold):
    positive = labels == 1
    negative = ~positive
    flagged = scores >= threshold
    return {
        "rows": int(len(labels)),
        "positive_rows": int(positive.sum()),
        "true_positive": int((positive & flagged).sum()),
        "true_negative": int((negative & ~flagged).sum()),
        "false_positive": int((negative & flagged).sum()),
        "false_negative": int((positive & ~flagged).sum()),
        "sensitivity": float(flagged[positive].mean()) if positive.any() else None,
        "specificity": float((~flagged[negative]).mean()) if negative.any() else None,
        "roc_auc": float(roc_auc_score(labels, scores)) if positive.any() and negative.any() else None,
        "average_precision": float(average_precision_score(labels, scores)) if positive.any() else None,
        "brier": float(np.mean((scores - labels) ** 2)),
    }


def group_results(labels, scores, threshold, groups):
    return {
        group: summarize(labels[groups == group], scores[groups == group], threshold)
        for group in np.unique(groups)
    }


def cluster_intervals(labels, scores, threshold, groups, draws=2000):
    rng = np.random.default_rng(20261111)
    group_rows = [np.flatnonzero(groups == group) for group in np.unique(groups)]
    if len(group_rows) < 2:
        return {}
    metrics = {key: [] for key in ("roc_auc", "sensitivity", "specificity", "brier")}
    for _ in range(draws):
        sampled_groups = rng.integers(0, len(group_rows), size=len(group_rows))
        rows = np.concatenate([group_rows[i] for i in sampled_groups])
        values = summarize(labels[rows], scores[rows], threshold)
        for key, samples in metrics.items():
            if values[key] is not None:
                samples.append(values[key])
    return {
        key: {"valid_draws": len(samples), "percentile_95": np.percentile(samples, [2.5, 97.5]).tolist()}
        for key, samples in metrics.items() if samples
    }


def development_matches(manifest, data_dir, test):
    matches = {}
    for name, official in (("training", "train"), ("validation", "valid")):
        descriptor = manifest["data"][name]["images"]
        path = data_dir / descriptor["path"]
        if digest(path) != descriptor["sha256"]:
            raise ValueError(f"{name} images differ from the locked development manifest")
        check_separation((None, manifest["provenance"]["audit"][official], {}), test)
        matches[name] = set()
        with h5py.File(path, "r") as handle:
            images = handle["x"]
            for start in range(0, len(images), 512):
                for image in images[start:start + 512]:
                    rgb = hashlib.sha256(image.tobytes()).hexdigest()
                    if rgb in test[2]:
                        matches[name].add(rgb)
        print(f"{name}: {len(matches[name])} distinct RGB hashes also occur in test", flush=True)
    return matches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("run-dir", "manifest", "archive-dir", "data-dir", "output-dir"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--model-lock-sha256", required=True)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()

    model_lock_path = args.run_dir / "model_lock.json"
    if digest(model_lock_path) != args.model_lock_sha256:
        raise ValueError("Saved lock differs from the separately recorded SHA-256")
    lock = json.loads(model_lock_path.read_text(encoding="utf-8"))
    if lock["mode"] != "study" or lock["manifest_sha256"] != digest(args.manifest):
        raise ValueError("Evaluation requires a clean study model and its original development manifest")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest["protocol_status"] != "locked":
        raise ValueError("The development protocol is not locked")
    if digest(Path(__file__).with_name("evaluate_internal.py")) != manifest["provenance"]["internal_evaluator_sha256"]:
        raise ValueError("Evaluation code differs from the locked development manifest")
    if lock["trainer_sha256"] != manifest["provenance"]["trainer_sha256"]:
        raise ValueError("Model lock identifies a different trainer")
    model_path = args.run_dir / "model.keras"
    if digest(model_path) != lock["model_sha256"]:
        raise ValueError("Checkpoint differs from the model lock")
    threshold = float(lock["threshold"])
    if not np.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("Invalid locked threshold")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if (args.output_dir / "results.json").exists() or (args.output_dir / "predictions.csv").exists():
        raise FileExistsError("Evaluation output exists. Preserve the existing result.")

    print("Verifying official PCam test files and split separation.", flush=True)
    test = prepare_split("test", args.archive_dir, args.data_dir, args.download)
    matches = development_matches(manifest, args.data_dir, test)
    descriptors, counts, _, metadata, labels = test
    included = []
    excluded = []
    with h5py.File(args.data_dir / descriptors["images"]["path"], "r") as handle:
        images = handle["x"]
        for start in range(0, len(images), 512):
            for index, image in enumerate(images[start:start + 512], start):
                rgb = hashlib.sha256(image.tobytes()).hexdigest()
                splits = [name for name, hashes in matches.items() if rgb in hashes]
                if splits:
                    excluded.append({"official_row": index, "slide": metadata[index][0], "development_splits": splits})
                else:
                    included.append(index)
    if not excluded or not included:
        raise ValueError("The amendment expects both excluded and eligible test rows.")
    evidence = {
        "reason": "Original strict evaluation stopped before model inference because decoded RGB pixels matched across splits.",
        "rule": "Exclude every test row with the same SHA-256 of decoded RGB bytes as any training or validation row.",
        "model_lock_sha256": args.model_lock_sha256,
        "amended_evaluator_sha256": digest(Path(__file__)),
        "official_test_rows": len(labels),
        "eligible_test_rows": len(included),
        "excluded_rows": excluded,
    }
    evidence_path = args.output_dir / "protocol_amendment.json"
    if evidence_path.exists():
        if json.loads(evidence_path.read_text()) != evidence:
            raise ValueError("Existing amendment differs from this audit.")
    else:
        write_json(evidence_path, evidence)
    print(f"Excluded {len(excluded)} test rows before inference; scoring {len(included)} eligible rows", flush=True)
    metadata = [metadata[index] for index in included]
    labels = labels[included]
    from tensorflow import keras

    model = keras.models.load_model(model_path, compile=False)
    n = len(labels)
    scores = np.empty(n, dtype=np.float64)
    batch_size = int(manifest["training"]["batch_size"])
    with h5py.File(args.data_dir / descriptors["images"]["path"], "r") as handle:
        images = handle["x"]
        for start in range(0, n, batch_size):
            stop = min(start + batch_size, n)
            scores[start:stop] = np.asarray(model(images[included[start:stop]], training=False)).reshape(-1)
    if not (np.isfinite(scores).all() and ((scores >= 0) & (scores <= 1)).all()):
        raise ValueError("Model produced invalid probability scores")

    groups = np.asarray([row[0] for row in metadata])
    per_slide = group_results(labels, scores, threshold, groups)
    metrics = summarize(labels, scores, threshold)
    intervals = cluster_intervals(labels, scores, threshold, groups)
    first_row_at_location = {}
    for index, location in enumerate(metadata):
        first_row_at_location.setdefault(location, index)
    unique_rows = np.asarray(list(first_row_at_location.values()))
    macro = {}
    for key in ("roc_auc", "specificity", "sensitivity"):
        values = [row[key] for row in per_slide.values() if row[key] is not None]
        macro[key] = {"value": float(np.mean(values)) if values else None, "slides": len(values)}

    predictions = args.output_dir / "predictions.csv"
    temporary = predictions.with_suffix(".csv.partial")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["official_row", "slide", "coord_x", "coord_y", "label", "score", "predicted_label"])
        for index, (slide, x, y), label, score in zip(included, metadata, labels, scores):
            writer.writerow([index, slide, x, y, int(label), float(score), int(score >= threshold)])
    temporary.replace(predictions)
    write_json(args.output_dir / "results.json", {
        "cohort": "Official PCam test rows after exact pixel overlap exclusion",
        "excluded_test_rows": len(excluded),
        "historical_exposure": "Test-designated PCam data were used in Pilot Model 0.",
        "cluster_unit": "source slide; patient identifiers unavailable in official patch metadata",
        "model_lock_sha256": args.model_lock_sha256,
        "predictions_sha256": digest(predictions),
        "threshold": threshold,
        "test_integrity": counts,
        "pooled": metrics,
        "one_row_per_source_location": summarize(labels[unique_rows], scores[unique_rows], threshold),
        "slide_cluster_intervals": intervals,
        "equal_slide": macro,
        "per_slide": per_slide,
    })
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
