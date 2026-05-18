"""Informer: ProbSparse attention + self-attention distilling.

Zhou et al., "Informer: Beyond Efficient Transformer for Long Sequence
Time-Series Forecasting," AAAI 2021.

Key mechanisms:
  - ProbSparse attention selects top-u queries with highest sparsity
  - Self-attention distilling halves sequence length per encoder layer
  - Complexity: O(L log L)
"""

import math
import torch
import torch.nn as nn
from scripts.utils import DataEmbedding


class ProbSparseAttention(nn.Module):
    """ProbSparse self-attention: selects top-u queries via max-mean divergence."""

    def __init__(self, d_model: int, n_heads: int, factor: int = 5, dropout: float = 0.1):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_k = d_model // n_heads
        self.n_heads = n_heads
        self.factor = factor  # sampling factor c

        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)
        self.w_o = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def _prob_qk(self, q: torch.Tensor, k: torch.Tensor, sample_k: int, n_top: int):
        """Sample U_part keys and select top-u queries."""
        B, H, L_Q, D = q.shape
        _, _, L_K, _ = k.shape

        # Randomly sample keys
        idx = torch.randint(0, L_K, (L_Q, sample_k), device=q.device)
        k_sample = k[:, :, idx, :]  # (B, H, L_Q, sample_k, D)

        # Compute sparsity measurement M(q_i, K)
        q_expanded = q.unsqueeze(-2)  # (B, H, L_Q, 1, D)
        qk_sample = torch.matmul(q_expanded, k_sample.transpose(-2, -1)).squeeze(-2)
        m = qk_sample.max(-1)[0] - qk_sample.sum(-1) / L_K  # (B, H, L_Q)

        # Select top-u queries
        m_top = m.topk(n_top, sorted=False)[1]
        q_reduce = torch.gather(q, dim=-2, index=m_top.unsqueeze(-1).expand(-1, -1, -1, D))
        qk = torch.matmul(q_reduce, k.transpose(-2, -1))

        return qk, m_top

    def forward(self, q: torch.Tensor, k: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
        B, L_Q, D = q.shape
        L_K = k.shape[1]

        q = self.w_q(q).view(B, L_Q, self.n_heads, self.d_k).transpose(1, 2)
        k = self.w_k(k).view(B, L_K, self.n_heads, self.d_k).transpose(1, 2)
        v = self.w_v(v).view(B, L_K, self.n_heads, self.d_k).transpose(1, 2)

        u = self.factor * int(math.ceil(math.log(L_K)))
        U_part = self.factor * int(math.ceil(math.log(L_K)))
        n_top = min(u, L_Q)

        if n_top < L_Q:
            scores, index = self._prob_qk(q, k, sample_k=U_part, n_top=n_top)
            scores = scores / math.sqrt(self.d_k)
            attn = self.dropout(torch.softmax(scores, dim=-1))

            # Compute output for selected queries
            v_reduced = torch.gather(
                v, dim=-2,
                index=index.unsqueeze(-1).expand(-1, -1, -1, self.d_k),
            )
            out_reduced = torch.matmul(attn, v_reduced)

            # Fill zeros for non-selected queries
            out = torch.zeros(B, self.n_heads, L_Q, self.d_k, device=q.device)
            out.scatter_(dim=-2, index=index.unsqueeze(-1).expand_as(out_reduced), src=out_reduced)
        else:
            scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.d_k)
            attn = self.dropout(torch.softmax(scores, dim=-1))
            out = torch.matmul(attn, v)

        out = out.transpose(1, 2).contiguous().view(B, L_Q, D)
        return self.w_o(out)


class ConvDistilling(nn.Module):
    """Self-attention distilling: halves sequence length via strided conv."""

    def __init__(self, d_model: int):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(d_model, d_model, kernel_size=3, stride=1, padding=1, padding_mode="circular"),
            nn.ELU(),
            nn.MaxPool1d(kernel_size=3, stride=2, padding=1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv(x.permute(0, 2, 1)).permute(0, 2, 1)


class InformerEncoderLayer(nn.Module):
    """Informer encoder layer with ProbSparse attention + distilling."""

    def __init__(self, d_model: int, n_heads: int, d_ff: int, factor: int = 5, dropout: float = 0.1):
        super().__init__()
        self.attention = ProbSparseAttention(d_model, n_heads, factor, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout),
        )
        self.distilling = ConvDistilling(d_model)
        self.norm3 = nn.LayerNorm(d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        attn_out = self.attention(x, x, x)
        x = self.norm1(x + attn_out)
        ffn_out = self.ffn(x)
        x = self.norm2(x + ffn_out)
        x = self.distilling(x)
        return self.norm3(x)


class Informer(nn.Module):
    """Informer for EDA arousal classification."""

    def __init__(
        self,
        n_channels: int = 3,
        seq_len: int = 160,
        d_model: int = 128,
        n_heads: int = 8,
        n_layers: int = 3,
        d_ff: int = 256,
        factor: int = 5,
        n_classes: int = 2,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.embedding = DataEmbedding(n_channels, d_model, dropout)
        self.encoder = nn.ModuleList([
            InformerEncoderLayer(d_model, n_heads, d_ff, factor, dropout)
            for _ in range(n_layers)
        ])
        self.projection = nn.Linear(d_model, n_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.embedding(x)
        for layer in self.encoder:
            x = layer(x)
        x = x.mean(dim=1)
        return self.projection(x)
