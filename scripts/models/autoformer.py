"""Autoformer: Auto-Correlation mechanism + progressive decomposition.

Wu et al., "Autoformer: Decomposition Transformers with Auto-Correlation
for Long-Term Series Forecasting," NeurIPS 2021.

Key mechanisms:
  - Auto-Correlation: discovers dominant periodicities via FFT
  - Time-delay aggregation: rolls and aggregates top-k correlated lags
  - Progressive seasonal-trend decomposition after each layer
  - Complexity: O(L log L)
"""

import math
import torch
import torch.nn as nn
from scripts.utils import DataEmbedding, SeriesDecomposition


class AutoCorrelation(nn.Module):
    """Auto-Correlation mechanism using FFT-based period discovery."""

    def __init__(self, factor: int = 1, dropout: float = 0.1):
        super().__init__()
        self.factor = factor
        self.dropout = nn.Dropout(dropout)

    def forward(self, q: torch.Tensor, k: torch.Tensor, v: torch.Tensor):
        """q, k, v: (B, L, D)"""
        B, L, D = q.shape

        # FFT-based correlation
        q_ft = torch.fft.rfft(q.permute(0, 2, 1).contiguous(), dim=-1)
        k_ft = torch.fft.rfft(k.permute(0, 2, 1).contiguous(), dim=-1)
        res = q_ft * k_ft.conj()  # cross-correlation via Wiener-Khinchin
        corr = torch.fft.irfft(res, n=L, dim=-1)  # (B, D, L)

        # Top-k lags
        top_k = int(self.factor * math.log(L))
        weights = torch.topk(corr, top_k, dim=-1)
        # weights: (values, indices) where indices are lag positions
        tmp_corr = torch.softmax(weights.values, dim=-1)

        # Time-delay aggregation
        delays_agg = torch.zeros_like(v)
        v_padded = v.permute(0, 2, 1)  # (B, D, L)

        for i in range(top_k):
            lag = weights.indices[..., i]
            pattern = torch.zeros_like(v_padded)
            for b in range(B):
                for d_idx in range(D):
                    shift = lag[b, d_idx].item()
                    if shift > 0:
                        pattern[b, d_idx, :-shift] = v_padded[b, d_idx, shift:]
                    elif shift < 0:
                        pattern[b, d_idx, -shift:] = v_padded[b, d_idx, :shift]
                    else:
                        pattern[b, d_idx] = v_padded[b, d_idx]
            delays_agg = delays_agg + pattern.permute(0, 2, 1) * tmp_corr[..., i].unsqueeze(-1)

        return delays_agg


class AutoformerEncoderLayer(nn.Module):
    """Autoformer encoder layer: Auto-Correlation + FFN + decomposition."""

    def __init__(self, d_model: int, d_ff: int, moving_avg_kernel: int, dropout: float = 0.1):
        super().__init__()
        self.auto_correlation = AutoCorrelation(factor=1, dropout=dropout)
        self.decomp1 = SeriesDecomposition(moving_avg_kernel)
        self.decomp2 = SeriesDecomposition(moving_avg_kernel)
        self.dropout = nn.Dropout(dropout)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout),
        )

    def forward(self, x: torch.Tensor):
        attn_out = self.auto_correlation(x, x, x)
        x = x + self.dropout(attn_out)
        seasonal, _ = self.decomp1(x)

        ffn_out = self.ffn(seasonal)
        seasonal = seasonal + self.dropout(ffn_out)
        seasonal, _ = self.decomp2(seasonal)

        return seasonal


class Autoformer(nn.Module):
    """Autoformer for EDA arousal classification."""

    def __init__(
        self,
        n_channels: int = 3,
        seq_len: int = 160,
        d_model: int = 128,
        n_heads: int = 8,
        n_layers: int = 2,
        d_ff: int = 256,
        moving_avg_kernel: int = 25,
        n_classes: int = 2,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.embedding = DataEmbedding(n_channels, d_model, dropout)
        self.encoder = nn.ModuleList([
            AutoformerEncoderLayer(d_model, d_ff, moving_avg_kernel, dropout)
            for _ in range(n_layers)
        ])
        self.projection = nn.Linear(d_model, n_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.embedding(x)
        for layer in self.encoder:
            x = layer(x)
        x = x.mean(dim=1)
        return self.projection(x)
