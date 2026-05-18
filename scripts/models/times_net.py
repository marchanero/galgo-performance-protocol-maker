"""TimesNet: FFT-based 1D→2D transformation + Inception blocks.

Wu et al., "TimesNet: Temporal 2D-Variation Modeling for General Time
Series Analysis," ICLR 2023.

Key mechanisms:
  - FFT period detection: discovers dominant periods from frequency domain
  - 1D→2D reshape: folds the sequence along discovered periods
  - Multi-scale Inception blocks with 2D convolutions
  - Complexity: O(L log L)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from scripts.utils import DataEmbedding


class InceptionBlock(nn.Module):
    """Multi-scale 2D convolutional Inception block.

    Applies parallel Conv2d layers with kernel sizes 1, 3, 5, 7, 9, 11
    and averages their outputs (parameter-efficient design).
    """

    def __init__(self, in_channels: int, out_channels: int, num_kernels: int = 6):
        super().__init__()
        self.kernels = nn.ModuleList([
            nn.Conv2d(in_channels, out_channels, kernel_size=2 * i + 1, padding=i)
            for i in range(num_kernels)
        ])

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, C, H, W)"""
        outs = [kernel(x) for kernel in self.kernels]
        return torch.stack(outs, dim=-1).mean(-1)


class TimesBlock(nn.Module):
    """Single TimesNet block: FFT → 1D→2D → Inception → 2D→1D."""

    def __init__(self, d_model: int, d_ff: int, top_k: int = 5, num_kernels: int = 6):
        super().__init__()
        self.top_k = top_k
        self.conv = nn.Sequential(
            InceptionBlock(d_model, d_ff, num_kernels),
            nn.GELU(),
            InceptionBlock(d_ff, d_model, num_kernels),
        )
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, T, d_model)"""
        B, T, N = x.shape
        residual = x

        # FFT period detection
        xf = torch.fft.rfft(x, dim=1)
        frequency_list = xf.abs().mean(0).mean(-1)
        frequency_list[0] = 0  # ignore DC
        _, top_list = torch.topk(frequency_list, self.top_k)
        periods = T // (top_list + 1e-8)
        periods = periods.long().clamp(min=2, max=T // 2)

        # Process each period
        res_list = []
        for i in range(self.top_k):
            period = periods[i].item()
            if period < 2:
                continue

            # Pad to multiple of period
            length = ((T + period - 1) // period) * period
            padding = torch.zeros(B, length - T, N, device=x.device)
            out = torch.cat([x, padding], dim=1)

            # 1D → 2D
            out = out.reshape(B, length // period, period, N)
            out = out.permute(0, 3, 1, 2)  # (B, N, H, W)

            # Inception convolution
            out = self.conv(out)

            # 2D → 1D
            out = out.permute(0, 2, 3, 1).reshape(B, -1, N)
            res_list.append(out[:, :T, :])

        if res_list:
            res = torch.stack(res_list, dim=-1).mean(-1)
        else:
            res = torch.zeros_like(x)

        return self.norm(residual + res)


class TimesNet(nn.Module):
    """TimesNet for EDA arousal classification."""

    def __init__(
        self,
        n_channels: int = 3,
        seq_len: int = 160,
        d_model: int = 64,
        n_layers: int = 2,
        d_ff: int = 128,
        top_k: int = 5,
        num_kernels: int = 6,
        n_classes: int = 2,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.embedding = DataEmbedding(n_channels, d_model, dropout)
        self.blocks = nn.ModuleList([
            TimesBlock(d_model, d_ff, top_k, num_kernels)
            for _ in range(n_layers)
        ])
        self.norm = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
        self.projection = nn.Linear(d_model * seq_len, n_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.embedding(x)
        for block in self.blocks:
            x = block(x)
        x = self.norm(x)
        x = F.gelu(x)
        x = self.dropout(x)
        x = x.reshape(x.shape[0], -1)
        return self.projection(x)
