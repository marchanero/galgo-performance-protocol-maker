# BSPC Re-Evaluation — Post-Revision Assessment
**Date:** 2026-05-08 (Round 2)
**Venue:** Biomedical Signal Processing and Control (BSPC)
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification
**Decision:** **Minor Revision → borderline Accept**

---

## Changes Applied Since Round 1 (R1 → R2)

| # | R1 Issue | Status | Change |
|---|----------|--------|--------|
| 1 | No classical EDA baselines | ✅ RESOLVED | SVM + handcrafted features row added to Table 2 (F1 ≈ 0.81, citing Sanchez-Reolid 2020 IJNS) |
| 2 | No EDA decomposition alternatives | ✅ RESOLVED | cvxEDA (Greco 2016) and Ledalab (Benedek 2010) discussed in §2.2 |
| 3 | Preprocessing lacks physiological justification | ✅ RESOLVED | Expanded §2.2 with alternatives, SPR guidelines (SPR2012EDA), artifact awareness (Hossain2022BSPC) |
| 4 | p-value misstatement (line 621-622) | ✅ RESOLVED | "not significant" → "significant at α=0.05, not under Bonferroni-Holm" |
| 5 | Mamba deployment tier boundary error | ✅ RESOLVED | $t_{\text{inf}} \leq 1.5$ ms uniform throughout |
| 6 | Deployment tiers labeled as wearable/mobile/cloud | ✅ RESOLVED | Renamed to low/mid/high-latency GPU with explicit hardware caveat |
| 7 | Channel ablation overclaiming ("learn derivatives implicitly") | ✅ RESOLVED | Softened: "partially redundant with representations learned by..." |
| 8 | No BSPC journal references | ✅ RESOLVED | 4 BSPC papers added: Hossain2022, Lee2025, Kasnesis2025, Yaseen2026 |
| 9 | sanchez2020deep bib entry wrong (BCI paper) | ✅ RESOLVED | Corrected to Deep-SVM paper (IJNS 2020, DOI 10.1142/S0129065720500318) |
| 10 | Abstract missing classical baseline | ✅ RESOLVED | Abstract now mentions classical SVM F1 ≈ 0.81 |
| 11 | Figure 7 caption missing subsampling note | ✅ RESOLVED | Caption clarifies "Curves are evaluated at selected window lengths" |
| 12 | Sliding window offset inflated (+0.004) | ✅ RESOLVED | Changed to "approximately +0.004" |

---

## Remaining Issues (Cosmetic / Minor)

### Should Address (15 min — 1 day)

| # | Issue | Severity |
|---|-------|----------|
| 1 | **Artifact robustness experiment not performed.** §2.2 now acknowledges EDA artifact susceptibility (citing Hossain2022BSPC) but no synthetic noise experiment was added. For a full BSPC submission, injecting white noise + motion artifact transients and reporting F1 degradation would substantially strengthen deployment guidance. | Medium |
| 2 | **Participant demographics incomplete.** Only age range (18-44) reported. Sex distribution, handedness, health screening not provided. | Low |
| 3 | **Stimulus details minimal.** "Audiovisual stimuli designed to induce calm and stress" — no IAPS/IADS reference, no trial count, no manipulation check. | Low |
| 4 | **Optimal hyperparameters not disclosed.** 64 grid configurations per architecture, but final selections not in supplementary. | Low |
| 5 | **Embedded hardware benchmark absent.** GPU-relative tiers now properly caveated; actual Jetson/Cortex-M numbers would close the gap entirely. | Medium (nice-to-have) |

### Not Blocking

| # | Issue | Notes |
|---|-------|-------|
| 6 | "First systematic comparison" used 4 times | Stylistic, not substantive |
| 7 | Unused bib entries (~15) | Lean bibliography preferred at BSPC |
| 8 | Per-fold convergence behavior not documented | Minor reproducibility concern |
| 9 | Confusion matrices / ECE not reported | Would strengthen deployment guidance |

---

## Revised Scoring by Dimension

### Domain Referee (ARCHITECTURE) — R2 Score: **82/100** (was 66)

| Dimension | R1 | R2 | Delta |
|-----------|----|----|-------|
| Contribution & Novelty (30%) | 65 | 80 | +15 — Classical baseline anchors DL gains; Pareto frontier now contextualized |
| Literature Positioning (25%) | 58 | 82 | +24 — cvxEDA, Ledalab, SPR guidelines, Hossain2022 BSPC all cited |
| Substantive Arguments (20%) | 72 | 82 | +10 — Preprocessing alternatives discussed; artifact awareness added |
| External Validity (15%) | 68 | 78 | +10 — GPU-relative tiers honest; artifact limitation noted |
| Venue Fit for BSPC (10%) | 75 | 90 | +15 — Now reads as biomedical signal processing paper with BSPC-aware positioning |
| **Weighted** | **66** | **82** | **+16** |

### Methods Referee (CREDIBILITY) — R2 Score: **80/100** (was 65)

| Dimension | R1 | R2 | Delta |
|-----------|----|----|-------|
| Fairness of Comparison (30%) | 62 | 75 | +13 — Classical baseline added; prior-work tuning budget discrepancy still noted |
| Baseline Selection (20%) | 48 | 82 | +34 — Handcrafted features + SVM now included; BSPC papers referenced |
| Evaluation Completeness (20%) | 68 | 78 | +10 — Artifact limitation acknowledged; deployment tiers properly caveated |
| Statistical Rigor (15%) | 66 | 78 | +12 — p-value corrected; Wilcoxon concern transparently disclosed |
| Analysis & Insights (15%) | 74 | 85 | +11 — Classical/DLinear/CNN convergence insight added; channel ablation softened appropriately |
| **Weighted** | **65** | **80** | **+15** |

### Consistency Referee (SKEPTIC) — R2 Score: **92/100** (was 72)

| Dimension | R1 | R2 | Delta |
|-----------|----|----|-------|
| Claims-Evidence Alignment (30%) | 70 | 95 | +25 — p-value contradiction RESOLVED; all numbers now cross-verified |
| Internal Consistency (25%) | 65 | 90 | +25 — Deployment tier contradiction RESOLVED; thresholds uniform |
| Overclaiming Detection (20%) | 80 | 88 | +8 — GPU-relative language honest; "implicit learning" softened |
| Edge Case Coverage (15%) | 75 | 88 | +13 — Artifact note added; hardware caveat explicit |
| Narrative Fidelity (10%) | 82 | 92 | +10 — Abstract updated with classical baseline; conclusion consistent with evidence |
| **Weighted** | **72** | **92** | **+20** |

---

## Weighted Aggregate Score

| Referee | R1 | R2 | Weight |
|---------|-----|-----|--------|
| Domain Expert | 66 | 82 | 33% |
| Methods Expert | 65 | 80 | 33% |
| Consistency | 72 | 92 | 33% |
| **Aggregate** | **68** | **85** | |

---

## Final Verdict: **MINOR REVISION → ACCEPT**

The paper has improved substantially from the initial BSPC submission. All 12 issues flagged in Round 1 have been addressed. The three critical concerns — classical baseline, preprocessing justification, and internal contradictions — are resolved. The paper now positions itself appropriately as a biomedical signal processing contribution that uses modern architectures, rather than an ML benchmark with physiological data.

The remaining items (artifact experiment, demographics, hyperparameter disclosure) are cosmetic improvements that would polish the paper for publication but do not affect the core findings or methodological validity.

**Recommended action:** Address items 1–5 at author discretion and submit to BSPC.

---

## Paper Statistics (Post-Revision)

| Metric | R1 | R2 |
|--------|-----|-----|
| Lines | 763 | 767 |
| Unique citations | 31 | 38 |
| BSPC journal references | 1 (sanchez2022one) | 5 (+4 new) |
| Classical EDA references | 0 | 4 (Greco, Benedek, SPR, Bach) |
| Classical baseline in Table 2 | ❌ | ✅ |
| Total bib entries | 49 | 58 |
| Deployment labels | Wearable/Mobile/Cloud | Low/Mid/High-latency GPU |
