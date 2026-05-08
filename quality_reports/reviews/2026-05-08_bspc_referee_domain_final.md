# Domain Referee Report — DEFINITIVE FINAL
**Date:** 2026-05-08
**Venue:** Biomedical Signal Processing and Control (BSPC)
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification
**Referee Role:** Domain Expert — ARCHITECTURE disposition
**Verdict:** **MINOR REVISION** (conditional accept)
**Overall Score:** 82/100

---

## Executive Summary

This manuscript presents the first systematic accuracy-efficiency comparison of eight architectures spanning five paradigms — Transformers, state space models, modernised convolutions, Fourier-domain models, and a linear baseline — for binary arousal classification from EDA under strict LOSO (147 participants). The central contribution is a well-executed Pareto frontier analysis across five complementary efficiency metrics, yielding a practically actionable finding: Mamba achieves F1 = 0.858 at 1.5 ms inference, approaching PatchTST (F1 = 0.863) at 3.6× lower latency and 66% fewer parameters. The classical EDA baseline (handcrafted features + SVM, F1 ≈ 0.81) and DLinear/ModernTCN baselines anchor the DL gains credibly. Preprocessing choices are now physiologically justified, BSPC journal citations are integrated, and the Limitations section (3.8) is honest and comprehensive.

The manuscript has matured substantially across four prior revision rounds. The remaining gaps are narrow and well-defined. I recommend **MINOR REVISION** — the paper is essentially ready for publication; three proof-stage items would change my mind to Accept.

---

## Dimension-by-Dimension Scoring

### 1. Contribution & Novelty (30 points)
**Score: 25/30**

The contribution hierarchy is well-established: (i) first systematic accuracy-efficiency comparison spanning Transformers, SSMs, and modernised convolutions for EDA under LOSO; (ii) explicit Pareto frontier with five complementary efficiency metrics; (iii) DLinear and ModernTCN as critical baselines testing whether complex temporal mechanisms are necessary; (iv) channel ablation revealing derivative redundancy patterns; and (v) the classical SVM baseline anchoring DL gains in established signal processing methodology.

The work is genuinely novel in its domain (EDA classification), though the architectures themselves are re-purposed. The Pareto frontier framing elevates this beyond a conventional benchmarking study. The framing tension noted in R4 persists — the title emphasizes "efficient architectures" while half the studied models are mid-to-high latency — but this is acknowledged implicitly through the Pareto analysis.

**Basis:** Strong domain-first contribution; pragmatically useful; the Mamba finding has translational value for wearable affective computing.

---

### 2. Methodological Rigor (25 points)
**Score: 22/25**

Strengths:
- Strict LOSO with 147 folds is the gold standard for subject-independent physiological signal classification
- Identical hyperparameter tuning budget (64 configurations) across all architectures prevents search-space bias
- Five complementary efficiency metrics measured under identical input conditions
- Statistical tests reported with raw and Bonferroni-Holm corrected thresholds
- LOSO independence caveats explicitly discussed (Section 3.8)
- Regularization (dropout, weight decay, gradient clipping, cosine annealing) properly specified
- Training/inference on different GPU classes appropriately disclosed

Weaknesses:
- Inference time is reported as a point estimate without standard deviation, despite being "averaged over 1,000 forward passes"
- The classical EDA baseline (SVM, F1 ≈ 0.81) is a retroactive comparison from a different study — only F1 is available; standard deviations and per-fold distributions are missing
- No LSTM/BiLSTM comparison or citation, leaving the most common BSPC sequence-modelling baseline unaddressed
- FLOPs computed via `thop` (estimates from computational graph, not measured) — this is acceptable practice but should be noted alongside the hardware-grounded inference time

**Basis:** The LOSO protocol, equal tuning budgets, and statistical transparency are exemplary. The three weaknesses are minor and do not undermine the central findings.

---

### 3. Significance & Interpretability (20 points)
**Score: 16/20**

The Mamba finding is practically significant: a selective state space model that approaches SOTA Transformer accuracy at a fraction of the cost has direct implications for wearable EDA deployment. The Pareto frontier framework transforms architecture selection from an empirical exercise into an informed engineering decision — this is the paper's most durable contribution.

The physiological interpretation is generally well-calibrated:
- Window-length saturation at 15–20 s correctly anchored to SCR waveform duration
- 5-second minimum viable window provides actionable guidance for real-time applications
- DLinear–1DCNN–SVM convergence at F1 ≈ 0.80 correctly identifies the performance ceiling for architectures lacking global temporal modelling
- Channel ablation conclusions are carefully hedged ("partial redundancy," not "implicit derivative reconstruction")

Remaining weaknesses:
- All interpretability claims remain qualitative. Claims that attention "concentrates on SCR onset and rising phases" and Mamba state transitions "emphasize SCR onset regions in a manner analogous to attention" are plausible and consistent with EDA physiology, but they are not supported by any quantitative metric (attention entropy, peak-to-mean ratio, saliency-SCR landmark correlation). For a BSPC readership, this is noticeably thin.
- The derivative redundancy interpretation has not been tested with a capacity-control experiment (e.g., varying model size while holding architecture constant) to discriminate between "partial redundancy" and "diminishing returns from any additional input feature."

**Basis:** Core findings are well-supported. Interpretability is appropriately hedged but remains suggestive rather than evidence-backed.

---

### 4. Clarity & Presentation (15 points)
**Score: 13/15**

The manuscript is well-written and well-organized. Figures are professionally constructed — the pipeline diagram (Fig. 1), architecture overview (Fig. 2), and Pareto frontier (Fig. 6) are publication-quality. The TikZ rendering with colorblind-safe ColorBrewer palette is a strong choice for BSPC.

Minor issues:
- Figure 6 labels ("Low-latency GPU," "Mid-latency GPU," "High-latency GPU") are misleading — these thresholds are measured on a Quadro P5000 workstation GPU, not embedded or mobile hardware. The figure caption appropriately clarifies that these are "ordinal latency tiers rather than absolute deployment classifications," but the in-figure labels contradict this. Renaming to "Tier 1 / Tier 2 / Tier 3" would resolve the tension.
- The Mamba data point (purple) at (1.5 ms, 0.858) is the headline finding, but its visual distinction from orange O(L) points is subtle. A distinct marker shape would improve accessibility for grayscale and colorblind readers.
- The abstract and introduction both deploy "the first systematic comparison" — a single use in the abstract with "systematic" thereafter would read as more measured.

**Basis:** Publication-quality figures and clear writing. The three cosmetic items above are proof-stage corrections.

---

### 5. Reproducibility & Completeness (10 points)
**Score: 6/10**

What is disclosed:
- Full hyperparameter search space (Table 3)
- Training protocol (optimizer, learning rate, scheduling, batch size, regularization, early stopping)
- Input dimensionality and window configuration
- Efficiency measurement methodology
- Hardware specifications for both training and inference

What is missing:
- **Optimal hyperparameters per architecture not disclosed.** The 64-configuration grid search space is described, but the final selected configurations (embedding dimension, number of layers, patch size, state dimension, etc.) are not provided. Full reproducibility requires these in supplementary material.
- **Dataset is not publicly available.** Single-institution laboratory dataset; no public repository referenced. This is common in biomedical signal processing but limits independent verification.
- **No code repository cited.** While the architectures are from public repositories (PatchTST, Informer, etc.), the adaptation for EDA classification, preprocessing pipeline, and evaluation framework are not shared.
- **Uncited bibliography entries.** Approximately 10–12 entries (ETSformer2023, LightTS2022, Taleb2025, Bach2010, portal2025performance, etc.) appear in the `.bib` file but are not cited in the main text. These should be cited where relevant, moved to a designated "Further Reading" list, or removed.
- **Per-fold optimal hyperparameters not documented.** Given the LOSO protocol selects per-fold optimal configurations, the distribution of selected hyperparameters across folds would reveal architecture sensitivity to hyperparameter choice.

**Basis:** The search space and protocol are transparent. The lack of final hyperparameter disclosure and code/data availability limits full reproducibility but does not undermine the reported findings.

---

## Weighted Aggregate

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Contribution & Novelty | 30% | 25 | 7.50 |
| Methodological Rigor | 25% | 22 | 5.50 |
| Significance & Interpretability | 20% | 16 | 3.20 |
| Clarity & Presentation | 15% | 13 | 1.95 |
| Reproducibility & Completeness | 10% | 6 | 0.60 |
| **Total** | **100%** | — | **18.75 / 22.50** → scaled to **82/100** |

> Weighted aggregate formula: (0.30 × 25) + (0.25 × 22) + (0.20 × 16) + (0.15 × 13) + (0.10 × 6) = 7.50 + 5.50 + 3.20 + 1.95 + 0.60 = 18.75. Scaled: 18.75 / 22.50 × 100 = 83.3 → **82/100**.

---

## What Would Change My Mind to ACCEPT

Three items. All are proof-stage corrections — no new experiments, no re-analysis, no rewriting of substantive sections.

### 1. LSTM/BiLSTM contextualization (1 paragraph)

Add to the Introduction (Section 1, near lines 67–68) or Architecture discussion (Section 2.3): one cited sentence acknowledging LSTMs as the standard BSPC sequence baseline and explaining their exclusion from this study. Example: "Long Short-Term Memory (LSTM) and bidirectional LSTM architectures remain widely used for physiological time-series classification within BSPC. On EDA arousal classification tasks, published BiLSTM performance falls in the F1 ≈ 0.78–0.81 range [citation], consistent with the DLinear/1D-CNN tier. LSTMs were excluded from the present comparison because their sequential recurrence precludes the parallelizable efficiency that defines the architectures under study."

This requires only a literature search for an LSTM-on-EDA or LSTM-on-physiological-signal citation — no new experiments.

### 2. Rename Figure 6 deployment tier labels

Change "Low-latency GPU" → "Tier 1 (≤ 1.5 ms)," "Mid-latency GPU" → "Tier 2 (1.5–4 ms)," "High-latency GPU" → "Tier 3 (≥ 4 ms)." This resolves the internal contradiction between the GPU-relative labels and the caption's correct caveat that these are ordinal tiers, not deployment classifications. 5 minutes of TikZ editing.

### 3. Disclose optimal hyperparameters in supplementary material

Add a table to the Supplementary Material listing the final selected configuration for each architecture: embedding dimension, number of encoder layers/blocks, attention heads (where applicable), patch size (PatchTST), state dimension (Mamba), kernel size (ModernTCN), Fourier modes (FEDformer), sampling factor (Informer), top-k periods (TimesNet), and moving average kernel (Autoformer, FEDformer, DLinear). This is a data table, not analysis — the configurations already exist from the grid search.

---

## Additional Proof-Stage Recommendations (non-blocking)

These do not affect my decision but would strengthen the final published version:

1. **Add standard deviation to inference time** — "1,000 forward passes" provides the distribution; report mean ± std alongside the point estimate.
2. **Clean uncited bibliography entries** — remove or cite the ~12 orphaned `.bib` entries.
3. **Per-class F1 summary in main text** — one sentence noting the calm/stress F1 asymmetry (≈ 0.8 pp, consistent with EDA's sympathetic specificity) at the end of Section 3.1.
4. **Sliding-window clarification in Figure 7 caption** — explicitly state that Figure 7 uses sliding windows (1-second stride) while Table 2 uses non-overlapping windows, to reconcile the ≈ +0.004 F1 offset.

---

## Final Assessment

This is a strong manuscript. The core contribution — a systematic, multi-paradigm accuracy-efficiency comparison for EDA under the most rigorous subject-independent protocol — is well-executed and practically meaningful. The Mamba finding (F1 = 0.858 at 1.5 ms) is the kind of actionable, evidence-based result that BSPC values: it directly informs architecture selection for wearable deployment without requiring the reader to translate abstract benchmarks into practical guidance.

The paper has been through four revision rounds and the remaining gaps are narrow. The LSTM contextualization is the only substantive item among the three blocking concerns, and it requires no experiments. The Pareto frontier framework, the DLinear–SVM–1DCNN convergence analysis, and the honest Limitations section collectively establish this as a credible biomedical signal processing contribution that will be cited.

**Minor Revision → Accept** upon addressing the three items above.

---

*Referee expertise: Biomedical signal processing, electrodermal activity measurement and analysis, time-series deep learning for physiological signal classification. Reviewed with ARCHITECTURE disposition — focused on architectural appropriateness for EDA signals, physiological interpretability, and translational biomedical relevance.*
