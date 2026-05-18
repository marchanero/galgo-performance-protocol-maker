"""Statistical significance testing.

Protocol (from paper):
  - Pairwise Wilcoxon signed-rank tests on per-fold F1-score distributions
  - α = 0.05 (conventional threshold)
  - Bonferroni-Holm correction for 28 pairwise comparisons
  - p-values are "descriptive indicators of effect consistency" (LOSO
    violates independence assumption)
"""

import numpy as np
from scipy.stats import wilcoxon
from typing import Dict, List, Tuple


def pairwise_wilcoxon(
    scores: Dict[str, np.ndarray],
    alpha: float = 0.05,
) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """Compute pairwise Wilcoxon signed-rank tests.

    Args:
        scores: Dictionary mapping model name → array of per-fold F1 scores.
        alpha: Significance threshold.

    Returns:
        Tuple of (p_value_matrix, significant_matrix, model_names).
    """
    model_names = list(scores.keys())
    n = len(model_names)

    p_values = np.ones((n, n))
    significant = np.zeros((n, n), dtype=bool)

    for i in range(n):
        for j in range(i + 1, n):
            a = scores[model_names[i]]
            b = scores[model_names[j]]

            if len(a) != len(b):
                continue

            # Wilcoxon signed-rank (two-sided)
            diff = a - b
            diff = diff[np.abs(diff) > 1e-10]

            if len(diff) == 0:
                p_values[i, j] = p_values[j, i] = 1.0
                continue

            try:
                _, p = wilcoxon(a, b, alternative="two-sided")
                p_values[i, j] = p_values[j, i] = p
                significant[i, j] = significant[j, i] = (p < alpha)
            except ValueError:
                p_values[i, j] = p_values[j, i] = 1.0

    return p_values, significant, model_names


def bonferroni_holm_correction(
    p_values: List[float],
    alpha: float = 0.05,
) -> Tuple[List[bool], List[float]]:
    """Apply Bonferroni-Holm correction for multiple comparisons.

    Args:
        p_values: List of p-values from pairwise comparisons.
        alpha: Significance threshold.

    Returns:
        Tuple of (rejected, corrected_thresholds).
    """
    try:
        from statsmodels.stats.multitest import multipletests
        rejected, corrected_p, _, _ = multipletests(
            p_values, alpha=alpha, method="holm",
        )
        return rejected.tolist(), corrected_p.tolist()
    except ImportError:
        # Manual Bonferroni-Holm
        n = len(p_values)
        sorted_indices = np.argsort(p_values)
        sorted_p = np.array(p_values)[sorted_indices]

        thresholds = alpha / (n - np.arange(n))
        rejected_manual = np.zeros(n, dtype=bool)
        corrected_manual = np.array(p_values) * n

        for k in range(n):
            if sorted_p[k] < thresholds[k]:
                rejected_manual[sorted_indices[k]] = True
                k_max = k
            else:
                break
        else:
            k_max = n - 1

        # All tests with higher p also rejected up to k_max
        for k in range(k_max + 1):
            rejected_manual[sorted_indices[k]] = True

        corrected_manual = np.minimum(corrected_manual, 1.0)
        return rejected_manual.tolist(), corrected_manual.tolist()


def compute_pairwise_significance_matrix(
    scores: Dict[str, np.ndarray],
    alpha: float = 0.05,
    apply_bh: bool = True,
) -> Dict:
    """Compute full pairwise significance matrix with corrections.

    Args:
        scores: Model → per-fold F1 array.
        alpha: Raw significance threshold.
        apply_bh: Whether to apply Bonferroni-Holm correction.

    Returns:
        Dictionary with raw_p_values, bh_corrected_significant, etc.
    """
    model_names = list(scores.keys())
    n = len(model_names)

    p_values, raw_significant, names = pairwise_wilcoxon(scores, alpha)

    # Extract upper triangle p-values for BH correction
    p_list = []
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            p_list.append(p_values[i, j])
            pairs.append((names[i], names[j]))

    result = {
        "model_names": model_names,
        "p_values": p_values.tolist(),
        "raw_significant": raw_significant.tolist(),
        "n_comparisons": len(p_list),
    }

    if apply_bh:
        rejected, corrected_p = bonferroni_holm_correction(
            p_list, alpha,
        )
        result["bh_rejected"] = rejected
        result["bh_corrected_p"] = corrected_p
        result["bh_threshold"] = alpha / len(p_list)
        result["pairs"] = pairs

    return result
