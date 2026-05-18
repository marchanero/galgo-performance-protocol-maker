"""Training loop with early stopping, cosine annealing, and AdamW.

Protocol:
  - AdamW optimiser with cosine annealing schedule
  - Cross-entropy loss
  - Early stopping (patience = 15) on validation loss
  - Gradient clipping (max norm = 1.0)
  - Batch size = 32
  - Max epochs = 100
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from typing import Optional, Dict, Any, Callable
from scripts.utils import get_device


class EarlyStopping:
    """Early stopping with patience on validation loss."""

    def __init__(self, patience: int = 15, min_delta: float = 1e-4):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = float("inf")
        self.best_state = None
        self.should_stop = False

    def __call__(self, val_loss: float, model: nn.Module) -> bool:
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
            self.best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True
        return self.should_stop


def train_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: optim.Optimizer,
    criterion: nn.Module,
    device: torch.device,
    grad_clip: float = 1.0,
) -> float:
    """Train for one epoch. Returns average loss."""
    model.train()
    total_loss = 0.0
    n_batches = 0

    for batch_x, batch_y in loader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        optimizer.zero_grad()
        logits = model(batch_x)
        loss = criterion(logits, batch_y)
        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
        optimizer.step()

        total_loss += loss.item()
        n_batches += 1

    return total_loss / max(n_batches, 1)


@torch.no_grad()
def evaluate(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> Dict[str, float]:
    """Evaluate model. Returns loss and predictions."""
    model.eval()
    total_loss = 0.0
    n_batches = 0
    all_preds = []
    all_labels = []
    all_probabilities = []

    for batch_x, batch_y in loader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        logits = model(batch_x)
        loss = criterion(logits, batch_y)

        total_loss += loss.item()
        n_batches += 1

        probs = torch.softmax(logits, dim=-1)
        preds = logits.argmax(dim=-1)

        all_preds.append(preds.cpu().numpy())
        all_labels.append(batch_y.cpu().numpy())
        all_probabilities.append(probs.cpu().numpy())

    return {
        "loss": total_loss / max(n_batches, 1),
        "predictions": np.concatenate(all_preds),
        "labels": np.concatenate(all_labels),
        "probabilities": np.concatenate(all_probabilities),
    }


def train_model(
    model: nn.Module,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    batch_size: int = 32,
    epochs: int = 100,
    lr: float = 1e-3,
    weight_decay: float = 1e-4,
    patience: int = 15,
    grad_clip: float = 1.0,
    device: Optional[torch.device] = None,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Train a model on a single LOSO fold.

    Args:
        model: PyTorch model.
        X_train, y_train: Training data.
        X_val, y_val: Validation data.
        batch_size: Mini-batch size.
        epochs: Maximum number of epochs.
        lr: Initial learning rate.
        weight_decay: AdamW weight decay.
        patience: Early stopping patience.
        grad_clip: Gradient clipping max norm.
        device: Compute device.
        verbose: Whether to print progress.

    Returns:
        Dictionary with best_epoch, train_history, best_state.
    """
    if device is None:
        device = get_device()

    model = model.to(device)

    # DataLoaders
    train_dataset = TensorDataset(
        torch.FloatTensor(X_train), torch.LongTensor(y_train),
    )
    val_dataset = TensorDataset(
        torch.FloatTensor(X_val), torch.LongTensor(y_val),
    )

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    # Optimizer and scheduler
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    criterion = nn.CrossEntropyLoss()

    # Early stopping
    early_stopping = EarlyStopping(patience=patience)

    train_losses = []
    val_losses = []

    for epoch in range(epochs):
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device, grad_clip)
        val_results = evaluate(model, val_loader, criterion, device)

        train_losses.append(train_loss)
        val_losses.append(val_results["loss"])

        scheduler.step()

        if verbose and epoch % 10 == 0:
            print(f"  Epoch {epoch:3d}: train_loss={train_loss:.4f}, val_loss={val_results['loss']:.4f}")

        if early_stopping(val_results["loss"], model):
            if verbose:
                print(f"  Early stopping at epoch {epoch}")
            break

    # Restore best state
    if early_stopping.best_state is not None:
        model.load_state_dict(early_stopping.best_state)

    return {
        "best_epoch": epoch,
        "train_losses": train_losses,
        "val_losses": val_losses,
    }
