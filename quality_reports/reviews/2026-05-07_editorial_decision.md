# Editorial Decision
**Date:** 2026-05-07
**Paper:** Efficient Transformer Architectures for Electrodermal Activity-based Arousal Classification
**Venue:** IEEE Transactions on Affective Computing (TAC)
**Decision:** **MAJOR REVISIONS**

---

## Summary

This paper presents the first systematic comparison of 8 efficient and modern architectures — spanning Transformers, state space models, and modern convolutions — for EDA-based arousal classification under strict LOSO validation. The reviewers and editor agree that the paper addresses a genuine gap, employs rigorous methodology, and provides actionable deployment guidance through the accuracy-efficiency Pareto frontier. However, significant issues must be resolved before the paper meets the publication bar for IEEE TAC.

Both referees independently identified concerns about the presentation of anticipated results as real data, the absence of a Related Work section, and statistical analysis clarity. The domain referee further noted weak literature positioning and single-dataset generalizability. The methods referee identified specific methodological clarifications needed for reproducibility.

---

## Referee Disagreements

**None.** Both referees independently converged on similar major concerns despite different dispositions (BASELINE vs. CREDIBILITY). This agreement strengthens the editorial assessment that these issues are genuine and must be addressed.

---

## MUST Address (Blocking for Acceptance)

### M1. Replace anticipated results with experimental data OR clearly mark as estimates
**FATAL — both referees.** The paper currently presents specific numerical values (Tables 2-4, Figures 3, 5, 6) that appear to be real experimental results. Both referees independently identified this as a credibility concern. Authors must either: (a) complete the experiments and report measured values, or (b) remove all specific values and replace with "[TBD]" placeholders, clearly marking the paper as a methodology proposal pending experimental validation.

### M2. Add a Related Work section
**FATAL — domain referee.** The paper lacks a dedicated Related Work section. This is a structural requirement for IEEE TAC. The section should cover: (a) EDA-based arousal classification methods, (b) efficient architectures for time series (positioning PatchTST, Informer, Autoformer, TimesNet, FEDformer), (c) SSM and modern convolution for biosignals (Mamba, ModernTCN), and (d) prior benchmarking/comparison studies in affective computing.

### M3. Clarify statistical significance framework
**FATAL — methods referee.** The paper uses inconsistent significance thresholds. Table 4 applies Bonferroni-Holm correction (α = 0.0018) while the Results text references raw α = 0.05 (calling p = 0.048 "non-significant"). Authors must: (a) choose and state a single primary threshold, (b) apply it consistently throughout the paper, and (c) adjust all claims about statistical significance accordingly.

### M4. Reduce self-citation density and broaden literature positioning
**ADDRESSABLE — domain referee.** The paper cites the authors' prior work [13] 8+ times while missing key EDA and affective computing references. Broaden the citation base to include seminal EDA papers and recent work from other groups.

---

## SHOULD Address (Expected for Acceptance)

### S1. Improve generalizability discussion
Add a paragraph acknowledging that single-dataset evaluation limits generalizability. If cross-dataset evaluation is not feasible for this submission, clearly state this as a limitation and outline planned validation.

### S2. Specify hyperparameter search methodology
Add explicit details: search method (grid/random/Bayesian), number of trials per architecture, validation protocol for hyperparameter selection.

### S3. Report per-class metrics
Include per-class F1 scores in addition to macro-averaged metrics. This is standard practice in affective computing where class balance may vary.

### S4. Clarify memory measurement methodology
Specify what is included in peak memory measurement (weights only, weights + activations, total framework memory).

### S5. Add training time as efficiency metric
Inference time captures deployment cost; training time is relevant for reproducibility and practical adoption.

---

## MAY Address (Non-blocking Suggestions)

- Consider adding a second dataset (WESAD) for cross-dataset validation in a future revision.
- Add confidence intervals alongside standard deviations in the main results table.
- Discuss the overlap in training sets across LOSO folds as a potential limitation of the Wilcoxon test.
- Add Mamba and DLinear to the window length analysis figure if real data becomes available.

---

## Decision Rationale

The paper has strong bones: a rigorous evaluation protocol (LOSO, equal tuning budget), a novel comparison of 8 architectures spanning 5 paradigms, and a compelling deployment-focused framing through the Pareto frontier. The joint accuracy-efficiency evaluation directly serves the wearable affective computing community.

However, the presentation of anticipated results as real data and the absence of a Related Work section are structural issues that prevent acceptance in the current form. The statistical analysis ambiguity further undermines the paper's key claim (Mamba ≈ PatchTST at lower cost). These issues are addressable with a major revision.

**MAJOR REVISIONS.** Authors are encouraged to resubmit after addressing MUST items M1-M4 and SHOULD items S1-S5.

---

## Revision Timeline

Expected revision effort: 4-8 weeks (assuming experiments are in progress). Priority: M1 (experiments or explicit marking) > M2 (Related Work section) > M3 (statistical clarity) > M4 (citation breadth).
