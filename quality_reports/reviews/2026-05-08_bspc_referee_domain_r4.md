# Domain Referee Report (Round 4 — FINAL, ARCHITECTURE Disposition)
**Date:** 2026-05-08
**Venue:** Biomedical Signal Processing and Control (BSPC)
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification
**Referee Role:** Domain Expert — ARCHITECTURE disposition (critic, not creator)
**Recommendation:** ACCEPT
**Overall Score:** 83/100

---

## Executive Summary

This manuscript returns for Round 4 after three prior revision cycles. The core contribution — the first systematic accuracy-efficiency comparison of Transformers, SSMs, and modernised convolutions for EDA under LOSO — is methodologically sound and practically meaningful. The classical EDA baseline (handcrafted features + SVM, F1 ≈ 0.81), discussion of alternative decomposition methods (cvxEDA, Ledalab), BSPC-specific journal positioning, and comprehensive Limitations section collectively establish biomedical signal processing credibility. The central finding — Mamba achieves F1 = 0.858 at 1.5 ms, approaching PatchTST (F1 = 0.863) at 3.6× lower latency and 66% fewer parameters — is well-supported.

All three Medium concerns from Round 3 remain partially or fully unaddressed in this revision. None threatens the core contribution, and the paper's strengths substantially outweigh the remaining gaps. I recommend ACCEPT.

---

## Dimension-by-Dimension Scoring

### 1. Contribution & Novelty (Weight: 30%)
**Score:** 82/100  *(Unchanged from R3)*

The paper's contribution hierarchy remains well-established: (i) first systematic accuracy-efficiency comparison spanning five paradigms for EDA under LOSO, (ii) explicit Pareto frontier characterisation with five complementary efficiency metrics, (iii) DLinear and ModernTCN as critical baselines testing the necessity of complex temporal mechanisms, and (iv) channel ablation analysis revealing derivative redundancy patterns. The classical SVM baseline anchors the deep learning gains in established signal processing methodology.

The framing tension noted in R3 persists: the title and abstract emphasise "efficient architectures," yet half the architectures studied (Informer, Autoformer, TimesNet, PatchTST) occupy the mid-to-high latency tier and are not developer-facing candidates for resource-constrained deployment. This tension is acknowledged implicitly through the Pareto analysis but is not reconciled in the framing language.

**What would change my mind:** A reframing of the introductory and abstract language from "efficient architectures" to "accuracy-efficiency trade-off characterisation across efficiency paradigms" would more precisely describe the paper's actual contribution. This is a framing adjustment, not a content change.

---

### 2. Literature Positioning (Weight: 25%)
**Score:** 84/100  *(−1 from R3)*

The citation base remains well-rounded. EDA physiology standards (Boucsein 2012, SPR2012), decomposition alternatives (cvxEDA, Ledalab), BSPC journal contributions (7 papers), architecture sources, and external validity references (WESAD) are all present. Prior self-citation density concerns are fully resolved.

The LSTM/BiLSTM gap noted in R3 as a Medium concern remains entirely unaddressed. No LSTM citation, comparison, or discussion has been added to the Introduction, architecture descriptions, Results, or Discussion sections. LSTMs remain the most widely used sequence-modelling baseline in biomedical signal processing and specifically in BSPC. While the selected architecture set (Transformers, SSMs, modernised convolutions) is defensible, the absence of even a cited LSTM performance reference on EDA or related physiological signals is conspicuous for a BSPC audience.

Additionally, the "Further Reading" supplementary list still contains bibliographic entries (e.g., portal2025performance, and approximately 10–12 others) that are not cited in the main text — a cosmetic issue noted in R3 (m5) that persists.

**What would change my mind:** A single cited comparison (e.g., "BiLSTM-based approaches on similar EDA classification tasks have reported F1 in the range X–Y [citation]") or a brief justification for excluding LSTMs from the architecture selection would close this gap. No new experiment is needed. If published evidence placed LSTMs at or below the DLinear tier on EDA, that would strengthen the paper's thesis about global temporal modelling driving the performance gap.

---

### 3. Substantive Arguments & Interpretation (Weight: 20%)
**Score:** 86/100  *(−2 from R3)*

The physiological interpretation of results remains generally well-calibrated and appropriately hedged. Specific strengths preserved from R3:
- Window-length analysis anchored to SCR waveform duration (15–20s saturation, 5s minimum viable window).
- Channel ablation interpretation carefully hedged as "partial redundancy" rather than overclaiming derivative reconstruction.
- Statistical transparency (raw + Bonferroni-Holm p-values, effect sizes in pp, acknowledged LOSO independence violation).
- DLinear–1DCNN–SVM convergence analysis identifying the F1 ≈ 0.80 ceiling for local/no temporal modelling.

Two R3 concerns degrade this score slightly:

1. **Interpretability analysis remains entirely qualitative (R3 Medium concern M2).** The claims that attention "concentrates on SCR onset and rising phases" (line 722), Mamba state transitions "emphasise SCR onset regions" (line 727), and gradient saliency shows "complementary contributions" (line 728) are still presented without any quantitative metric support. No attention entropy, peak-to-mean ratio, saliency-SCR landmark correlation, or period-detection overlap coefficient has been added. For a BSPC readership accustomed to quantitative signal analysis, these claims remain suggestive rather than evidence-backed.

2. **Derivative redundancy interpretation not further supported (R3 Medium concern M1, sub-point).** The alternative explanation noted in R3 — that attention/SSM architectures benefit less from any additional input feature due to higher overall capacity (diminishing returns), regardless of internal derivative-like computation — has not been addressed with a control experiment or discussion.

**What would change my mind:** Quantitative interpretability metrics (attention entropy, saliency peak correlation with SCR onset landmarks) for at minimum PatchTST and Mamba would elevate this to 90+. Conversely, if quantitative analysis showed no reliable concentration pattern, the interpretability narrative would need revision.

---

### 4. External Validity & Generalizability (Weight: 15%)
**Score:** 80/100  *(Unchanged from R3)*

Internal validity remains strong: 147 participants, strict LOSO, identical hyperparameter budgets, transparent limitation acknowledgment. The Limitations section (Section 3.8) is comprehensive.

The three external validity concerns from R3 remain unchanged:
1. **Single dataset, single laboratory, healthy participants only.** No cross-dataset evaluation on WESAD or any other dataset has been performed. Generalizability to clinical populations, older adults, ambulatory settings, and different stress protocols remains unestablished.
2. **EDA decomposition method fixed to CDA.** Despite discussing cvxEDA and Ledalab alternatives, no sensitivity analysis has been performed. The robustness of architecture rankings to decomposition method choice is untested.
3. **No stimulus validation/manipulation check.** The absence of self-report or physiological validation that stimuli produced differential arousal was noted in R3 and has not been addressed.

**What would change my mind:** A cross-dataset evaluation on WESAD for 2–3 architectures (DLinear, Mamba, PatchTST) would provide strong generalizability evidence. Even a more detailed discussion of expected generalizability patterns — informed by the EDA literature — would be valuable.

---

### 5. Fit for BSPC (Weight: 10%)
**Score:** 87/100  *(−1 from R3)*

The paper reads as a biomedical signal processing contribution. The physiological signal processing pipeline (CDA decomposition, derivative channels), classical EDA baseline, SPR2012 guidelines discussion, BSPC journal references, and deployment narrative oriented toward wearable biomedical devices all establish BSPC fit. The computational efficiency focus is directly relevant to translational biomedical engineering.

The slight downward adjustment reflects the persistent LSTM absence, which slightly weakens the paper's positioning within the BSPC baseline landscape. This is minor — the paper's fit remains strong.

---

## Major Comments

### M1. Missing LSTM Citation/Discussion (Medium — carried from R3)
**Location:** Introduction / Section 2.3

LSTM and BiLSTM architectures remain the most common sequence-modelling baselines in BSPC. Their absence — even as a cited performance reference — is conspicuous. The paper's architecture selection is defensible (focusing on Transformer variants, SSMs, modernised convolutions), but a BSPC audience will notice the omission.

**What would change my mind:** A cited comparison or brief justification. Example: "LSTM-based approaches on EDA arousal classification have reported F1 in the range 0.78–0.81 [citation], consistent with the DLinear/1D-CNN tier, suggesting that recurrent gating alone — without global temporal dependency — does not exceed the local-information ceiling." This requires only a literature search, not new experiments.

---

### M2. Interpretability Analysis Lacks Quantification (Medium — carried from R3)
**Location:** Section 3.6

All interpretability claims remain qualitative. The convergence of attention-based models on SCR onset/rising phases is noted across PatchTST, Informer, Autoformer, and FEDformer — but the degree of "concentration" is not quantified. Mamba state transitions are described as "emphasising SCR onset regions in a manner analogous to attention" without metric support. Gradient saliency contributions are described qualitatively.

**What would change my mind:** Quantitative metrics for at minimum PatchTST and Mamba: (a) attention entropy or peak-to-mean ratio to quantify temporal focus, (b) correlation between saliency peak timing and SCR onset landmarks from CDA, (c) Jensen-Shannon distance between attention distributions across architectures. If quantitative analysis confirmed the qualitative descriptions, the interpretability narrative would shift from suggestive to evidence-backed.

---

### M3. EDA Decomposition Sensitivity Not Tested (Medium — carried from R3)
**Location:** Section 2.2

The paper discusses cvxEDA (Greco 2016) and Ledalab (Benedek 2010) as decomposition alternatives and cites SPR2012 guidelines, but all experiments use only CDA. The robustness of the headline finding — Mamba approaching PatchTST accuracy at 3.6× lower latency — to decomposition method choice remains untested.

**What would change my mind:** A limited sensitivity analysis applying cvxEDA to the phasic extraction and re-running the top 3 architectures (DLinear, Mamba, PatchTST), or a referenced argument from the EDA literature demonstrating that CDA, cvxEDA, and Ledalab produce rank-order-preserving phasic signals for arousal classification. An explicit note in the Limitations section acknowledging this as a direction for future work would also partially address the concern.

---

## Minor Comments

### m1. Optimal Hyperparameters Not Disclosed (carried from R3)
The 64-configuration grid search space is well-described (Table 3), but the final selected hyperparameters for each architecture are not provided. For full reproducibility, these should appear in the supplementary material: optimal embedding dimension, number of layers/blocks, patch size (PatchTST), state dimension (Mamba), kernel size (ModernTCN), Fourier modes (FEDformer), sampling factor (Informer), top-k periods (TimesNet), moving average kernel (Autoformer/FEDformer/DLinear).

### m2. Figure 6 (Pareto Frontier) Visual Distinction (carried from R3)
Mamba (purple) sits at (1.5ms, 0.858) on the Pareto frontier — the paper's headline finding. The visual distinction between purple (Mamba) and orange O(L) points (ModernTCN, FEDformer) is subtle in grayscale. Using distinct marker shapes (e.g., square for Mamba, circles for others) would improve accessibility.

### m3. "First" Claim Density (carried from R3)
The abstract and introduction both use "the first systematic comparison" (lines 58, 75). While defensible for the specific combination of architectures × EDA × LOSO × five efficiency metrics, a single "first" claim in the abstract with "systematic" used thereafter would read as more measured for a BSPC audience.

### m4. Uncited Bibliography Entries (carried from R3)
Approximately 10–12 bibliography entries (ETSformer2023, LightTS2022, Taleb2025, Suresh2025, Pativada2024, Souto2024, Gopi2025, Saravana2026, Choi2016, Caruana1997, Nandipati2024, Sun2025, Liu2025, portal2025performance, Zhu2024, Luo2024, Kim2024, Wang2024, Ahmadi2025, Naithani2026, Bach2010, Braithwaite2013) appear in the bibliography but are not cited in the main text. These should be either cited in the main text (where relevant), moved to a designated "Further Reading" list, or removed to maintain a lean bibliography.

### m5. Per-Class F1 Summary (carried from R3)
Table S3 reports per-class F1 (stress > calm by approximately 0.8 pp across architectures). A one-sentence summary of this finding in the main text (Section 3.1, near line 488) would strengthen the physiological narrative, as this asymmetry is consistent with EDA's role as a sympathetic activation marker.

### m6. Sliding vs. Non-Overlapping Window Clarification
Line 710 notes that sliding-window F1 values show an offset of "approximately +0.004" over non-overlapping windows. Figure 7 uses sliding windows (1-second stride) while main Table 2 uses non-overlapping windows. The Figure 7 caption should explicitly state the segmentation strategy to avoid confusion between the slightly different absolute F1 values in the two presentations.

---

## Summary of R3 → R4 Resolution

| R3 Concern | Severity | R4 Status |
|-----------|----------|-----------|
| M1: EDA Decomposition Sensitivity | Medium | **Unaddressed.** No sensitivity analysis, no referenced argument from EDA literature. |
| M2: Interpretability Quantification | Medium | **Unaddressed.** All interpretability claims remain qualitative. |
| M3: Missing LSTM Citation | Medium | **Unaddressed.** No LSTM reference or discussion added. |
| m1: Hyperparameter Disclosure | Minor | **Unaddressed.** Optimal configs not provided. |
| m2: Attention Weight Quantification | Minor | **Unaddressed.** |
| m3: Figure 6 Marker Shapes | Minor | **Unaddressed.** |
| m4: "First" Claims Softening | Minor | **Unaddressed.** |
| m5: Unused Bibliography | Minor | **Unaddressed.** ~12 uncited entries remain. |
| m6: Per-Class F1 Summary | Minor | **Unaddressed.** |
| m7: Sliding Window Caption | Minor | **Unaddressed.** |

---

## Scoring Summary

| Dimension | Weight | R3 Score | R4 Score | Delta | Notes |
|-----------|--------|----------|----------|-------|-------|
| Contribution & Novelty | 30% | 82 | 82 | 0 | Framing tension noted; contribution solid |
| Literature Positioning | 25% | 85 | 84 | −1 | LSTM gap persists without acknowledgment |
| Substantive Arguments | 20% | 88 | 86 | −2 | Interpretability remains qualitative; derivative redundancy not further supported |
| External Validity | 15% | 80 | 80 | 0 | Single-dataset constraint honestly acknowledged |
| Venue Fit (BSPC) | 10% | 88 | 87 | −1 | LSTM absence slightly weakens BSPC positioning |
| **Weighted Aggregate** | **100%** | **84** | **83** | **−1** | |

**Weighted calculation:** 0.30 × 82 + 0.25 × 84 + 0.20 × 86 + 0.15 × 80 + 0.10 × 87 = 24.6 + 21.0 + 17.2 + 12.0 + 8.7 = **83.5 ≈ 83**

---

## Final Recommendation: ACCEPT

This manuscript has matured substantially across four rounds of review. The core contribution — the first systematic accuracy-efficiency comparison spanning Transformers, SSMs, and modernised convolutions for EDA under strict LOSO — is well-executed, clearly communicated, and practically meaningful. The classical EDA baseline, decomposition method discussion, BSPC journal positioning, statistical transparency, and honest Limitations section collectively establish this as a credible biomedical signal processing contribution.

The three Medium concerns from Round 3 (decomposition sensitivity, interpretability quantification, LSTM citation) remain partially or fully unaddressed. The minor comments have not been incorporated. None of these threatens the core contribution. The 1-point score decrease from R3 (84 → 83) reflects the lack of movement on these items rather than any regression in the paper's quality, which remains solid.

I recommend ACCEPT. The remaining concerns are addressable at the proof stage (LSTM citation, minor corrections) or are suitable as directions for future work (decomposition sensitivity, quantitative interpretability). The paper's strengths — a well-designed comparison across five efficiency paradigms, the Pareto frontier characterisation, the DLinear/SVM/1D-CNN convergence analysis, and the Mamba finding — substantially outweigh the remaining gaps.

---

*Referee expertise: Biomedical signal processing, electrodermal activity measurement and analysis, time-series deep learning for physiological signals. Reviewed with ARCHITECTURE disposition — focused on architectural appropriateness for EDA signals, physiological interpretability, and translational biomedical relevance.*
