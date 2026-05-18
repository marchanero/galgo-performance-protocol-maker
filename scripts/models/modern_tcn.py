"""ModernTCN: Modernised convolutions with large kernels and inverted bottlenecks.

Luo & Wang, "ModernTCN: A Modern Pure Convolution Structure for General
Time Series Analysis," ICLR 2024.

Key mechanisms:
  - Depthwise separable convolutions with inverted bottlenecks
  - Large kernels (up to k=51) for wide receptive fields
  - Adjacent connection scheme preserving multi-scale features
  - Squeeze-and-Excitation channel attention
  - Complexity: O(L)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from scripts.utils import RevIN


class SEBlock(nn.Module):
    """Squeeze-and-Excitation channel attention."""

    def __init__(self, channels: int, reduction: int = 16):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(channels, channels // reduction),
            nn.ReLU(),
            nn.Linear(channels // reduction, channels),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, C, L)"""
        B, C, L = x.shape
        y = x.mean(dim=-1)  # global average pooling
        y = self.fc(y).unsqueeze(-1)
        return x * y


class DepthwiseConvBN(nn.Module):
    """Depthwise convolution + BatchNorm for ModernTCN block.

    Uses large kernel size for wide receptive field.
    """

    def __init__(self, in_channels: int, out_channels: int, kernel_size: int,
                 groups: int, stride: int = 1):
        super().__init__()
        self.conv = nn.Conv1d(
            in_channels, out_channels, kernel_size=kernel_size,
            stride=stride, padding=kernel_size // 2, groups=groups,
            bias=False,
        )
        self.bn = nn.BatchNorm1d(out_channels)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.bn(self.conv(x))


class ModernTCNBlock(nn.Module):
    """Single ModernTCN block with dual FFN structure.

    Operates on 4D tensor: (B, n_vars, d_model, patch_num).
    """

    def __init__(
        self,
        n_vars: int,
        d_model: int,
        kernel_size: int = 51,
        ffn_ratio: int = 1,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.n_vars = n_vars
        self.d_model = d_model
        d_ff = d_model * ffn_ratio

        # Depthwise conv: groups = n_vars * d_model
        total_groups = n_vars * d_model
        total_channels = total_groups

        self.dwconv = nn.Sequential(
            nn.Conv1d(total_channels, total_channels, kernel_size=kernel_size,
                      padding=kernel_size // 2, groups=total_groups, bias=False),
            nn.BatchNorm1d(total_channels),
        )

        # SE attention
        self.se = SEBlock(total_channels)

        # FFN1: per-variable (groups=n_vars)
        self.ffn1_pw1 = nn.Conv1d(total_channels, n_vars * d_ff, kernel_size=1,
                                   groups=n_vars)
        self.ffn1_pw2 = nn.Conv1d(n_vars * d_ff, total_channels, kernel_size=1,
                                   groups=n_vars)

        # FFN2: per-channel (groups=d_model)
        self.ffn2_pw1 = nn.Conv1d(total_channels, d_model * d_ff, kernel_size=1,
                                   groups=d_model)
        self.ffn2_pw2 = nn.Conv1d(d_model * d_ff, total_channels, kernel_size=1,
                                   groups=d_model)

        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, n_vars, d_model, patch_num)"""
        B, M, D, N = x.shape
        residual = x

        # DWConv
        x = x.reshape(B, M * D, N)
        x = self.se(self.dwconv(x))

        # FFN1: per-variable processing
        x = self.ffn1_pw1(x)
        x = F.gelu(x)
        x = self.dropout(x)
        x = self.ffn1_pw2(x)

        # FFN2: per-channel processing
        x = x.reshape(B, M, D, N)
        x = x.permute(0, 2, 1, 3)  # (B, D, M, N)
        x = x.reshape(B, D * M, N)

        x = self.ffn2_pw1(x)
        x = F.gelu(x)
        x = self.dropout(x)
        x = self.ffn2_pw2(x)

        x = x.reshape(B, D, M, N).permute(0, 2, 1, 3)  # (B, M, D, N)
        x = x.reshape(B, M, D, N)

        return self.dropout(x) + residual


class ModernTCN(nn.Module):
    """ModernTCN for EDA arousal classification.

    Uses a simplified architecture suitable for 3-channel EDA input:
      - Stem convolution for patching
      - Stack of ModernTCN blocks
      - Global pooling + classification head
    """

    def __init__(
        self,
        n_channels: int = 3,
        seq_len: int = 160,
        patch_size: int = 16,
        patch_stride: int = 8,
        d_model: int = 64,
        n_layers: int = 4,
        kernel_size: int = 51,
        ffn_ratio: int = 1,
        n_classes: int = 2,
        dropout: float = 0.1,
        revin: bool = True,
    ):
        super().__init__()
        self.n_channels = n_channels
        self.d_model = d_model

        patch_num = int((seq_len - patch_size) / patch_stride + 1)

        self.revin = RevIN(n_channels) if revin else None

        # Stem: project each channel independently to d_model via patching
        self.stem = nn.Conv1d(
            n_channels, n_channels * d_model,
            kernel_size=patch_size, stride=patch_stride,
        )

        self.blocks = nn.ModuleList([
            ModernTCNBlock(n_channels, d_model, kernel_size, ffn_ratio, dropout)
            for _ in range(n_layers)
        ])

        self.act = nn.GELU()
        self.dropout = nn.Dropout(dropout)
        self.flatten_dim = n_channels * d_model * patch_num

        self.head = nn.Linear(self.flatten_dim, n_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, L, C)"""
        if self.revin is not None:
            x = self.revin(x, mode="norm")

        x = x.permute(0, 2, 1)  # (B, C, L)

        # Stem convolution: (B, C, L) → (B, C*d_model, patch_num)
        x = self.stem(x)

        B, CD, N = x.shape
        C = self.n_channels
        D = self.d_model
        x = x.reshape(B, C, D, N)

        for block in self.blocks:
            x = block(x)

        x = self.act(x)
        x = self.dropout(x)
        x = x.reshape(B, -1)  # flatten

        return self.head(x)
