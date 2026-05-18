"""Model registry: factory functions for all 8 DL architectures + SVM baseline."""

from typing import Optional, Dict, Any
import torch.nn as nn

from scripts.models.patch_tst import PatchTST
from scripts.models.informer import Informer
from scripts.models.autoformer import Autoformer
from scripts.models.times_net import TimesNet
from scripts.models.fedformer import FEDformer
from scripts.models.mamba import Mamba
from scripts.models.modern_tcn import ModernTCN
from scripts.models.dlinear import DLinear
from scripts.models.classical import ClassicalSVMBaseline
from scripts.config import ArchitectureConfig


def create_model(config: ArchitectureConfig, **overrides) -> nn.Module:
    """Factory function to create a model from an ArchitectureConfig.

    Args:
        config: ArchitectureConfig instance.
        **overrides: Override any parameter from the config.

    Returns:
        Instantiated PyTorch model.
    """
    # Build kwargs from config, allowing overrides
    kwargs: Dict[str, Any] = {}

    # Common parameters
    for key in [
        "encoder_layers", "embedding_dim", "feedforward_dim", "dropout",
        "head_dropout", "attention_heads", "patch_size", "patch_stride",
        "moving_avg_kernel", "sampling_factor", "fourier_modes",
        "top_k_periods", "state_dimension", "conv_kernel_size",
    ]:
        val = getattr(config, key, None)
        if val is not None:
            kwargs[key] = val

    # Rename for model constructors
    kwargs.setdefault("n_layers", kwargs.pop("encoder_layers", 3))
    kwargs.setdefault("d_model", kwargs.pop("embedding_dim", 128))
    kwargs.setdefault("d_ff", kwargs.pop("feedforward_dim", 256))
    kwargs.setdefault("n_heads", kwargs.pop("attention_heads", 8))
    kwargs.setdefault("factor", kwargs.pop("sampling_factor", 5))
    kwargs.setdefault("modes", kwargs.pop("fourier_modes", 32))
    kwargs.setdefault("top_k", kwargs.pop("top_k_periods", 5))
    kwargs.setdefault("d_state", kwargs.pop("state_dimension", 16))
    kwargs.setdefault("kernel_size", kwargs.pop("conv_kernel_size", 51))

    # Apply overrides
    kwargs.update(overrides)

    # Instantiate
    model_map = {
        "PatchTST": PatchTST,
        "Informer": Informer,
        "Autoformer": Autoformer,
        "TimesNet": TimesNet,
        "FEDformer": FEDformer,
        "Mamba": Mamba,
        "ModernTCN": ModernTCN,
        "DLinear": DLinear,
    }

    if config.name not in model_map:
        raise ValueError(f"Unknown architecture: {config.name}")

    # Remove unused kwargs per model
    if config.name == "DLinear":
        # DLinear only needs moving_avg_kernel
        kwargs = {k: v for k, v in kwargs.items() if k in [
            "n_channels", "seq_len", "moving_avg_kernel", "n_classes",
        ]}
    elif config.name == "Mamba":
        # Mamba-specific kwargs
        pass  # Mamba uses d_model, n_layers, d_state, etc.
    elif config.name == "ModernTCN":
        kwargs.setdefault("patch_size", 16)
        kwargs.setdefault("patch_stride", 8)

    return model_map[config.name](**kwargs)


def list_available_models() -> list:
    """Return list of available model names."""
    return [
        "PatchTST", "Informer", "Autoformer", "TimesNet",
        "FEDformer", "Mamba", "ModernTCN", "DLinear", "SVM",
    ]
