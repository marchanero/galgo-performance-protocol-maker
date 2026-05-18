# Strategy Review: main.tex
**Date:** 2026-05-18
**Reviewer:** strategist-critic (paired critic for the Strategist)

## Phase 1: Claim Identification
- **Paper type:** Comparative benchmark (primary) with Application/Deployment elements
- **Approach:** Systematic comparison of 8 architectures spanning 5 efficiency paradigms (patch-based attention, sparse attention, frequency-domain, state space model, modernised convolution) + 1 linear baseline
- **Task:** Binary arousal classification (calm/stress) from EDA signals (SCR + ΔSCR + Δ²SCR, 4 Hz, 40 s windows, T=160, C=3)
- **Dataset/domain:** 147 participants, controlled laboratory audiovisual stimuli, balanced binary labels
- **Claimed contributions:**
  1. First systematic accuracy-efficiency comparison of Transformers, SSMs, and modernised convolutions for EDA under strict LOSO
  2. Explicit characterisation of the accuracy-efficiency Pareto frontier across 5 complementary efficiency metrics
  3. Mamba (SSM) achieves F1=0.858 at 1.5 ms, approaching PatchTST (F1=0.863) with 3.6× lower latency and 66% fewer parameters — the difference does not survive Bonferroni-Holm correction
  4. Derivative channels most beneficial for simpler architectures; attention/SSM partially learn equivalent context
  5. Global temporal modelling (not specific computational primitives) drives the ~5 pp F1 improvement over classical/conventional baselines

### Claim Support Assessment
- **Main claim (Pareto frontier):** Supported by design — 5 efficiency metrics measured on identical input, consistent hardware, equal-budget tuning. Credibility hinges on Phase 2 fairness checks.
- **Mamba ≈ PatchTST claim:** Rests on ΔF1=0.005, p=0.048 (not surviving correction), single seed — the design does not robustly support this equivalence.
- **Derivative channel claim:** Well-supported by controlled channel ablation (supplementary Table S1).
- **"First systematic" claim:** Reasonable given the literature review; no prior work comparing these paradigms on EDA under LOSO has been identified.

---

## Phase 2: Core Experimental Design
### Design Check: Comparative Benchmark
**Assessment:** CONCERNS (multiple MAJOR issues, no CRITICAL)

#### Issues Found: 6

##### Issue 2.1: Single random seed for a comparative benchmark
- **Location:** Section 2.4 (line 397): "All experiments used a single random seed (42)"
- **Severity:** MAJOR
- **Problem:** In a comparative benchmark where 8 architectures are ranked and the top-2 differ by ΔF1=0.005, a single seed cannot establish reliable ranking. Weight initialisation alone can produce performance variation larger than this margin. The paper acknowledges this limitation (Section 3.8) but does not mitigate it. Without multi-seed results (with mean ± std across seeds), the central claim that "Mamba approaches PatchTST accuracy" rests on an unverifiable single-seed ordering.
- **Suggested fix:** Run at minimum 3–5 seeds per architecture (or report seed sensitivity from an exploratory subset). If resources are constrained, at minimum verify the Mamba vs. PatchTST ordering across 3 additional seeds and report. Alternatively, weaken the ranking language to "Mamba and PatchTST form a top tier with no statistically robust ordering difference."

##### Issue 2.2: Ambiguous "equal-budget" grid search mechanism
- **Location:** Section 2.4 (line 399): "Hyperparameters were tuned using grid search with identical trial budgets (64 configurations per architecture)"
- **Severity:** MAJOR
- **Problem:** The hyperparameter search space (Table 1) has different cardinalities per architecture. The common subspace alone includes 4 (layers) × 4 (embed_dim) × 4 (ff_dim) = 64 combinations, leaving no budget for architecture-specific params. PatchTST additionally has 3 (patch_size) × 4 (heads) = 12× multiplier, yielding a far larger grid. The paper does not specify how 64 configurations were selected from grids of different sizes: random sub-sampling, manually pruned grids, or something else. Without this clarification, "equal budget" may be misleading — 64 trials from a 768-point grid vs. 64 trials from a 48-point grid are not "equal" in effective coverage. Furthermore, 64 trials is insufficient for a 5+ dimensional search space regardless.
- **Suggested fix:** Clarify whether random search, Bayesian optimisation, or sub-sampled grid was used. If grid search, specify the exact combinations evaluated for each architecture. If random, state it and discuss the implications of sparse coverage. Consider reporting performance variation across the top-K configurations as a sensitivity check.

##### Issue 2.3: FLOPs measurement fundamentally unreliable for Mamba
- **Location:** Section 2.5.3 (line 442); limitation acknowledged line 809
- **Severity:** MAJOR
- **Problem:** `thop` uses PyTorch forward hooks and cannot capture custom CUDA kernels. Mamba's selective scan (the core operation determining its efficiency advantage) is typically implemented as a custom Triton/CUDA kernel. The FLOPs value reported for Mamba (12.8M) likely counts only PyTorch-level operations and misses the scan kernel entirely. The paper acknowledges this in limitations (line 809) but still presents Mamba FLOPs in the main efficiency table without a caveat. This overstates Mamba's apparent efficiency advantage.
- **Suggested fix:** Either (a) measure Mamba FLOPs with Mamba's own profiling, (b) annotate the Mamba FLOPs cell in Table 4 with a footnote noting it may be underestimated, or (c) drop FLOPs as a metric for architectures using custom ops and rely solely on inference time and memory for cross-paradigm comparison.

##### Issue 2.4: Wilcoxon test independence assumption violated by LOSO overlap
- **Location:** Section 2.5.2 (line 434); acknowledged line 807
- **Severity:** MAJOR
- **Problem:** The Wilcoxon signed-rank test assumes independent paired observations. Under LOSO, training sets overlap by 146/147 subjects between any two folds — the per-fold F1 scores are strongly correlated and not independent. The paper correctly acknowledges this limitation (Section 3.8), yet the main text (Section 3.1–3.5) uses p-values to support ranking claims (e.g., "significant at the conventional level," line 679). The inflated sample size (147 folds treated as 147 independent observations) produces artificially low p-values, overstating the statistical confidence in between-architecture differences.
- **Suggested fix:** Use a corrected test that accounts for dependence (e.g., a corrected variance estimator for cross-validation, or a permutation-based test that respects the LOSO structure). Failing that, report the test as purely descriptive with a stronger caveat in the main text (not just Section 3.8), avoid "significant"/"not significant" language in the results, and rely primarily on effect sizes and rank consistency.

##### Issue 2.5: SVM baseline not re-executed under the current pipeline
- **Location:** Section 3.1, Table 2 notes (line 492): "from [prior work]"; limitation line 802
- **Severity:** MAJOR
- **Problem:** The classical SVM baseline (F1≈0.81) anchors the deep learning performance gains — a core contribution claim. However, this result is from a prior study and was not re-executed. Per-fold standard deviations are unavailable, preventing formal statistical comparison. More importantly, the prior study may have used different preprocessing (no Δ²SCR, possibly different decomposition, different windowing) or different LOSO partitioning. The claim that deep architectures provide "~5 pp improvement" over classical methods cannot be rigorously verified without a shared evaluation pipeline.
- **Suggested fix:** Re-run the classical feature + SVM pipeline under the current preprocessing and LOSO splits. If this is not possible, downgrade the comparison from a quantitative benchmark to a qualitative reference point, and clearly state the pipeline differences between the two studies.

##### Issue 2.6: Architecture implementation sources not specified
- **Location:** Section 2.3 (architectural descriptions)
- **Severity:** MINOR
- **Problem:** The paper does not state whether official author implementations, community re-implementations, or custom implementations were used. Differences between implementations (e.g., transformer library backends, custom layer variants) can affect both accuracy and efficiency measurements. For a comparative benchmark, this is a reproducibility concern.
- **Suggested fix:** State the source of each architecture implementation (e.g., "Official PatchTST codebase," "Community implementation from Time-Series-Library," "Custom PyTorch implementation following the paper"). If custom, describe validation against published results.

### Sanity Check
- **Performance:** Plausible. F1 range 0.80–0.86 for EDA binary classification on 147 subjects aligns with expectations for physiological signals. Prior work (PatchTST F1=0.852) is consistent with the expanded result (0.863, +Δ²SCR + expanded search). No ceiling/floor effects visible.
- **Efficiency:** Plausible. DLinear at 0.08M params/0.05M FLOPs is consistent with a simple linear layer on 160×3 input. PatchTST at 4.52M params with 78.5M FLOPs is consistent with a small 4-layer transformer on patched sequences. Inference times (0.3–5.4 ms on Quadro P5000) are within expected ranges. However, Mamba FLOPs (12.8M) are likely underestimated due to thop limitations (see Issue 2.3).
- **Baseline match:** Prior work results (1D-CNN, TCN, InceptionTime, TST, PatchTST from Sanchez-Reolid 2022) are reproduced. PatchTST improvement from 0.852→0.863 is quantitatively explained (+0.011 from Δ²SCR + expanded search). DLinear (0.800) ≈ 1D-CNN (0.796) convergence is plausible but not independently verified.
- **Improvement magnitude:** ΔF1 = 0.005 (Mamba→PatchTST) is plausibly within noise. ΔF1 = 0.058 (DLinear→PatchTST) is practically meaningful. The ~5 pp gap between classical/conventional tier and Transformer/SSM tier is plausible and matches the narrative that global temporal modelling matters.
- **Outlier check:** No anomalous results. Rankings are monotonic with theoretical complexity class, as expected. FEDformer slightly underperforms its O(L) peers in F1 but compensates in efficiency — consistent with the Fourier approximation trade-off.

---

## Phase 3: Experimental Execution

### Issues Found: 5

##### Issue 3.1: Missing formal effect sizes
- **Location:** Sections 3.1, 3.5 (statistical significance discussion)
- **Severity:** MINOR (addressed via qualitative discussion)
- **Problem:** The paper discusses F1 differences as effect sizes (e.g., ΔF1=0.005) but does not report standardised effect sizes (Cohen's d, Hedges' g). For a benchmark with violated test assumptions, standardised effect sizes are more interpretable than p-values. The supplementary material provides the full pairwise p-value matrix but no effect size matrix.
- **Suggested fix:** Add a pairwise Cohen's d matrix to the supplementary material, computed as mean difference divided by pooled per-fold standard deviation. This would directly show that the Mamba–PatchTST effect size is small (d≈0.1 given the similar std).

##### Issue 3.2: No convergence analysis or loss curves
- **Location:** Sections 2.4, 3.1
- **Severity:** MINOR
- **Problem:** A comparative benchmark should demonstrate that all models converged. The supplementary Table S4 reports epochs-to-convergence but no loss/validation curves. Some architectures (e.g., Informer at 68 epochs) converge slower than others (DLinear at 32 epochs). Without loss curves, it's unclear whether slower-converging architectures would benefit from more patience or a different learning rate schedule — a potential source of unfairness.
- **Suggested fix:** Include representative loss curves (train and validation) for a subset of folds, or at minimum report that all models reached a stable plateau before early stopping triggered.

##### Issue 3.3: Class balance not explicitly reported
- **Location:** Section 2.1 (dataset description)
- **Severity:** MINOR
- **Problem:** The paper states "balanced binary classification dataset" but does not report the exact number of calm vs. stress trials, the number of trials per participant, or the total number of windows after segmentation. Class balance information is needed to interpret macro-averaged F1 and to assess whether per-class F1 differences (supplementary Table S3) reflect class imbalance or genuine asymmetry in discriminability.
- **Suggested fix:** Report the total number of calm/stress trials, trials per participant (mean ± std), and total windows after segmentation with both non-overlapping and sliding-window strategies.

##### Issue 3.4: Hardware diversity for inference benchmarking
- **Location:** Section 2.5.3 (line 443): "Quadro P5000"
- **Severity:** MINOR
- **Problem:** Inference time is measured on a single GPU model (Quadro P5000, Pascal 2016). While relative rankings may transfer across GPU generations, absolute latencies and the Pareto frontier shape depend on hardware. Pascal's tensor core absence and older memory bandwidth may disadvantage architectures optimised for newer hardware features (e.g., Mamba's scan kernel may benefit disproportionately from Ampere tensor cores). The paper appropriately labels these as "GPU-relative rankings" but does not discuss this hardware specificity.
- **Suggested fix:** Note in limitations that rankings on newer architectures (Ampere, Ada Lovelace) may shift, particularly for Mamba which relies on hardware-aware algorithms. Ideally, measure on at least one additional GPU generation.

##### Issue 3.5: Segmentation strategy inconsistency in window-length ablation
- **Location:** Section 3.4 (line 763): "sliding-window curves show slightly higher plateau F1 values... average offset +0.004"
- **Severity:** MINOR
- **Problem:** The main results (Table 2) use non-overlapping windows, but the window-length ablation (Figure 5) appears to use sliding windows (1 s stride). This mixing of segmentation strategies across analyses is acknowledged but not justified. The +0.004 offset prevents direct comparison between the main results table and the window-length curves. Additionally, using sliding windows for the ablation but non-overlapping for the main results means the ablation overestimates F1 relative to the main results.
- **Suggested fix:** Report the window-length ablation using the same non-overlapping segmentation as the main results, or provide both curves (non-overlapping and sliding) on the same plot for direct comparison.

---

## Phase 4: Polish & Completeness

### Issues Found: 7

##### Issue 4.1: Missing hyperparameter sensitivity analysis
- **Severity:** MINOR
- **Problem:** Only the best configuration per architecture is reported. No sensitivity analysis shows how F1 varies with key hyperparameters (embedding dimension, number of layers, patch size). For a paper recommending architecture selection under deployment constraints, sensitivity to model size (which directly affects latency and memory) is practically important — a smaller PatchTST or Mamba might achieve similar accuracy at even lower cost.
- **Suggested fix:** Report F1 vs. parameter count curves (Pareto frontier across model sizes within each architecture family), or at minimum show how the top-3 configurations per architecture perform relative to the best.

##### Issue 4.2: Missing seed sensitivity quantification
- **Severity:** MAJOR (but acknowledged, so treated here as MINOR for completeness)
- **Problem:** The single-seed limitation is acknowledged but not bounded. Without even a 2-seed pilot study, the reader cannot assess whether the Mamba–PatchTST ΔF1=0.005 is within or beyond expected seed-dependent variation.
- **Suggested fix:** Run at minimum Mamba and PatchTST with 3 additional seeds. Even if other architectures remain single-seed, this would bound the key comparison.

##### Issue 4.3: Missing cross-dataset or cross-decomposition validation
- **Severity:** MINOR (acknowledged as limitation)
- **Problem:** Rankings are established under CDA decomposition only. The paper cites evidence that decomposition method affects downstream classification (SPR2012EDA, cvxEDA, Ledalab) but does not test sensitivity. A single-dataset, single-decomposition study limits generalisability — acknowledged by authors.

##### Issue 4.4: No pure-MLP baseline
- **Severity:** MINOR
- **Problem:** DLinear serves as the linear baseline. An MLP (2–3 dense layers on the flattened input) would test whether the performance gain over DLinear comes from non-linearity alone rather than structured temporal modelling. This is a low-cost baseline that would strengthen the "global temporal modelling matters" claim.

##### Issue 4.5: Pareto frontier uses only one efficiency dimension
- **Severity:** MINOR
- **Problem:** The Pareto frontier (Figure 3) plots F1 vs. inference time only. The paper claims 5 complementary efficiency metrics, but the central visualisation uses only one. A multi-dimensional Pareto analysis (e.g., F1 vs. both latency and memory) or a table of Pareto-optimal architectures per metric would better serve the stated goal of "informing architecture selection under specific deployment constraints."

##### Issue 4.6: Citation fidelity — minor discrepancies
- **Location:** References throughout
- **Severity:** MINOR
- **Notes:**
  - PatchTST venue: ICLR 2023 ✓ (Table 1 correctly states)
  - Informer: AAAI 2021 ✓
  - Autoformer: NeurIPS 2021 ✓
  - TimesNet: ICLR 2023 ✓
  - FEDformer: ICML 2022 ✓
  - Mamba: arXiv 2023 ✓ (correctly not presented as peer-reviewed)
  - ModernTCN: ICLR 2024 ✓
  - DLinear: AAAI 2023 ✓
  - AdamW (Loshchilov & Hutter 2019): ICLR ✓
  - No obvious citation errors detected.

##### Issue 4.7: "Further Reading" section in supplementary not cited in main text
- **Severity:** MINOR (cosmetic)
- **Problem:** The supplementary material includes a "Further Reading" section with references not cited in the main text (Boucsein 2012, Picard 1997, Meijer & Verschuere 2023, etc.). While meta-literature is acceptable in supplementary material, this section blurs the line between a literature review and the paper's reference list. Some of these (Boucsein 2012, Picard 1997) are foundational enough to cite in the main text Introduction.

---

## Summary
- **Overall assessment:** MAJOR ISSUES
- **Critical issues (must fix):** 0
- **Major issues (should fix):** 5 (Issues 2.1, 2.2, 2.3, 2.4, 2.5)
- **Minor issues (consider):** 10 (Issues 2.6, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.7)

**Verdict narrative:** The paper has a sound overall design — LOSO prevents subject-level leakage, preprocessing is domain-appropriate, evaluation metrics are comprehensive, and the limitations section is unusually candid. However, four clustered MAJOR issues undermine the central comparative claims: (1) a single seed cannot support the 8-way ranking, particularly the Mamba–PatchTST ordering at ΔF1=0.005; (2) the "equal-budget" grid search mechanism is ambiguously described and likely not truly equal across architectures with different search-space dimensionalities; (3) FLOPs for Mamba are likely underestimated due to thop limitations; (4) Wilcoxon p-values are used as evidence for ranking despite acknowledged violation of independence. These four issues do not individually invalidate the paper but collectively weaken the credibility of the ranking claims and the Pareto frontier. None rise to CRITICAL (no evidence of data leakage, implausible results, or fundamentally unfair comparison), but all four should be addressed before submission.

## Priority Recommendations
1. **[MAJOR]** Multi-seed validation — Run Mamba and PatchTST with 3+ additional seeds. If the ordering flips in any seed, the Mamba≈PatchTST claim must be qualified. At minimum, report per-seed results for both architectures.
2. **[MAJOR]** Clarify the hyperparameter search protocol — Specify whether grid search, random search, or Bayesian optimisation was used. If grid, provide the exact 64 configurations per architecture. If random, state the sampling method and discuss coverage.
3. **[MAJOR]** Address Mamba FLOPs reliability — Either (a) profile with Mamba's custom kernel, (b) add a footnote to Table 4 noting the FLOPs underestimate, or (c) remove FLOPs as a comparative metric for Mamba.
4. **[MAJOR]** De-escalate Wilcoxon-based language — In the main text results sections, replace "significant/not significant" framing with effect-size-based descriptions (e.g., "The Mamba–PatchTST F1 difference of 0.005 is smaller than the per-fold standard deviation of 0.05, indicating near-equivalent performance"). Reserve formal p-values for the supplementary table with the acknowledged caveats.
5. **[MAJOR]** Re-execute the SVM baseline under the current pipeline, or explicitly downgrade the classical-vs-deep comparison to a qualitative reference with fully documented pipeline differences.

## Positive Findings
1. **LOSO protocol is correctly implemented.** Subject-level leakage prevention via per-fold z-score normalisation and strict out-of-subject testing is methodologically sound and aligns with best practices for physiological signal classification (Azad et al., 2025).
2. **The limitations section (3.8) is exemplary.** The authors acknowledge 9 distinct limitations — including the Wilcoxon independence violation, single seed, thop limitations, CDA dependency, and SVM re-use — with appropriate specificity. This is far more candid than typical biomedical engineering papers.
3. **The supplementary material is thorough.** Full pairwise p-value matrix, per-class F1, channel ablation, and training time/convergence data enable independent verification of the main-text claims.
4. **Physiological grounding of architecture behaviour.** The interpretability analysis (Section 3.6) connects architectural mechanisms (attention weight concentration on SCR onsets, TimesNet period discovery matching SCR duration, derivative channel interaction with temporal modelling capacity) to established EDA physiology. This elevates the paper beyond a pure benchmark into domain-informed analysis.
5. **The DLinear baseline is a well-chosen sanity check.** Its convergence with 1D-CNN at F1≈0.80 provides a credible lower bound and supports the claim that global temporal modelling — not the specific computational primitive — drives the ~5 pp improvement.
