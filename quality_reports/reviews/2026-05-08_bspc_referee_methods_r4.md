# Methods Referee Report (Round 4 — FINAL)
**Date:** 2026-05-08
**Venue:** Biomedical Signal Processing and Control (BSPC)
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification
**Paper type:** Comparative Benchmark
**Referee:** Methods Expert (CREDIBILITY disposition)
**Recommendation:** Minor Revision → Accept
**Overall Score:** 83/100

---

## Round-over-Round Evolution

| Dimension | Weight | R1 | R2 | R3 | R4 | Delta (R3 to R4) |
|-----------|--------|-----|-----|-----|-----|-------------------|
| Fairness of Comparison | 30% | 65 | 75 | 78 | **79** | +1 |
| Baseline Selection | 20% | 70 | 82 | 85 | **86** | +1 |
| Evaluation Completeness | 20% | 60 | 78 | 80 | **81** | +1 |
| Statistical Rigor | 15% | 68 | 78 | 82 | **83** | +1 |
| Analysis & Insights | 15% | 72 | 85 | 87 | **88** | +1 |
| **Weighted** | 100% | **65** | **80** | **82** | **83** | **+1** |

---

## Summary

The manuscript has reached near-publishable quality for BSPC. The R4 revision is a disciplined, text-level update that addresses all five medium-severity editorial issues from R3 and the most consequential methods-reviewer concerns. No new experiments were conducted, which is appropriate for a Minor Revision cycle. The changes are surgical and honest.

The two blocking R3 issues (Table 2 bold formatting, "5-6 pp" overstatement) are resolved. Deployment tier labels are correctly qualified as GPU-relative ordinal rankings. EDA decomposition alternatives (cvxEDA, Ledalab) are discussed in the Methods section with appropriate caveats. Interpretability claims are properly hedged with "qualitative" qualifiers throughout. The classical signal-processing baseline is in Table 2 with transparent notes acknowledging its retrospective nature. BSPC positioning is strengthened with five venue-specific citations.

Six residual concerns remain, all text-level (requiring no new experiments). The most important is the continued absence of seed/reproducibility specification — a basic element of methodological reporting. Five additional cosmetic items (convergence std, derivative method, optimal hyperparameters, thop version, window-length curve markers) would further strengthen transparency.

---

## What Changed from Round 3

### Issues Resolved

| # | Issue | R3 Severity | R4 Status |
|---|-------|-------------|-----------|
| 1 | Table 2 bold (Mamba erroneously bolded over PatchTST) | Blocking | FIXED. PatchTST correctly bolded on all 5 metrics |
| 2 | "5-6 pp" overstates Mamba-classical gap | Medium | FIXED. Now "approximately 5 percentage point improvement (Mamba: +4.8 pp, PatchTST: +5.3 pp)" |
| 3 | Interpretability claims unqualified | Medium | FIXED. "Qualitative inspection," "qualitatively replicated," "qualitative analysis," "qualitatively suggest" throughout Section 3.6 |
| 4 | EDA decomposition alternatives absent | Medium | FIXED. cvxEDA, Ledalab, and SPR2012EDA now discussed in Section 2.2; acknowledged in Section 3.8 |
| 5 | Deployment tier labels overstated ("Wearable/Mobile/Cloud") | Medium | FIXED. Changed to "Low/Mid/High-latency GPU" with explicit caveat about embedded hardware differences |
| 6 | Statistical language vs. LOSO independence | Low | FIXED. p-values now described as "descriptive indicators of effect consistency"; PatchTST-Mamba properly qualified |
| -- | Classical baseline in Table 2 | New in R3 | IMPROVED. Now with explicit notes (double-dagger, *, a) transparently disclosing retrospective nature |
| -- | "Parasympathetic confounds" | Cosmetic | FIXED to "parasympathetic influence" |
| -- | BSPC journal positioning | Medium | IMPROVED. Five BSPC-specific citations added to Introduction |
| -- | "Derivative learned implicitly" claim | Cosmetic | FIXED. Rephrased as "partially redundant with representations" — more precise and defensible |
| -- | Figure 2 caption | Cosmetic | FIXED. Colour coding now explained as "computational complexity class" rather than "paradigm," resolving the figure-vs-text mismatch |

---

## Remaining Concerns (Non-Blocking, Text-Level)

### C1. "Five paradigms" count internally inconsistent (MINOR)

The abstract (line 58) lists 5 paradigms: *patch-based attention, sparse attention, frequency-domain modelling, state space models, modernised convolutions.* Correct.

But line 75 says "five paradigms" while listing **7** parenthetical descriptors: PatchTST (patch-based attention), Informer (sparse attention), Autoformer and TimesNet (frequency/periodicity-based), FEDformer (Fourier attention), Mamba (SSM), ModernTCN (modernised convolution), DLinear (linear decomposition).

This was R3 editorial issue #2 (Medium). The fix: group FEDformer under frequency-domain modelling alongside Autoformer/TimesNet. Proposed text:

> "...eight architectures spanning five paradigms: patch-based attention (PatchTST), sparse attention (Informer), frequency-domain modelling (Autoformer, TimesNet, and FEDformer), state space models (Mamba), and modernised convolutions (ModernTCN), with DLinear as a linear decomposition baseline."

This costs nothing and resolves the last remaining R3 editorial flag.

### C2. Random seed unspecified (MINOR)

The word "seed" does not appear anywhere in the manuscript or supplementary. The training protocol (Section 2.4) describes optimiser, schedule, batch size, early stopping, and regularisation — but never states how many random seeds were used, or whether a fixed seed was set.

With ~117 training subjects per fold, deep networks exhibit non-trivial seed-to-seed variance. The R3 review flagged this (item 3) as a blocking concern. The R4 revision added statistical caveats but did not address seeds.

**Fix:** One sentence in Section 2.4 stating: (a) number of seeds used, (b) seed value(s) if fixed, (c) whether deterministic mode was enabled. If single seed, add a caveat in Section 3.8.

### C3. Convergence epochs reported as single integers (MINOR)

Supplementary Table S4 reports epochs-to-convergence as single integers (32, 45, 58, etc.). With 147 independent folds and early stopping patience=15 applied per fold, the probability that all folds converged in exactly the same number of epochs is near zero.

The R3 review explicitly requested mean ± std. This requires only computing descriptive statistics on already-collected per-fold data.

**Fix:** Report as "58 ± 12" or whatever the data show.

### C4. Derivative computation method unspecified (COSMETIC)

Line 94 states "two derivative channels were computed from the phasic signal" but never specifies the method (forward differences, central differences, Savitzky-Golay). At 4 Hz, the choice materially affects noise amplification. One sentence is sufficient.

### C5. Optimal hyperparameters not disclosed (COSMETIC)

64-configuration grid search was conducted. The winning configurations (layers, embedding dim, attention heads, kernel sizes) are not reported anywhere. A supplementary table for the Pareto-optimal architectures would aid practitioner adoption and reproducibility.

### C6. Window-length curves: evaluation points unmarked (COSMETIC)

Figure 7 connects evaluation points with solid/dashed lines, implying linear interpolation from as few as 12 data points. The caption now states evaluation points explicitly — a clear improvement. Adding small dot markers would make the figure fully self-documenting.

---

## Items Acknowledged as Limitations (Accepted)

The following were recommended in R3 but are acknowledged in Section 3.8. None threatens the paper's central findings:

| Item | Status |
|------|--------|
| Artifact robustness experiment | Acknowledged. Hossain2022BSPC cited in Section 2.2. |
| Prior-work tuning budget sensitivity (24 vs 64 configs) | Transparently disclosed in Table 2 notes. |
| Classical baseline re-evaluation (SVM on current pipeline) | Retrospective but honestly documented. The convergence insight (classical ~ DLinear ~ 1D-CNN ~ F1 0.80) does not depend on per-fold std. |
| Cluster-robust bootstrap for PatchTST-vs-Mamba | p-values now properly downgraded to "descriptive indicators of effect consistency" |
| Embedded hardware benchmark | GPU-relative caveat present. |
| Confusion matrices / ECE | Per-class F1 (Supplementary Table S3) partially addresses asymmetry. |
| thop version / Mamba CUDA FLOPs caveat | Minor reproducibility detail. |

---

## Sanity Check Results

| Check | Result | Detail |
|-------|--------|--------|
| Baseline consistency | PASS | Classical SVM (F1 ~ 0.81) retrospective but transparently noted. Gap values (Mamba +4.8 pp, PatchTST +5.3 pp) correctly computed. |
| Performance plausibility | PASS | F1 0.800-0.863 under 147-fold LOSO is plausible. Hierarchy PatchTST > Mamba > TimesNet > Autoformer > Informer > FEDformer > ModernTCN > DLinear internally consistent. |
| Tuning budget | QUALIFIED PASS | 64 configs per architecture equitable. Prior-work baselines at 24 — honestly disclosed in Table 2 note. |
| Section cross-references | PASS | All supplementary table references (S1-S4) resolve. Section 3.3 and 3.8 forward references correct. |
| "Five paradigms" count | CONCERN | Abstract: 5 correct. Line 75: claims 5, enumerates 7 descriptors. See C1. |
| Seed specification | CONCERN | Completely absent. See C2. |
| Convergence reporting | CONCERN | Single integers imply impossible precision across 147 folds. See C3. |
| Derivative computation | CONCERN | Method unspecified. See C4. |

---

## Dimension-by-Dimension Assessment

### Fairness of Comparison (79/100)
64-config tuning budget equitable across candidates. Prior-work differential disclosed. Deployment labels properly qualified. Seed specification absent — the main gap.

### Baseline Selection (86/100)
Classical SVM anchors deep learning results in abstract, Table 2, and Section 3.1. EDA decomposition alternatives discussed. Five BSPC citations ground the paper. The convergence of classical/DLinear/1D-CNN at F1 ~ 0.80 is genuinely valuable.

### Evaluation Completeness (81/100)
5+5 metrics across all 8 architectures. Per-class F1, channel ablation, training data in supplementary. Pareto frontier properly qualified. Artifact/hardware experiments absent but acknowledged.

### Statistical Rigor (83/100)
Wilcoxon + Bonferroni-Holm correct. LOSO independence violation acknowledged inline. Effect sizes alongside p-values. Seed specification absent.

### Analysis & Insights (88/100)
Channel ablation insight ("partial redundancy") well-supported. Pareto frontier actionable. Classical/DLinear/CNN convergence narrative elegant and well-argued. Interpretability properly qualified.

---

## Overall Assessment

The central contributions — Pareto frontier characterisation, Mamba-PatchTST accuracy-efficiency trade-off, and the convergence of classical/DLinear/CNN baselines at F1 ~ 0.80 — are well-supported and practically valuable. The authors have been honest about limitations; the deployment tier relabelling from R3 is a model of responsible revision.

The six remaining concerns (C1-C6) are text-level clarifications requiring no new experiments. C1 (paradigm count) and C2 (seed) warrant fixing before final acceptance; C3-C6 are advisory.

**Recommendation: Accept with minor text-level revisions.**

---

## Required Actions

1. **Fix "five paradigms" count** (line 75) — regroup FEDformer under frequency-domain to make the count match
2. **Add seed specification** (Section 2.4) — one sentence with seed count and values
3. **Report convergence epochs as mean ± std** (Supplementary Table S4)
4. **Specify derivative computation method** (line 94)
5. **Disclose optimal hyperparameters** (Supplementary, new table)
6. **Add markers to window-length curves** (Figure 7, optional)

