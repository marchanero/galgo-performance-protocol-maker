"""DLinear: Trend-seasonal decomposition with linear layers.

Zeng et al., "Are Transformers Effective for Time Series Forecasting?"
AAAI 2023.

Key mechanisms:
  - Moving average decomposition: trend (moving avg) + seasonal (residual)
  - Independent single-layer linear networks per component
  - Fusion via summation before softmax classifier
  - Complexity: O(L) with minimal parameters

This is the efficiency baseline: tests whether linear decomposition
captures sufficient discriminative information from EDA signals.
"""

import torch
import torch.nn as nn
from scripts.utils import SeriesDecomposition


class DLinear(nn.Module):
    """DLinear for EDA arousal classification.

    Decomposes input into trend and seasonal, applies linear projection
    to each, and fuses for classification.
    """

    def __init__(
        self,
        n_channels: int = 3,
        seq_len: int = 160,
        moving_avg_kernel: int = 25,
        n_classes: int = 2,
    ):
        super().__init__()
        self.n_channels = n_channels
        self.seq_len = seq_len

        self.decomposition = SeriesDecomposition(moving_avg_kernel)

        # One linear layer per component, per channel
        seasonal_dim = n_channels * seq_len
        self.Linear_Seasonal = nn.Linear(seasonal_dim, n_classes)
        self.Linear_Trend = nn.Linear(seasonal_dim, n_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, L, C)"""
        seasonal, trend = self.decomposition(x)

        seasonal_flat = seasonal.reshape(x.shape[0], -1)
        trend_flat = trend.reshape(x.shape[0], -1)

        seasonal_out = self.Linear_Seasonal(seasonal_flat)
        trend_out = self.Linear_Trend(trend_flat)

        return seasonal_out + trend_out
