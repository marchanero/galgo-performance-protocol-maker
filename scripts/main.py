#!/usr/bin/env python3
"""
Efficient and Modern Architectures for EDA-based Arousal Classification
======================================================================

Main entry point for the complete experimental pipeline:
  1. EDA preprocessing (FIR filter, Gaussian smoothing, CDA, derivatives)
  2. LOSO cross-validation across 8 DL architectures + SVM baseline
  3. Classification metrics (F1, Acc, Prec, Rec, AUC)
  4. Computational efficiency (params, FLOPs, inference time, memory, training time)
  5. Statistical significance (Wilcoxon signed-rank + Bonferroni-Holm)
  6. Channel ablation (SCR, ΔSCR, Δ²SCR)
  7. Window length analysis (1-40 seconds)

Usage:
  python scripts/main.py --data_dir data/ --output_dir results/
  python scripts/main.py --models PatchTST,Mamba --n_folds 10 --epochs 50
"""

import argparse
import json
import os
import sys
import time
import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.config import (
    ARCHITECTURES, get_architecture_config, N_CLASSES, SAMPLING_RATE,
    DEFAULT_WINDOW_SECONDS, DEFAULT_SEQ_LEN, N_CHANNELS, N_SUBJECTS,
)
from scripts.models import create_model, ClassicalSVMBaseline
from scripts.data.preprocessing import preprocess_eda_pipeline, extract_handcrafted_features
from scripts.training.loso import create_loso_folds, prepare_loso_fold
from scripts.training.trainer import train_model, evaluate
from scripts.evaluation.metrics import compute_classification_metrics, aggregate_fold_metrics
from scripts.evaluation.efficiency import compute_all_efficiency_metrics
from scripts.evaluation.statistics import compute_pairwise_significance_matrix
from scripts.ablations.channels import run_channel_ablation
from scripts.ablations.window_length import run_window_length_ablation
from scripts.utils import set_seed, get_device
from torch.utils.data import DataLoader, TensorDataset


def parse_args():
    parser = argparse.ArgumentParser(
        description="EDA-based Arousal Classification: Benchmark Pipeline"
    )
    parser.add_argument("--data_dir", type=str, default="data/",
                        help="Path to data directory")
    parser.add_argument("--output_dir", type=str, default="results/",
                        help="Path to output directory")
    parser.add_argument("--models", type=str,
                        default="PatchTST,Informer,Autoformer,TimesNet,FEDformer,Mamba,ModernTCN,DLinear",
                        help="Comma-separated models to evaluate")
    parser.add_argument("--n_folds", type=int, default=147,
                        help="Number of LOSO folds (max 147)")
    parser.add_argument("--epochs", type=int, default=100,
                        help="Maximum training epochs")
    parser.add_argument("--batch_size", type=int, default=32,
                        help="Training batch size")
    parser.add_argument("--lr", type=float, default=1e-3,
                        help="Initial learning rate")
    parser.add_argument("--patience", type=int, default=15,
                        help="Early stopping patience")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed")
    parser.add_argument("--no_cuda", action="store_true",
                        help="Disable CUDA")
    parser.add_argument("--run_ablations", action="store_true",
                        help="Also run channel and window length ablations")
    parser.add_argument("--run_svm", action="store_true",
                        help="Also run classical SVM baseline")
    return parser.parse_args()


def main():
    args = parse_args()
    set_seed(args.seed)
    device = torch.device("cpu") if args.no_cuda else get_device()
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Device: {device}")
    print(f"Models: {args.models}")
    print(f"LOSO folds: {args.n_folds}")
    print(f"Epochs: {args.epochs}, Batch size: {args.batch_size}")

    # ── Load data ────────────────────────────────────────────────────────
    # Expected format: preprocessed windows as .npy files
    # X: (n_samples, 3, 160)  y: (n_samples,)  subject_ids: (n_samples,)
    X_path = os.path.join(args.data_dir, "X_windows.npy")
    y_path = os.path.join(args.data_dir, "y_labels.npy")
    subjects_path = os.path.join(args.data_dir, "subject_ids.npy")

    if not all(os.path.exists(p) for p in [X_path, y_path, subjects_path]):
        print(f"Data files not found in {args.data_dir}.")
        print("Expected: X_windows.npy (n_samples, 3, 160), y_labels.npy, subject_ids.npy")
        print("Run preprocessing first or provide preprocessed data.")
        sys.exit(1)

    X = np.load(X_path)
    y = np.load(y_path)
    subject_ids = np.load(subjects_path)
    print(f"Data loaded: X={X.shape}, y={y.shape}, subjects={len(np.unique(subject_ids))}")

    # ── Main benchmark ──────────────────────────────────────────────────
    model_names = [m.strip() for m in args.models.split(",")]
    all_results = {}
    all_fold_scores = {}

    for model_name in model_names:
        print(f"\n{'='*60}")
        print(f"  {model_name}")
        print(f"{'='*60}")

        config = get_architecture_config(model_name)
        fold_metrics = []

        fold_generator = create_loso_folds(subject_ids)
        start_time = time.time()

        for fold_idx, (train_idx, val_idx, test_idx) in enumerate(fold_generator):
            if fold_idx >= args.n_folds:
                break

            fold_data = prepare_loso_fold(X, y, train_idx, val_idx, test_idx)

            model = create_model(config)
            n_params = sum(p.numel() for p in model.parameters() if p.requires_grad) / 1e6

            train_model(
                model,
                fold_data["X_train"], fold_data["y_train"],
                fold_data["X_val"], fold_data["y_val"],
                batch_size=args.batch_size, epochs=args.epochs,
                lr=args.lr, patience=args.patience, device=device,
                verbose=(fold_idx == 0),
            )

            test_dataset = TensorDataset(
                torch.FloatTensor(fold_data["X_test"]),
                torch.LongTensor(fold_data["y_test"]),
            )
            test_loader = DataLoader(test_dataset, batch_size=args.batch_size)
            criterion = torch.nn.CrossEntropyLoss()
            eval_result = evaluate(model, test_loader, criterion, device)

            metrics = compute_classification_metrics(
                eval_result["labels"], eval_result["predictions"],
                eval_result["probabilities"],
            )
            fold_metrics.append(metrics)

            if (fold_idx + 1) % 20 == 0:
                current_f1 = np.mean([m["f1"] for m in fold_metrics])
                elapsed = time.time() - start_time
                print(f"  Fold {fold_idx + 1}/{args.n_folds}: F1={current_f1:.4f}, {elapsed:.0f}s elapsed")

        # Aggregate
        aggregated = aggregate_fold_metrics(fold_metrics)
        elapsed_total = time.time() - start_time

        print(f"\n  {model_name} results:")
        for metric in ["f1", "accuracy", "precision", "recall", "auc"]:
            if metric in aggregated:
                m = aggregated[metric]
                print(f"    {metric}: {m['mean']:.4f} ± {m['std']:.4f}")

        # Efficiency
        print(f"\n  Efficiency metrics:")
        model_eval = create_model(config).to(device)
        eff = compute_all_efficiency_metrics(model_eval, device=device)
        print(f"    Params: {eff['params_m']:.2f}M, FLOPs: {eff['flops_m']:.1f}M, "
              f"Inference: {eff['inference_ms']:.2f}ms, Peak memory: {eff['peak_memory_mb']:.1f}MB")

        all_results[model_name] = {
            "metrics": aggregated,
            "efficiency": eff,
            "n_params": eff["params_m"],
            "total_time_s": elapsed_total,
            "n_folds": len(fold_metrics),
        }
        all_fold_scores[model_name] = np.array([m["f1"] for m in fold_metrics])

    # ── Statistical significance ────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  Statistical Significance (Wilcoxon signed-rank)")
    print(f"{'='*60}")

    stats = compute_pairwise_significance_matrix(all_fold_scores, apply_bh=True)
    print(f"  N comparisons: {stats['n_comparisons']}")
    print(f"  BH threshold: {stats.get('bh_threshold', 'N/A'):.6f}")

    # ── SVM baseline ────────────────────────────────────────────────────
    if args.run_svm:
        print(f"\n{'='*60}")
        print("  Classical SVM Baseline")
        print(f"{'='*60}")

        svm = ClassicalSVMBaseline()
        fold_f1_svm = []

        for fold_idx, (train_idx, val_idx, test_idx) in enumerate(
            create_loso_folds(subject_ids)
        ):
            if fold_idx >= args.n_folds:
                break

            X_train_feat = svm.extract_features(X[train_idx])
            y_train_fold = y[train_idx]
            X_test_feat = svm.extract_features(X[test_idx])
            y_test_fold = y[test_idx]

            svm.fit(X_train_feat, y_train_fold)
            y_pred = svm.predict(X_test_feat)
            y_prob = svm.predict_proba(X_test_feat)

            metrics = compute_classification_metrics(y_test_fold, y_pred, y_prob)
            fold_f1_svm.append(metrics["f1"])

        svm_f1 = np.mean(fold_f1_svm)
        svm_std = np.std(fold_f1_svm)
        print(f"  SVM F1: {svm_f1:.4f} ± {svm_std:.4f}")
        all_fold_scores["SVM"] = np.array(fold_f1_svm)

    # ── Save results ────────────────────────────────────────────────────
    output_file = os.path.join(args.output_dir, "results.json")
    # Convert numpy arrays for JSON serialization
    serializable = {}
    for name, data in all_results.items():
        serializable[name] = {
            "metrics": {
                k: {"mean": v["mean"], "std": v["std"]}
                for k, v in data["metrics"].items()
            },
            "efficiency": {k: float(v) for k, v in data["efficiency"].items()},
            "n_params": float(data["n_params"]),
            "total_time_s": data["total_time_s"],
            "n_folds": data["n_folds"],
        }

    with open(output_file, "w") as f:
        json.dump(serializable, f, indent=2)
    print(f"\nResults saved to {output_file}")

    # ── Ablations (optional) ────────────────────────────────────────────
    if args.run_ablations:
        print(f"\n{'='*60}")
        print("  Ablation Studies")
        print(f"{'='*60}")

        # Channel ablation for key architectures
        for ablate_model in ["Mamba", "PatchTST", "DLinear"]:
            if ablate_model not in model_names:
                continue
            print(f"\n  Channel ablation: {ablate_model}")

            def factory(n_ch):
                cfg = get_architecture_config(ablate_model)
                return create_model(cfg, n_channels=n_ch)

            channel_results = run_channel_ablation(
                factory, X, y, subject_ids,
                n_folds=min(args.n_folds, 30),
                batch_size=args.batch_size, device=device, verbose=True,
            )

            ablation_file = os.path.join(
                args.output_dir, f"channel_ablation_{ablate_model}.json",
            )
            with open(ablation_file, "w") as f:
                json.dump(channel_results, f, indent=2)

    print("\nDone.")


if __name__ == "__main__":
    main()
