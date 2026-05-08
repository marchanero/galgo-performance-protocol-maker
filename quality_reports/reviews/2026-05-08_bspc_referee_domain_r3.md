# Domain Referee Report (Round 3 — ARCHITECTURE Disposition)
**Date:** 2026-05-08
**Venue:** Biomedical Signal Processing and Control (BSPC)
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification
**Referee Role:** Domain Expert — ARCHITECTURE disposition (critic, not creator)
**Recommendation:** Minor Revisions
**Overall Score:** 84/100

---

## Executive Summary

This manuscript has undergone substantial improvement across two prior rounds of revision. The addition of a classical EDA signal processing baseline (handcrafted features + SVM, F1 ≈ 0.81), discussion of alternative EDA decomposition methods (cvxEDA, Ledalab, SPR2012 guidelines), BSPC-specific journal references, corrected statistical reporting, and an honest Limitations section collectively transform this from an ML-benchmark-with-physiological-data into a credible biomedical signal processing contribution. The central finding — that Mamba (a selective state space model) approaches PatchTST accuracy at 3.6× lower latency while requiring 66% fewer parameters — is well-supported and practically meaningful.

I have updated my scores upward on all five dimensions since Round 2, reflecting the resolved issues. Three remaining concerns are Medium severity from a BSPC domain perspective. None threatens the core contribution, but each would strengthen the paper's biomedical signal processing credibility.

---

## Dimension-by-Dimension Scoring

### 1. Contribution & Novelty (Weight: 30%)
**Score:** 82/100

The paper's primary contribution — the first systematic accuracy-efficiency comparison of Transformers, SSMs, and modernised convolutions for EDA under LOSO — is genuine and well-executed. The inclusion of five complementary efficiency metrics (params, FLOPs, inference time, peak memory, training time) as primary evaluation dimensions is methodologically distinctive. The Pareto frontier characterisation directly informs deployment decisions, moving beyond the common practice of reporting accuracy in isolation.

The classical baseline (handcrafted EDA features + SVM, F1 ≈ 0.81, from Sanchez-Reolid 2020) anchors the deep learning performance gains in a way that the previous version lacked. The finding that DLinear (F1 = 0.800), 1D-CNN (0.796), and classical feature engineering (≈0.81) all converge to a similar performance ceiling — and that global temporal modelling adds a consistent 5–6 pp improvement — is a transferable insight that extends beyond this specific dataset.

The channel ablation analysis revealing that derivative channels provide the greatest benefit for simpler architectures (DLinear, ModernTCN: +2.7–2.8%) and smaller gains for attention/SSM architectures (+1.8–1.9%) is physiologically informative and practically useful for practitioners choosing input representations.

**Remaining concern:** The paper frames itself around "efficient" architectures but includes PatchTST (O(N²), 4.52M params, 5.4ms inference) as the accuracy ceiling. This is methodologically sound — the Pareto frontier needs an upper bound — but the title and framing create a slight tension: half the architectures studied (Informer, Autoformer, TimesNet, PatchTST) are not especially efficient for the 40-second EDA window, occupying the mid-to-high latency tier. A more precise framing would be "accuracy-efficiency trade-off characterisation" rather than "efficient architectures" as the primary framing.

**What would change my mind:** A sensitivity analysis showing that the relative architectural rankings are preserved under different EDA decomposition methods (cvxEDA, Ledalab) would elevate this to 88+. If the rankings reversed under a different decomposition, that would be a critical finding requiring discussion.

---

### 2. Literature Positioning (Weight: 25%)
**Score:** 85/100

The citation base is now well-rounded. The paper references:
- EDA physiology and measurement standards: Boucsein 2012 (LongTermVariability), Posada-Quintero 2020, SPR2012 guidelines, Hossain 2024
- EDA decomposition alternatives: cvxEDA (Greco 2016), Ledalab (Benedek 2010)
- BSPC journal contributions: Zhao 2023, Anusha 2022, Ramadan 2024, Hossain 2022, Kasnesis 2025, Lee 2025, Yaseen 2026
- EDA-specific deep learning: Ganapathy 2021, Tsirmpas 2025
- Architecture sources: all 8 architectures properly cited with venues
- Efficient Transformer survey: Wen 2023, Tay 2022
- ECG-specific baselines for Mamba: ECGMamba 2024
- Related biosignal classification: IsmailFawaz 2019, Meng 2022
- WESAD dataset for external validity: Schmidt 2018

The prior self-citation density issues from Round 1 are fully resolved. The authors' own prior work is cited appropriately as the methodological foundation (Sanchez-Reolid 2020, 2022) and prior architecture benchmark, while 30+ external references provide independent context.

**Remaining concern (Medium):** The paper lacks citation of any LSTM or BiLSTM baseline in the EDA or BSPC literature. LSTMs remain the most widely used architecture in biomedical signal processing for sequence classification and constitute a natural baseline that sits between DLinear/1D-CNN and the Transformer family in terms of both capacity and computational cost. The Efficient Transformer survey (Wen 2023) and time-series classification review (IsmailFawaz 2019) both position LSTMs as foundational baselines. Including an LSTM benchmark — or at minimum citing work that has compared LSTMs to the included architectures on physiological signals — would close this gap.

Also notably absent: the recent BSPC paper by Portal et al. (2025) on deep learning architecture evaluation for physiological signal classification is listed in the supplementary "Further Reading" but not cited in the main text. This paper is directly relevant to the manuscript's methodology and should be discussed in the introduction or comparison section.

**What would change my mind:** A citation and brief discussion of LSTM/BiLSTM performance on EDA or related physiological signals — even from prior work rather than a new experiment — would demonstrate awareness of the most common BSPC baseline architecture.

---

### 3. Substantive Arguments & Interpretation (Weight: 20%)
**Score:** 88/100

The physiological interpretation of results is generally sound and well-calibrated. Specific strengths:

- **Window length analysis (Fig. 7):** The observation that performance saturates at 15–20 seconds and that this corresponds to the characteristic SCR waveform duration is physiologically grounded (cited Boucsein 2012). The 5-second minimum viable window finding directly informs wearable deployment.
- **Channel ablation (Table S1):** The interpretation that "the additional temporal context provided by derivative channels is partially redundant with the representations learned by attention and state-space mechanisms" is well-phrased and appropriately hedged — it avoids the overclaiming ("implicitly learns derivatives") from Round 1.
- **Attention weight concentration on SCR onset/rising phases:** This is replicated across all attention-based models (PatchTST, Informer, Autoformer, FEDformer), providing convergent evidence that diverse efficiency mechanisms preserve physiologically meaningful temporal focus. However, more precise quantification of this "concentration" (e.g., attention entropy, peak-to-mean ratio, specific time-segment statistics) would strengthen the claim beyond visual inspection.
- **Class asymmetry (Table S3):** The finding that stress states are more discriminable than calm states (mean +0.8 pp across architectures) is physiologically consistent with EDA's role as a sympathetic activation marker. The narrowing of this asymmetry in stronger architectures is an insightful secondary finding.
- **Statistical transparency:** Reporting both raw and Bonferroni-Holm corrected p-values, explicitly acknowledging the LOSO independence violation, and providing effect sizes (F1 differences in pp) is exemplary methodological practice.

**Remaining concerns (Medium):**

1. **Derivative channel redundancy interpretation needs more caution.** The claim that derivative gains are "partially redundant" with attention/SSM representations is plausible but underdetermined by the evidence. An alternative explanation is that attention/SSM architectures have higher overall capacity and therefore benefit less from any additional input feature (diminishing returns), regardless of whether the architecture internally reconstructs derivative-like information. A control experiment — e.g., adding a random/irrelevant third channel and measuring F1 gain — would distinguish these explanations.

2. **Interpretability analysis lacks quantification.** The descriptions of attention weight distributions (concentrating on SCR onset and rising phases), TimesNet periodicities (2–5 second range), Mamba state transitions (emphasising SCR onset), and gradient saliency (complementary channel contributions) are all qualitative. For a BSPC readership, quantitative metrics (e.g., Jensen-Shannon distance between attention distributions across architectures, correlation between saliency peaks and known SCR landmarks, overlap coefficient for period detection against ground-truth SCR timing) would substantially strengthen the interpretability claims.

3. **Optimal hyperparameters not disclosed.** The paper reports a 64-configuration grid search per architecture but the final selected hyperparameters for each architecture are not provided in the main text or supplementary material. For reproducibility — a growing expectation in BSPC — this information should be included in the supplementary material.

**What would change my mind:** Adding quantitative interpretability metrics (attention entropy/distribution overlap, saliency-SCR landmark correlation) for at minimum PatchTST and Mamba would elevate this to 92+. Conversely, if the qualitative claims could not be replicated with quantitative measures, that would require revision of the interpretability narrative.

---

### 4. External Validity & Generalizability (Weight: 15%)
**Score:** 80/100

The internal validity of this study is strong: 147 participants, strict LOSO protocol, identical hyperparameter search budgets, and transparent limitation acknowledgment. However, external validity remains the weakest dimension, and the authors acknowledge this honestly.

**Strengths:**
- The LOSO protocol provides the strongest possible internal validity for subject-independent evaluation and prevents the subject-level data leakage known to inflate EDA classification performance (Azad 2025).
- The Limitations section (Section 3.7) is comprehensive and honest, covering dataset constraints, hardware specificity, statistical test assumptions, and FLOPs measurement limitations.
- The explicit caveat that absolute latency values will differ on embedded hardware — while relative rankings are expected to persist — is appropriately guarded.
- The acknowledgment that LOSO training sets share 146 of 147 subjects, potentially inflating effective sample size for Wilcoxon tests, demonstrates methodological awareness.

**Remaining concerns:**

1. **Single dataset, single laboratory, healthy participants only.** All 147 participants are healthy adults (18–44 years) exposed to audiovisual stimuli in controlled laboratory conditions. Generalizability to:
   - **Clinical populations** (anxiety disorders, PTSD, depression) where EDA dynamics may differ
   - **Older adults** where skin conductance amplitude decreases with age (Boucsein 2012, Ch. 4)
   - **Ambulatory/free-living settings** where motion artefacts, ambient temperature, and hydration affect EDA (Hossain 2022 BSPC is cited but only as an acknowledgment)
   - **Different stress elicitation protocols** (social evaluative threat, cognitive load, physical stress)
   
   remains entirely unestablished. The WESAD dataset (Schmidt 2018) is mentioned as a candidate for cross-dataset validation but this has not been performed. For a BSPC paper, cross-dataset evidence or at minimum a more detailed discussion of how the identified architecture rankings might generalise (or fail to generalise) to these populations would be valuable.

2. **EDA decomposition method fixed to CDA.** The paper discusses cvxEDA and Ledalab alternatives (a Round 1–2 improvement) but uses only CDA for all experiments. The SPR2012 guidelines explicitly note that decomposition method choice affects downstream signal characteristics. Without a sensitivity analysis, the reader cannot assess whether Mamba's advantage over PatchTST, or the derivative channel contributions, are robust to the choice of decomposition method.

3. **No stress manipulation check or stimulus validation.** The paper states stimuli were "designed to induce calm and stress states" but provides no validation that the stimuli actually produced differential arousal (no self-report measures, no manipulation check). While the ground-truth labels are presumably based on stimulus condition, the absence of validation data limits confidence that the classification problem is well-posed.

**What would change my mind:** A cross-dataset evaluation on WESAD (even on a subset of 2–3 representative architectures — e.g., DLinear, Mamba, PatchTST — rather than all 8) would provide strong evidence of generalizability and elevate this score to 88+. Conversely, if Mamba substantially underperformed PatchTST on WESAD, that would be a critical finding requiring revision of the central claim.

---

### 5. Fit for BSPC (Weight: 10%)
**Score:** 88/100

The paper now reads as a biomedical signal processing contribution rather than an ML benchmark. The following elements establish BSPC fit:

- The problem is biomedical: EDA-based arousal classification with deployment to mental health monitoring, stress detection, and adaptive HCI.
- The signal processing pipeline is physiologically motivated (CDA decomposition, derivative channels encoding sympathetic activation dynamics).
- The classical EDA feature-engineering baseline (handcrafted SCR features + SVM) anchors the deep learning results in established BSPC methodology.
- The discussion of EDA decomposition alternatives (cvxEDA, Ledalab) and SPR2012 guidelines demonstrates awareness of signal processing standards.
- The BSPC journal references (7 papers) place the work within the venue's literature.
- The computational efficiency focus — params, FLOPs, memory, inference time — is directly relevant to the translational biomedical engineering question of deployability.

The remaining tension is that the paper's core methodology (systematic architecture comparison under LOSO) is equally publishable in a pure ML venue (e.g., IEEE TAC, Neural Networks, Pattern Recognition). What tips it toward BSPC is the physiological signal processing pipeline, the classical EDA baseline, the interpretability analysis tied to SCR physiology, and the deployment narrative oriented toward wearable biomedical devices. This balance is now well-struck.

---

## Major Comments

### M1. EDA Decomposition Sensitivity (Medium)
**Location:** Section 2.2

The paper discusses cvxEDA (Greco 2016) and Ledalab (Benedek 2010) as alternative decomposition methods and cites SPR2012 guidelines noting that decomposition choice affects downstream signal characteristics. However, all experiments use only CDA. The question of whether the architecture rankings — particularly Mamba vs. PatchTST and the derivative channel ablation patterns — are robust to the decomposition method remains untested.

For a BSPC audience that routinely chooses between decomposition methods, this is a notable gap. Even a limited sensitivity analysis (e.g., applying cvxEDA to the phasic extraction and re-running the top 3 architectures) would substantially strengthen confidence in the reported rankings.

**What would change my mind:** A decomposition sensitivity analysis on 2–3 representative architectures, or at minimum a referenced argument from the EDA literature demonstrating that CDA, cvxEDA, and Ledalab produce rank-order-preserving phasic signals for arousal classification. If the top-3 architecture rankings were shown to be robust across decomposition methods, this score elevates; if they reversed, that's a critical finding.

### M2. Interpretability Quantification (Medium)
**Location:** Section 3.6

The interpretability analysis currently relies on qualitative descriptions: attention "concentrates on SCR onset and rising phases," Mamba state transitions "emphasise SCR onset regions in a manner analogous to attention," saliency maps reveal "complementary contributions." For a BSPC readership accustomed to quantitative signal analysis, these claims would benefit from metric support.

**What would change my mind:** Quantitative metrics such as (a) attention entropy or peak-to-mean ratio across architectures to quantify focus, (b) correlation between saliency peak timing and known SCR onset landmarks from the CDA decomposition, (c) overlap coefficients for TimesNet period detection against ground-truth SCR inter-response intervals. If these metrics were provided for even PatchTST and Mamba, the interpretability claims would shift from suggestive to evidence-backed.

### M3. Missing LSTM Baseline Citation/Discussion
**Location:** Introduction, Section 2.3

LSTM and BiLSTM architectures remain the most common baselines in biomedical signal processing papers published in BSPC. While the paper's architectural selection is defensible — focusing on Transformer variants, SSMs, and modernised convolutions — the absence of any LSTM comparison or citation is conspicuous. The computational cost of an LSTM on a 160-timestep sequence is modest, and it would provide a natural bridging point between DLinear (no temporal modelling) and the Transformer family (global attention). Even citing published LSTM results on EDA or related physiological signals — without running a new experiment — would demonstrate awareness of this baseline.

**What would change my mind:** A cited comparison (e.g., "LSTM-based approaches on similar EDA datasets have reported F1 in the range X–Y [citation]") or a brief discussion of why LSTM was excluded from the architecture selection. If published evidence shows LSTMs at or below the DLinear/1D-CNN tier on EDA, that strengthens the paper's claim that global temporal modelling drives the performance gap.

---

## Minor Comments

### m1. Hyperparameter Disclosure
The 64-configuration grid search is well-described (§2.4, Table 3), but the final selected hyperparameters for each architecture are not reported. These should be included in the supplementary material for full reproducibility. At minimum: optimal embedding dimension, number of layers, patch size (PatchTST), state dimension (Mamba), kernel size (ModernTCN), and Fourier modes (FEDformer).

### m2. Attention Weight Quantification
At line 722: "attention weight distributions concentrate on SCR onset and rising phases." This claim is plausible but unquantified. Even a simple summary statistic (e.g., "attention weights in the onset region [0–5s] are 2.3× higher than the baseline uniform distribution") would add credibility.

### m3. Figure 6 (Pareto Frontier) — Mamba Placement
Mamba sits at (1.5ms, 0.858) on the Pareto frontier, dominating ModernTCN (1.2ms, 0.827) and FEDformer (2.1ms, 0.836). This is the paper's headline finding and is correctly identified. However, the visual distinction between Mamba (purple) and the orange O(L) points is subtle in grayscale printing. Consider using distinct marker shapes in addition to colours.

### m4. "First" Claims
The abstract and introduction use "first systematic comparison" multiple times. While defensible for the specific combination of architectures × EDA × LOSO × efficiency metrics, consider softening to "the first" (single mention) and using "systematic" thereafter. BSPC reviewers tend to be cautious about absolute novelty claims.

### m5. Unused Bibliography Entries
Approximately 10–12 bibliography entries (ETSformer2023, LightTS2022, Taleb2025, Suresh2025, Pativada2024, Souto2024, Gopi2025, Saravana2026, Choi2016, Caruana1997, Nandipati2024, Sun2025, Liu2025, portal2025performance, Zhu2024, Luo2024, Kim2024, Wang2024, Ahmadi2025, Naithani2026, Bach2010, Braithwaite2013) are not cited in the main text (some appear only in the supplementary "Further Reading"). BSPC prefers a lean, fully-cited bibliography. Consider moving truly uncited entries to the supplementary reading list or removing them.

### m6. Per-Class F1 Note
Table S3 reports per-class F1. The main text (line 380) says these "are reported in the Supplementary Material." The connection is clear, but a one-sentence summary of the key finding (stress > calm by 0.8 pp) would strengthen the main text.

### m7. Sliding Window Offset
Line 710 reports that sliding-window F1 values show an offset of "approximately +0.004" over non-overlapping windows. This is correctly hedged. However, the main results (Table 2) use non-overlapping windows while Figure 7 uses sliding windows (1-second stride). The caption should more explicitly state which segmentation strategy each figure/table uses, as the two yield slightly different absolute F1 values.

---

## Summary of Changes Since Round 2

| Issue (from R2) | Status | Assessment |
|-----------------|--------|------------|
| Related Work section absent | Still absent | Paper uses extended Introduction to position against prior work; BSPC format (llncs) does not require a separate Related Work section. Acceptable. |
| Limitations placement | IMPROVED | Now integrated into the results/discussion flow rather than interrupting it. |
| WESAD mention | ACKNOWLEDGED | Noted as future work (Section 4). Cross-dataset validation not performed. |
| DLinear-1DCNN parity discussion | RESOLVED | Line 489 explicitly discusses this convergence and connects it to the classical baseline. |
| Figure 6 axis limits | PARTIALLY RESOLVED | Y-axis now starts at 0.70 (was 0.68), compressing the plateau region less severely. Could still start at 0.74 given the data range. |
| Per-class F1 supplementary | CONFIRMED | Table S3 in supplementary material. |

---

## Scoring Summary

| Dimension | Weight | R2 Score | R3 Score | Delta | Notes |
|-----------|--------|----------|----------|-------|-------|
| Contribution & Novelty | 30% | 80 | 82 | +2 | Well-established; framing tension noted but minor |
| Literature Positioning | 25% | 82 | 85 | +3 | BSPC refs solid; LSTM gap remains |
| Substantive Arguments | 20% | 82 | 88 | +6 | Physiological interpretations well-calibrated and hedged |
| External Validity | 15% | 78 | 80 | +2 | Single-dataset constraint honestly acknowledged |
| Venue Fit (BSPC) | 10% | 90 | 88 | −2 | Strong, but LSTM absence slightly weakens BSPC positioning |
| **Weighted Aggregate** | **100%** | **82** | **84** | **+2** | |

**Weighted calculation:** 0.30 × 82 + 0.25 × 85 + 0.20 × 88 + 0.15 × 80 + 0.10 × 88 = 24.6 + 21.25 + 17.6 + 12.0 + 8.8 = **84.25 ≈ 84**

---

## Final Recommendation: MINOR REVISIONS → ACCEPT

This manuscript has matured substantially through the revision process. The core contribution — the first systematic accuracy-efficiency comparison spanning Transformers, SSMs, and modernised convolutions for EDA under LOSO — is well-executed and clearly communicated. The classical EDA baseline, decomposition method discussion, BSPC journal positioning, and honest limitations section collectively address the most important concerns from earlier rounds.

The three Medium concerns (decomposition sensitivity, interpretability quantification, LSTM citation) are genuine but do not threaten the paper's contribution. Addressing them would elevate an already-solid paper to a stronger one. The minor comments are cosmetic or documentation-level improvements.

I recommend **minor revisions** with the expectation that the authors address the Medium concerns to the extent feasible (particularly adding LSTM citation/discussion, which requires only a literature search, not new experiments) and incorporate the minor corrections before final acceptance.

---

*Referee expertise: Biomedical signal processing, electrodermal activity measurement and analysis, time-series deep learning for physiological signals. Reviewed with ARCHITECTURE disposition — focused on architectural appropriateness for EDA signals, physiological interpretability, and translational biomedical relevance.*
