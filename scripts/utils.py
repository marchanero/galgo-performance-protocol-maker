"""Shared utilities for the EDA classification pipeline."""

import torch
import torch.nn as nn
import numpy as np
from typing import Optional, Tuple


def set_seed(seed: int = 42) -> None:
    """Set random seed for reproducibility."""
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)


def get_device() -> torch.device:
    """Get the best available device."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


class RevIN(nn.Module):
    """Reversible Instance Normalization (Kim et al., ICLR 2022).

    Normalises each input instance to zero mean and unit variance,
    then applies affine transformation. The inverse transform is
    applied to restore original statistics for forecasting tasks;
    for classification, only the forward normalisation is used.
    """

    def __init__(self, num_features: int, eps: float = 1e-5, affine: bool = True):
        super().__init__()
        self.eps = eps
        self.affine = affine
        if affine:
            self.affine_weight = nn.Parameter(torch.ones(num_features))
            self.affine_bias = nn.Parameter(torch.zeros(num_features))

    def forward(self, x: torch.Tensor, mode: str = "norm") -> torch.Tensor:
        """x: (batch, seq_len, n_channels)"""
        if mode == "norm":
            self._last_mean = x.mean(dim=1, keepdim=True)
            self._last_std = x.std(dim=1, keepdim=True, unbiased=False) + self.eps
            x = (x - self._last_mean) / self._last_std
            if self.affine:
                x = x * self.affine_weight + self.affine_bias
            return x
        elif mode == "denorm":
            if self.affine:
                x = (x - self.affine_bias) / (self.affine_weight + self.eps)
            x = x * self._last_std + self._last_mean
            return x
        else:
            raise ValueError(f"Unknown mode: {mode}")


class MovingAverage(nn.Module):
    """Moving average for trend-seasonal decomposition."""

    def __init__(self, kernel_size: int, stride: int = 1):
        super().__init__()
        self.kernel_size = kernel_size
        self.avg = nn.AvgPool1d(kernel_size=kernel_size, stride=stride, padding=0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (batch, seq_len, channels)"""
        padding_left = (self.kernel_size - 1) // 2
        padding_right = self.kernel_size - 1 - padding_left
        front = x[:, :1, :].repeat(1, padding_left, 1)
        end = x[:, -1:, :].repeat(1, padding_right, 1)
        x_padded = torch.cat([front, x, end], dim=1)
        x_padded = x_padded.permute(0, 2, 1)
        x_padded = self.avg(x_padded)
        return x_padded.permute(0, 2, 1)


class SeriesDecomposition(nn.Module):
    """Decompose time series into trend (moving average) and seasonal (residual)."""

    def __init__(self, kernel_size: int):
        super().__init__()
        self.moving_avg = MovingAverage(kernel_size, stride=1)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """x: (batch, seq_len, channels) -> (seasonal, trend)"""
        trend = self.moving_avg(x)
        seasonal = x - trend
        return seasonal, trend


class PositionalEncoding(nn.Module):
    """Sinusoidal positional encoding."""

    def __init__(self, d_model: int, max_len: int = 5000, dropout: float = 0.1):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-np.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (batch, seq_len, d_model)"""
        x = x + self.pe[:, : x.size(1), :]
        return self.dropout(x)


class TokenEmbedding(nn.Module):
    """Linear projection of input features to model dimension."""

    def __init__(self, c_in: int, d_model: int):
        super().__init__()
        self.token_conv = nn.Conv1d(
            in_channels=c_in, out_channels=d_model,
            kernel_size=3, padding=1, padding_mode="circular"
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (batch, seq_len, channels) -> (batch, seq_len, d_model)"""
        x = self.token_conv(x.permute(0, 2, 1)).transpose(1, 2)
        return x


class DataEmbedding(nn.Module):
    """Combined token + positional embedding."""

    def __init__(self, c_in: int, d_model: int, dropout: float = 0.1):
        super().__init__()
        self.token_embedding = TokenEmbedding(c_in, d_model)
        self.positional_encoding = PositionalEncoding(d_model, dropout=dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.positional_encoding(self.token_embedding(x))
