"""Channel ablation: quantify marginal contribution of derivative channels.

Protocol:
  (i)   SCR only
  (ii)  SCR + ΔSCR
  (iii) SCR + ΔSCR + Δ²SCR

Evaluated under the same LOSO framework for each architecture.
"""

import numpy as np
from typing import Dict, List, Callable
import torch.nn as nn

from scripts.training.loso import create_loso_folds, prepare_loso_fold
from scripts.training.trainer import train_model, evaluate
from scripts.evaluation.metrics import compute_classification_metrics
from scripts.utils import get_device
from torch.utils.data import DataLoader, TensorDataset
import torch


def run_channel_ablation(
    model_factory: Callable[[int], nn.Module],
    X_full: np.ndarray,
    y: np.ndarray,
    subject_ids: np.ndarray,
    n_folds: int = 147,
    batch_size: int = 32,
    device: torch.device = None,
    verbose: bool = True,
) -> Dict[str, Dict[str, float]]:
    """Run channel ablation across LOSO folds.

    Args:
        model_factory: Function(n_channels) → model instance.
        X_full: (n_samples, 3, seq_len) — full 3-channel data.
        y: Labels.
        subject_ids: Per-sample subject IDs.
        n_folds: Number of LOSO folds.
        batch_size: Training batch size.
        device: Compute device.
        verbose: Print progress.

    Returns:
        Dictionary mapping channel_config → aggregated metrics.
    """
    if device is None:
        device = get_device()

    channel_configs = {
        "SCR_only": [0],
        "SCR_delta": [0, 1],
        "SCR_delta_delta2": [0, 1, 2],
    }

    results = {}

    for config_name, channel_indices in channel_configs.items():
        if verbose:
            print(f"\n=== Channel ablation: {config_name} ===")

        n_channels = len(channel_indices)
        X = X_full[:, channel_indices, :]

        fold_metrics = []
        fold_generator = create_loso_folds(subject_ids)

        for fold_idx, (train_idx, val_idx, test_idx) in enumerate(fold_generator):
            if fold_idx >= n_folds:
                break

            fold_data = prepare_loso_fold(X, y, train_idx, val_idx, test_idx)

            model = model_factory(n_channels)

            train_model(
                model,
                fold_data["X_train"], fold_data["y_train"],
                fold_data["X_val"], fold_data["y_val"],
                batch_size=batch_size, device=device, verbose=False,
            )

            test_dataset = TensorDataset(
                torch.FloatTensor(fold_data["X_test"]),
                torch.LongTensor(fold_data["y_test"]),
            )
            test_loader = DataLoader(test_dataset, batch_size=batch_size)
            criterion = nn.CrossEntropyLoss()
            eval_result = evaluate(model, test_loader, criterion, device)

            metrics = compute_classification_metrics(
                eval_result["labels"], eval_result["predictions"],
                eval_result["probabilities"],
            )
            fold_metrics.append(metrics)

            if verbose and (fold_idx + 1) % 20 == 0:
                current_f1 = np.mean([m["f1"] for m in fold_metrics])
                print(f"  Fold {fold_idx + 1}/{n_folds}, F1 = {current_f1:.4f}")

        # Aggregate
        aggregated = {}
        for name in fold_metrics[0].keys():
            values = np.array([m[name] for m in fold_metrics])
            aggregated[name] = {
                "mean": float(np.mean(values)),
                "std": float(np.std(values)),
            }

        results[config_name] = aggregated

        if verbose:
            print(f"  {config_name}: F1 = {aggregated['f1']['mean']:.4f} ± {aggregated['f1']['std']:.4f}")

    return results
