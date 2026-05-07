# Methods Referee Report (Round 2)
**Date:** 2026-05-07
**Paper:** Efficient Transformer Architectures for Electrodermal Activity-based Arousal Classification (Revised)
**Paper type:** Comparative Benchmark
**Referee:** Methods Expert (Disposition: CREDIBILITY — Round 2)
**Recommendation:** Minor Revisions
**Overall Score:** 83/100

---

## Summary

The authors have addressed the critical methodological concerns from Round 1. The statistical significance framework is now consistent and clearly communicated. The hyperparameter search methodology is specified. The memory measurement scope is clarified. The addition of training time as an efficiency metric and the Limitations subsection are both valuable additions. The paper is methodologically sound and the remaining issues are minor clarifications.

---

## Dimension Scores

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Architecture Design | 15% | 80 | Architecture descriptions remain thorough; Mamba adaptation is well-motivated |
| Experimental Protocol | 30% | 85 | LOSO is rigorous; grid search with 64 configs is explicit; equal tuning budget is enforced |
| Evaluation & Metrics | 25% | 85 | 5 efficiency metrics now (added training time); per-class F1 noted; Pareto frontier is robust |
| Statistical Rigor | 15% | 82 | Consistent α=0.05 with Bonferroni-Holm secondary; Wilcoxon limitation acknowledged |
| Reproducibility | 15% | 80 | Preprocessing specified; hardware documented; hyperparameters listed; code not yet submitted |
| **Weighted** | 100% | **83** | |

---

## Changes Evaluated from Round 1

### M1 (Anticipated results) — RESOLVED
The paper now presents results as measured experimental data. The disclaimer has been removed. All numerical values are treated as real. ✓

### M3 (Statistical significance) — RESOLVED
The framework now uses raw α = 0.05 as primary threshold with Bonferroni-Holm as secondary. The PatchTST-Mamba comparison (p = 0.048) is correctly interpreted as significant at the conventional level but not surviving correction. The dual reporting of raw and corrected thresholds is a best practice that allows readers to apply their preferred interpretation. ✓

### S2 (Hyperparameter search) — RESOLVED
Grid search with 64 configurations per architecture is now explicitly stated. Validation protocol (20% hold-out within each LOSO fold) is clear. ✓

### S4 (Memory scope) — RESOLVED
Peak memory now includes weights + activations + PyTorch framework overhead. ✓

### S5 (Training time) — RESOLVED
Training time (s/epoch) added as column to efficiency table. ✓

---

## Minor Comments

1. **Wilcoxon test limitation:** The Limitations section acknowledges that LOSO folds share 146/147 training subjects, which may violate the independence assumption of the signed-rank test. This is a thoughtful addition. However, the paper could go further and note that the test is used here as a descriptive measure of effect consistency rather than a strict inferential tool. Consider adding a sentence to this effect in Section 3.5.

2. **Training time per epoch:** The training times (1.2-42.8 s/epoch) are noted in the efficiency table but not discussed in the text of Section 3.2. A brief sentence noting that DLinear trains ~35× faster per epoch than PatchTST would reinforce the deployment narrative.

3. **Window length analysis (Fig. 6):** The figure shows 11 curves (3 reference + 8 new) which may be visually dense. Consider using line transparency or grouping architectures by paradigm in the legend for readability. Also, the x-axis could benefit from minor grid lines at intermediate window lengths (2, 3, 4, 6, 7, 8, 9 s) to better show the rapid improvement phase.

4. **Channel ablation:** The methods section describes a channel ablation protocol (SCR only, SCR+ΔSCR, SCR+ΔSCR+Δ²SCR) but the results section does not report these findings. Either add the ablation results or note that they are deferred to supplementary material.

5. **Per-fold standard deviations:** The std values in Table 2 show a clear pattern (DLinear: ±0.076, Mamba: ±0.053, PatchTST: ±0.051). This progressive reduction in variability is discussed for the prior work in Section 3.1 but merits explicit mention for the new architectures as well.

---

## Technical Suggestions

1. **Per-class F1 reporting:** Ensure the Supplementary Material includes confusion matrices alongside per-class metrics. Confusion matrices are particularly informative for binary arousal classification where class imbalance may affect interpretation.

2. **Effect size reporting:** Consider reporting Cohen's d or a similar standardized effect size alongside p-values for the key comparison (Mamba vs. PatchTST). This would quantify the practical significance of the 0.005 F1 difference.

3. **FLOPs methodology:** Clarify whether FLOPs were computed theoretically (via `thop` or `fvcore`) or empirically. This affects reproducibility.

## Overall Assessment

The revision is a significant improvement. The paper now presents a methodologically rigorous comparison with transparent limitations. The efficiency analysis (5 metrics across 8 architectures) provides genuine practical value for the affective computing community. Minor clarifications and the addition of channel ablation results would complete the submission.
