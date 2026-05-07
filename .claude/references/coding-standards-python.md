# Coding Standards: Python (ML/DL)

These standards apply to all Python code produced by the Coder agent. Derived from software engineering discipline, adapted for ML/DL research in CS/AI and biomedical engineering. The coder-critic enforces these rules.

---

## 1. Runtime and Dependencies

- **Python >= 3.11** (`tomllib`, improved error messages, `ExceptionGroup`)
- **`conda`** (preferred) or **`venv`** for environments
- `environment.yml` or `requirements.txt` committed, versions pinned
- No `pip install` inside scripts

### Core Stack

| Package | Purpose |
|---------|---------|
| `torch` (PyTorch) | Deep learning framework (primary) |
| `torchvision` / `torchaudio` | Domain-specific extensions if needed |
| `numpy` | Array operations |
| `scipy` | Signal processing (filters, stats) |
| `pandas` | Tabular data manipulation, results tables |
| `scikit-learn` | Metrics, cross-validation splits, preprocessing |
| `matplotlib` | All figures (PDF output) |
| `seaborn` | Confusion matrices, statistical plots (paper figures only via matplotlib backend) |
| `tqdm` | Progress bars |
| `tensorboard` or `wandb` | Experiment logging |
| `thop` or `fvcore` | FLOPs/profiling |
| `pyyaml` | Config file parsing |
| `pathlib` | File path handling |

### Optional (Based on Domain)

| Package | Purpose |
|---------|---------|
| `cvxEDA` / `neurokit2` | EDA signal decomposition (tonic/phasic) |
| `mne` | General physiological signal processing |
| `pytorch-lightning` | Training loop standardization (optional, for complex projects) |

### Prohibited

| Package | Reason | Replacement |
|---------|--------|-------------|
| `sklearn` for neural network models | Not designed for DL | PyTorch / TensorFlow |
| `plotly` for paper figures | PDF issues in LaTeX | `matplotlib` with PDF backend |
| `tensorflow` + `pytorch` mixed | Increases complexity | Choose one framework |

---

## 2. Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Files / modules | `snake_case.py` | `trainer.py`, `eda_dataset.py` |
| Functions | `snake_case` | `compute_f1()`, `set_seed()` |
| Variables | `snake_case` | `n_subjects`, `learning_rate` |
| Constants | `UPPER_SNAKE_CASE` | `N_SEEDS`, `BATCH_SIZE`, `DROPOUT_RATE` |
| Classes | `PascalCase` | `LightweightTransformer`, `EDADataset` |
| Type aliases | `PascalCase` | `TensorDict` |
| Booleans | `is_`, `has_` prefix | `is_training`, `has_converged` |
| Private helpers | `_leading_underscore` | `_validate_input_shape()` |
| Model components | `PascalCase` | `MultiScaleAttention`, `LightweightPE` |

---

## 3. Code Style

- **Formatter:** `black` (mandatory, run before commit)
- **Linter:** `ruff` (mandatory, zero warnings)
- **Import order:** `isort` (stdlib → third-party → local)
- **Line width:** 88 characters (Black default)
- **Docstrings:** NumPy style
- **Type hints:** required on all function signatures

```python
from pathlib import Path
from typing import Optional, Union

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader


class EDADataset(Dataset):
    """Dataset for EDA time-series classification.

    Parameters
    ----------
    data_path : Path
        Path to preprocessed data file.
    window_size : int
        Number of timesteps per sample.
    stride : int
        Stride between consecutive windows.
    """
    def __init__(
        self,
        data_path: Path,
        window_size: int = 256,
        stride: int = 128,
    ) -> None:
        ...
```

---

## 4. Numerical Discipline

### Float Safety
```python
def safe_loss(predictions: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    """Compute loss with NaN/Inf checking."""
    loss = nn.functional.cross_entropy(predictions, targets)
    if torch.isnan(loss) or torch.isinf(loss):
        raise RuntimeError(f"NaN/Inf loss detected")
    return loss
```

### Output Clamping
```python
# Clamp probabilities to avoid log(0) issues
probs = torch.clamp(raw_output, min=1e-7, max=1.0 - 1e-7)
log_probs = torch.log(probs)
```

### Reproducibility
```python
import random
import numpy as np
import torch


def set_seed(seed: int) -> None:
    """Set all random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

# WRONG: only setting one seed
torch.manual_seed(42)
```

### Pre-allocation
```python
# RIGHT: pre-allocate results array
n_models, n_folds, n_metrics = 5, 5, 4
results = np.empty((n_models, n_folds, n_metrics), dtype=np.float32)

# WRONG: growing a list
results = []
for model in models:
    model_results = []
    for fold in range(n_folds):
        model_results.append(evaluate(model, fold))
    results.append(model_results)
```

---

## 5. Model Design Standards

### Architecture Class Structure
```python
class BaseModel(nn.Module):
    """Abstract base class for all models."""

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError

    def count_parameters(self) -> int:
        """Return number of trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def get_complexity(self, input_shape: tuple) -> dict:
        """Return parameter count and estimated FLOPs."""
        return {
            "n_params": self.count_parameters(),
            "input_shape": input_shape,
        }
```

### Component Isolation
Each novel component goes in its own class:
```python
class MultiScaleAttention(nn.Module):
    """Multi-scale attention module.

    Computes attention at multiple temporal resolutions and fuses
    the results via learned weights.
    """
    def __init__(
        self,
        d_model: int,
        n_heads: int = 8,
        scales: list[int] = [1, 2, 4],
        dropout: float = 0.1,
    ) -> None:
        ...
```

### Forward Pass Clarity
```python
def forward(self, x: torch.Tensor) -> torch.Tensor:
    # Embedding
    x = self.embedding(x)

    # Transformer encoder
    x = self.encoder(x)

    # Pooling
    x = self.pooling(x)

    # Classification head
    x = self.classifier(x)

    return x
```

---

## 6. Training Loop Standards

### Trainer Pattern
```python
class Trainer:
    """Training loop with early stopping and logging."""

    def __init__(self, model: nn.Module, config: dict, device: torch.device):
        self.model = model.to(device)
        self.device = device
        self.config = config
        self.optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=config["learning_rate"],
            weight_decay=config["weight_decay"],
        )
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
            self.optimizer, T_0=config["T_0"]
        )
        self.criterion = nn.CrossEntropyLoss()

    def train_epoch(self, loader: DataLoader) -> float:
        self.model.train()
        total_loss = 0.0
        for batch in loader:
            inputs, targets = batch["signal"].to(self.device), batch["label"].to(self.device)
            self.optimizer.zero_grad()
            outputs = self.model(inputs)
            loss = self.criterion(outputs, targets)
            loss.backward()
            self.optimizer.step()
            total_loss += loss.item()
        return total_loss / len(loader)

    @torch.no_grad()
    def validate(self, loader: DataLoader) -> dict:
        self.model.eval()
        all_preds, all_targets = [], []
        for batch in loader:
            inputs, targets = batch["signal"].to(self.device), batch["label"].to(self.device)
            outputs = self.model(inputs)
            preds = outputs.argmax(dim=1)
            all_preds.append(preds.cpu())
            all_targets.append(targets.cpu())
        return compute_metrics(
            torch.cat(all_preds), torch.cat(all_targets)
        )
```

### Gradient Accumulation (for large models)
```python
ACCUMULATION_STEPS = 4
for i, batch in enumerate(loader):
    outputs = self.model(inputs)
    loss = self.criterion(outputs, targets) / ACCUMULATION_STEPS
    loss.backward()
    if (i + 1) % ACCUMULATION_STEPS == 0:
        self.optimizer.step()
        self.optimizer.zero_grad()
```

---

## 7. GPU Discipline

```python
# Device management
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model to device
model = model.to(device)

# Data to device in training loop, not in Dataset
for inputs, targets in loader:
    inputs, targets = inputs.to(device), targets.to(device)

# Memory management between experiments
del model, optimizer
torch.cuda.empty_cache()

# Mixed precision (optional, for large models)
from torch.cuda.amp import autocast, GradScaler
scaler = GradScaler()
with autocast():
    outputs = model(inputs)
    loss = criterion(outputs, targets)
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

---

## 8. Experiment Configuration

```python
# config.py — single source of truth for all experiment parameters
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
RESULTS_DIR = PROJECT_ROOT / "results"

# Model
D_MODEL = 128
N_HEADS = 8
N_LAYERS = 4
DROPOUT = 0.1

# Training
BATCH_SIZE = 64
LEARNING_RATE = 1e-4
WEIGHT_DECAY = 1e-4
N_EPOCHS = 100
EARLY_STOPPING_PATIENCE = 15
GRADIENT_CLIP_NORM = 1.0

# Data
WINDOW_SIZE = 256
STRIDE = 128
LOWPASS_CUTOFF = 4.0  # Hz

# Experiment
N_FOLDS = 5
N_SEEDS = 5
SEED_BASE = 42

# Hardware
DEVICE = "cuda"  # or "cpu"
N_WORKERS = 4
```

---

## 9. Evaluation Standards

```python
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_score: np.ndarray | None = None) -> dict:
    """Compute standard classification metrics."""
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "f1_macro": f1_score(y_true, y_pred, average="macro"),
        "f1_weighted": f1_score(y_true, y_pred, average="weighted"),
        "precision_macro": precision_score(y_true, y_pred, average="macro"),
        "recall_macro": recall_score(y_true, y_pred, average="macro"),
    }
    if y_score is not None and len(np.unique(y_true)) == 2:
        metrics["auc_roc"] = roc_auc_score(y_true, y_score[:, 1])
    return metrics
```

---

## 10. Metric Reporting Format

Always report:
- Mean ± standard deviation across folds/seeds
- Primary metric first
- Appropriate precision (3-4 significant digits for percentages)

```python
# RIGHT
f"F1 = {mean_f1:.3f} ± {std_f1:.3f}"

# WRONG
f"F1 = {mean_f1}"
```

---

## 11. Error Handling

- Raise `ValueError` for bad inputs, `RuntimeError` for computation failures
- Never return silently on failure
- Check for `NaN` / `Inf` after loss computation and forward pass
- Validate input shapes before model forward
- Validate output shapes after model forward

```python
def forward(self, x: torch.Tensor) -> torch.Tensor:
    if x.dim() != 3:
        raise ValueError(f"Expected 3D input (batch, time, features), got {x.dim()}D")

    output = self._forward_impl(x)

    if torch.isnan(output).any():
        raise RuntimeError("NaN detected in model output")

    return output
```

---

## 12. Prohibited Patterns

| Pattern | Reason | Replacement |
|---------|--------|-------------|
| `os.chdir()` | Breaks portability | `pathlib.Path` relative to project root |
| Hardcoded paths | Breaks portability | `config.py` constants with `pathlib` |
| `from module import *` | Namespace pollution | Explicit imports |
| `DataLoader(shuffle=True)` for val/test | Misleading metrics | `shuffle=False` |
| `np.random.seed()` alone | Incomplete reproducibility | `set_seed()` (all sources) |
| `torch.save(model)` without `model.eval()` | Wrong batch-norm stats | Set eval mode first |
| Test set in hyperparameter tuning | Data leakage | Strict train/val/test separation |
| Mixing numpy/torch without device awareness | CPU/GPU mismatch | Consistent `to(device)` |
| `except:` bare | Swallows all errors | `except SpecificError:` |
| Mutable default arguments | Shared state bug | `None` default + create inside |
| `print()` for training progress | Messy output | `tqdm` or `logging` |
| Growing lists in evaluation loops | Memory inefficiency | Pre-allocate numpy arrays |
| Global variables for experiment state | Non-reproducible | Pass state via config dicts |
| Not saving preprocessing parameters | Can't reproduce pipeline | Save scalers/filters alongside data |
