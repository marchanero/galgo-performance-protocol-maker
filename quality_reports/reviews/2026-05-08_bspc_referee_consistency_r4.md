# Round 4 (FINAL) — Consistency/Skeptic Referee Report

**Journal:** Biomedical Signal Processing and Control (BSPC)
**Manuscript:** _Efficient Transformer Architectures for Electrodermal Activity-based Arousal Classification_
**Reviewer disposition:** SKEPTIC
**Review date:** 2026-05-08
**Review focus:** FINAL cross-reference audit: Abstract ↔ Results, Tables ↔ Text, Figures ↔ Captions, prior-round issue resolution status

---

## Overview

This is the FINAL consistency review (Round 4). The manuscript has been cross-referenced in its entirety — main text, supplementary material, all six figures, all four tables, abstract, and conclusion. Section 5 summarises the resolution status of every R3 issue.

---

## 1. Cross-Referencing Protocol: Numeric Audit

### 1.1 Abstract ↔ Results ↔ Conclusion (full matrix)

| Claim | Abstract (line 58) | Main Results | Conclusion (line 755) | Match? |
|-------|-------------------|-------------|----------------------|--------|
| Mamba F1 = 0.858 | 0.858 | Table 3 (line 431): 0.858 | 0.858 | ✅ |
| Mamba inference = 1.5 ms | 1.5 ms | Table 4 (line 505): 1.5 | 1.5 ms | ✅ |
| PatchTST F1 = 0.863 | 0.863 | Table 3 (line 432): 0.863 | 0.863 | ✅ |
| 3.6× lower latency | 3.6× | 5.4 / 1.5 = 3.6 | 3.6× | ✅ |
| 66% fewer parameters | 66% | 1 − 1.52/4.52 = 66.4% ≈ 66% | 66% | ✅ |
| Classical SVM F1 ≈ 0.81 | 0.81 | Table 3 footnote (line 438) | 0.81 | ✅ |
| Mamba: +4.8 pp | +4.8 pp | 0.858 − 0.81 = +4.8 | +4.8 pp | ✅ |
| PatchTST: +5.3 pp | +5.3 pp | 0.863 − 0.81 = +5.3 | +5.3 pp | ✅ |
| "approximately 5 pp" | ✓ | covers 4.8–5.3 range | ✓ | ✅ |

**Verdict:** All numeric claims are consistent across abstract, results, and conclusion.

### 1.2 Tables ↔ Text

| Check | Table value | Text reference | Match? |
|-------|------------|---------------|--------|
| DLinear F1 | Table 3: 0.800 | Line 489: F1 = 0.800 | ✅ |
| ModernTCN F1 | Table 3: 0.827 | Line 740: "0.827, Δ = 1.5 pp" vs prior TCN 0.812 | ✅ |
| Mamba F1 | Table 3: 0.858 | Line 624, 716, 736, 755 | ✅ |
| PatchTST F1 | Table 3: 0.863 | Line 432, 624, 626, 755 | ✅ |
| PatchTST params | Table 4: 4.52 M | Line 736: "4.52 M" | ✅ |
| Mamba params | Table 4: 1.52 M | Line 736: "1.52 M" | ✅ |
| DLinear epoch time | Table 4: 1.2 s | Line 553: 1.2 s | ✅ |
| PatchTST epoch time | Table 4: 42.8 s | Line 553: 42.8 s | ✅ |
| 35× training speed | — | 42.8 / 1.2 = 35.7 ≈ 35 | ✅ |
| Prior work: 1D-CNN F1 | Table 3: 0.796 | Line 420, 734 | ✅ |
| Prior work: TCN F1 | Table 3: 0.812 | Line 421, 734 | ✅ |
| Prior work: InceptionTime F1 | Table 3: 0.822 | Line 422, 734 | ✅ |
| Prior work: TST F1 | Table 3: 0.840 | Line 423, 734 | ✅ |
| Prior work: PatchTST F1 | — | 0.852 vs current 0.863 (Table 3 footnote explains +0.011 via expanded HP search + Δ²SCR) | ✅ |

**Verdict:** All table-to-text numeric cross-references are consistent.

### 1.3 Figures ↔ Captions ↔ Text ↔ Tables

#### Figure 1 (Pipeline, `fig:pipeline`)
- Caption (line 184): "eight architectures grouped by computational complexity class" — shown as 8 nodes in the figure ✅
- Color scheme declared: blue=preprocessing, green=O(L log L), orange=O(L), red=linear, purple=evaluation — matches figure ✅

#### Figure 2 (Architecture overview, `fig:arch_overview`)
- Caption (line 305): "Colour coding follows the computational complexity class: blue = O(N²) patch attention, green = O(L log L) (frequency/periodicity and sparse attention), orange = O(L) (Fourier/convolution), purple = O(L) state space model, red = O(L) linear baseline."
- Green group includes Informer (sparse attention). Caption now explicitly acknowledges "sparse attention" alongside "frequency/periodicity." This partially addresses R3's concern about Informer misclassification. ✅
- FEDformer (orange) = Fourier/convolution. ModernTCN (orange) = convolution. Same color, different mechanisms — consistent with the caption which groups them by complexity class, not mechanism. ⚠️ Acceptable.

#### Figure 3 (F1 bars, `fig:f1_bars`)
All bar values cross-checked against Table 3:
- 1D-CNN: 0.796 ↔ Table 3: 0.796 ✅
- TCN: 0.812 ↔ Table 3: 0.812 ✅
- InceptionTime: 0.822 ↔ Table 3: 0.822 ✅
- TST: 0.840 ↔ Table 3: 0.840 ✅
- DLinear: 0.800 ↔ Table 3: 0.800 ✅
- ModernTCN: 0.827 ↔ Table 3: 0.827 ✅
- FEDformer: 0.836 ↔ Table 3: 0.836 ✅
- Informer: 0.845 ↔ Table 3: 0.845 ✅
- Autoformer: 0.848 ↔ Table 3: 0.848 ✅
- TimesNet: 0.853 ↔ Table 3: 0.853 ✅
- Mamba: 0.858 ↔ Table 3: 0.858 ✅
- PatchTST: 0.863 ↔ Table 3: 0.863 ✅

✅ All match.

#### Figure 4 (Pareto frontier, `fig:pareto`)
All data points cross-checked against Tables 3 & 4:
- DLinear: (0.3 ms, 0.800) ↔ Table 4: 0.3, Table 3: 0.800 ✅
- ModernTCN: (1.2 ms, 0.827) ↔ Table 4: 1.2, Table 3: 0.827 ✅
- FEDformer: (2.1 ms, 0.836) ↔ Table 4: 2.1, Table 3: 0.836 ✅
- Informer: (3.6 ms, 0.845) ↔ Table 4: 3.6, Table 3: 0.845 ✅
- Autoformer: (4.2 ms, 0.848) ↔ Table 4: 4.2, Table 3: 0.848 ✅
- TimesNet: (3.0 ms, 0.853) ↔ Table 4: 3.0, Table 3: 0.853 ✅
- Mamba: (1.5 ms, 0.858) ↔ Table 4: 1.5, Table 3: 0.858 ✅
- PatchTST: (5.4 ms, 0.863) ↔ Table 4: 5.4, Table 3: 0.863 ✅

Pareto frontier dashed line: DLinear → ModernTCN → Mamba → PatchTST. These are indeed non-dominated points. ✅

Caption region labels: "Low-latency GPU (≤1.5 ms)", "Mid-latency (1.5–4 ms)", "High-latency (≥4 ms)" — boundaries match the figure shading. ✅

#### Figure 5 (Window length, `fig:f1_window_length`)
⚠️ **The figure uses sliding-window data (1-second stride), while Table 3 uses non-overlapping windows.** Text line 710 explicitly states: "The window-length curves obtained from the sliding-window segmentation strategy... show slightly higher plateau F1 values than the non-overlapping windows used for the main results in Table 3, with an average offset of approximately +0.004 across architectures."

Spot checks:
- Mamba at 40s: figure 0.862 vs Table 3 0.858 → offset +0.004. Matches. ✅
- PatchTST at 40s: figure 0.865 vs Table 3 0.863 → offset +0.002. Within tolerance. ✅
- DLinear at 40s: figure 0.800 vs Table 3 0.800 → offset 0. ✅

The text adequately explains this discrepancy. ✅

Caption (line 702): _"Mamba and PatchTST (thick lines) degrade most gracefully at short windows."_

- At n = 1s: Mamba 0.730, PatchTST 0.730, TimesNet 0.720, DLinear 0.700
- At n = 5s: Mamba 0.810, PatchTST 0.800
- Drop from plateau (40s) to n = 5s: Mamba 0.862 → 0.810 = −0.052, PatchTST 0.865 → 0.800 = −0.065
- Mamba outperforms PatchTST at every short window (1–15s)

The "most gracefully" claim is defensible in aggregate but **conceals that Mamba holds a consistent short-window advantage over PatchTST** (0.010 at 5s, 0.015 at 10s). A more precise caption would note this explicitly.

---

## 2. Specific Items Requested for Verification

### 2.1 ✔ Bold formatting in Table 1 (tab:overall) — FIXED

**R3 issue:** PatchTST led on all 5 metrics but Mamba was erroneously bolded on Acc, Prec, Rec, F1.

**R4 status:** PatchTST is now bolded on all five classification metrics (lines 432, this is `tab:overall` = Table 1 in LaTeX output):
```
PatchTST   & \textbf{0.873 ...} & \textbf{0.867 ...} & \textbf{0.858 ...} & \textbf{0.863 ...} & \textbf{0.915 ...}
```
Caption (line 411): "Bold indicates best performance per metric." PatchTST leads numerically in all five metrics. ✅ **Fully resolved.**

### 2.2 ✔ "5–6 pp" → "approximately 5 pp" — FIXED in abstract and conclusion

**Abstract (line 58):** _"an approximately 5 percentage point improvement (Mamba: +4.8 pp, PatchTST: +5.3 pp)"_ ✅

**Conclusion (line 755):** _"architectures with global temporal dependency modelling provide an approximately 5 percentage point improvement (Mamba: +4.8 pp, PatchTST: +5.3 pp)"_ ✅

**Line 489** still uses "0.05–0.06" (decimal), referring to the gap between the "classical/DLinear tier and the best Transformer/SSM architectures (Mamba, PatchTST)." This is a range of gaps:
- DLinear (0.800) → PatchTST (0.863): gap 0.063 → 6.3 pp (in range)
- DLinear (0.800) → Mamba (0.858): gap 0.058 → 5.8 pp (in range)
- Classical (~0.81) → PatchTST (0.863): gap 0.053 → 5.3 pp (in range)
- Classical (~0.81) → Mamba (0.858): gap 0.048 → 4.8 pp (**below** 0.05 lower bound)

The "0.05–0.06" range does not fully cover the Mamba vs classical comparison (4.8 pp). Since the sentence explicitly names "Mamba, PatchTST" as the best architectures compared against "this classical/DLinear tier," the range implicitly includes the Mamba–classical gap. **Minor:** 0.048 rounds to 0.05 but reading "0.05–0.06" literally excludes it.

### 2.3 ❌ Paradigm count — NOT FULLY RESOLVED

**Abstract (line 58):** 5 paradigms clearly listed: patch-based attention, sparse attention, frequency-domain modelling, state space models, modernised convolutions. ✅

**Introduction (line 75):** _"eight architectures spanning five paradigms: PatchTST (patch-based attention), Informer (sparse attention), Autoformer and TimesNet (frequency/periodicity-based), FEDformer (Fourier attention), Mamba (selective state space model), ModernTCN (modernised convolution), and DLinear (linear decomposition)."_

The enumeration lists **seven** distinct parenthetical paradigm descriptors: (1) patch-based attention, (2) sparse attention, (3) frequency/periodicity-based, (4) Fourier attention, (5) selective state space model, (6) modernised convolution, (7) linear decomposition. A reader counting unique descriptors gets 7, not 5. ❌

The intended 5 are: patch attention, sparse attention, frequency-domain (subsuming Autoformer, TimesNet, and FEDformer), SSM, modernised convolution — with DLinear as a baseline excluded from the paradigm count. This intention is not clearly conveyed.

**Figure captions:** The 5 color groups do not perfectly align with the 5 claimed paradigms either (Informer = sparse attention → green = "frequency/periodicity"; FEDformer = frequency-domain but orange alongside ModernTCN = convolution).

**Resolution required:** Either (a) align parenthetical descriptors with the 5-paradigm list (e.g., FEDformer → "frequency-domain attention", exclude DLinear's descriptor), or (b) clarify in text that DLinear is a baseline rather than a paradigm, and that FEDformer belongs to the frequency-domain paradigm.

### 2.4 ⚠️ Interpretability language — PARTIALLY ADDRESSED

Qualitative qualifiers now appear:
- Line 722: "qualitative inspection" ✅
- Line 722: "qualitatively replicated" ✅
- Line 726: "qualitative analysis" ✅
- Line 728: "qualitatively suggest" ✅

**Remaining issues:**

1. **Line 724:** _"TimesNet's period discovery mechanism identifies dominant periods in the 2--5 second range"_ — "identifies" is unqualified. Should be "qualitatively identifies" or "is observed to identify."

2. **Methods §2.5.4 (line 398):** _"attention weight distributions were extracted and analysed to quantify temporal relevance"_ — uses "quantify" but no quantitative metrics (mean attention entropy, temporal concentration indices, etc.) are reported anywhere. The Methods promise quantifications that Results deliver only qualitatively.

3. **No visual/quantitative interpretability outputs:** Despite promising attention heatmaps, saliency maps, and state transition matrix analysis in Methods (lines 396–400), none appear in the main paper or supplementary material.

### 2.5 ⚠️ Statistical language cross-references LOSO limitation — PARTIALLY ADDRESSED

**Section 3.5 (Statistical Significance, lines 714–717):**
_"As noted in Section~3.8, these p-values should be interpreted as descriptive indicators of effect consistency due to overlap in training sets across LOSO folds."_ ✅ Cross-reference added.

**BUT: Section 3.3 (Pareto Frontier, line 626):**
_"The 0.005 F1 difference between Mamba and PatchTST is statistically significant at the conventional α = 0.05 level (p = 0.048)"_ — uses "statistically significant" **without** cross-referencing the LOSO caveat. ❌

**Section 3.7 (Comparison with Prior Work, line 736):**
_"a 0.005 F1 difference that is statistically significant at the conventional α = 0.05 level (p = 0.048)"_ — again **without** the LOSO caveat or Section 3.8 cross-reference. ❌

**Internal contradiction persists:** The paper simultaneously claims p-values provide "statistical significance" (inferential claim) while acknowledging they are "descriptive indicators of effect consistency rather than exact inferential statistics" (Section 3.8). The R3 recommendation to either remove "statistically significant" language or add a justification for approximate validity was not fully implemented. The three locations using "statistically significant" should either (a) all cross-reference 3.8, or (b) use descriptive language consistent with the stated limitation.

---

## 3. Supplementary Material Cross-Audit

### 3.1 Channel Ablation (Table S1) ↔ Main text (line 730)

| Claim in main text | Table S1 value | Match? |
|--------------------|----------------|--------|
| DLinear: +2.8% | 0.778 → 0.800 = +2.8% | ✅ |
| ModernTCN: +2.7% | 0.805 → 0.827 = +2.7% | ✅ |
| Mamba: +1.9% | 0.842 → 0.858 = +1.9% | ✅ |
| PatchTST: +1.8% | 0.848 → 0.863 = +1.8% | ✅ |
| "2.7–2.8%" range (simpler architectures) | ✓ | ✅ |
| "1.8–1.9%" range (attention/SSM) | ✓ | ✅ |

✅ Fully consistent.

### 3.2 Statistical Table (Table S2) — SIGNIFICANT INCONSISTENCIES FOUND

**Issue 1: Bold formatting in Table S2 violates its own convention**

Table S2 caption (line 55): _"Bold values indicate statistical significance at the conventional α = 0.05 level (raw, uncorrected)."_

The following 10 p-values are < 0.05 but are **NOT bolded** in the table:
- PatchTST–Mamba: 0.048 (should be bold)
- Mamba–Informer: 0.021 (should be bold)
- Mamba–Autoformer: 0.032 (should be bold)
- TimesNet–FEDformer: 0.004 (should be bold)
- Autoformer–ModernTCN: 0.005 (should be bold)
- Autoformer–FEDformer: 0.038 (should be bold)
- Informer–ModernTCN: 0.008 (should be bold)
- Informer–FEDformer: 0.045 (should be bold)
- FEDformer–ModernTCN: 0.032 (should be bold)
- ModernTCN–DLinear: 0.002 (should be bold)

Currently bolded values: 14. Values that should be bolded: 24. **The table's own bolding convention is violated for 10/28 comparisons.**

**Issue 2: Text description count does not match table data**

Supplementary line 73: _"Under the conventional α = 0.05 threshold, 22 of 28 comparisons are statistically significant."_

Actual count from the table: **24 comparisons have p < 0.05** (14 currently bolded + 10 that should be bolded but aren't). 22 ≠ 24. ❌

**Issue 3: Bonferroni-Holm count does not match table data**

Supplementary line 73 and main text line 717: _"Under the corrected threshold, 18 of 28 comparisons remain significant."_

The supplementary states the corrected threshold is _"$p_{\text{BH}} < 0.0018$"_ (line 51) — this is the plain Bonferroni threshold α/28 = 0.05/28 ≈ 0.0018, **not** the Bonferroni-Holm threshold (which uses sequential thresholds, not a single value).

Under the plain Bonferroni threshold of 0.0018:
- Comparisons with p < 0.0018: `<10⁻⁴, 0.0002, 0.0003(x2), 0.0004(x2), 0.0005(x2), 0.0006, 0.0008(x2), 0.0012, 0.0015` = 13 comparisons
- 18 ≠ 13 ❌

Under true Bonferroni-Holm (sequential thresholds starting at α/28 = 0.00179, α/27 = 0.00185, ..., α/13 = 0.00385):
- The smallest 15 p-values pass (k=15: 0.0028 < 0.00357 ✓; k=16: 0.004 < 0.00385 ✗)
- 18 ≠ 15 ❌

**The text's claim of 18 significant comparisons under either correction does not match the p-values in the table.**

**Issue 4: "all p < 0.002" claim for DLinear comparisons**

Main text line 717: _"Statistically significant differences between DLinear and all other architectures (all p < 0.002)"_

Table S2 shows ModernTCN–DLinear: p = 0.002. "p < 0.002" is false for this comparison; it should be "p ≤ 0.002."

### 3.3 Per-Class Performance (Table S3) ↔ Main text

Table S3 values are internally consistent and referenced correctly at line 380. Main text line 714 claims existence but makes no numeric claims requiring verification against S3. ✅

### 3.4 Training Time (Table S4) ↔ Main text

| Claim | Table S4 | Match? |
|-------|---------|--------|
| DLinear: 1.2 s/epoch | 1.2 | ✅ |
| PatchTST: 42.8 s/epoch | 42.8 | ✅ |
| DLinear total 0.6 h | 0.6 | ✅ |
| PatchTST total 60.6 h | 60.6 | ✅ |
| "100× faster" total | 60.6 / 0.6 = 101 | ✅ |

**NOTE (unresolved R3):** Main text line 553 uses 35× for per-epoch speed. Supplementary line 127 uses 100× for total wall-clock. The main text does not clarify these are different metrics. No parenthetical disambiguation has been added.

---

## 4. NEW Issues Discovered in R4

### 4.1 N4.1 [MAJOR]: Supplementary Table S2 — bold formatting + count errors (see §3.2)

This is a direct analogue of the R3 Table 1 bold error now replicated in the supplementary. The p-value bolding convention is violated for 10 comparisons, and both text counts (22, 18) are inconsistent with the table data (24, 13 or 15).

### 4.2 N4.2 [MODERATE]: Statistical significance language inconsistent across sections (§2.5)

Only 1 of 3 sections using "statistically significant" cross-references the LOSO independence limitation. The remaining two sections make unqualified inferential claims.

### 4.3 N4.3 [MODERATE]: ModernTCN–DLinear p-value boundary claim ("< 0.002" vs = 0.002)

Line 717: "all p < 0.002" should be "all p ≤ 0.002" since ModernTCN–DLinear = 0.002 (not less than).

### 4.4 N4.4 [MINOR]: Introduction line 94 cross-reference targets incorrect section

Line 94: _"a factor relevant to the deployment scenarios discussed in Section~3.3."_ Section 3.3 is the Pareto Frontier (accuracy-efficiency trade-off, latency tiers). Motion artefacts are more relevant to Section 3.8 (Limitations → cross-dataset evaluation, ambulatory settings). This cross-reference target is imprecise.

### 4.5 N4.5 [MINOR]: FEDformer omitted from tier narrative (line 483)

Line 483 lists the tier hierarchy: "state space models (Mamba) and patch-based attention (PatchTST) occupy the top tier, followed by frequency-domain Transformers (TimesNet, Autoformer) and sparse attention (Informer), with linear decomposition (DLinear) providing the lower bound." FEDformer (F1 = 0.836) is omitted despite outperforming ModernTCN (0.827) and nearly matching TST (0.840) from prior work. Its exclusion from the narrative tier description is inconsistent with its performance.

### 4.6 N4.6 [MINOR]: Figure 3.5 caption overgeneralization (line 702)

_"Mamba and PatchTST (thick lines) degrade most gracefully at short windows."_ Mamba consistently outperforms PatchTST at short windows (1–15s), so describing them as jointly "most graceful" obscures Mamba's distinct advantage in this regime.

---

## 5. R3 Issue Resolution Status

| R3 # | R3 Severity | Issue | R4 Status |
|------|------------|-------|-----------|
| R3.1 | MAJOR | Table 1 bold formatting error | ✅ **RESOLVED** — PatchTST bolded on all 5 metrics |
| R3.2 | MAJOR | "Five paradigms" inconsistency | ❌ **NOT RESOLVED** — Introduction still lists 7 paradigm descriptors |
| R3.3 | MODERATE | Statistical significance vs LOSO contradiction ❌ | ⚠️ **PARTIAL** — §3.5 cross-references §3.8, but §§3.3 and 3.7 do not |
| R3.4 | MODERATE | "First" claim overreaches (line 73) | ❌ **NOT RESOLVED** — still says "physiological" instead of "EDA" |
| R3.5 | MODERATE | Interpretability — qualitative vs quantitative gap | ⚠️ **PARTIAL** — qualifiers added, but "quantify" remains in Methods, no quantitative outputs |
| R3.6 | MODERATE | "5–6 pp" overstates Mamba improvement | ✅ **RESOLVED** in abstract/conclusion; ⚠️ "0.05–0.06" in line 489 borderline |
| R3.7 | MINOR | Training speed 35× vs 100× disambiguation | ❌ **NOT RESOLVED** |
| R3.8 | MINOR | FEDformer narrative omission | ❌ **NOT RESOLVED** |
| R3.9 | MINOR | Fig 3.5 caption overgeneralization | ❌ **NOT RESOLVED** |
| R3.10 | MINOR | Section 3.3 vs 3.8 cross-reference target | ❌ **NOT RESOLVED** |

**Resolution: 3 of 10 resolved, 2 partially resolved, 5 unresolved.**

---

## 6. Weighted Composite Score

| Dimension | Weight | Raw Score | Weighted | Notes |
|-----------|--------|-----------|----------|-------|
| Claims–Evidence Alignment | 30% | 72 | 21.6 | S2 bold/count errors deduct; "quantify" still unfounded |
| Internal Consistency | 25% | 65 | 16.3 | Paradigm count, S2 count, p=0.002 claim |
| Overclaiming Detection | 20% | 72 | 14.4 | "First" and "statistically significant" w/o caveat |
| Edge Case Coverage | 15% | 78 | 11.7 | Decomposition sensitivity noted but not tested |
| Narrative Fidelity | 10% | 75 | 7.5 | FEDformer omission, caption overgeneralization |
| **Aggregate** | | | **71.5** | |

---

## 7. Verdict

**Minor Revision** — conditionally accept after corrections.

The core experimental findings remain robust and well-supported. The accuracy-efficiency Pareto frontier contribution is sound. However, this FINAL review identifies:

**Must fix (2 MAJOR):**
1. **Supplementary Table S2 bold formatting + count errors** (§3.2): The same type of bold-formatting error flagged in R3 for the main text table now appears in S2, compounded by incorrect counts (22 vs 24, 18 vs 13/15).
2. **Paradigm count inconsistency** (§2.3): Introduction enumerates 7 paradigm descriptors for "5 paradigms." Still unresolved from R3.

**Should fix (3 MODERATE):**
3. "Statistically significant" language without LOSO caveat in §§3.3 and 3.7 (§2.5)
4. "all p < 0.002" → "all p ≤ 0.002" (§4.3)
5. "First" claim on line 73: "physiological" → "EDA" (§5, R3.4)

**Consider fixing (5 MINOR):**
6. "0.05–0.06" range in line 489 (§2.2)
7. Training speed 35× vs 100× disambiguation (§5, R3.7)
8. FEDformer narrative omission (§4.5)
9. Figure 3.5 caption overgeneralization (§4.6)
10. Section 3.3 cross-reference target (§4.4)

All items are straightforward to address and none invalidates the experimental results.
