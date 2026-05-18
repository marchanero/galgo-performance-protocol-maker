"""
Paper-to-Code Naming Map
========================
Maps paper terminology to code identifiers for full traceability.

Paper                          | Code
-------------------------------|------------------
X in R^{T x C}                 | x: (batch, seq_len, channels)
T = 4n (timesteps)             | seq_len = 4 * window_seconds
C = 3 (SCR, ΔSCR, Δ²SCR)      | n_channels = 3
LOSO (147 folds)               | n_folds = 147
F1-score (macro-averaged)      | f1_score(average='macro')
N_params (M)                   | params_millions
t_inf (ms)                    | inference_time_ms
M_peak (MB)                   | peak_memory_mb
t_train (s/epoch)             | train_time_per_epoch
Wilcoxon signed-rank          | scipy.stats.wilcoxon
Bonferroni-Holm correction    | statsmodels.multipletests
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple

# ── Signal parameters ──────────────────────────────────────────────────────
SAMPLING_RATE = 4  # Hz
DEFAULT_WINDOW_SECONDS = 40
DEFAULT_SEQ_LEN = SAMPLING_RATE * DEFAULT_WINDOW_SECONDS  # T = 160
N_CHANNELS = 3  # SCR, ΔSCR, Δ²SCR

# ── Dataset ─────────────────────────────────────────────────────────────────
N_SUBJECTS = 147
N_CLASSES = 2  # calm, stress
CLASS_NAMES = ["calm", "stress"]

# ── LOSO ────────────────────────────────────────────────────────────────────
N_FOLDS = 147
VAL_SPLIT = 0.2  # 80/20 within training subjects

# ── Training defaults ──────────────────────────────────────────────────────
DEFAULT_BATCH_SIZE = 32
DEFAULT_EPOCHS = 100
DEFAULT_EARLY_STOPPING_PATIENCE = 15
DEFAULT_LEARNING_RATE = 1e-3
DEFAULT_WEIGHT_DECAY = 1e-4
DEFAULT_GRAD_CLIP = 1.0
DEFAULT_DROPOUT = 0.1
DEFAULT_SEED = 42

# ── Hyperparameter search space (Table: hyperparams) ────────────────────────
HYPERPARAM_SEARCH_SPACE = {
    "encoder_layers": [1, 2, 3, 4],
    "attention_heads": [1, 2, 4, 8],
    "embedding_dim": [16, 32, 64, 128],
    "feedforward_dim": [32, 64, 128, 256],
    "patch_size": [4, 8, 16],           # PatchTST, ModernTCN
    "moving_avg_kernel": [3, 5, 7, 9, 11],  # Autoformer, FEDformer, DLinear
    "sampling_factor": [3, 5, 7],        # Informer
    "fourier_modes": [16, 32, 64],       # FEDformer
    "top_k_periods": [3, 5, 7],          # TimesNet
    "state_dimension": [8, 16, 32],      # Mamba
    "conv_kernel_size": [13, 25, 51],    # ModernTCN
}
N_GRID_CONFIGS = 64

# ── Efficiency measurement ──────────────────────────────────────────────────
EFFICIENCY_INPUT_SHAPE = (1, DEFAULT_SEQ_LEN, N_CHANNELS)  # batch_size=1
EFFICIENCY_N_WARMUP = 100
EFFICIENCY_N_REPEATS = 1000

# ── Statistical tests ──────────────────────────────────────────────────────
ALPHA = 0.05
N_PAIRWISE_COMPARISONS = 28  # 8 choose 2
BONFERRONI_HOLM_CORRECTION = True


@dataclass
class ArchitectureConfig:
    """Configuration for a single architecture."""
    name: str
    paradigm: str  # patch_attention, sparse_attention, frequency, ssm, modern_conv, linear
    complexity: str  # O(N^2), O(L log L), O(L)
    paper_reference: str

    encoder_layers: int = 3
    embedding_dim: int = 128
    feedforward_dim: int = 256
    dropout: float = 0.1
    head_dropout: float = 0.0

    # Architecture-specific
    attention_heads: Optional[int] = None
    patch_size: Optional[int] = None
    patch_stride: Optional[int] = None
    moving_avg_kernel: Optional[int] = None
    sampling_factor: Optional[int] = None
    fourier_modes: Optional[int] = None
    top_k_periods: Optional[int] = None
    state_dimension: Optional[int] = None
    conv_kernel_size: Optional[int] = None


# ── Architecture registry ───────────────────────────────────────────────────
ARCHITECTURES: Dict[str, ArchitectureConfig] = {
    "PatchTST": ArchitectureConfig(
        name="PatchTST",
        paradigm="patch_attention",
        complexity="O(N^2)",
        paper_reference="Nie et al., ICLR 2023",
        patch_size=16,
        patch_stride=8,
        attention_heads=16,
        encoder_layers=3,
        embedding_dim=128,
        feedforward_dim=256,
        dropout=0.2,
    ),
    "Informer": ArchitectureConfig(
        name="Informer",
        paradigm="sparse_attention",
        complexity="O(L log L)",
        paper_reference="Zhou et al., AAAI 2021",
        sampling_factor=5,
        attention_heads=8,
        encoder_layers=3,
        embedding_dim=128,
        feedforward_dim=256,
        dropout=0.1,
    ),
    "Autoformer": ArchitectureConfig(
        name="Autoformer",
        paradigm="frequency",
        complexity="O(L log L)",
        paper_reference="Wu et al., NeurIPS 2021",
        moving_avg_kernel=25,
        attention_heads=8,
        encoder_layers=2,
        embedding_dim=128,
        feedforward_dim=256,
        dropout=0.1,
    ),
    "TimesNet": ArchitectureConfig(
        name="TimesNet",
        paradigm="frequency",
        complexity="O(L log L)",
        paper_reference="Wu et al., ICLR 2023",
        top_k_periods=5,
        encoder_layers=2,
        embedding_dim=64,
        feedforward_dim=128,
        dropout=0.1,
    ),
    "FEDformer": ArchitectureConfig(
        name="FEDformer",
        paradigm="frequency",
        complexity="O(L)",
        paper_reference="Zhou et al., ICML 2022",
        fourier_modes=32,
        moving_avg_kernel=25,
        attention_heads=8,
        encoder_layers=2,
        embedding_dim=128,
        feedforward_dim=256,
        dropout=0.1,
    ),
    "Mamba": ArchitectureConfig(
        name="Mamba",
        paradigm="ssm",
        complexity="O(L)",
        paper_reference="Gu & Dao, 2023",
        state_dimension=16,
        encoder_layers=4,
        embedding_dim=128,
        dropout=0.1,
    ),
    "ModernTCN": ArchitectureConfig(
        name="ModernTCN",
        paradigm="modern_conv",
        complexity="O(L)",
        paper_reference="Luo & Wang, ICLR 2024",
        conv_kernel_size=51,
        patch_size=16,
        patch_stride=8,
        encoder_layers=4,
        embedding_dim=64,
        dropout=0.1,
    ),
    "DLinear": ArchitectureConfig(
        name="DLinear",
        paradigm="linear",
        complexity="O(L)",
        paper_reference="Zeng et al., AAAI 2023",
        moving_avg_kernel=25,
    ),
}


def get_architecture_config(name: str) -> ArchitectureConfig:
    """Retrieve configuration for a named architecture."""
    if name not in ARCHITECTURES:
        raise ValueError(f"Unknown architecture: {name}. Available: {list(ARCHITECTURES.keys())}")
    return ARCHITECTURES[name]
