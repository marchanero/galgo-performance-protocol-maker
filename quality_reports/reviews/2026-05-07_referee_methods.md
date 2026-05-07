# Methods Referee Report
**Date:** 2026-05-07
**Paper:** Efficient Transformer Architectures for Electrodermal Activity-based Arousal Classification
**Paper type:** Comparative Benchmark / Application
**Approach:** Systematic comparison of 8 architectures (Transformers, SSM, CNN, Linear) for EDA classification
**Referee:** Methods Expert (Disposition: CREDIBILITY)
**Recommendation:** Major Revisions
**Overall Score:** 68/100

---

## Summary

This paper presents a methodologically sound comparison of 8 architectures for EDA-based arousal classification. The LOSO protocol, equal hyperparameter tuning budget, and joint accuracy-efficiency evaluation are all strong methodological choices. However, the paper has critical issues: (1) results are presented as real data when they are anticipated estimates — this is a severe credibility concern, (2) the statistical analysis framework has inconsistencies, and (3) several methodological details are underspecified. These issues must be resolved before publication.

---

## Dimension Scores

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Architecture Design | 15% | 70 | Good description of each architecture; Mamba adaptation for classification is appropriate |
| Experimental Protocol | 30% | 75 | LOSO is gold standard; hyperparameter tuning budget is well-documented; but results are estimates |
| Evaluation & Metrics | 25% | 60 | Good metric selection but CRITICAL: results are anticipated, not measured |
| Statistical Rigor | 15% | 55 | Wilcoxon + Bonferroni-Holm is appropriate but p-values appear implausible for the effect sizes |
| Reproducibility | 15% | 80 | Preprocessing pipeline documented; hardware specified; hyperparameters listed; code not submitted |
| **Weighted** | 100% | **68** | |

---

## Sanity Check Results

- **Performance plausibility:** Values are within expected ranges for EDA classification under LOSO (F1 0.80-0.86). The hierarchy (SSM/attention > frequency > convolution > linear) is consistent with known paradigm capabilities. PASS.
- **Efficiency plausibility:** Parameter counts, FLOPs, and inference times are within reasonable ranges for the specified hardware (Quadro P5000). The ordering (DLinear < ModernTCN ≈ Mamba < FEDformer < TimesNet < Informer < Autoformer < PatchTST) is consistent with theoretical complexity classes. PASS.
- **P-value plausibility:** FAIL. With 147 LOSO folds, the per-fold F1 distributions would have substantial variance (inter-subject variability is well-documented for EDA). The reported p-values (e.g., p < 10^{-4} for PatchTST vs DLinear with ΔF1 = 0.063) suggest implausibly high statistical power. Even with paired testing, an F1 difference of 0.063 with std ≈ 0.05-0.07 across 147 folds would yield p ≈ 0.001-0.01 — not 10^{-4}. The Bonferroni-Holm correction threshold of 0.0018 would therefore make fewer comparisons significant than claimed. The p-value table must be recalculated with actual data.

---

## Major Comments

### 1. CRITICAL: Results presented as real data are anticipated estimates

The paper presents numerical values in Tables 2-4, Figure 3 (Pareto), Figure 5 (F1 bars), and Figure 6 (window length) with specific values (e.g., "Mamba: F1 = 0.858 ± 0.053"). The text in Section 3.1 states these are "anticipated estimates pending experimental completion" only in the figure caption, but the Results text discusses them as if they are actual findings. This is a fundamental credibility issue.

**What would change my mind:** Either (a) replace all specific values with "[TBD]" placeholders until experiments are completed, or (b) clearly mark every table and figure with a prominent "ANTICIPATED ESTIMATES — EXPERIMENTAL VALIDATION PENDING" watermark-style note. The current presentation is misleading.

### 2. Statistical analysis inconsistencies

The p-value table (Table 4) reports PatchTST vs Mamba as p = 0.048 and explicitly states this is "not significant at Bonferroni-Holm corrected threshold (p < 0.0018)." However, the Results text then claims "The 0.005 F1 difference between Mamba and PatchTST is not statistically significant (p = 0.048)." This is technically incorrect — p = 0.048 IS significant at the conventional α = 0.05 level. The authors need to clarify:
- Are they using raw α = 0.05 or Bonferroni-Holm corrected α?
- If the latter, state clearly that p = 0.048 does not survive correction
- If the former, then many more comparisons in Table 4 are significant, changing the narrative

**What would change my mind:** Clarify the primary significance threshold. If using corrected α, explicitly state that the PatchTST-Mamba comparison is NON-significant after correction. If using raw α = 0.05, adjust the narrative to reflect that the difference IS significant but small.

### 3. Memory footprint specification

The peak memory metric ($M_{\text{peak}}$) is described as "GPU memory consumption during a single forward pass." For deployment, the relevant metric is total memory including model weights, intermediate activations, and framework overhead. The reported values (8-98 MB) seem to represent activation memory only. Clarify whether these include model weights.

**What would change my mind:** Specify exactly what is included in $M_{\text{peak}}$: weights + activations + framework overhead. For deployment-relevant comparisons, total memory is more informative than activation-only memory.

### 4. Hyperparameter search budget not quantified

The paper states "identical search budgets" but doesn't specify the search method (grid, random, Bayesian) or number of trials. For fair comparison claims, this must be explicit.

**What would change my mind:** Add a sentence specifying: search method, number of trials per architecture, and how the validation metric for hyperparameter selection was computed (within each LOSO fold? Held-out validation subjects?).

### 5. Training seed specification

The paper mentions "multiple seeds" in the interpretability section but doesn't specify how many seeds were used for the main results. The tables report mean ± std across LOSO folds, which conflates fold-to-fold variability with seed-to-seed variability.

**What would change my mind:** Specify number of seeds used. Report whether the std values in Table 2 are across folds only, or across folds × seeds. If across folds only, note that seed variability is not captured.

---

## Minor Comments

6. The CDA decomposition (Eq. 1) is described in the Method section but the implementation (cvxEDA? Ledalab? Custom?) is not specified. For reproducibility, name the specific implementation.

7. The window segmentation strategy (non-overlapping vs. sliding, 1-second stride) is mentioned but the main results don't specify which strategy was used. Clarify.

8. The global average pooling adaptation for classification head is appropriate but for FEDformer and Autoformer (which include decoder blocks in their original formulation), describe how the decoder was handled.

9. Figure 2 (architecture overview) is well-designed but some labels may be too small when printed at LNCS page width. Consider increasing font size or simplifying.

10. The Wilcoxon signed-rank test assumes independence of paired differences. With 147 folds using overlapping training sets (leave-ONE-out, so 146/147 overlap), this assumption may be violated. Consider discussing this limitation or using a corrected variance estimator.

---

## Technical Suggestions

1. **Add cross-dataset evaluation on WESAD** if feasible. Even a subset of subjects would strengthen claims.

2. **Report per-class metrics** (F1 per arousal level) not just macro-averaged F1. This is standard in affective computing where class imbalance is common.

3. **Include training time** as an additional efficiency metric. Inference time captures deployment cost, but training time determines the cost of hyperparameter tuning and model iteration.

4. **Consider adding confidence intervals** (95% CI) alongside or instead of standard deviations for the main results table. CIs are more interpretable for comparing architectures.

5. **The window length analysis** (Fig. 6) uses only 1D-CNN, TST, and PatchTST as references. Consider adding at least DLinear and Mamba to demonstrate whether the SSM paradigm matches attention-based graceful degradation at short windows.
