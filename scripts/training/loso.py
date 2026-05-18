"""Leave-One-Subject-Out (LOSO) cross-validation.

Protocol (from sanchez2020deep):
  - 147 folds, one participant held out for testing
  - Remaining 146 subjects: 80% training, 20% validation
  - Z-score normalisation using training-fold statistics only
  - All windows belonging to the same subject preserved in the same fold
"""

import numpy as np
from typing import List, Tuple, Dict, Iterator
from sklearn.model_selection import train_test_split


def create_loso_folds(
    subject_ids: np.ndarray,
    val_split: float = 0.2,
    seed: int = 42,
) -> Iterator[Tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """Generate LOSO fold splits.

    Args:
        subject_ids: Array of subject IDs (one per window/sample).
        val_split: Fraction of training subjects to use for validation.
        seed: Random seed for reproducibility.

    Yields:
        (train_indices, val_indices, test_indices) for each fold.
    """
    unique_subjects = np.unique(subject_ids)

    for test_subject in unique_subjects:
        test_mask = subject_ids == test_subject
        train_val_mask = ~test_mask

        test_indices = np.where(test_mask)[0]
        train_val_indices = np.where(train_val_mask)[0]

        # Get unique training subjects
        train_val_subjects = np.unique(subject_ids[train_val_indices])
        train_subjects, val_subjects = train_test_split(
            train_val_subjects, test_size=val_split, random_state=seed,
        )

        train_indices = np.where(np.isin(subject_ids, train_subjects))[0]
        val_indices = np.where(np.isin(subject_ids, val_subjects))[0]

        yield train_indices, val_indices, test_indices


def compute_fold_statistics(
    data: np.ndarray,
    train_indices: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute per-channel mean and std from training data only.

    Args:
        data: Array of shape (n_samples, n_channels, seq_len).
        train_indices: Indices of training samples.

    Returns:
        Tuple of (mean, std) each of shape (n_channels,).
    """
    train_data = data[train_indices]
    # Compute per-channel statistics across samples and timesteps
    mean = train_data.mean(axis=(0, 2))
    std = train_data.std(axis=(0, 2))
    return mean, std


def normalize_fold(
    data: np.ndarray,
    indices: np.ndarray,
    mean: np.ndarray,
    std: np.ndarray,
) -> np.ndarray:
    """Apply Z-score normalisation to fold data using pre-computed statistics.

    Args:
        data: Full data array.
        indices: Indices to normalize.
        mean: Per-channel means from training set.
        std: Per-channel standard deviations from training set.

    Returns:
        Normalized data for the specified indices.
    """
    fold_data = data[indices].copy()
    std = np.maximum(std, 1e-8)
    fold_data = (fold_data - mean.reshape(1, -1, 1)) / std.reshape(1, -1, 1)
    return fold_data


def prepare_loso_fold(
    X: np.ndarray,
    y: np.ndarray,
    train_indices: np.ndarray,
    val_indices: np.ndarray,
    test_indices: np.ndarray,
) -> Dict[str, np.ndarray]:
    """Prepare data for a single LOSO fold with proper normalization.

    Args:
        X: Features of shape (n_samples, n_channels, seq_len).
        y: Labels of shape (n_samples,).
        train_indices: Training sample indices.
        val_indices: Validation sample indices.
        test_indices: Test sample indices.

    Returns:
        Dictionary with X_train, y_train, X_val, y_val, X_test, y_test.
    """
    mean, std = compute_fold_statistics(X, train_indices)

    X_train = normalize_fold(X, train_indices, mean, std)
    X_val = normalize_fold(X, val_indices, mean, std)
    X_test = normalize_fold(X, test_indices, mean, std)

    return {
        "X_train": X_train,
        "y_train": np.asarray(y[train_indices], dtype=np.int64),
        "X_val": X_val,
        "y_val": np.asarray(y[val_indices], dtype=np.int64),
        "X_test": X_test,
        "y_test": np.asarray(y[test_indices], dtype=np.int64),
    }
