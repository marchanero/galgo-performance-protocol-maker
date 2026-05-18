"""Computational efficiency metrics.

Five complementary metrics (Table: efficiency):
  - N_params (M): Total trainable parameters (millions)
  - FLOPs (M): Floating-point operations for a single forward pass (millions)
  - t_inf (ms): Inference time per sample, averaged over 1000 passes
  - M_peak (MB): Peak GPU memory consumption during forward pass
  - t_train (s/epoch): Training time per epoch

Measurement conditions:
  - Identical input: T = 160, C = 3, batch_size = 1
  - Inference: NVIDIA Quadro P5000 (or available CUDA GPU)
  - Training time: averaged across LOSO folds
"""

import time
import torch
import torch.nn as nn
import numpy as np
from typing import Dict, Optional


def count_parameters(model: nn.Module) -> float:
    """Count trainable parameters in millions."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad) / 1e6


def measure_flops(
    model: nn.Module,
    input_shape: tuple = (1, 160, 3),
    device: Optional[torch.device] = None,
) -> float:
    """Measure FLOPs using thop library.

    Args:
        model: PyTorch model.
        input_shape: Input tensor shape (batch, seq_len, channels).
        device: Compute device.

    Returns:
        FLOPs in millions.
    """
    try:
        from thop import profile
    except ImportError:
        print("thop not installed. Install with: pip install thop")
        return 0.0

    if device is None:
        device = next(model.parameters()).device

    model.eval()
    dummy_input = torch.randn(*input_shape).to(device)

    with torch.no_grad():
        flops, _ = profile(model, inputs=(dummy_input,), verbose=False)

    return flops / 1e6


def measure_inference_time(
    model: nn.Module,
    input_shape: tuple = (1, 160, 3),
    device: Optional[torch.device] = None,
    n_warmup: int = 100,
    n_repeats: int = 1000,
) -> float:
    """Measure inference time per sample in milliseconds.

    Args:
        model: PyTorch model.
        input_shape: Input tensor shape (batch, seq_len, channels).
        device: Compute device.
        n_warmup: Number of warmup iterations.
        n_repeats: Number of measurement iterations.

    Returns:
        Average inference time in milliseconds.
    """
    if device is None:
        device = next(model.parameters()).device

    model.eval()
    dummy_input = torch.randn(*input_shape).to(device)

    # Warmup
    with torch.no_grad():
        for _ in range(n_warmup):
            _ = model(dummy_input)

    # Measure
    if device.type == "cuda":
        start_event = torch.cuda.Event(enable_timing=True)
        end_event = torch.cuda.Event(enable_timing=True)

        with torch.no_grad():
            start_event.record()
            for _ in range(n_repeats):
                _ = model(dummy_input)
            end_event.record()
            torch.cuda.synchronize()
            total_time = start_event.elapsed_time(end_event)
    else:
        with torch.no_grad():
            start_time = time.perf_counter()
            for _ in range(n_repeats):
                _ = model(dummy_input)
            end_time = time.perf_counter()
            total_time = (end_time - start_time) * 1000.0  # ms

    return total_time / n_repeats


def measure_peak_memory(
    model: nn.Module,
    input_shape: tuple = (1, 160, 3),
    device: Optional[torch.device] = None,
) -> float:
    """Measure peak GPU memory consumption during forward pass (MB).

    Args:
        model: PyTorch model.
        input_shape: Input tensor shape.
        device: Compute device.

    Returns:
        Peak memory in MB.
    """
    if device is None:
        device = next(model.parameters()).device

    model.eval()
    dummy_input = torch.randn(*input_shape).to(device)

    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
        with torch.no_grad():
            _ = model(dummy_input)
        return torch.cuda.max_memory_allocated(device) / (1024 ** 2)
    else:
        return 0.0


def measure_training_time_per_epoch(
    model: nn.Module,
    train_loader: torch.utils.data.DataLoader,
    device: Optional[torch.device] = None,
    n_warmup: int = 2,
    n_repeats: int = 5,
) -> float:
    """Measure average training time per epoch in seconds.

    Args:
        model: PyTorch model (in training mode).
        train_loader: DataLoader for training data.
        device: Compute device.
        n_warmup: Number of warmup epochs.
        n_repeats: Number of measurement epochs.

    Returns:
        Average training time per epoch in seconds.
    """
    import torch.optim as optim

    if device is None:
        device = next(model.parameters()).device

    optimizer = optim.AdamW(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    model.train()

    # Warmup
    for _ in range(n_warmup):
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            optimizer.zero_grad()
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()

    # Measure
    if device.type == "cuda":
        torch.cuda.synchronize()

    times = []
    for _ in range(n_repeats):
        start_time = time.perf_counter()
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            optimizer.zero_grad()
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()
        if device.type == "cuda":
            torch.cuda.synchronize()
        times.append(time.perf_counter() - start_time)

    return float(np.mean(times))


def compute_all_efficiency_metrics(
    model: nn.Module,
    input_shape: tuple = (1, 160, 3),
    train_loader: Optional[torch.utils.data.DataLoader] = None,
    device: Optional[torch.device] = None,
) -> Dict[str, float]:
    """Compute all five efficiency metrics.

    Returns:
        Dictionary with params_m, flops_m, inference_ms, peak_memory_mb, train_s_per_epoch.
    """
    if device is None:
        device = next(model.parameters()).device

    metrics = {
        "params_m": count_parameters(model),
        "flops_m": measure_flops(model, input_shape, device),
        "inference_ms": measure_inference_time(model, input_shape, device),
        "peak_memory_mb": measure_peak_memory(model, input_shape, device),
    }

    if train_loader is not None:
        metrics["train_s_per_epoch"] = measure_training_time_per_epoch(
            model, train_loader, device,
        )
    else:
        metrics["train_s_per_epoch"] = 0.0

    return metrics
