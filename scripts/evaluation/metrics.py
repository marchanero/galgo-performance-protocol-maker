"""Classification metrics for arousal detection.

Metrics (per-fold, then averaged across 147 LOSO folds):
  - Accuracy
  - Precision (macro-averaged)
  - Recall (macro-averaged)
  - F1-score (macro-averaged)
  - AUC-ROC (one-vs-rest)
  - Per-class F1 for calm and stress conditions
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score,
)
from typing import Dict


def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray,
    class_names: list = None,
) -> Dict[str, float]:
    """Compute all classification metrics for a single fold.

    Args:
        y_true: Ground truth labels (n_samples,).
        y_pred: Predicted labels (n_samples,).
        y_prob: Predicted probabilities (n_samples, n_classes).
        class_names: Optional list of class names for per-class metrics.

    Returns:
        Dictionary of metric values.
    """
    if class_names is None:
        class_names = ["calm", "stress"]

    metrics = {}
    metrics["accuracy"] = accuracy_score(y_true, y_pred)
    metrics["precision"] = precision_score(y_true, y_pred, average="macro", zero_division=0)
    metrics["recall"] = recall_score(y_true, y_pred, average="macro", zero_division=0)
    metrics["f1"] = f1_score(y_true, y_pred, average="macro", zero_division=0)

    # AUC (one-vs-rest for binary, handle single-class edge case)
    if y_prob.shape[1] >= 2 and len(np.unique(y_true)) > 1:
        metrics["auc"] = roc_auc_score(y_true, y_prob[:, 1])
    else:
        metrics["auc"] = 0.5

    # Per-class F1
    per_class_f1 = f1_score(y_true, y_pred, average=None, zero_division=0)
    for i, name in enumerate(class_names):
        if i < len(per_class_f1):
            metrics[f"f1_{name}"] = per_class_f1[i]

    return metrics


def aggregate_fold_metrics(
    fold_metrics: list,
) -> Dict[str, Dict[str, float]]:
    """Aggregate metrics across all LOSO folds.

    Args:
        fold_metrics: List of per-fold metric dictionaries.

    Returns:
        Dictionary with mean, std, and per-fold values.
    """
    if not fold_metrics:
        return {}

    metric_names = fold_metrics[0].keys()
    aggregated = {}

    for name in metric_names:
        values = np.array([m[name] for m in fold_metrics])
        aggregated[name] = {
            "mean": float(np.mean(values)),
            "std": float(np.std(values)),
            "per_fold": values.tolist(),
        }

    return aggregated
