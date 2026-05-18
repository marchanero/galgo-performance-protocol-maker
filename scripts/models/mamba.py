"""Mamba (Bi-Mamba): Selective state space model for EDA classification.

Gu & Dao, "Mamba: Linear-Time Sequence Modeling with Selective State Spaces,"
arXiv:2312.00752, 2023.

Bidirectional configuration inspired by ECGMamba:
  - Forward and backward Mamba blocks with concatenated outputs
  - Selective SSM with input-dependent parameters (B, C, Δ)
  - Hardware-aware parallel scan algorithm
  - Complexity: O(L)

Note: This implementation uses a pure-PyTorch selective scan when the
`mamba-ssm` CUDA package is not available. For GPU acceleration, install:
  pip install mamba-ssm causal-conv1d
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class SelectiveSSM(nn.Module):
    """Pure-PyTorch selective state space model.

    Implements the selective scan algorithm:
      h_t = A_bar * h_{t-1} + B_bar * x_t
      y_t = C_t^T * h_t + D * x_t
    """

    def __init__(self, d_model: int, d_state: int = 16, d_conv: int = 4, expand: int = 2):
        super().__init__()
        self.d_model = d_model
        self.d_inner = int(expand * d_model)
        self.d_state = d_state
        self.d_conv = d_conv

        # Input projection: x → (x, z) gating branch
        self.in_proj = nn.Linear(d_model, 2 * self.d_inner)

        # Depthwise 1D convolution for local context
        self.conv1d = nn.Conv1d(
            self.d_inner, self.d_inner, kernel_size=d_conv,
            groups=self.d_inner, padding=d_conv - 1,
        )

        # x_proj: produces Δ, B, C
        self.x_proj = nn.Linear(self.d_inner, d_state * 2 + 1)  # Δ, B, C

        # Learnable A (diagonal state matrix, S4D init)
        A = torch.arange(1, d_state + 1, dtype=torch.float32)
        self.A_log = nn.Parameter(torch.log(A))

        # D skip connection
        self.D = nn.Parameter(torch.ones(self.d_inner))

        # Output projection
        self.out_proj = nn.Linear(self.d_inner, d_model)

    def _selective_scan(self, u: torch.Tensor, delta: torch.Tensor,
                        A: torch.Tensor, B: torch.Tensor, C: torch.Tensor,
                        D: torch.Tensor) -> torch.Tensor:
        """Sequential scan: O(B * D * L)."""
        B_batch, D_inner, L = u.shape
        N = A.shape[-1]

        A_bar = -torch.exp(A)  # (D_inner, N)

        h = torch.zeros(B_batch, D_inner, N, device=u.device)
        y = torch.zeros(B_batch, D_inner, L, device=u.device)

        for t in range(L):
            dt = F.softplus(delta[:, :, t])
            discretized_A = torch.exp(dt.unsqueeze(-1) * A_bar)
            discretized_B = dt.unsqueeze(-1) * B[:, :, t].unsqueeze(-1)

            h = discretized_A * h + discretized_B * u[:, :, t].unsqueeze(-1)
            y[:, :, t] = (h * C[:, :, t].unsqueeze(-1)).sum(-1)

        y = y + D.unsqueeze(0).unsqueeze(-1) * u
        return y

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, L, D)"""
        B, L, D = x.shape

        # Input projection
        xz = self.in_proj(x)  # (B, L, 2*d_inner)
        x_in, z = xz.chunk(2, dim=-1)

        # Convolution (causal padding, trim extra)
        x_conv = x_in.permute(0, 2, 1)  # (B, d_inner, L)
        x_conv = F.silu(self.conv1d(x_conv)[:, :, :L])

        # Project to Δ, B, C
        x_proj_out = self.x_proj(x_conv.permute(0, 2, 1))  # (B, L, d_state*2+1)
        x_proj_out = x_proj_out.permute(0, 2, 1)  # (B, d_state*2+1, L)
        delta, B_state, C_state = x_proj_out.split([1, self.d_state, self.d_state], dim=1)

        # Selective scan
        A_broadcast = self.A_log.unsqueeze(0).expand(self.d_inner, -1)
        y = self._selective_scan(
            x_conv, delta, A_broadcast, B_state, C_state, self.D,
        )

        # Gate and output
        y = y.permute(0, 2, 1)  # (B, L, d_inner)
        y = y * F.silu(z)
        y = self.out_proj(y)

        return y


class BiMambaBlock(nn.Module):
    """Bidirectional Mamba block (Vim-style stacking)."""

    def __init__(self, d_model: int, d_state: int = 16, d_conv: int = 4, expand: int = 2):
        super().__init__()
        self.mamba_fwd = SelectiveSSM(d_model, d_state, d_conv, expand)
        self.mamba_bwd = SelectiveSSM(d_model, d_state, d_conv, expand)
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = x
        x_norm = self.norm(x)

        x_fwd = self.mamba_fwd(x_norm)
        x_bwd = self.mamba_bwd(x_norm.flip([1])).flip([1])

        return residual + x_fwd + x_bwd


class Mamba(nn.Module):
    """Bi-Mamba for EDA arousal classification.

    Bidirectional configuration: forward + backward Mamba blocks with
    concatenated outputs, inspired by ECGMamba.
    """

    def __init__(
        self,
        n_channels: int = 3,
        seq_len: int = 160,
        d_model: int = 128,
        n_layers: int = 4,
        d_state: int = 16,
        d_conv: int = 4,
        expand: int = 2,
        n_classes: int = 2,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.embed = nn.Linear(n_channels, d_model)
        self.dropout = nn.Dropout(dropout)

        self.layers = nn.ModuleList([
            BiMambaBlock(d_model, d_state, d_conv, expand)
            for _ in range(n_layers)
        ])

        self.norm = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, n_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.embed(x)
        x = self.dropout(x)

        for layer in self.layers:
            x = layer(x)

        x = self.norm(x)
        x = x.mean(dim=1)
        return self.head(x)
