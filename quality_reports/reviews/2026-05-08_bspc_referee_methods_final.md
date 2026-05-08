# Methods Referee Report — DEFINITIVE FINAL
**Date:** 2026-05-08
**Venue:** Biomedical Signal Processing and Control (BSPC)
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification
**Paper type:** Comparative Benchmark
**Referee:** Methods Expert (CREDIBILITY disposition)
**Recommendation:** Accept with minor text-level revisions
**Final Score:** 82/100

---

## Round-over-Round Evolution

| Dimension | Weight | R1 | R2 | R3 | R4 | FINAL | Trend |
|-----------|--------|-----|-----|-----|-----|-------|-------|
| Fairness of Comparison | 30% | 65 | 75 | 78 | 79 | **78** | -1 |
| Baseline Selection | 20% | 70 | 82 | 85 | 86 | **86** | 0 |
| Evaluation Completeness | 20% | 60 | 78 | 80 | 81 | **80** | -1 |
| Statistical Rigor | 15% | 68 | 78 | 82 | 83 | **82** | -1 |
| Analysis & Insights | 15% | 72 | 85 | 87 | 88 | **87** | -1 |
| **Weighted** | 100% | **65** | **80** | **82** | **83** | **82** | **-1 vs R4** |

**Score revision rationale:** The -1 from R4 reflects an independent recalibration. No manuscript changes have occurred since R4; all six R4 residual concerns (C1-C6) remain open. The R4 score of 83 was marginally optimistic given the persistence of a factual inconsistency ("five paradigms" count at line 75), the complete absence of seed specification, and convergence epochs reported with spurious precision. The weighted aggregate of 81.95 rounds to **82**.

---

## DEFINITIVE Sanity Checks

| # | Check | Result | Detail |
|---|-------|--------|--------|
| 1 | Paradigm count consistency | **FAIL (MINOR)** | Abstract (line 58): 5 paradigms ✓. Line 75: "five paradigms" but 6 parenthetical descriptors (DLinear as "linear baseline" is the 6th). R4 C1 unfixed. |
| 2 | Seed specification | **FAIL (MINOR)** | "seed" absent from main.tex and supplementary. No seed count, value(s), or deterministic mode. R4 C2 unfixed. |
| 3 | Convergence epochs reporting | **FAIL (MINOR)** | Table S4: single integers (32, 45, 58, 62, 55, 68, 72, 85). 147 folds with patience=15 cannot all converge identically. R4 C3 unfixed. |
| 4 | Derivative computation method | **FAIL (COSMETIC)** | Line 94: method unspecified (forward/central differences? Savitzky-Golay?). R4 C4 unfixed. |
| 5 | Optimal hyperparameters disclosed | **FAIL (COSMETIC)** | No table anywhere listing grid-search winning configurations. R4 C5 unfixed. |
| 6 | Window-length curve markers | **FAIL (COSMETIC)** | Fig 7: evaluation points unmarked; curves imply continuous interpolation. R4 C6 unfixed. |
| 7 | Performance numerical consistency | **PASS** | F1 values internally consistent across Table 2, Fig 3, Fig 5, Fig 7, Tables S1-S3. |
| 8 | Delta values correct | **PASS** | Mamba +4.8 pp (0.858 - 0.81 = 0.048). PatchTST +5.3 pp (0.863 - 0.81 = 0.053). |
| 9 | Cross-reference integrity | **PASS** | S1-S4 exist. Forward references (3.3, 3.8) resolve. |
| 10 | Table 2 bold formatting | **PASS** | PatchTST correctly bolded on all 5 metrics. R3 blocking issue resolved. |
| 11 | Statistical p-value characterisation | **PASS** | PatchTST-Mamba p=0.048 at a=0.05, not surviving BH. R2 contradiction resolved. |
| 12 | Deployment tier labelling | **PASS** | "Low/Mid/High-latency GPU" with embedded hardware caveat. R3 resolved. |
| 13 | Interpretability hedging | **PASS** | "Qualitative" qualifiers throughout Section 3.6. R3 resolved. |
| 14 | EDA decomposition alternatives | **PASS** | cvxEDA, Ledalab discussed; SPR2012EDA cited. R3 resolved. |
| 15 | Classical baseline transparency | **PASS** | SVM baseline with double-dagger, asterisk, note (a). R3 resolved. |
| 16 | Performance plausibility | **PASS** | F1 0.800-0.863 under 147-fold LOSO entirely plausible. |
| 17 | Tuning budget equity | **QUALIFIED PASS** | 64 configs per candidate equitable. Prior-work at 24 (2.7x disadvantage) disclosed but acknowledged only for PatchTST. |
| 18 | BSPC venue alignment | **PASS** | 5 BSPC citations. Paper reads as biomedical signal processing contribution. |

**Sanity pass rate:** 12/18 (67%). All 6 failures are R4 residuals (text-level only).

---

## DIMENSION-BY-DIMENSION ASSESSMENT

### 1. Fairness of Comparison — 78/100 (Weight: 30%)

Equal 64-configuration grid search across all 8 candidate architectures with identical preprocessing is the gold standard for benchmark fairness. The Pareto frontier methodology is principled and dominance-based.

**Deductions:**
- Prior-work baselines (1D-CNN, TCN, InceptionTime, TST) tuned with 24 configurations vs. 64 for candidates (2.7x advantage). The disparity is disclosed in Table 2 notes for PatchTST only, not for the broader set. The implication that ModernTCN or FEDformer might appear to outperform TCN/InceptionTime partly due to tuning budget is not explicitly acknowledged.
- Seed completely unspecified. With ~117 training subjects per fold, deep networks exhibit non-trivial seed-to-seed variance. Fold-wise standard deviations in Table 2 may partially reflect seed-dependent initialization rather than pure subject variability.
- Search space cardinalities differ (PatchTST ~768 combos, DLinear ~320). 64 trials explores ~8% vs. ~20% of each space. Inherent to heterogeneous grid search but not noted.

### 2. Baseline Selection — 86/100 (Weight: 20%)

The classical SVM + handcrafted EDA features (F1 ~ 0.81) anchors the deep learning gains. DLinear provides an elegant "no temporal modelling" lower bound. ModernTCN represents the SOTA convolutional paradigm. The convergence of classical features, linear decomposition, and simple convolutions at F1 ~ 0.80 isolates the contribution of global temporal modelling (+4.8-5.3 pp) — genuinely insightful. Five BSPC-specific citations ground the paper in venue.

**Deductions:**
- Classical baseline is retrospective (cited, not re-evaluated). Per-fold standard deviations unavailable.
- No threshold-based SCR detector or template-matching approach.
- Prior deep learning baselines 4+ years old.
- Retrospective comparison prevents direct variability/statistical comparisons.

### 3. Evaluation Completeness — 80/100 (Weight: 20%)

5 classification + 5 efficiency metrics. Channel ablation (3 configs x 8 architectures). Window-length analysis (all 8 architectures, 1-40 s). Per-class F1 (Table S3). Training time (Table S4). Pareto frontier (Fig 5) integrates classification and efficiency.

**Deductions:**
- No artifact/noise robustness experiment — largest remaining gap. Acknowledged but not addressed.
- No confusion matrices, no ECE.
- No embedded hardware benchmark (Quadro P5000 only).
- Window-length curves lack markers, implying continuous interpolation.
- Convergence epochs without standard deviation.

### 4. Statistical Rigor — 82/100 (Weight: 15%)

Wilcoxon + Bonferroni-Holm for 28 comparisons correctly applied. Full p-value matrix (Table S2). Effect sizes alongside p-values. LOSO independence violation candidly discussed. p-values downgraded to "descriptive indicators of effect consistency." PatchTST-Mamba characterization now correct and consistent: p = 0.048 at a = 0.05, not surviving BH correction.

**Deductions:**
- Seed specification completely absent — basic element of methodological reporting.
- LOSO independence acknowledged but not remedied (no bootstrap/mixed-effects model).
- Convergence epochs as single integers implying spurious precision.
- Search space cardinality differences not noted.

### 5. Analysis & Insights — 87/100 (Weight: 15%)

Strongest dimension. Pareto frontier is actionable and novel for EDA. Channel ablation reveals inverse relationship between architecture capacity and derivative benefit (DLinear +2.8%, PatchTST +1.8%). Classical/DLinear/CNN convergence at F1 ~ 0.80 isolates global temporal modelling as the key driver. Mamba-PatchTST trade-off quantified (0.005 F1 at 3.6x lower latency, 66% fewer params). Window-length analysis provides 5-second minimum window for wearable feedback. Training implications (35x DLinear vs PatchTST speed) practical for development.

**Deductions:**
- No failure-mode analysis.
- Interpretability exclusively qualitative (appropriately disclosed).
- No preprocessing-paradigm interaction analysis.

---

## Items Acknowledged as Limitations (Accepted)

| Item | Status |
|------|--------|
| Artifact robustness experiment | Acknowledged with Hossain2022BSPC citation; not tested |
| Prior-work tuning budget differential | Transparently disclosed in Table 2 notes |
| Classical baseline re-evaluation | Honestly documented with explicit caveats |
| Embedded hardware benchmark | GPU-relative caveat in Fig 5 caption |
| Single-dataset evaluation | Acknowledged; WESAD suggested as future work |
| Confusion matrices / ECE | Per-class F1 partially addresses asymmetry |
| thop version / Mamba CUDA FLOPs | Acknowledged in Section 3.8 |

---

## BLOCKING Fixes Required Before Final Acceptance

These 3 items are blocking. All require text changes only — **zero new experiments.**

### B1. Fix paradigm count inconsistency (line 75)

Line 75 claims "five paradigms" but enumerates 6 groups (DLinear as "linear baseline" is the 6th). The abstract correctly lists 5.

**Fix:** "...eight architectures spanning five paradigms: patch-based attention (PatchTST), sparse attention (Informer), frequency-domain modelling (Autoformer, TimesNet, and FEDformer), state space models (Mamba), and modernised convolutions (ModernTCN), with DLinear as a linear decomposition baseline."

### B2. Add seed specification (Section 2.4)

State: (a) number of seeds, (b) seed values if fixed, (c) PyTorch deterministic mode status.

**Example:** "All experiments were conducted with three random seeds (42, 123, 456) for parameter initialisation and data ordering. Reported metrics represent the mean across seeds, with fold-wise statistics computed from seed-averaged per-fold scores. PyTorch deterministic algorithms were not enabled due to CUDA performance constraints."

If single-seed, acknowledge in Section 3.8 that fold-wise SD may partially reflect seed-dependent initialization.

### B3. Report convergence epochs as mean ± std (Table S4)

Change single integers (32, 45, 58, 62, 55, 68, 72, 85) to mean ± std across 147 folds. Requires only computing descriptive statistics on existing per-fold data.

---

## Advisory Improvements (Recommended, Not Blocking)

| # | Item | Effort |
|---|------|--------|
| A1 | Specify derivative computation method at line 94 | 1 sentence |
| A2 | Add optimal hyperparameter table to supplementary | 1 table |
| A3 | Add dot markers at evaluation points in Figure 7 | Graphics tweak |
| A4 | Note Mamba FLOPs via thop may be approximate (CUDA kernel) | 1 sentence |
| A5 | Acknowledge search space cardinality differences | 1 sentence |

---

## Score Composition

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Fairness of Comparison | 30% | 78 | 23.40 |
| Baseline Selection | 20% | 86 | 17.20 |
| Evaluation Completeness | 20% | 80 | 16.00 |
| Statistical Rigor | 15% | 82 | 12.30 |
| Analysis & Insights | 15% | 87 | 13.05 |
| **Weighted Aggregate** | **100%** | | **81.95 → 82** |

---

## Verdict

This manuscript meets the methodological standard for BSPC. The central contributions — Pareto frontier characterisation of 8 architectures spanning 5 paradigms, Mamba as the accuracy-efficiency sweet spot (F1 = 0.858 at 1.5 ms, 66% fewer params than PatchTST), and the convergence of classical/DLinear/CNN at F1 ~ 0.80 isolating global temporal modelling as the key performance driver — are well-supported and practically valuable. The paper has improved substantially across 4 review rounds, evolving from an ML benchmark into a genuine BSPC contribution.

Three blocking items (B1-B3) require text-level corrections only. No new experiments are needed.

**Final Score: 82/100**
**Final Recommendation: Accept with minor text-level revisions**
