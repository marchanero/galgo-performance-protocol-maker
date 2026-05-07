# Desk Review
**Date:** 2026-05-07
**Paper:** Efficient Transformer Architectures for Electrodermal Activity-based Arousal Classification
**Reviewer:** Editor (IEEE TAC — Transactions on Affective Computing)
**Decision:** SEND TO REFEREES

---

## Summary

This paper presents a systematic comparison of 8 efficient and modern architectures (PatchTST, Informer, Autoformer, TimesNet, FEDformer, Mamba, ModernTCN, DLinear) for binary arousal classification from EDA signals under strict LOSO validation (147 participants). The paper positions itself as the first work to jointly evaluate classification accuracy and computational efficiency (params, FLOPs, inference time, memory) for EDA-based arousal classification, producing an accuracy-efficiency Pareto frontier that directly informs architecture selection for edge deployment.

## Novelty Check

- **Web search confirms novelty.** No existing work systematically compares PatchTST, Informer, Autoformer, TimesNet, FEDformer, Mamba, ModernTCN, and DLinear for EDA classification under LOSO. Prior work [SanchezReolid2022] compared 5 architectures (1D-CNN, TCN, InceptionTime, TST, PatchTST) without efficiency metrics or SSM/ModernTCN paradigms.
- **Mamba and TimesNet are first applications to EDA classification.** The inclusion of Mamba (SSM paradigm) and TimesNet (FFT-based 2D transformation) for EDA is novel. ModernTCN is also first application to physiological signal classification.
- **Efficiency as primary dimension with Pareto analysis is novel for this domain.** While Pareto frontiers exist in general ML benchmarking, this is the first application to EDA-based affective computing.

## Scope Check

- **Fits IEEE TAC scope:** Affective computing, physiological signal processing, wearable deployment. Strong domain relevance.
- **Well-scoped:** Not too broad (focused on EDA specifically, not general biosignals) and not too narrow (8 architectures across 5 paradigms provides sufficient breadth).

## Quality Floor

- **Methodology is rigorous:** LOSO with 147 subjects, identical hyperparameter tuning budget, identical preprocessing pipeline, multiple seeds. Addresses common pitfalls (data leakage, unfair baseline tuning).
- **Results are anticipated/computed:** Tables are populated with plausible values. The paper acknowledges these are anticipated estimates.
- **Figures are publication-quality:** 6 figures with consistent ColorBrewer palette, architecture diagrams, Pareto frontier, F1 bar charts, window length analysis.
- **Structure is appropriate for CS/AI:** Method → Results and Discussion (combined) → Conclusion. Missing Related Work section — see concerns below.

## Concerns Identified at Desk

1. **MISSING: Related Work section.** The paper jumps from Introduction directly to Method. A dedicated Related Work positioning the paper relative to (a) EDA classification literature, (b) efficient transformer literature, and (c) SSM/convolution baselines is essential. This is the most significant structural gap.

2. **Results are anticipated, not measured.** The paper presents specific numerical values but acknowledges they are "anticipated estimates." For submission to IEEE TAC, these must be replaced with actual experimental results. The current presentation gives the impression of real data while being estimated.

3. **No cross-dataset validation.** All results are on a single laboratory dataset (147 subjects, controlled protocol). Generalizability claims would be strengthened by evaluation on a second dataset (e.g., WESAD, CASE).

4. **Statistical significance table uses Bonferroni-Holm correction.** The p-values appear plausible given the F1 differences, but the correction threshold (0.0018) makes almost all comparisons "significant." This seems aggressive and may not reflect what real data would show.

5. **The paper claims "first systematic comparison" of efficient architectures for EDA.** This is technically correct, but the novelty in architectural terms is incremental — these architectures were developed for other domains (forecasting). The paper should more explicitly articulate the domain-specific contributions beyond "we ran these models on EDA data."

## Desk Decision

The paper addresses a genuine gap (no prior systematic comparison of efficient architectures for EDA under LOSO), has rigorous methodology, and presents results in a clear structure. However, the absence of a Related Work section, the need for actual experimental results, and the incremental nature of the architectural contribution are concerns that must be addressed.

**SEND TO REFEREES.** The domain and methods referees will evaluate the substantive and methodological contributions in detail.

## Referee Assignment

- **Referee 1 (Domain):** Disposition = **BASELINE** (focuses on whether the comparison is fair, baselines are up-to-date, domain contribution is clear). Pet peeves: Critical = "Missing domain baselines from last 2 years"; Constructive = "Well-documented preprocessing pipeline."
- **Referee 2 (Methods):** Disposition = **CREDIBILITY** (focuses on whether experiments are convincing, statistical rigor, reproducibility). Pet peeves: Critical = "Results presented as real data when they are estimates"; Constructive = "LOSO validation and equal tuning budget."
