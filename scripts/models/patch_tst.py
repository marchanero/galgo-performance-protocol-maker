"""PatchTST: Channel-independent patching + Transformer encoder.

Nie et al., "A Time Series is Worth 64 Words: Long-term Forecasting with
Transformers," ICLR 2023.

Key mechanisms:
  - Patch tokenisation: segments each channel into non-overlapping patches
  - Channel-independent encoding: all channels share Transformer weights
  - Global average pooling before classification head
"""

import torch
import torch.nn as nn
from scripts.utils import RevIN


class PatchTSTEncoder(nn.Module):
    """Transformer encoder for channel-independent patch processing."""

    def __init__(self, d_model: int, n_heads: int, d_ff: int, dropout: float):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(
            d_model, n_heads, dropout=dropout, batch_first=True
        )
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        attn_out, _ = self.self_attn(x, x, x)
        x = self.norm1(x + attn_out)
        ffn_out = self.ffn(x)
        x = self.norm2(x + ffn_out)
        return x


class PatchTST(nn.Module):
    """PatchTST for EDA arousal classification."""

    def __init__(
        self,
        n_channels: int = 3,
        seq_len: int = 160,
        patch_len: int = 16,
        stride: int = 8,
        d_model: int = 128,
        n_heads: int = 16,
        n_layers: int = 3,
        d_ff: int = 256,
        n_classes: int = 2,
        dropout: float = 0.2,
        head_dropout: float = 0.0,
        revin: bool = True,
    ):
        super().__init__()
        self.n_channels = n_channels
        self.patch_len = patch_len
        self.stride = stride
        self.d_model = d_model

        patch_num = int((seq_len - patch_len) / stride + 1)

        self.revin = RevIN(n_channels) if revin else None
        self.w_p = nn.Linear(patch_len, d_model)
        self.pos_embed = nn.Parameter(torch.randn(1, patch_num, d_model) * 0.02)

        self.encoder = nn.ModuleList([
            PatchTSTEncoder(d_model, n_heads, d_ff, dropout)
            for _ in range(n_layers)
        ])

        self.dropout = nn.Dropout(head_dropout)
        self.flatten_dim = d_model * patch_num
        self.head = nn.Linear(self.flatten_dim, n_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (batch, seq_len, n_channels)"""
        # RevIN
        if self.revin is not None:
            x = self.revin(x, mode="norm")

        x = x.permute(0, 2, 1)  # (B, C, L)

        # Patching: (B, C, P, N)
        x = x.unfold(dimension=-1, size=self.patch_len, step=self.stride)

        # Linear projection per channel (shared weights)
        x = self.w_p(x)  # (B, C, N, D)

        # Flatten batch and channel dims for shared Transformer
        B, C, N, D = x.shape
        x = x.reshape(B * C, N, D)
        x = x + self.pos_embed

        # Transformer encoder
        for layer in self.encoder:
            x = layer(x)

        # Unflatten and global average pooling
        x = x.reshape(B, C, N, D)
        x = x.mean(dim=1)  # mean over channels
        x = x.reshape(B, -1)  # (B, N * D)

        x = self.dropout(x)
        return self.head(x)
