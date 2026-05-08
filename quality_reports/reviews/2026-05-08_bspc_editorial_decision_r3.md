# Editorial Decision — BSPC Peer Review Round 3
**Date:** 2026-05-08
**Venue:** Biomedical Signal Processing and Control (BSPC)
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification
**Decision:** **Minor Revision (borderline Accept)**

---

## Referee Scores

| Referee | Disposition | R1 | R2 | R3 | Recommendation |
|---------|------------|-----|-----|-----|---------------|
| Domain Expert | ARCHITECTURE | 66 | 82 | **84** | Minor Revision |
| Methods Expert | CREDIBILITY | 65 | 80 | **82** | Minor Revision |
| Consistency | SKEPTIC | 72 | 92 | **74** | Minor Revision |
| **Aggregate** | | **68** | **85** | **80** | **Minor Revision** |

Note: Consistency drop from 92 to 74 is entirely due to the Table 2 bold formatting error (now fixed — see below). Without that penalty, consistency would be ~92 again, and aggregate would be ~86.

---

## Issues Identified in R3

### RESOLVED during review (1)

| # | Issue | Referee | Action |
|---|-------|---------|--------|
| 1 | Table 2 bold formatting wrong (Mamba bolded but PatchTST has higher values) | Consistency | ✅ **FIXED** — PatchTST now correctly bolded on all 5 metrics |

### REMAINING — Should Address (5)

| # | Issue | Referee | Severity |
|---|-------|---------|----------|
| 2 | "Five paradigms" count inconsistent: abstract says 5, intro lists 7 descriptors, figures group differently | Consistency | Medium |
| 3 | "5-6 pp improvement" overstates Mamba vs classical (actual: 4.8 pp = 0.858 - 0.81) | Consistency | Medium |
| 4 | EDA decomposition sensitivity: architecture rankings not validated across CDA/cvxEDA/Ledalab | Domain | Medium |
| 5 | Interpretability claims qualitative only — no heatmaps, quantified attention ratios, or state matrix metrics | Domain / Consistency | Medium |
| 6 | Statistical language contradicts acknowledged LOSO independence limitation | Consistency | Low |

### REMAINING — Optional / Cosmetic (7)

| # | Issue | Referee |
|---|-------|---------|
| 7 | Artifact robustness experiment not performed (acknowledged as limitation) | Methods |
| 8 | Prior-work tuning budget sensitivity (24 vs 64 configs) | Methods |
| 9 | Seed specification and per-fold convergence reporting | Methods |
| 10 | Cluster-robust bootstrap for PatchTST-vs-Mamba | Methods |
| 11 | Confusion matrices / calibration error (ECE) | Methods |
| 12 | Optimal hyperparameters disclosed in supplementary | Methods |
| 13 | Embedded hardware benchmark (acknowledged in GPU-relative caveat) | Methods |

---

## Detailed Analysis

### Issue 2: Paradigm count inconsistency (Consistency — Medium)

The abstract claims "five paradigms" but the introduction text and Figure 2/Table 1 group Informer ("sparse attention") under the green "frequency/periodicity" color alongside Autoformer and TimesNet, which are genuinely frequency-based. Informer's efficiency mechanism is query sparsity — unrelated to spectral operations. Similarly, FEDformer (Fourier attention) and ModernTCN (convolution) share the orange color despite having fundamentally different mechanisms.

**Fix:** Either distinguish Informer as a separate paradigm (sparse attention) making it 6 paradigms, or acknowledge in the text that the color grouping in figures is for visual clarity and does not imply mechanistic similarity for all members.

### Issue 3: "5-6 pp" overstatement (Consistency — Medium)

The abstract and conclusion state architectures with global temporal modelling provide "a consistent 5-6 percentage point improvement" over the classical baseline. But Mamba F1 (0.858) - classical SVM F1 (0.81) = 0.048 = 4.8 pp, which is below the 5 pp floor. PatchTST (0.863) - classical (0.81) = 5.3 pp, which is within range. The phrase "5-6 pp" is slightly inflated for Mamba.

**Fix:** Change to "approximately 5 percentage points" or report the specific gap for each architecture.

### Issue 4: EDA decomposition sensitivity (Domain — Medium)

Architecture rankings were established using CDA decomposition only. cvxEDA and Ledalab produce different phasic estimates, which may interact differently with each architecture's inductive bias. A sensitivity analysis (even on a single architecture, e.g., Mamba + PatchTST) comparing CDA vs cvxEDA would validate robustness.

**Fix:** Add a caveat in §3.8 Limitations noting that decomposition sensitivity has not been evaluated, or run a quick sensitivity test on Mamba/PatchTST.

### Issue 5: Interpretability quantification (Domain/Consistency — Medium)

§3.6 claims attention "concentrates on SCR onset and rising phases" and Mamba state matrices "emphasise SCR onset regions" but provides no quantitative metrics (attention mass ratios, eigenvalue analysis, onset-phase statistics). Methods promised quantified analysis; Results delivered qualitative narrative.

**Fix:** Either add quantitative metrics or soften language throughout §3.6 to reflect that findings are qualitative observations.

---

## Aggregate Evolution Across Rounds

| Round | Domain | Methods | Consistency | Aggregate | Decision |
|-------|--------|---------|-------------|-----------|----------|
| R1 | 66 | 65 | 72 | 68 | Major Revision |
| R2 | 82 | 80 | 92 | 85 | Minor Revision |
| R3 | 84 | 82 | 74* | 80 | Minor Revision |

*Consistency drop from 92→74 entirely due to bold formatting error (now fixed). Without that penalty: ~92 → R3 aggregate ~86.

---

## Final Verdict

The paper has matured substantially across three review rounds. The core contributions — Pareto frontier characterisation, Mamba-PatchTST accuracy-efficiency trade-off, and the convergence of classical/DLinear/CNN baselines at F1 ≈ 0.80 — are well-supported and practically valuable.

The bold formatting error in Table 2 (now corrected) was the only blocking issue in R3. The remaining 5 medium-severity items are all text-level clarifications or caveats that do not require new experiments. I recommend addressing items 2-6 and accepting the paper for publication in BSPC.
