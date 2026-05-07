# Domain Referee Report
**Date:** 2026-05-07
**Paper:** Efficient Transformer Architectures for Electrodermal Activity-based Arousal Classification
**Field:** Affective Computing / Biomedical AI / Time-Series Deep Learning
**Referee:** Domain Expert (Disposition: BASELINE)
**Recommendation:** Major Revisions
**Overall Score:** 72/100

---

## Summary

This paper compares 8 architectures for EDA-based arousal classification under LOSO. The work is positioned as the first systematic comparison of efficient architectures for this task, adding Mamba, TimesNet, and ModernTCN to the authors' prior evaluation [13]. The inclusion of efficiency metrics and a Pareto frontier analysis is a valuable contribution that directly addresses practical deployment concerns. However, the paper has significant gaps in literature positioning, domain justification, and the framing of its contribution that must be addressed before it meets the bar for publication in this venue.

---

## Dimension Scores

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Contribution & Novelty | 30% | 65 | Incremental extension of prior work; SSM/2D paradigms are new for EDA but architectures not novel |
| Literature Positioning | 25% | 55 | Missing Related Work section; sparse citation of EDA-specific literature beyond authors' own work |
| Substantive Arguments | 20% | 75 | Good deployment-focused narrative; Pareto analysis is compelling; physiological interpretation is solid |
| External Validity | 15% | 70 | Single dataset limits generalizability; LOSO is rigorous but within-dataset only |
| Venue Fit | 10% | 85 | Strong fit for IEEE TAC; addresses practical deployment question in affective computing |
| **Weighted** | 100% | **72** | |

---

## Major Comments

### 1. Missing Related Work section (CRITICAL)

The paper jumps from Introduction directly to Method without a Related Work section. This is a fundamental structural gap. The reader needs to understand:
- What prior work exists on EDA-based arousal classification (beyond the authors' own [13])
- How efficient transformer variants have been applied to physiological signals
- Where Mamba/SSM and TimesNet fit in the biosignal classification landscape
- Why existing comparisons are inadequate (the paper mentions this in passing in the Intro but doesn't substantiate)

**What would change my mind:** Add a dedicated Related Work section (500-800 words) organized by topic: (a) EDA-based arousal classification, (b) efficient architectures for time series, (c) SSM and modern convolution for biosignals. Position the current work explicitly against the closest 3-5 papers.

### 2. Over-reliance on authors' own prior work

The introduction and methodology sections cite [13] (SanchezReolid2022) 8+ times as the primary reference point. While building on prior work is appropriate, the paper reads as "our previous paper + 3 new models" rather than an independent contribution to the literature. Key domain papers that should be cited and discussed:
- Posada-Quintero & Chon (2020) on EDA-based emotion recognition
- Schmidt et al. (2018) on WESAD as benchmark
- Picard et al. on affective computing foundations
- Tsirmpas et al. (2025) on Transformer-based EDA decomposition

**What would change my mind:** Position the paper relative to the broader EDA/affective computing literature, not just the authors' prior work. Reduce self-citation density in the introduction.

### 3. Incremental architectural contribution

The paper claims "first systematic comparison" but this is an extension, not a new paradigm. The architectures were developed for forecasting. The paper's contribution is in evaluation methodology and deployment analysis, not architectural innovation. The introduction should frame contributions accordingly.

**What would change my mind:** Rephrase contributions to emphasize (i) the evaluation methodology — first systematic efficiency-accuracy assessment for EDA under LOSO, (ii) the Pareto frontier as a decision tool for deployment, and (iii) domain-specific insights about which paradigms work for EDA. De-emphasize "novel architecture" language.

### 4. Single dataset limits generalizability claims

All experiments use a single laboratory dataset (147 subjects, controlled audiovisual stimuli). The paper claims the Pareto frontier "directly informs architecture selection for edge deployment" but cannot demonstrate that the rankings generalize to other EDA datasets or real-world conditions. 

**What would change my mind:** Either (a) add a cross-dataset evaluation on a public dataset (WESAD, CASE), or (b) explicitly qualify generalizability claims, acknowledging that cross-dataset validation is future work.

### 5. Missing WESAD and public benchmark context

The paper uses a proprietary dataset. While this is acceptable, the absence of discussion about how these architectures would perform on standard benchmarks (WESAD, CASE, DEAP) limits the paper's practical impact. At minimum, the related work should discuss why existing benchmarks were not used and what the implications are for comparability.

---

## Minor Comments

6. The term "Materials and Methods" was used in the reference paper but is atypical for CS/AI venues. The current "Method" section is appropriate.

7. DLinear as a "sanity check" is well-motivated, but the paper should also discuss what specific finding from DLinear would validate vs. invalidate the necessity of attention mechanisms for EDA.

8. The window length analysis (Fig. 6) is an important complement to prior work [13] but could benefit from physiological interpretation: at what window length does a complete SCR waveform become available? How does this relate to the performance plateau?

---

## Missing Literature

- Posada-Quintero, H.F. & Chon, K.H. "Phasic Electrodermal Activity Signal Processing for Emotion Recognition." (2020 or similar EDA review)
- Picard, R.W. "Affective Computing" — foundational reference
- Additional EDA-specific deep learning papers beyond the authors' group
- Recent survey on transformers for time series (Wen et al., 2023, already cited — good)
- A survey specifically on lightweight/efficient architectures for biosignals

---

## Questions for the Authors

1. Why was WESAD not included as a validation dataset? The public availability would strengthen reproducibility and generalizability claims.

2. The p-values in Table 4 suggest almost all pairwise comparisons are significant after Bonferroni-Holm correction. Given the small effect sizes (e.g., ΔF1 = 0.005 between Mamba and PatchTST), is this realistic for 147 folds?

3. How do you envision practitioners using Figure 3 (Pareto frontier)? Is the intent to select an architecture pre-deployment or to inform hardware-software co-design?
