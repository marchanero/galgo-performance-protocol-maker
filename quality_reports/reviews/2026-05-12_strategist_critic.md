# Strategist-Critic Experimental Design Audit
**Date:** 2026-05-12  
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification  
**Paper type:** Comparative benchmarking (primary) + application/deployment (secondary)  
**Review scope:** 4-phase structured audit of the full manuscript (767 lines main + 166 lines supplementary)  
**Target venue:** Biomedical Signal Processing and Control (BSPC) — LNCS/llncs format

---

## Paper Statistics (Verified)

| Metric | Value |
|--------|-------|
| Lines (main) | 767 |
| Lines (supplementary) | 166 |
| Sections | 4 (Introduction, Method, Results and Discussion, Conclusion) |
| Subsections (body) | 13 |
| Figures (main) | 6 (pipeline, architecture overview, F1 bars, efficiency bars, Pareto, window length) |
| Tables (main) | 4 (architectures, hyperparameters, overall performance, efficiency) |
| Tables (supplementary) | 4 (S1 channel ablation, S2 Wilcoxon, S3 per-class, S4 training) |
| Architectures evaluated | 8 (PatchTST, Informer, Autoformer, TimesNet, FEDformer, Mamba, ModernTCN, DLinear) |
| Paradigms represented | 5 (patch-based attention, sparse attention, frequency-domain, SSM, modernised convolution) |
| Participants | 147 |
| LOSO folds | 147 |

---

## Phase 1: Claim Identification

### Research Questions (RQ)

| ID | Question | Explicit? | Well-specified? |
|----|----------|-----------|-----------------|
| RQ1 | Can efficient/modern architectures approach/exceed PatchTST accuracy at substantially lower computational cost? | Yes (line 735–737) | Yes — operationalised via F1 + 5 efficiency metrics |
| RQ2 | What is the accuracy-efficiency Pareto frontier for EDA arousal classification under LOSO? | Yes (line 75, line 555–628) | Yes — explicit frontier identified in Figure 6 |
| RQ3 | How do different paradigms (attention, SSM, convolution, linear) interact with EDA phasic dynamics? | Yes (line 75, line 718–731) | Partially — operationalised via interpretability analysis and channel ablation, but no formal hypothesis tests |
| RQ4 | How does window length affect classification performance across paradigms? | Implicit (line 104–105, line 630–712) | Yes — adequately operationalised in Figure 6 |
| RQ5 | Do derivative channels provide marginal benefit, and does this vary by architecture paradigm? | Yes (line 400–401, line 730–731) | Yes — operationalised via channel ablation |

### Validation Protocol

- **Protocol:** Leave-One-Subject-Out (LOSO), 147 folds
- **Training/validation split:** 80/20 within 146 training subjects per fold
- **Test:** 1 held-out subject per fold
- **Metrics:** Accuracy, Precision, Recall, F1 (macro), AUC — plus 5 efficiency metrics
- **Hyperparameter tuning:** Grid search, 64 configurations per architecture, identical budget
- **Statistical testing:** Pairwise Wilcoxon signed-rank tests + Bonferroni-Holm correction
- **Anchoring baselines:** (1) 4 prior architectures from Sanchez-Reolid 2022, (2) classical EDA feature-engineering + SVM from Sanchez-Reolid 2020

### Scope Assessment

**Strengths:**

- Claims are explicitly stated and appropriately bounded to this dataset, this preprocessing pipeline, and this LOSO protocol.
- The paper does not overstate: it consistently uses "suggest", "indicate", "implies" rather than definitive causal language.
- The comparison with prior work (Sanchez-Reolid 2022) grounds the improvement in a transparent, reproducible context.
- The classical baseline (SVM + handcrafted features, F1 ≈ 0.81) anchors the deep learning results and prevents over-claiming.

**Concerns:**

- **C-P1.1 (MINOR):** The claim of "the first systematic comparison of eight efficient and modern architectures" for EDA is defensible, but the paper does not explicitly delimit the scope of "systematic comparison." The grid search (64 configs per model) is systematic; the model selection is not — it's a curated set. This is not a problem per se, but the word "systematic" in the abstract could be qualified (e.g., "systematic equal-budget comparison").

  *What would change my mind:* Wording tweak from "systematic comparison" to "systematic equal-budget comparison" in the abstract.

- **C-P1.2 (MINOR):** The "approximately 5 percentage point improvement" claim (line 58, 489) refers to the F1 gap between the classical/SVM/DLinear tier (≈0.80–0.81) and the best Transformer/SSM tier (≈0.858–0.863). This is a pooled estimate across two distinct comparisons (classical SVM vs. Mamba, classical SVM vs. PatchTST) with a retrospective baseline where only F1 point estimates are available. The claim is qualified, but the per-fold variance of the classical baseline is unknown, making a formal confidence interval impossible.

  *What would change my mind:* Reporting this as a range ("approximately 4.8–5.3 percentage points") or qualifying it as "retrospective comparison" rather than a point estimate.

### Phase 1 Verdict: PASS
Claims are well-specified, appropriately scoped, and consistent with the paper's benchmarking design. Two minor wording concerns.

---

## Phase 2: Core Design Validity

### 2.1 LOSO Protocol Enforcement

**Claim:** Test subject fully excluded from training, validation, AND normalization.

**Evidence:**
- Line 88–94: Preprocessing (FIR filter, Gaussian smoothing, CDA) is per-subject, single-signal — no cross-subject contamination possible at this stage.
- Line 370: "Z-score normalisation was computed using training-fold statistics only (mean and standard deviation estimated from training subjects within each fold) and applied identically to validation and test subjects." ✓
- Line 84: "All trials belonging to the same participant were preserved within the same fold during cross-validation to prevent subject-level data leakage." ✓
- Line 376–377: "In each of the 147 folds, one participant was withheld for testing, while the remaining 146 participants were used for training (80%) and validation (20%)." ✓

**Assessment:** The protocol is correctly described and the stated safeguards, if faithfully implemented, eliminate subject-level leakage. The CDA decomposition is per-subject, per-signal so it cannot leak across subjects.

**One caveat:** The FIR filter and Gaussian smoothing are described as "preprocessing" (line 88–89) applied before windowing. If these operations use per-signal parameters estimated from the entire recording, there is no leakage. However, if smoothing uses a fixed kernel width, there is no parameter estimation at all, so this is safe. The paper should clarify whether filtering/smoothing parameters are globally fixed or estimated per-subject. If globally fixed: safe. If estimated per-subject but before fold assignment: also safe since the operations are per-signal. This is a **documentation gap, not a leakage risk**.

**Verdict:** PASS. Z-score is explicitly within-fold. The FIR/CDA/smoothing pipeline is per-signal and inherently free of cross-subject contamination.

### 2.2 Equal Hyperparameter Budget (64 Configurations per Architecture)

**Claim:** Identical grid search budget (64 configurations) eliminates tuning bias.

**Evidence:**
- Line 345: "Hyperparameters were tuned using grid search with identical trial budgets (64 configurations per architecture) across all architectures."
- Table 2 (line 347–368): Detailed search space per architecture with architecture-specific parameters explicitly marked.

**Assessment:**

| Architecture | Continuous params | Categorical params | Total combos | Grid points |
|-------------|-------------------|-------------------|-------------|-------------|
| PatchTST | 4 cont + 1 cat | 4×3×4×4×3 = 576 | Wrapped to 64 |
| Informer | 3 cont + 2 cat | 4×3×4×4 = 192 + 3 cat | Wrapped to 64 |
| Mamba | 2 cont + 2 cat | 4×3×4×4 = 192 + 3 cat | Wrapped to 64 |

**Strengths:**
- The equal trial budget (64) is explicitly justified and transparent.
- Architecture-specific parameters are enumerated (patch size, sampling factor, state dimension, kernel size, moving average window), which is honest about cross-architecture differences.

**Concerns:**

- **C-P2.2.1 (MODERATE):** "Identical trial budgets" does NOT equal "equal effective search coverage." With 64 grid configurations, architectures with more hyperparameters (PatchTST: 5 tuned dimensions) have proportionally sparser coverage of their search space than architectures with fewer parameters (DLinear: 3 tuned dimensions). The total search space for PatchTST is 576 combinations (4×3×4×4×3), while DLinear has substantially fewer (4×3×4 = 48, if moving average kernel is the only architecture-specific parameter besides encoders, embedding, FF). With 48 possible configurations, DLinear effectively undergoes exhaustive search; PatchTST's 64 configurations cover only 11% of its space. This is not necessarily a bias — both are tuned — but the paper should acknowledge this differential coverage.

  *What would change my mind:* Adding a sentence in the limitations section noting that the grid search density differs across architectures due to different numbers of tunable parameters, and that this could favour simpler architectures where near-exhaustive coverage is achieved. Alternatively, computing the effective coverage ratio for each architecture.

- **C-P2.2.2 (MINOR):** The paper states "the optimal configuration for each fold was selected based on validation F1-score" (line 345). This means a different hyperparameter configuration may be selected for each of the 147 folds. The paper should clarify: (a) Are the results in Table 3 based on per-fold optimal configurations (i.e., 147 potentially different hyperparameter sets), or a single configuration selected as best-on-average across folds? (b) If per-fold optimal, is this a realistic deployment scenario? In practice, you would select one configuration for all subjects.

  *What would change my mind:* Clarifying the hyperparameter selection and reporting strategy, and if per-fold optimal is used, discussing the deployability implication.

**Verdict:** PASS with 2 concerns. The equal-budget approach is fair **in principle**, but differential grid coverage and per-fold vs. global optimal selection are underdiscussed.

### 2.3 Z-score Normalization Within Folds

**Claim:** Z-score within-fold prevents test-subject leakage.

**Evidence:** Line 370: "Z-score normalisation was computed using training-fold statistics only (mean and standard deviation estimated from training subjects within each fold) and applied identically to validation and test subjects."

**Assessment:** This is a textually clear statement. If implemented as described, it correctly prevents leakage. No concerns.

**One unaddressed question:** The paper uses per-fold Z-score, meaning each LOSO fold normalises its training and test subjects to zero mean, unit variance based on training subjects. This is methodologically sound for within-fold evaluation. However, it complicates the comparison of performance **across folds** — the test subject in fold 1 is normalised to different statistics than the test subject in fold 2. This affects the interpretation of the per-fold F1 distribution and therefore the Wilcoxon test. This is inherent to LOSO + within-fold normalisation and not a flaw, but worth acknowledging.

**Verdict:** PASS.

### 2.4 Same-Subject Windows Preserved in Same LOSO Fold

**Claim:** All windows from the same subject remain in the same fold.

**Evidence:** Line 84: "All trials belonging to the same participant were preserved within the same fold during cross-validation to prevent subject-level data leakage."

**Assessment:** This is the correct, standard practice for subject-dependent physiological data (Azad 2025). No concerns.

**Verdict:** PASS.

### 2.5 Separate GPU for Inference (Quadro P5000) vs Training (RTX 4080)

**Claim:** Inference benchmarking on a deployment-class GPU provides more realistic latency estimates.

**Evidence:**
- Line 343: Training on RTX 4080 (16 GB GDDR6X, Ada Lovelace).
- Line 343: Inference on Quadro P5000 (16 GB GDDR5X, Pascal, 2560 CUDA cores).

**Assessment:**

**Strengths:**
- Using a separate, older GPU for inference is methodologically appropriate for a deployment-focused paper. The Quadro P5000 is closer to embedded/deployment hardware than the RTX 4080.
- The paper explicitly acknowledges that absolute latency will differ on target hardware (line 746).

**Concerns:**

- **C-P2.5.1 (MINOR):** The Quadro P5000 (Pascal, 2016) is still a workstation-class GPU with 16 GB VRAM and 2560 CUDA cores. It is far more powerful than actual embedded deployment hardware (Jetson Nano: 128 CUDA cores, 4 GB; Raspberry Pi: 0 CUDA cores). The latency tiers (1.5 ms, 4 ms) are therefore "workstation-class floor" values, not deployment estimates. The paper acknowledges this (line 619, 746) but the shaded Tier 1–3 regions in Figure 6 could mislead a casual reader into thinking these are actual deployment feasibility boundaries. The figure caption now includes the disclaimer — this is adequate.

  *What would change my mind:* Not needed; the disclaimer is already present. No action required beyond possibly renaming "Deployment regions" to "GPU-relative latency tiers" (the figure caption already does this — Figure 6 caption: "these tiers serve as GPU-relative rankings, not deployment classifications").

- **C-P2.5.2 (MINOR):** Inference time is averaged over 1,000 forward passes (line 389). For Mamba (1.5 ms), this is well-averaged. But for DLinear (0.3 ms), 1,000 passes = 300 ms total measurement window, which may be influenced by GPU warm-up, kernel launch overhead, and CUDA synchronisation granularity. DLinear's 0.3 ms is below typical CUDA kernel launch overhead (≈5–10 µs per kernel, but multiple kernels). At 0.3 ms, measurement precision may be ±0.05 ms or worse. This does not affect the Pareto frontier materially (DLinear is trivially fastest regardless), but the precision claim should be tempered.

  *What would change my mind:* Reporting measurement uncertainty (±std over the 1,000 passes) for inference time, or acknowledging sub-ms measurement granularity for DLinear and ModernTCN.

**Verdict:** PASS with minor measurement precision concern. The separate-GPU approach is appropriate and well-documented.

### 2.6 Five Efficiency Metrics — Correctness and Consistency

**Claim:** Five complementary efficiency metrics measured under consistent conditions.

**Evidence (line 384–394):**
1. **Parameter count:** Trainable parameters (M). Standard metric. ✓
2. **FLOPs:** Forward pass, thop library (PyTorch-OpCounter). Acknowledged as estimate (line 750). ✓
3. **Inference time:** 1,000 forward passes, batch size = 1, Quadro P5000. ✓
4. **Peak memory:** Maximum GPU memory during forward pass, including weights, activations, framework overhead. ✓
5. **Training time:** Per-epoch wall-clock, RTX 4080, batch size 32. ✓

**Concerns:**

- **C-P2.6.1 (MINOR):** The three deployment-focused metrics (params, FLOPs, inference, memory) are measured at batch size 1. The training-time metric is measured at batch size 32. This is justified — deployment inference is typically single-sample, while training uses mini-batches. But the reader may miss this distinction; it should be explicitly stated: "Batch size = 1 for single-inference metrics, batch size = 32 for training time."

  The paper already says "batch size = 1 for single-inference metrics" in line 384, and training context in line 343 mentions batch size 32. This is adequate. ✓

- **C-P2.6.2 (MINOR):** Peak memory is reported as a single value per architecture. However, peak memory during a forward pass with batch size 1 includes: (a) model weights, (b) input tensor, (c) intermediate activations, (d) PyTorch autograd graph (even in `torch.no_grad()`, some framework overhead persists), and (e) CUDA context. The contribution of (e) is architecture-independent but non-zero (typically 300–500 MB for CUDA context on a 16 GB GPU). For DLinear (8 MB reported), the CUDA context overhead dominates. The paper should clarify whether framework/CUDA overhead is included or subtracted.

  *What would change my mind:* Clarifying whether CUDA context overhead is included, and if so, noting that DLinear's 8 MB is dominated by framework overhead rather than model memory.

- **C-P2.6.3 (MINOR):** FLOPs are computed with thop, an estimate library. The paper acknowledges this (line 750). For SSMs like Mamba, thop may not accurately count the parallel scan operations, which are implemented as custom CUDA kernels. Mamba's FLOPs (12.8 M) may be underestimated relative to its actual compute. The paper's reporting of both FLOPs and wall-clock inference time partially mitigates this.

  *What would change my mind:* Adding a note that FLOPs for Mamba may be underestimated due to custom scan kernel operations not captured by thop.

**Verdict:** PASS with minor documentation concerns. The metrics are well-chosen, measured under appropriate conditions, and the paper is transparent about limitations.

### 2.7 Single Seed (42) and No PyTorch Deterministic Mode

**Claim:** Single seed limitation discussed but not resolved.

**Evidence:**
- Line 343: "All experiments used a single random seed (42) for parameter initialisation and data ordering."
- Line 343: "PyTorch deterministic algorithms were not enabled due to CUDA performance constraints."
- Line 343: "Consequently, the per-fold standard deviations reported in Section 3.1 may partially reflect seed-dependent weight initialisation in addition to inter-subject variability — a limitation discussed in Section 3.8."

**Assessment:**

**Strengths:**
- The paper explicitly acknowledges this as a limitation.
- The justification (CUDA performance constraints) is plausible: `torch.use_deterministic_algorithms(True)` substantially degrades performance on CUDA, especially with attention operations.
- The per-fold standard deviations are interpreted as reflecting both inter-subject variability AND seed sensitivity — this is honest.

**Concerns:**

- **C-P2.7.1 (MODERATE):** With 147 LOSO folds, the effect of seed-dependent initialization is averaged over 147 independently initialised models (assuming each fold trains from scratch). This provides partial mitigation against seed sensitivity — the per-fold mean F1 averages over 147 random initialisations. However, the paper reports "standard deviation across 147 folds" (e.g., PatchTST: 0.863 ± 0.051). This standard deviation conflates inter-subject variability (the quantity of interest) with seed sensitivity. The paper acknowledges this but does not quantify how much of the variance is attributable to seed vs. subject.

  Furthermore, with a single seed, the ranking of architectures could be seed-dependent. If Mamba benefits more from seed 42 than PatchTST, the F1 ranking could flip with a different seed. The observed ΔF1 between Mamba and PatchTST is 0.005 (p = 0.048, uncorrected), which is extremely close to the significance threshold. Even a small seed-induced perturbation could change the pairwise ordering and its statistical significance.

  *What would change my mind:* (a) A sensitivity check with 3 seeds on a subset of architectures (e.g., the top 3: PatchTST, Mamba, TimesNet) to bound the seed-induced variation; or (b) a more prominent limitation statement noting that the Mamba–PatchTST comparison (ΔF1 = 0.005) is particularly sensitive to seed choice, and the ranking should be interpreted cautiously; or (c) a statement that across 147 random initialisations (one per fold), the mean F1 estimate is substantially more stable than single-seed per-fold, and the reported ranking is therefore robust despite the single global seed.

- **C-P2.7.2 (MINOR):** The paper uses a single seed for data ordering as well as parameter initialization. While LOSO folds are inherently deterministic (subject-based, not random), the training data ordering within each fold may affect SGD trajectory if not shuffled per epoch. Standard practice uses per-epoch shuffling, which introduces randomness regardless of the initial seed. The paper does not specify whether per-epoch shuffling is used — if it is, the single-seed issue is partially mitigated (shuffling provides a different order each epoch), but the per-fold variance still partially reflects seed. If per-epoch shuffling is NOT used, this would be a more serious concern.

  *What would change my mind:* Clarifying whether per-epoch data shuffling is used.

**Verdict:** PASS with concerns. The paper is transparent about this limitation, but the single-seed choice is especially consequential given the narrow Mamba–PatchTST margin (ΔF1 = 0.005). The severity of this concern depends on whether the 147-fold averaging provides sufficient mitigation.

### 2.8 Validation Split (80/20 within Training Subjects)

**Claim:** 20% hold-out within training subjects for hyperparameter selection.

**Evidence:** Line 343–345: "Training was conducted for up to 100 epochs with early stopping (patience = 15) based on validation loss computed on a 20% hold-out subset of the training subjects within each LOSO fold."

**Assessment:**

**Strengths:**
- Within-fold validation split prevents test-subject leakage.
- The paper uses validation F1 (not loss) for hyperparameter selection, which aligns with the primary evaluation metric.

**Concerns:**

- **C-P2.8.1 (MINOR):** The 80/20 split is performed within the 146 training subjects, yielding approximately 117 training / 29 validation subjects per fold. With only 29 validation subjects, the validation F1 used to select the optimal hyperparameter configuration has non-trivial variance. The paper does not report validation F1 variance or discuss whether the selected configuration is stable under different 80/20 splits.

  However, the grid search selects from 64 configurations, and the best-on-validation configuration is then evaluated on the single test subject. This 20% hold-out is a hyperparameter selection set, not a generalisation estimate. The test-subject F1 is the generalisation estimate. So the impact of validation-set variance is on **which configuration is selected**, not on the reported performance. Configurations with similar validation F1 may have different test F1, and with only 29 validation subjects, the selected configuration may not be the true optimum. This is inherent to any validation-based model selection.

  *What would change my mind:* Adding a note on the limited validation set size (29 subjects) and its potential impact on hyperparameter selection stability.

- **C-P2.8.2 (MINOR):** The 80/20 split is presumably random within each fold. Is the same random split used across all folds (e.g., subject ID-based split), or a different random split per fold? If the same 20% of subjects are used for validation across all 147 folds, those subjects never serve as test subjects, reducing the effective number of unique test subjects from 147 to some smaller number. This would be a CRITICAL error. The paper should confirm.

  *What would change my mind:* Clarifying whether the 80/20 split is per-fold random (different validation set per fold) or fixed across folds. If fixed across folds, this is a CRITICAL concern because some subjects are never tested.

**Verdict:** NEEDS CLARIFICATION. The 80/20 split mechanism must be specified more precisely — specifically whether validation subjects vary per fold.

### 2.9 Wilcoxon Independence Assumption Violation

**Claim:** LOSO folds share 146/147 subjects in training sets; p-values should be interpreted as descriptive.

**Evidence:**
- Line 716: "Mamba achieves F1 = 0.858, approaching PatchTST (F1 = 0.863) — a difference of 0.005 that is statistically significant at the conventional α = 0.05 level (p = 0.048) but does not survive the stringent Bonferroni-Holm correction for 28 comparisons."
- Line 748: "The Wilcoxon signed-rank test used for pairwise comparisons assumes independence of paired differences across folds. With leave-one-subject-out cross-validation, training sets for different folds share 146 of 147 subjects, introducing overlap that may inflate the effective sample size. The reported p-values should be interpreted as descriptive indicators of effect consistency rather than exact inferential statistics."

**Assessment:**

**Strengths:**
- The paper explicitly acknowledges the assumption violation (line 748). This is unusually transparent for the field.
- The Bonferroni-Holm correction is applied, providing a more conservative threshold.
- Effect sizes (F1 differences in pp) are reported alongside p-values.

**Concerns:**

- **C-P2.9.1 (MODERATE):** The acknowledgment is good, but the paper continues to use p-values as decision criteria in the text. For example, line 626: "The 0.005 F1 difference between Mamba and PatchTST reaches the conventional α = 0.05 threshold (p = 0.048) but does not survive the Bonferroni-Holm correction." This gives the reader a mixed message: "these p-values are not valid inferential statistics" BUT "we'll still report whether they cross α = 0.05." The first 13 lines of Section 3.5 perform conventional NHST interpretation on potentially inflated test statistics.

  *What would change my mind:* Consistently treating p-values as descriptive throughout (e.g., "p = 0.048, indicating weak consistency of the effect across folds under this test") rather than invoking significance thresholds.

- **C-P2.9.2 (MINOR):** A more appropriate analysis for this data structure would be a linear mixed-effects model (random intercepts for subject, fixed effects for architecture) or a cluster-robust bootstrap that accounts for the nested structure. The paper does not need to implement these, but acknowledging their absence and the reason (LOSO folds are not independent observations under any correction) would strengthen the limitations.

  *What would change my mind:* Adding a sentence suggesting that future work could employ mixed-effects models or bootstrapping approaches that properly account for the dependence structure.

**Verdict:** PASS with concerns. The transparency is commendable, but the paper's mixed treatment of p-values (acknowledging the violation while still performing NHST) creates tension in the narrative.

### 2.10 Claims about "Pareto Frontier" and "Approximately 5 pp Improvement"

**Pareto Frontier Claim:** Figure 6 identifies DLinear → ModernTCN → Mamba → PatchTST as the Pareto-optimal set.

**Assessment:**

**Strengths:**
- The Pareto frontier is correctly constructed: these four architectures are genuinely non-dominated. No other architecture simultaneously achieves higher F1 AND lower inference time.
- The diminishing returns pattern is visually striking and well-discussed.
- The deployment tier concept (Tier 1–3) contextualises the frontier for practitioners.

**Concerns:**

- **C-P2.10.1 (MINOR):** The Pareto frontier is defined with respect to two dimensions: F1 (accuracy) and inference time (latency). However, the paper reports five efficiency metrics. The frontier in parameter count × F1 or memory × F1 space may differ. Mamba dominates ModernTCN in F1 but has 1.8× more parameters (1.52M vs 0.85M). If parameter count were the efficiency axis, ModernTCN would appear on the frontier. The paper should note that the frontier is contingent on the chosen efficiency axis and may shift under different deployment constraints.

  *What would change my mind:* Adding a note that the Pareto frontier is defined in (F1, inference time) space, and the optimal architecture depends on the specific deployment constraint (memory-limited vs. latency-limited vs. FLOP-limited).

- **C-P2.10.2 (MINOR):** TimesNet (F1 = 0.853 at 3.0 ms) and Informer (F1 = 0.845 at 3.6 ms) are both dominated by Mamba (F1 = 0.858 at 1.5 ms). But this assumes that inference time measured on a Quadro P5000 is monotonic with respect to inference time on all deployment hardware. As acknowledged in Section 3.8, the relative ordering is "expected to be preserved across platforms with comparable memory bandwidth and parallel compute characteristics." For hardware with fundamentally different architectures (e.g., DSPs, FPGAs), the ordering could change. This is a minor concern given the acknowledged limitations.

  *What would change my mind:* Already addressed by the limitations section. No further action needed beyond potential qualifying the Pareto frontier as GPU-relative.

**"Approximately 5 pp Improvement" Claim:** The classical EDA feature-engineering + SVM achieved F1 ≈ 0.80–0.83, while PatchTST/Mamba achieve F1 ≈ 0.858–0.863.

**Assessment:**

**Strengths:**
- This comparison anchors the deep learning results in a meaningful classical baseline.
- The paper correctly identifies that the gap narrows when comparing against prior convolutional architectures (1D-CNN: 0.796, not 0.81).

**Concerns:**

- **C-P2.10.3 (MINOR):** The "approximately 5 pp" claim pools two conceptually distinct comparisons: (a) classical SVM (retrospective, single F1 point estimate) vs. PatchTST (prospective, 147-fold mean), and (b) DLinear (prospective, this study) vs. PatchTST (prospective, this study). These occupy different levels of evidence. The retrospective baseline lacks per-fold standard deviations, and its F1 range (0.80–0.83) reflects varying window lengths in the original study, not LOSO fold variance. The paper handles this honestly in the table notes (line 436–441) but should avoid presenting these two comparisons as a single pooled estimate.

  *What would change my mind:* Separating the two comparisons: "The classical SVM baseline and DLinear both achieve F1 ≈ 0.80–0.81, while the best deep learning models achieve F1 ≈ 0.86. This represents a 5–6 pp improvement for models with global temporal modelling."

**Verdict:** PASS with minor framing concerns. Both claims are defensible and appropriately qualified in the text.

### 2.11 Missing Sanity Checks and Robustness Tests

**Present:**
- Channel ablation (Table S1) — varying input channels ✓
- Window-length analysis (Figure 6) — varying temporal context ✓
- Per-class F1 (Table S3) — assessing class asymmetry ✓
- Per-fold standard deviations — assessing inter-subject robustness ✓
- Classical baseline — anchoring deep learning performance ✓
- Wilcoxon significance tests — formal pairwise comparison ✓

**Potentially Missing:**

- **C-P2.11.1 (MODERATE):** No per-subject performance distribution. The paper reports mean ± std across 147 folds, but does not show the distribution of per-subject F1 scores (histogram, boxplot, or at minimum quartiles). This matters because a mean F1 of 0.863 could mask bimodal performance (e.g., 130 subjects at F1 > 0.90, 17 subjects at F1 < 0.60). Per-subject distributions would reveal whether poor performance clusters in specific subjects, which is clinically/operationally relevant.

  *What would change my mind:* Adding a per-subject F1 histogram or boxplot (even in supplementary), or reporting the 5th/25th/50th/75th/95th percentiles.

- **C-P2.11.2 (MINOR):** No calibration analysis. AUC is reported, but calibration error (expected calibration error, ECE; reliability diagrams) is not assessed. For a binary classification task where decisions may trigger clinical interventions, calibration quality matters: a model with AUC = 0.91 could still systematically over/under-estimate arousal probability. This is a nice-to-have, not a requirement for a benchmarking paper.

  *What would change my mind:* Not essential for this paper type. Could be noted as a potential future analysis.

- **C-P2.11.3 (MINOR):** No analysis of per-trial performance by stimulus type. The dataset contains audiovisual stimuli designed to induce calm and stress states, but the paper does not examine whether classification difficulty varies by specific stimulus content (e.g., are certain calm-inducing stimuli harder to classify?). This is a secondary analysis for a domain/application paper.

  *What would change my mind:* Not required. Could be noted as out of scope.

- **C-P2.11.4 (MINOR):** No formal test of the "diminishing returns" claim on the Pareto frontier. The paper states "The shape of the Pareto frontier reveals a clear diminishing returns pattern" (line 626). This is visually apparent but not quantitatively assessed (e.g., slope of the frontier segments, marginal F1 gain per ms of latency). This is a stylistic choice, not a methodological flaw.

  *What would change my mind:* Quantifying the marginal gain per unit latency along the frontier (e.g., ΔF1/Δms).

- **C-P2.11.5 (MODERATE):** No robustness to preprocessing choices. The paper uses CDA decomposition but acknowledges that cvxEDA and Ledalab produce different phasic estimates (line 94). The paper states "the choice of decomposition method is known to influence downstream signal characteristics" but does not evaluate whether the architecture ranking changes under a different decomposition method. This is concerning because the paper's practical deployment guidance ("use Mamba for edge deployment") implicitly assumes the ranking is stable under reasonable preprocessing variation.

  *What would change my mind:* (a) Evaluating the top 3 architectures (PatchTST, Mamba, TimesNet) under cvxEDA decomposition as a robustness check; or (b) explicitly stating that the architecture ranking is conditioned on CDA decomposition and may not generalise to other preprocessing pipelines.

- **C-P2.11.6 (MINOR):** No demographic stratification. The dataset includes 147 participants aged 18–44, but no subgroup analysis by age, sex, or other demographic variables is performed. For a deployment paper, it is useful to know whether certain architectures perform better/worse for specific demographic subgroups.

  *What would change my mind:* Not required for a benchmarking paper. Could be noted as future work.

- **C-P2.11.7 (MINOR):** No formal comparison of non-overlapping vs. sliding window segmentation. The paper mentions that sliding windows produce +0.004 F1 on average (line 710–711) but does not present this as a formal analysis. Given the practical relevance (sliding windows increase training data but introduce temporal dependence between windows within a subject), a brief comparative table would be useful.

  *What would change my mind:* Reporting the sliding window F1 values alongside non-overlapping in the supplementary.

**Verdict:** PASS with concerns. The most notable gaps are: (1) no per-subject performance distribution, which could mask bimodal failure cases; (2) no preprocessing sensitivity analysis given that architecture rankings may depend on decomposition method.

---

### Phase 2 Overall Verdict: PASS with 6 concerns documented
(1 MODERATE: hyperparameter grid coverage asymmetry; 1 MODERATE: single-seed sensitivity at narrow margin; 1 NEEDS CLARIFICATION: validation split per-fold mechanism; plus minor concerns as documented)

---

## Phase 3: Inference

### 3.1 Statistical Tests: Wilcoxon + Bonferroni-Holm

**Assessment:**

**Strengths:**
- Wilcoxon signed-rank test is appropriate for paired per-fold F1 comparisons (non-parametric, handles non-normal distributions typical of per-subject metrics).
- Bonferroni-Holm correction is applied to control family-wise error rate across 28 pairwise comparisons.
- Both raw and corrected p-values are reported in Table S2 and discussed in the text.

**Concerns:**

- **C-P3.1.1 (MODERATE, also in C-P2.9.1):** The independence assumption is violated (LOSO training sets overlap by 146/147 subjects). The paper acknowledges this (line 748) but the test is still presented as the primary inferential tool. The appropriate framing would be: "We report Wilcoxon p-values as descriptive indicators of between-architecture F1 consistency across folds, with the caveat that the independence assumption of the test is not satisfied under LOSO." The current text (line 748) gets close to this but precedes it with conventional NHST framing.

  *What would change my mind:* Replacing p-value threshold language ("significant at α = 0.05") with descriptive effect-size language throughout Section 3.5, and moving the independence caveat BEFORE the p-value reporting.

- **C-P3.1.2 (MINOR):** The Bonferroni-Holm correction is applied to 28 comparisons, but these 28 comparisons are not independent (they involve the same 8 models). The Bonferroni-Holm correction controls FWER even under dependence (it's conservative), so this is statistically valid. However, the paper could note that more powerful alternatives exist (e.g., permutation-based max-T correction) if stronger inferential claims were desired.

  *What would change my mind:* Not needed. Bonferroni-Holm is conservative but valid.

**Verdict:** PASS. Tests are appropriate in principle; the independence assumption violation is the primary concern (addressed in Phase 2.9).

### 3.2 Effect Sizes

**Evidence:**
- F1 differences in percentage points are reported throughout (line 489: "+4.8 pp, +5.3 pp"; line 626: "0.005 F1 difference"; line 738: "66% reduction in parameter count").
- Per-fold standard deviations are reported (Table 3) allowing Cohen's d-like reasoning.
- Efficiency ratios are reported (3.6× latency reduction, 35× training speed difference).

**Assessment:** Effect sizes are consistently reported alongside p-values, which is good practice and partially mitigates the independence assumption concern. One minor note: Cohen's d or similar standardised effect sizes are not formally reported, but F1 differences in percentage points are interpretable in this domain.

**Verdict:** PASS.

### 3.3 Code-Theory Alignment: Reproducibility

**What the paper provides:**
- Detailed hyperparameter search space (Table 2)
- Architecture descriptions with mathematical formulations for core mechanisms
- Training protocol: optimizer (AdamW), learning rate (1e-3), cosine annealing, batch size 32, early stopping patience 15, dropout range, weight decay, gradient clipping
- Preprocessing pipeline described step-by-step
- Dataset description: 147 participants, 40 s windows, 4 Hz, CDA decomposition

**What is missing for full reproducibility:**
- No code repository reference or URL. The paper does not indicate whether the implementation code will be released.
- No mention of which specific implementations were used (e.g., official author repositories, TSlib, custom implementations).
- No detailed description of the architecture adaptations for classification (e.g., how exactly the forecasting head was replaced, classifier layer dimensions).
- The bidirectional Mamba configuration (Bi-Mamba) is described conceptually (line 331) but implementation details (concatenation vs. averaging of forward/backward outputs, number of Mamba blocks, expansion factor) are not specified precisely enough to reproduce without consulting the Mamba/ECGMamba paper or code.
- Data availability: "controlled stress elicitation protocol described in previous work" — the dataset is not publicly available (not stated as such, but no access link or repository is provided).

**Assessment:**

- **C-P3.3.1 (MODERATE):** For a paper that makes explicit deployment recommendations ("A practitioner deploying an EDA-based stress monitor on a smartwatch... can consult Figure 6"), the absence of code release plans undermines the claimed practical impact. The paper should at minimum state whether code will be released, and if so, where.

  *What would change my mind:* Adding a "Code and Data Availability" statement.

- **C-P3.3.2 (MINOR):** The architecture adaptations for classification (forecasting head → global average pooling → linear classifier) are described qualitatively but lack specific dimension information. For example, for PatchTST: what is the embedding dimension? The grid search range is given (16–128), but the optimal value used for the reported results is not stated. Same for all architectures.

  *What would change my mind:* Reporting the optimal hyperparameter configuration per architecture in a supplementary table.

**Verdict:** NEEDS IMPROVEMENT. The methodology description is detailed for the experimental protocol but thin on implementation specifics. The absence of code availability information is a gap for a deployment-focused paper.

### Phase 3 Verdict: CONDITIONAL PASS
Statistical tests are appropriate with acknowledged limitations. Effect sizes are well-reported. Reproducibility documents need improvement (code availability, optimal hyperparameter values).

---

## Phase 4: Polish and Completeness

### 4.1 Robustness Checks: Sufficiency Assessment

| Check | Present? | Quality |
|-------|----------|---------|
| Channel ablation | ✓ (Table S1) | Good — 3 conditions, all 8 architectures |
| Window-length analysis | ✓ (Figure 6) | Good — 17 window lengths, all 8 architectures |
| Per-class F1 | ✓ (Table S3) | Adequate — calm/stress breakdown |
| Per-fold variability | ✓ (Table 3) | Good — mean ± std across 147 folds |
| Sliding vs. non-overlapping | ✓ (mentioned, line 710) | Minimal — only +0.004 avg offset stated |
| Multiple efficiency metrics | ✓ (Table 4) | Good — 5 complementary metrics |
| Classical baseline | ✓ (Table 3, note) | Good — anchors DL performance |
| Statistical significance | ✓ (Table S2) | Good — raw + corrected p-values |

**Missing or underdeveloped:**
- Preprocessing sensitivity (CDA vs. cvxEDA vs. Ledalab) — acknowledged but not tested
- Per-subject performance distribution — not reported
- Demographic stratification — not reported
- Calibration error — not reported
- Multiple seeds — not tested (acknowledged)
- Cross-dataset generalisation — acknowledged as future work

**Assessment:** For a benchmarking paper, the robustness checks are comprehensive. The two most important missing checks (preprocessing sensitivity and per-subject distributions) are discussed above (C-P2.11.1, C-P2.11.5).

### 4.2 Limitations Section: Quality Assessment

**What the limitations section covers (line 742–750):**
1. Single laboratory dataset, controlled conditions, healthy participants — generalisability unknown ✓
2. CDA decomposition only — different decomposition methods may produce different architecture rankings ✓
3. Single GPU inference benchmarking — absolute latencies hardware-specific ✓
4. Wilcoxon independence assumption violation — p-values should be descriptive ✓
5. FLOPs estimation via thop — hardware-independent estimate, not actual compute ✓

**What is missing from the limitations section:**
1. Single seed (discussed in Section 3.8 but NOT in the limitations section — line 343 mentions it but Section 3.8 does not contain a dedicated limitations subsection; the seed limitation appears only in the training description).
2. Per-fold hyperparameter selection vs. global optimal — not discussed.
3. Differential grid search coverage across architectures — not discussed.
4. Validation split mechanism and stability — not discussed.
5. Code/data availability — not mentioned anywhere in the paper.

- **C-P4.2.1 (MODERATE):** The limitations section is thorough by the standards of the field but has an omission: the single-seed limitation, discussed only in the training description (line 343), should receive explicit mention in the limitations.

  *What would change my mind:* Adding a sentence on single-seed limitations to Section 3.8 or the Conclusion limitations.

- **C-P4.2.2 (MINOR):** The limitations section (line 742–750) is embedded within Section 3 of the paper ("Results and Discussion"). In many papers, limitations appear in the Conclusion section. This is a stylistic choice and not a concern, but the numbering suggests Section 3.8 is a subsection of Results — it should be clear that this is reflective meta-analysis, not results.

  *What would change my mind:* Not needed. Stylistic preference.

**Verdict:** GOOD with one notable omission (single seed).

### 4.3 Missing Analyses

**Calibration error:** Not assessed. For a deployment paper where predicted probabilities might drive interventions, ECE or reliability diagrams would be useful. This is a nice-to-have.

**Demographic stratification:** Not assessed. Given 147 participants aged 18–44, subgroup analysis by age or sex could reveal differential architecture performance. This is domain/application territory rather than core benchmarking.

**Test-retest reliability:** Not assessed. The dataset is a single session per participant; test-retest reliability of architecture ranking across sessions is unknown. This is beyond the scope of the current paper.

**Cross-dataset generalisation:** Acknowledged as future work (line 744–745: "Cross-dataset evaluation on publicly available benchmarks such as WESAD would strengthen external validity"). This is a planned future direction, not a missing analysis.

**Assessment:** The paper includes an appropriate set of analyses for its scope. The acknowledged future directions (self-supervised pre-training, multi-modal integration, deployment optimisation) are well-chosen.

### Phase 4 Verdict: PASS
Robustness checks are comprehensive for a benchmarking paper. Limitations are honest and thorough with one minor omission (single seed not in limitations section). Missing analyses are appropriately scoped to future work.

---

## Aggregate Scores

| Phase | Description | Score | Gate |
|-------|-------------|-------|------|
| Phase 1 | Claim Identification | 92/100 | PASS |
| Phase 2 | Core Design Validity | 82/100 | PASS |
| Phase 3 | Inference | 85/100 | PASS |
| Phase 4 | Polish and Completeness | 88/100 | PASS |

**Weighted aggregate (3:5:2:1 weights):** (3×92 + 5×82 + 2×85 + 1×88) / 11 = 944/11 = **85.8/100**

---

## Overall Verdict: MINOR ISSUES

The core experimental design is sound. LOSO is properly enforced, hyperparameter budgets are equal, z-score normalisation is within-fold, and the paper is unusually transparent about its limitations (especially the Wilcoxon independence violation and the single-seed choice). The Pareto frontier analysis is well-constructed and directly addresses the paper's stated goal of informing architecture selection under deployment constraints.

However, several issues prevent a clean SOUND verdict:

1. **The single-seed choice is especially consequential** given the narrow Mamba–PatchTST margin (ΔF1 = 0.005, p = 0.048 uncorrected). With 147 folds providing 147 independent initialisations, the mean F1 estimates are relatively stable, but the ranking between closely-matched architectures could be seed-sensitive. This deserves more prominent discussion than a single sentence in the training description.

2. **The validation split mechanism is underspecified.** Whether the 80/20 split produces different validation sets per fold or uses a fixed hold-out set across all folds has implications for the effective number of test subjects. This needs clarification.

3. **The mixed treatment of p-values** — acknowledging the Wilcoxon independence violation while simultaneously using p < 0.05 thresholds as interpretive guides — creates tension in the narrative. Consistent descriptive treatment of p-values would be more appropriate.

4. **Per-subject performance distributions are not reported.** For a paper that makes deployment recommendations affecting individual users, knowing whether poor performance clusters in specific subjects is practically important.

5. **Preprocessing sensitivity** (CDA vs. cvxEDA/Ledalab) is acknowledged as a limitation but not tested, despite the paper's claim that the choice of decomposition method affects downstream signal characteristics.

6. **Code availability is not addressed** — for a paper with explicit deployment guidance, this limits practical impact.

### Summary of Required Changes for SOUND Verdict

| # | Issue | Severity | What would change the verdict |
|---|-------|----------|-------------------------------|
| 1 | Single-seed limitation | MODERATE | Add to Limitations section; discuss whether 147-fold averaging is sufficient mitigation |
| 2 | Validation split mechanism | CLARIFICATION | Specify whether 80/20 split varies per fold |
| 3 | Mixed p-value treatment | MODERATE | Consistently treat p-values as descriptive throughout Section 3.5 |
| 4 | Per-subject distributions | MODERATE | Report per-subject F1 histogram or quartiles (supplementary) |
| 5 | Preprocessing sensitivity | MODERATE | Add explicit caveat that rankings are conditioned on CDA decomposition |
| 6 | Code/data availability | MODERATE | Add availability statement (even if code is not public, state the plan) |
| 7 | Grid coverage asymmetry | MINOR | Acknowledge that simpler architectures benefit from denser effective search |
| 8 | FLOPs estimation for Mamba | MINOR | Note potential underestimation of Mamba scan kernel operations |
| 9 | Optimal hyperparameter values | MINOR | Report the selected configuration per architecture (supplementary) |
| 10 | Mamba–PatchTST "5 pp" vs classical | MINOR | Separate the two comparisons (SVM vs. DLinear baseline) |

---

## "What Would Change My Mind" for the Overall Verdict

The overall verdict would upgrade to **SOUND** if:
- X The validation split mechanism is clarified (per-fold random vs. fixed) — this is a potential CRITICAL issue if fixed.
- X The single-seed limitation receives prominent treatment in the limitations section, with a discussion of its interaction with the narrow Mamba–PatchTST margin.
- X The p-value interpretation is made consistently descriptive (removing α = 0.05 threshold language from Section 3.5).
- X Code availability is addressed (even a brief statement suffices).

The overall verdict would degrade to **MAJOR ISSUES** if:
- X The 80/20 split is fixed across folds (some subjects never serve as test subjects).
- X The single-seed limitation is not acknowledged in the limitations section at all.
- X Evidence emerges that the Z-score normalization uses global (across all subjects) rather than within-fold statistics. (Currently the text states within-fold; this would require code inspection to verify definitively.)

---

*Audit completed 2026-05-12 by Strategist-Critic agent.*  
*This is a CRITIC review — no files were modified.*  
*Target file: /Users/Roberto.Sanchez/Repositorio/tsi_eda_paper/paper/main.tex*
