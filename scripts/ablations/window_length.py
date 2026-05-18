"""Window length ablation: minimal temporal interval analysis.

Protocol:
  - Window lengths n from 1 to 40 seconds
  - Two segmentation strategies: non-overlapping and sliding (1s stride)
  - All windows from same subject preserved in same LOSO fold
  - Reference: F1 curve showing rapid improvement up to ~15s, plateau beyond
"""

import numpy as np
from typing import Dict, List, Tuple, Callable
import torch.nn as nn
import torch
from torch.utils.data import DataLoader, TensorDataset

from scripts.data.preprocessing import segment_into_windows
from scripts.training.loso import create_loso_folds, compute_fold_statistics, normalize_fold
from scripts.training.trainer import train_model, evaluate
from scripts.evaluation.metrics import compute_classification_metrics
from scripts.utils import get_device


def run_window_length_ablation(
    model_factory: Callable[[int], nn.Module],
    raw_signal: np.ndarray,
    labels: np.ndarray,
    subject_ids: np.ndarray,
    window_lengths: List[int] = None,
    fs: float = 4.0,
    stride_strategy: str = "non_overlapping",
    n_channels: int = 3,
    n_folds: int = 147,
    batch_size: int = 32,
    device: torch.device = None,
    verbose: bool = True,
) -> Dict[int, Dict[str, float]]:
    """Run window length ablation.

    Args:
        model_factory: Function(seq_len) → model instance.
        raw_signal: Preprocessed 3-channel signal (3, total_samples).
        labels: Labels per window (aligned with windowing output).
        subject_ids: Per-window subject IDs.
        window_lengths: List of window lengths in seconds.
        fs: Sampling frequency (Hz).
        stride_strategy: "non_overlapping" or "sliding".
        n_channels: Number of input channels.
        n_folds: Number of LOSO folds.
        device: Compute device.

    Returns:
        Dict mapping window_length → metrics dict.
    """
    if device is None:
        device = get_device()

    if window_lengths is None:
        window_lengths = list(range(1, 16)) + [20, 25, 30, 35, 40]

    stride_seconds = 1 if stride_strategy == "sliding" else None
    results = {}

    for wl in window_lengths:
        if verbose:
            print(f"\n=== Window length: {wl}s ===")

        seq_len = int(wl * fs)

        # Segment data for this window length
        windows, valid_mask = segment_into_windows(
            raw_signal, window_seconds=wl, fs=fs, stride_seconds=stride_seconds,
        )
        windows = windows[valid_mask]
        wl_labels = labels[valid_mask] if len(labels) == len(valid_mask) else labels[:len(windows)]
        wl_subjects = subject_ids[valid_mask] if len(subject_ids) == len(valid_mask) else subject_ids[:len(windows)]

        model = model_factory(seq_len)

        fold_metrics = []
        fold_generator = create_loso_folds(wl_subjects)

        for fold_idx, (train_idx, val_idx, test_idx) in enumerate(fold_generator):
            if fold_idx >= n_folds:
                break

            mean, std = compute_fold_statistics(windows, train_idx)
            X_train = normalize_fold(windows, train_idx, mean, std)
            X_val = normalize_fold(windows, val_idx, mean, std)
            X_test = normalize_fold(windows, test_idx, mean, std)

            train_model(
                model,
                X_train, wl_labels[train_idx],
                X_val, wl_labels[val_idx],
                batch_size=batch_size, device=device, verbose=False,
            )

            test_dataset = TensorDataset(
                torch.FloatTensor(X_test),
                torch.LongTensor(wl_labels[test_idx]),
            )
            test_loader = DataLoader(test_dataset, batch_size=batch_size)
            criterion = nn.CrossEntropyLoss()
            eval_result = evaluate(model, test_loader, criterion, device)

            metrics = compute_classification_metrics(
                eval_result["labels"], eval_result["predictions"],
                eval_result["probabilities"],
            )
            fold_metrics.append(metrics)

        aggregated = {}
        for name in fold_metrics[0].keys():
            values = np.array([m[name] for m in fold_metrics])
            aggregated[name] = {"mean": float(np.mean(values)), "std": float(np.std(values))}

        results[wl] = aggregated

        if verbose:
            print(f"  {wl}s: F1 = {aggregated['f1']['mean']:.4f} ± {aggregated['f1']['std']:.4f}")

    return results
