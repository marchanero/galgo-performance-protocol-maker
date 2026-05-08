# Editorial Decision — BSPC Peer Review
**Date:** 2026-05-08
**Venue:** Biomedical Signal Processing and Control (BSPC)
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification
**Decision:** **Major Revision**

---

## Summary

This paper benchmarks eight DL architectures across five paradigms for EDA-based arousal classification under LOSO (147 participants). All three referees agree the work is methodologically sound and the Pareto frontier analysis is genuinely useful. However, both domain and methods referees identify a critical shared concern: the absence of classical EDA signal processing baselines (handcrafted features + SVM/RF, threshold-based SCR detection) against which to contextualise the DL performance gains. The consistency referee identifies two internal contradictions (p-value misstatement, deployment tier boundary) that are factual errors. The paper needs three categories of revision: (i) add classical baselines, (ii) justify preprocessing choices with EDA signal theory, and (iii) correct the statistical and deployment inconsistencies.

---

## Referee Scores

| Referee | Disposition | Score | Recommendation |
|---------|------------|-------|---------------|
| Domain Expert | ARCHITECTURE | 66/100 | Major Revision |
| Methods Expert | CREDIBILITY | 65/100 | Major Revision |
| Consistency | SKEPTIC | 72/100 | Major Revision |
| **Average** | | **68/100** | **Major Revision** |

---

## Consensus Concerns (Shared Across Referees)

### 1. No Classical EDA Signal Processing Baselines (CRITICAL — Domain + Methods)

Both the domain referee and methods referee independently identify the same gap: the paper benchmarks eight DL architectures against only other DL architectures. No traditional biomedical signal processing approach is included.

**Required:**
- Add a feature-engineering baseline: extract SCR features (amplitude, rise time, AUC, NS-SCR frequency, peak count) per 40s window following Boucsein (2012) / SPR guidelines, then train SVM/RF under the identical LOSO protocol
- Report results alongside Table 2
- If classical baseline achieves F1 > 0.75, reframe DL contribution; if F1 < 0.70, the DL advantage is validated

### 2. Preprocessing Pipeline Lacks Explicit Physiological Justification (CRITICAL — Domain + Methods)

The preprocessing steps (FIR filter at 4 Hz, Gaussian smoothing, CDA, derivative channels) are described but not motivated by EDA signal theory or SNS physiology.

**Required in Section 2.2:**
- Justify the 4 Hz FIR cutoff given the 2 Hz Nyquist bound and EDA spectral power below 1 Hz
- Specify Gaussian sigma and the noise source it targets
- Justify CDA vs. cvxEDA (Greco 2016) and Ledalab (Benedek 2010), both now cited in the text
- Clarify how derivatives are computed at 4 Hz sampling (finite differences amplify noise)
- Mention EDA vulnerability to artifacts (Hossain2022BSPC, now cited)

### 3. Internal Contradictions Corrected ✓ (Consistency Referee)

Two factual errors were identified and have been corrected during this review cycle:

| Issue | Location | Fix Applied |
|-------|----------|-------------|
| p-value misstatement: "is not statistically significant ($p = 0.048$)" | Line 621-622 (Pareto section) | Changed to "is statistically significant at $\alpha = 0.05$ ($p = 0.048$) but does not survive Bonferroni-Holm correction" |
| Mamba deployment tier: $t_{\text{inf}} < 1.5$ ms excluded Mamba (1.5 ms) | Line 619 + Fig 6 caption | Changed to $\leq 1.5$ ms uniformly |

---

## Architecture-Specific Concerns (Domain Referee)

### 4. Interpretability Claims Need Quantitative Support (Section 3.6)
- Attention "concentration on SCR onset" — no heatmaps or quantitative onset-phase attention ratios shown
- TimesNet periods "2–5 s" — no distribution histogram across folds
- Mamba state transition matrices — promised in Methods, not delivered in Results

### 5. Channel Ablation Claim Needs Stronger Evidence
The claim that SSMs "implicitly learn derivative information" could be a ceiling effect (SSMs already perform better on raw SCR). Suggested fix: linear probe analysis predicting $\Delta$SCR from internal representations.

---

## Methods-Specific Concerns

### 6. No Robustness to Signal Quality Degradation
EDA is noise-sensitive. No artifact injection experiment, no SNR degradation curves. FEDformer's "implicit denoising" claim is untested. BSPC audience expects this.

**Suggested:** Inject synthetic white noise at 20/10/0 dB SNR and motion artifact transients; report F1 degradation curves.

### 7. Deployment Thresholds Defined on Wrong Hardware Class
Wearable/microcontroller labels based on Quadro P5000 (workstation GPU) benchmarks. The same model would run 50-500× slower on actual embedded hardware. Either re-label tiers to GPU-relative names or benchmark on embedded target.

---

## Minor Issues (Consistency Referee)

- Sliding vs non-overlapping offset: +0.004 claimed, actual mean = +0.0031 (line 705)
- "approximately 100 GPU-hours" vs supplementary "over 100 GPU-hours" (minor inconsistency)
- Window-length curves subsampled (not every integer second 1–40 shown) — note in caption
- Four-fold repetition of "first systematic comparison" — stylistically excessive
- Mamba state transition analysis promised in Methods but not delivered in Results
- Per-fold optimal hyperparameters not disclosed (reproducibility concern)
- Participant demographics beyond age missing (sex distribution needed)
- Stimulus details absent (type, number of trials, manipulation check)

---

## New References Added During This Review

The following references have been integrated into the manuscript during this review cycle:

**BSPC Journal (target venue):**
- Hossain2022BSPC — Motion artifact detection in EDA (cited in §2.2)
- Kasnesis2025BSPC — CNN-Transformer for PPG stress detection (cited in §1)
- Lee2025BSPC — Explainable DNN for stress with biosignals (cited in §1)
- Yaseen2026BSPC — Self-supervised transformers for stress (cited in §5)

**Classical EDA Signal Processing:**
- Greco2016 — cvxEDA (cited in §2.2)
- Benedek2010 — Ledalab (cited in §2.2)
- SPR2012EDA — EDA publication guidelines (cited in §2.2)
- Bach2010 — SCR modeling (added to bib)

---

## Required Changes (for Revision Submission)

| # | Change | Priority | Estimated effort |
|---|--------|----------|-----------------|
| 1 | Add classical EDA feature-engineering baseline (handcrafted SCR features + SVM/RF) under LOSO | MUST | 1-2 weeks |
| 2 | Expand §2.2 with physiological justification for each preprocessing step | MUST | 1-2 days |
| 3 | Reconcile Mamba deployment region (≤ 1.5ms threshold) — **ALREADY DONE** | MUST | ✓ |
| 4 | Correct p-value characterisation in Pareto section — **ALREADY DONE** | MUST | ✓ |
| 5 | Add signal-quality robustness experiment (synthetic noise/artifact injection) | SHOULD | 3-5 days |
| 6 | Provide quantitative support for interpretability claims or soften language | SHOULD | 2-3 days |
| 7 | Soften channel ablation inference about "implicit derivative learning" to differential benefit | SHOULD | 1 day |
| 8 | Re-label deployment tiers to GPU-relative names or add embedded benchmark point | SHOULD | 1 day or 1-2 weeks |
| 9 | Disclose per-fold optimal hyperparameters in supplementary | MAY | 1 day |
| 10 | Add stimulus details and participant demographics | MAY | 1 day |
| 11 | Reconcile sliding-window offset (+0.004 → +0.003) and GPU-hours estimates | MAY | 30 min |
| 12 | Note window-length curve subsampling in Figure 7 caption | MAY | 5 min |

---

## Editor's Note

The paper has a solid foundation — the Pareto frontier analysis and five-metric efficiency evaluation are genuinely useful contributions. However, for BSPC specifically, the current version reads as an ML benchmarking study that happens to use EDA, rather than a biomedical signal processing contribution that uses modern architectures. The principal revision needed is to engage with how EDA signals are classically processed: cite the EDA decomposition literature (now added), justify preprocessing choices physiologically, and — critically — add a classical signal processing baseline against which the DL gains can be assessed. Without this baseline, the reader cannot judge whether F1 = 0.80–0.86 represents a genuine advance over what a domain expert would achieve with feature engineering plus SVM.

The two internal contradictions flagged by the consistency referee (p-value, deployment tier) have been corrected. The remaining concerns are addressable within a major revision timeline. I look forward to receiving the revised manuscript.

---

**Dispositions assigned:** Domain-ARCHITECTURE, Methods-CREDIBILITY, Consistency-SKEPTIC.
**Review reports saved:**
- `quality_reports/reviews/2026-05-08_bspc_referee_domain.md`
- `quality_reports/reviews/2026-05-08_bspc_referee_methods.md`
- `quality_reports/reviews/2026-05-08_bspc_referee_consistency.md`
