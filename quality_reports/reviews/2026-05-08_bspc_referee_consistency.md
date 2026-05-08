# Consistency Referee Report
**Date:** 2026-05-08
**Venue:** Biomedical Signal Processing and Control (BSPC)
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification
**Disposition:** SKEPTIC / Cross-domain consistency
**Calibrated to:** BSPC
**Recommendation:** Major Revision
**Overall Score:** 72/100

## Summary

The paper is well-structured and methodologically sound, with careful cross-referencing of most numerical values between tables, figures, and text. However, two internal contradictions require mandatory correction: (1) the Pareto frontier section misstates the statistical significance of the Mamba-PatchTST comparison, directly contradicting the statistical analysis section and the p-value itself; (2) Mamba is claimed to fall within the wearable deployment region despite the threshold definition placing it at the boundary of a different tier. The "first" claim is defensible but repeated excessively. Missing methodological details (stimulus characteristics, participant demographics beyond age range) reduce reproducibility.

## Dimension Scores

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Claims-Evidence Alignment | 30% | 70 | p-value misstatement in Pareto section undermines the central claim about Mamba-PatchTST |
| Internal Consistency | 25% | 65 | Direct contradiction on statistical significance between Sections 3.3 and 3.5; deployment-tier boundary error |
| Overclaiming Detection | 20% | 80 | "First" claims defensible but repeated 4+ times; deployment narrative partially exceeds GPU-only evidence |
| Edge Case Coverage | 15% | 75 | Limitations section is honest; missing demographics and stimulus details are notable gaps |
| Narrative Fidelity | 10% | 82 | Conclusion largely recapitulates abstract; some redundancy between Sections 3.1 and 3.7 |
| **Weighted** | 100% | **72.2** | |

## Cross-Reference Issues

### Abstract ↔ Results
- Abstract: "Mamba achieves F1 = 0.858 at 1.5 ms inference time, approaching PatchTST accuracy (F1 = 0.863) at 3.6× lower latency and 66% fewer parameters" — All values verified against Table 2 (F1: 0.858, 0.863) and Table 3 (inference time: 1.5 ms, 5.4 ms; 5.4/1.5 = 3.6; parameters: 1.52M vs 4.52M → 66.4% reduction). ✓
- Abstract: "derivative channels provide greatest benefit for simpler architectures" — Confirmed by Table S1: DLinear (+2.8%), ModernTCN (+2.7%) vs PatchTST (+1.8%), Mamba (+1.9%). ✓
- Abstract: "147 participants" — Matches method section (line 82). ✓

### Introduction ↔ Conclusion
- Introduction contribution (i): "first systematic accuracy-efficiency comparison" → Conclusion line 750: matches. (Claim assessed under Overclaiming below.)
- Introduction contribution (ii): "Pareto frontier" → Conclusion line 752: matches. ✓
- Introduction contribution (iii): "DLinear and ModernTCN as critical baselines" → Conclusion line 754: mentions both. ✓
- Introduction contribution (iv): "physiologically-grounded insights" → Conclusion mentions interpretability via Section 3.6. ✓
- All four contributions map from Introduction to Conclusion. ✓

### Methods ↔ Results
- Methods (Section 2.6): channel ablation described (i—iii) → Results (Section 3.6, line 725): references Table S1. ✓
- Methods (Section 2.6): attention weight interpretation → Results (Section 3.6, line 717): describes attention concentration patterns. ✓
- Methods (Section 2.6): gradient-based saliency described → Results (Section 3.6, line 723): presents saliency findings. ✓
- Methods (Section 2.5): statistical significance via Wilcoxon → Results (Section 3.5, line 711): reports p-values. ✓
- Methods (Section 2.2): window length variation 1–40 s → Results (Section 3.4, Figure 6): full curves shown. ✓
- Methods (Section 2.2): two segmentation strategies → Results (line 705): sliding vs non-overlapping offset of +0.004 discussed. ✓
- Methods (Section 2.5): five efficiency metrics (params, FLOPs, t_inf, M_peak, t_train) → Results (Table 3): all five reported. ✓
- **Gap:** Methods (Section 2.6, line 398): "For Mamba, the discretised state transition matrices were examined to characterise how information propagates across the sequence" → Results (Section 3.6, line 721) provides only a qualitative statement with no quantitative metrics, no visualisation, and no specific matrix properties reported. The Methods section promises an analysis that is not fulfilled. **—5**

### Tables ↔ Text
*All values cited in text matched against Tables 2, 3, and S1—S4:*

| Text claim | Table value | Match |
|------------|-------------|-------|
| DLinear F1 = 0.800 (line 484) | Table 2: 0.800 | ✓ |
| 1D-CNN F1 = 0.796 (line 484) | Table 2: 0.796 | ✓ |
| Mamba F1 = 0.858, t_inf = 1.5 ms (lines 429, 500) | Table 2: 0.858, Table 3: 1.5 | ✓ |
| PatchTST F1 = 0.863, t_inf = 5.4 ms | Tables 2, 3 | ✓ |
| DLinear t_train = 1.2 s/epoch (line 499) | Table 3: 1.2 | ✓ |
| PatchTST t_train = 42.8 s/epoch (line 505) | Table 3: 42.8 | ✓ |
| 35× faster per-epoch (line 548): 42.8/1.2 = 35.7 | ✓ |
| 3.6× less inference time (line 621): 5.4/1.5 = 3.6 | Table 3 | ✓ |
| 66% fewer params (line 731): (4.52-1.52)/4.52 = 66.4% | Table 3 | ✓ |
| ModernTCN F1 = 0.827 (line 735) | Table 2: 0.827 | ✓ |
| TCN F1 = 0.812, Δ = 1.5 pp (line 735) | 0.827 - 0.812 = 0.015 = 1.5 pp | ✓ |
| Mamba at n = 5 s: F1 = 0.81 (line 707) | Figure 6 data: 5 s = 0.810 | ✓ |
| PatchTST at n = 5 s: F1 = 0.80 (line 707) | Figure 6 data: 5 s = 0.800 | ✓ |
| DLinear parameter count: 0.08 M (line 498) | Table 3: 0.08 | ✓ |
| TimesNet parameter count: 2.05 M (line 502) | Table 3: 2.05 | ✓ |

- **Discrepancy 1:** Text (line 705) claims "an average offset of +0.004 across architectures" between sliding and non-overlapping window F1 values. The actual mean offset computed from Figure 6 vs Table 2 values is +0.0031 (individual offsets: PatchTST +0.002, Mamba +0.004, TimesNet +0.003, Autoformer +0.004, Informer +0.005, FEDformer +0.004, ModernTCN +0.003, DLinear 0.000). The reported +0.004 is slightly inflated. **—2**
- **Discrepancy 2:** Supplementary (line 128) states "over 100 GPU-hours" while main text (line 548) states "approximately 100 GPU-hours." Minor inconsistency. **—1**
- **Discrepancy 3:** Supplementary (line 127) states "DLinear converging approximately 100× faster than PatchTST in total wall-clock time (0.6 h vs. 60.6 h)." The main text (line 548) states "35× faster" which refers to per-epoch speed, while the supplementary refers to total convergence time (which includes different epoch counts). These are different comparisons but the main text does not clearly distinguish them, which could confuse a reader. **—2**

### Figures ↔ Captions ↔ Text

- **Figure 1 (pipeline):** Caption describes eight architectures grouped by complexity class. Figure shows exactly eight architecture boxes plus preprocessing/evaluation blocks. Colors match caption description. ✓
- **Figure 2 (architecture overview):** Shows all eight architectures with three blocks each. Complexity classes and venues match Table 1 caption. ✓
- **Figure 4 (F1 bars):** All 12 bar heights match Table 2 values exactly. ✓
- **Figure 5 (parameter bars):** All values match Table 3 exactly. ✓
- **Figure 6 (Pareto frontier):** All 8 data points match Tables 2 and 3 exactly. The Pareto frontier line (DLinear → ModernTCN → Mamba → PatchTST) is correctly identified: Mamba dominates FEDformer (higher F1 at lower latency), TimesNet, Informer, and Autoformer. ✓

- **Figure 6 caption issue:** Caption defines wearable as $t_{\text{inf}} < 1.5$ ms and mobile/edge as $1.5 \leq t_{\text{inf}} < 4$ ms. However, the figure's red-shaded wearable region extends to $x = 1.5$ (the fill rectangle ends at `axis cs:1.5`). This places the visual boundary ambiguously. More critically, **the text at line 619 includes Mamba (t_inf = 1.5 ms) in the wearable region**, which contradicts the caption's strict inequality ($t_{\text{inf}} < 1.5$). Under the caption's definition, Mamba belongs to the mobile/edge tier. **—8 (see Internal Contradictions)**

- **Figure 7 (window length):** PatchTST at 40s shows F1 = 0.865 in the figure but Table 2 reports 0.863. This is noted in text as due to sliding vs non-overlapping windows. However, the curve shows PatchTST at specific x-values (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30, 35, 40) that differ from the "systematically varied from n = 1 to n = 40 seconds" claimed in Methods. The figure omits intermediate points (11, 13, 14, 16–19, 21–24, 26–29, 31–34, 36–39) but the caption does not mention this subsampling. **—2**

### Prior Work Comparisons

- Prior work values in Table 2 (marked $\dagger$): 1D-CNN (0.796), TCN (0.812), InceptionTime (0.822), TST (0.840), PatchTST (0.852) — all verified against the reference paper at `master_supporting_docs/supporting_papers/reference_paper.tex` lines 184–188. ✓
- Condition equivalence: Text transparently notes expanded hyperparameter search (64 vs 24 configs) and additional Δ²SCR channel. ✓
- PatchTST F1 in reference paper was 0.852; current paper's PatchTST achieves 0.863. The difference is attributed to these methodological changes. ✓

## Overclaiming Instances

1. **"First systematic comparison"** — Used in Abstract (line 58), Introduction (line 75, twice), and Conclusion (line 750). The claim is defensible given the cited gap in the literature, but the four-fold repetition crosses from establishing novelty into self-citation. Not a factual error, but stylistically excessive.

2. **"Lightweight"/"efficient" without qualification** — These terms appear in the title and throughout but are always backed by the five complementary efficiency metrics. ✓ (No deduction.)

3. **"Significantly better" without stats** — Not found. All comparative claims reference p-values or effect sizes. ✓

4. **"Actionable, evidence-based guidance for selecting and deploying arousal classifiers" (Abstract, line 58)** — The Pareto frontier provides actionable guidance within the studied conditions. However, deployment readiness is demonstrated only on workstation-class GPUs (Quadro P5000, RTX 4080), not on actual wearable/edge hardware. The phrase "deploying" partially overreaches. **—3**

5. **"First explicit characterisation of the accuracy-efficiency trade-off for EDA classification" (Conclusion, line 750)** — Defensible given the specific combination of architectures, metrics, and LOSO protocol. ✓

6. **"Enabling real-time, on-device arousal classification for mental health monitoring" (Conclusion, line 757)** — Positioned as future work, which is appropriate context. However, the leap from lab stimuli (audiovisual, controlled) to mental health monitoring in ambulatory settings is large. The limitations section correctly hedges this, but the conclusion's aspirational framing softens that hedging. **—2**

## Internal Contradictions

### Contradiction 1 (CRITICAL): Statistical Significance of Mamba vs PatchTST

**Line 621–622 (Section 3.3, Pareto Frontier):**
> "The 0.005 F1 difference between Mamba and PatchTST is **not** statistically significant ($p = 0.048$, Supplementary Material (Table~S2))"

**Line 711 (Section 3.5, Statistical Significance):**
> "Mamba achieves F1 = 0.858, approaching PatchTST (F1 = 0.863) with a difference of 0.005---statistically significant at the conventional $\alpha = 0.05$ level ($p = 0.048$)"

**Line 731 (Section 3.7, Comparison with Prior Work):**
> "a 0.005 F1 difference that is statistically significant at the conventional $\alpha = 0.05$ level ($p = 0.048$)"

$p = 0.048 < 0.05$, therefore the difference IS statistically significant at $\alpha = 0.05$. Lines 711 and 731 are correct; line 621–622 is incorrect. The Pareto frontier section — which the paper identifies as "the central contribution of this work" (line 617) — misinforms the reader about the statistical support for its headline finding. This is not merely a matter of interpretation (Bonferroni-Holm correction is discussed separately); it is a factual error in describing the conventional-test outcome. **Deduction: —25**

### Contradiction 2: Mamba Deployment Region Assignment

**Line 619:** "The wearable/microcontroller region ($t_{\text{inf}} < 1.5$ ms)... DLinear (0.3 ms), ModernTCN (1.2 ms), and Mamba (1.5 ms) fall within this region."

**Figure 6 caption (line 613):** Defines wearable as $t_{\text{inf}} < 1.5$ ms and mobile/edge as $1.5 \leq t_{\text{inf}} < 4$ ms.

Mamba's inference time of 1.5 ms is not strictly less than 1.5 ms. Under the caption's definition, Mamba belongs to the mobile/edge tier, not wearable. The text at line 619 contradicts its own threshold definition. **Deduction: —8**

### Contradiction 3: Mamba State Transition Analysis

**Methods, line 398:** "For Mamba, the discretised state transition matrices were examined to characterise how information propagates across the sequence."

**Results, line 721:** "For Mamba, analysis of the discretised state transition matrices reveals that the selective state space mechanism emphasises SCR onset regions in a manner analogous to attention, despite the fundamentally different computational primitive."

The Methods section describes a quantitative analysis (examining matrices); the Results section provides only a qualitative, single-sentence observation without any matrix property values, visualisations, or quantitative evidence. This is an unfulfilled methods promise. **Deduction: —5**

## Edge Cases and Blind Spots

1. **Participant demographics incomplete:** "147 healthy participants (aged 18–44 years)" (line 82). No sex/gender distribution, ethnicity, handedness, medication use, or health screening criteria are reported. For a study making claims about inter-subject variability and deployment to diverse populations, this is a notable gap. The Limitation section mentions "other populations (clinical samples, older adults)" but does not address whether the base sample itself is demographically balanced.

2. **Stimulus characteristics absent:** The paper mentions "audiovisual stimuli designed to induce calm and stress states under controlled laboratory conditions" (line 82–83) but provides zero detail about the stimuli: what were they? How many trials? What was the stress induction method (IAPS images? video? mental arithmetic?). This makes it impossible to assess the construct validity of the arousal manipulation. The "stress" being classified could range from mild annoyance to genuine distress — the classification difficulty depends entirely on this difference.

3. **GPU as deployment proxy:** Inference time is benchmarked on a Quadro P5000 (2016 workstation GPU, Pascal architecture, 2560 CUDA cores) positioned as "more representative deployment-class hardware" (line 344). This is a questionable claim. Actual wearable deployment targets (ARM Cortex-M, Qualcomm Hexagon, Apple Neural Engine, Google Coral TPU) have fundamentally different compute characteristics. The paper acknowledges this in Limitations (line 741–742) but the framing throughout the Pareto section still implies deployment relevance from GPU benchmarks.

4. **LOSO overlap inflation:** The Limitations section (line 743) correctly notes that training sets overlap by 146 of 147 subjects across LOSO folds, violating the independence assumption of the Wilcoxon test. This is commendably transparent. However, the remaining sections (3.3, 3.5, 3.7) continue to cite p-values without this caveat, and the conclusion (line 731) frames the Mamba-PatchTST significance without qualification. Readers who do not reach Section 3.8 will be unaware of this limitation.

5. **No validation of stimulus effectiveness:** The classification task is binary (calm vs stress), but no manipulation check is reported. Were participants actually stressed by the stress stimuli? Without verifying that the ground-truth labels correspond to genuine physiological states, the classification results may reflect stimulus differences rather than arousal differences.

6. **Hyperparameter configuration not reported:** The paper states 64 configurations were searched per architecture, but the final selected hyperparameters for each architecture are not disclosed (even in supplementary material). This impedes exact reproducibility.

## Major Comments

1. **CRITICAL — Correct the statistical significance misstatement at line 621—622.**
   The text claims the Mamba-PatchTST F1 difference "is not statistically significant" despite reporting $p = 0.048 < 0.05$. This directly contradicts lines 711 and 731, and the p-value itself. If the intended interpretation is "not significant under Bonferroni-Holm correction," this qualifier must be added explicitly. As written, the sentence is factually incorrect and misleads readers of the Pareto frontier section — which the paper positions as its central contribution.
   - **What would change my mind:** Replace the sentence with the correct interpretation and add the Bonferroni-Holm qualifier. E.g., "The 0.005 F1 difference between Mamba and PatchTST is statistically significant at the conventional $\alpha = 0.05$ level ($p = 0.048$) but does not survive the Bonferroni-Holm correction for 28 comparisons."

2. **Clarify Mamba's deployment tier assignment.**
   The text includes Mamba in the wearable region ($t_{\text{inf}} < 1.5$ ms) but Mamba's inference time is exactly 1.5 ms, which falls into the mobile/edge tier per the figure caption's definition. Either adjust the threshold to $\leq 1.5$ ms uniformly or reassign Mamba to mobile/edge.
   - **What would change my mind:** Consistent threshold usage throughout the figure caption, shaded regions, and accompanying text. Changing the wearable threshold to $t_{\text{inf}} \leq 1.5$ ms would resolve the contradiction with minimal impact on the narrative.

3. **Disclose participant demographics and stimulus details.**
   A single sentence on sex distribution and a brief description of the stress-induction stimuli would substantially improve reproducibility and allow readers to assess construct validity. Without this, the clinical deployment claims rest on an opaque experimental foundation.
   - **What would change my mind:** Addition of (a) sex/gender breakdown of the 147 participants, and (b) 2–3 sentences describing the stress and calm stimuli, number of trials, and whether a manipulation check was performed.

4. **Report the selected hyperparameter configurations.**
   Each architecture's final hyperparameters (after grid search) should be reported, at minimum in the supplementary material. With 64 configurations searched and fold-wise selection based on validation F1, it is impossible to reproduce the results without knowing which configurations were ultimately used.
   - **What would change my mind:** A supplementary table listing the optimal hyperparameters for each architecture, or, if per-fold variation exists, reporting the most frequently selected configuration and the range of selections.

## Minor Comments

1. **Line 705:** The claimed average offset of +0.004 between sliding and non-overlapping window F1 values should be recalculated. The arithmetic mean across the eight architectures is +0.0031. Rounding to +0.003 would be more precise.

2. **Line 548 ("approximately 100 GPU-hours") vs Supplementary line 128 ("over 100 GPU-hours"):** Reconcile these two estimates.

3. **Line 548 ("35× faster") vs Supplementary line 127 ("100× faster"):** The main text discusses per-epoch speed (35×) while the supplementary discusses total convergence time (100×). Clarify which comparison is being made in each context to avoid reader confusion.

4. **Figure 7 caption:** Note that the window-length curves are subsampled (not every integer second from 1–40 is shown) for readability.

5. **Methods line 398 → Results line 721:** The Mamba state transition matrix analysis description is too vague to be considered a fulfilled methods promise. Either provide quantitative results (trace of state matrices, eigenvalue analysis, transition weights) or remove this analysis from the Methods section.

6. **Abstract and Conclusion:** Reduce the four-fold repetition of "first systematic comparison." The novelty claim is made in the abstract; repeating it verbatim in introduction, methods-adjacent text, and conclusion dilutes its impact.

7. **Line 480–481:** "The original Mamba evaluation reported 5× inference throughput..." This claim about the original Mamba paper's results \cite{Mamba2023} should be verified. If the Mamba paper compared against Transformers of equivalent size on NLP tasks, the 5× number may not be directly applicable to the EDA classification context.

8. **Table S2 footnote/Limitations:** The p-value interpretation caveat regarding LOSO fold overlap (acknowledged in Section 3.8) should be cross-referenced from the statistical significance section (Section 3.5) so readers do not encounter the caveat only after reading all p-value claims.

---

**Disposition note:** The statistical significance contradiction alone warrants Major Revision — it is a factual error in the paper's self-described "central contribution" section. All other issues are addressable with minor edits. None of the required revisions would change the paper's conclusions, only their accurate presentation.
