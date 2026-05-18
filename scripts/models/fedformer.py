"""FEDformer: Fourier-enhanced attention with random mode selection.

Zhou et al., "FEDformer: Frequency Enhanced Decomposed Transformer for
Long-term Series Forecasting," ICML 2022.

Key mechanisms:
  - Fourier-enhanced attention: computes attention in frequency domain
  - Random Fourier mode selection (M << L)
  - Seasonal-trend decomposition blocks
  - Complexity: O(L)
"""

import torch
import torch.nn as nn
from scripts.utils import DataEmbedding, SeriesDecomposition


class FourierAttention(nn.Module):
    """Frequency-domain attention with random mode selection."""

    def __init__(self, d_model: int, n_heads: int, modes: int = 32, dropout: float = 0.1):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        self.modes = modes

        # Learnable complex weights per head, per mode
        self.weights = nn.Parameter(
            torch.randn(n_heads, self.d_k, self.d_k, modes, dtype=torch.cfloat) * 0.02
        )
        self.dropout = nn.Dropout(dropout)

    def _get_frequency_modes(self, seq_len: int) -> torch.Tensor:
        """Select random frequency modes up to Nyquist limit."""
        modes = min(self.modes, seq_len // 2)
        indices = torch.randperm(seq_len // 2)[:modes]
        return indices.sort()[0]

    def forward(self, q: torch.Tensor, k: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
        """q, k, v: (B, L, D)"""
        B, L, D = q.shape
        H = self.n_heads

        q = q.view(B, L, H, self.d_k).permute(0, 2, 3, 1)  # (B, H, d_k, L)
        k = k.view(B, L, H, self.d_k).permute(0, 2, 3, 1)
        v = v.view(B, L, H, self.d_k).permute(0, 2, 3, 1)

        # FFT
        q_ft = torch.fft.rfft(q, dim=-1)
        k_ft = torch.fft.rfft(k, dim=-1)
        v_ft = torch.fft.rfft(v, dim=-1)

        # Select random modes
        indices = self._get_frequency_modes(L).to(q.device)
        q_ft = q_ft[:, :, :, indices]
        k_ft = k_ft[:, :, :, indices]

        # Frequency-domain attention
        attn_ft = torch.einsum("bhxm,bhym->bhxy", q_ft, k_ft)
        attn_ft = attn_ft.tanh()
        out_ft = torch.einsum("bhxy,bhym->bhxm", attn_ft, v_ft[:, :, :, indices])

        # Weighted output per mode
        out_ft = torch.einsum("bhem,heom->bhom", out_ft, self.weights[:, :, :, :len(indices)])

        # Inverse FFT (scatter back)
        out_ft_full = torch.zeros(B, H, self.d_k, L // 2 + 1, dtype=torch.cfloat, device=q.device)
        out_ft_full[:, :, :, indices] = out_ft
        out = torch.fft.irfft(out_ft_full, n=L, dim=-1)

        out = out.permute(0, 3, 1, 2).contiguous().view(B, L, D)

        return self.dropout(out)


class FEDformerEncoderLayer(nn.Module):
    """FEDformer encoder layer with Fourier attention + decomposition."""

    def __init__(self, d_model: int, n_heads: int, d_ff: int, modes: int,
                 moving_avg_kernel: int, dropout: float = 0.1):
        super().__init__()
        self.attention = FourierAttention(d_model, n_heads, modes, dropout)
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

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        attn_out = self.attention(x, x, x)
        x = x + self.dropout(attn_out)
        seasonal, _ = self.decomp1(x)

        ffn_out = self.ffn(seasonal)
        seasonal = seasonal + self.dropout(ffn_out)
        seasonal, _ = self.decomp2(seasonal)

        return seasonal


class FEDformer(nn.Module):
    """FEDformer for EDA arousal classification."""

    def __init__(
        self,
        n_channels: int = 3,
        seq_len: int = 160,
        d_model: int = 128,
        n_heads: int = 8,
        n_layers: int = 2,
        d_ff: int = 256,
        fourier_modes: int = 32,
        moving_avg_kernel: int = 25,
        n_classes: int = 2,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.embedding = DataEmbedding(n_channels, d_model, dropout)
        self.encoder = nn.ModuleList([
            FEDformerEncoderLayer(d_model, n_heads, d_ff, fourier_modes, moving_avg_kernel, dropout)
            for _ in range(n_layers)
        ])
        self.projection = nn.Linear(d_model, n_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.embedding(x)
        for layer in self.encoder:
            x = layer(x)
        x = x.mean(dim=1)
        return self.projection(x)
