# Methods Referee Report (Round 3)
**Date:** 2026-05-08
**Venue:** Biomedical Signal Processing and Control (BSPC)
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification
**Paper type:** Comparative Benchmark
**Referee:** Methods Expert (CREDIBILITY disposition)
**Recommendation:** Minor Revision → Accept
**Overall Score:** 82/100

---

## Summary

The manuscript has improved substantially over three review rounds. The three critical concerns from Round 1 — absence of classical signal processing baselines, lack of preprocessing justification, and internal statistical contradictions — are now resolved. The addition of the handcrafted EDA features + SVM baseline (F1 ≈ 0.81) anchors the deep learning gains against a conventional BSPC reference point, and the convergence insight that classical features, linear decomposition, and simple convolutions all saturate around F1 ≈ 0.80 is a genuinely valuable finding. The paper now reads as a biomedical signal processing contribution that happens to use modern architectures, rather than an ML benchmark with EDA data.

Seven residual methodological concerns remain, all of which are moderate in severity and well-acknowledged by the authors. None threatens the paper's central findings, but each represents an opportunity to strengthen the contribution before final acceptance.

---

## Dimension Scores

| Dimension | Weight | R2 Score | R3 Score | Δ | Notes |
|-----------|--------|----------|----------|---|-------|
| Fairness of Comparison | 30% | 75 | 78 | +3 | Equal tuning budget across candidate architectures (64 each) is solid. Prior-work baselines (1D-CNN, TCN, InceptionTime, TST) remain at 24-configuration budget — this is now transparently disclosed but not remedied. Single-seed training unresolved. |
| Baseline Selection | 20% | 82 | 85 | +3 | Classical SVM + handcrafted features now anchors the deep learning results. cvxEDA and Ledalab decomposition alternatives discussed. Four BSPC journal papers added. The gap remains: no threshold-based SCR detector or classical frequency-domain baseline. |
| Evaluation Completeness | 20% | 78 | 80 | +2 | Five classification + five efficiency metrics. Per-class F1, channel ablation, and window-length analysis in supplementary. Pareto frontier is the paper's strongest contribution. Artifact-robustness experiment still absent; confusion matrices and calibration error not reported. |
| Statistical Rigor | 15% | 78 | 82 | +4 | Wilcoxon + Bonferroni-Holm framework correct. p-value contradiction resolved. Effect sizes reported alongside p-values. LOSO independence violation now candidly discussed — but no cluster-robust alternative offered. Seed specification still absent. |
| Analysis & Insights | 15% | 85 | 87 | +2 | Channel ablation insight (inverse relationship between architecture capacity and derivative benefit) is novel and well-supported. Pareto frontier characterisation is actionable. Classical/DLinear/CNN convergence narrative is elegant. Window-length analysis covers all 8 architectures. |
| **Weighted** | 100% | **80** | **82** | **+2** | |

---

## Sanity Check Results

| Check | Result | Detail |
|-------|--------|--------|
| Baseline consistency | **QUALIFIED PASS** | Classical SVM baseline is a retrospective comparison (F1 ≈ 0.81 from Sanchez-Reolid 2020 IJNS). Not evaluated by the authors themselves under the current preprocessing pipeline — cited from prior work with the "identical dataset." The representative value ("at 40 s window") is stated but the original study evaluated varying window lengths; whether 40 s was the optimal window for the SVM is unclear. The F1 range of 0.80–0.83 is broad enough that precise anchoring to 0.81 may slightly over- or under-represent the classical pipeline's capability. |
| Performance plausibility | **PASS** | F1 range (0.800–0.863) under strict LOSO with 147 subjects and 40s windows is plausible. The 0.05–0.06 pp gap between classical/DLinear tier and the best Transformer/SSM architectures aligns with expected gains from global temporal modelling. The hierarchy (SSM/attention > frequency > convolution > linear) is consistent with known paradigm capabilities. |
| Tuning budget equal | **QUALIFIED PASS** | 64 configurations per candidate architecture is stated and appears equitable. However, the search space cardinalities differ substantially (PatchTST ≈768 combinations vs DLinear ≈320), meaning 64 trials explore ~8% vs ~20% of each space respectively. This is inherent to grid search with heterogeneous parameter spaces but should be explicitly noted. The prior-work baselines (1D-CNN, TCN, InceptionTime, TST) were tuned with only 24 configurations and were NOT re-evaluated in this study. |
| Deployment metrics measured on real hardware | **CONCERN** | Inference times measured on Quadro P5000 (Pascal, 2560 CUDA cores) — a workstation GPU. The deployment tier labels have been corrected to "low/mid/high-latency GPU" with an explicit caveat that "absolute latency on embedded hardware will differ substantially." This is honest. However, 1,000-forward-pass averaging on a specific GPU provides no information about variance in inference time (important for real-time applications) and no deployment-class hardware benchmark exists (Jetson, Cortex-M, mobile SoC). |
| Model convergence | **CONCERN** | Epochs-to-convergence reported as single integers (32, 45, 58, etc.) in Supplementary Table S4. These are presumably averages across 147 folds, but no standard deviation is reported. It is improbable that all 147 folds converged in exactly the same number of epochs. Whether any folds failed to converge, exhibited loss divergence, or required gradient-clipping rescue is undisclosed. |

---

## Major Comments

### 1. Artifact Robustness Remains Untested (MODERATE)

The paper acknowledges that EDA signals are susceptible to motion artefacts and electrode noise (citing Hossain2022BSPC), that the laboratory dataset minimises these, and that this limits translational value. The FEDformer discussion (Section 2.3.4) speculates that "sparse Fourier mode selection provides implicit denoising" — but this claim is never tested. Similarly, Mamba's selective state-space mechanism is posited to filter content-adaptively. For a BSPC benchmark paper, evaluating architectures only on clean laboratory data limits the practical deployment guidance that the paper's own framing (Section 1, paragraphs 5–6) promises.

This concern has been raised in every review round and remains the single largest gap between the paper's stated ambition (deployment guidance for resource-constrained, real-world settings) and its experimental evidence.

- **What would change my mind:** A synthetic noise-injection experiment. Inject white Gaussian noise at 3–4 SNR levels (e.g., 20, 10, 5, 0 dB) into the test-set signals, then report F1 degradation curves for all 8 architectures. Additionally, inject 2–3 transient motion-artefact perturbations (high-amplitude square-wave pulses spanning 0.5–2 s at random positions) and measure the resulting performance drop. This experiment requires no new data collection, can be implemented in < 50 lines of Python, and would directly validate/refute the denoising claims made for FEDformer and Mamba. Even reporting this for the top 4 architectures (Mamba, PatchTST, TimesNet, FEDformer) would substantially strengthen the BSPC contribution.

### 2. Prior-Work Baselines Not Re-Tuned (MODERATE)

Table 2 places prior-work architectures (1D-CNN, TCN, InceptionTime, TST) from Sanchez-Reolid 2022 alongside the eight candidate architectures evaluated here. The prior-work models were tuned with 24 configurations; the new models with 64 — a 2.7× tuning budget advantage. The table note discloses the PatchTST discrepancy (0.852 → 0.863 due to expanded budget + Δ²SCR channel), but the systematic advantage for the new architectures over the old ones is not explicitly acknowledged.

This matters because the paper's narrative rests on the claim that the new efficient architectures "narrow the performance gap" relative to PatchTST. But if the prior baselines (1D-CNN, TCN, etc.) were similarly given 64 configurations, they might also close part of that gap, potentially weakening the apparent advantage of ModernTCN or FEDformer over TCN/InceptionTime.

The practical solution — re-running the top 2–3 prior baselines with the full 64-configuration budget — was recommended in R1 but not implemented. I recognise this is computationally expensive (~100 GPU-hours for PatchTST alone), but it is the only way to establish a truly level comparison.

- **What would change my mind:** At minimum, a sensitivity analysis showing that the relative ordering of ALL architectures is preserved when the search is restricted to 24 random configurations drawn from the 64-configuration grid. This would cost nothing computationally (subsample existing results) and would demonstrate that the 64→24 budget reduction does not rearrange the Pareto frontier. Alternatively, re-run the strongest prior baseline (TST, F1 = 0.840) with the 64-configuration budget and identical preprocessing (including Δ²SCR), and report the result.

### 3. Single-Seed Training and Per-Fold Convergence (MODERATE)

The paper reports performance as mean ± std across 147 LOSO folds. It does not state whether a single random seed was used for initialisation and data ordering. If one seed was used, the reported standard deviations conflate fold-to-fold subject variability with the particular random initialisation for that seed. This is especially relevant because:
- Deep networks trained on small per-fold datasets (146 subjects, 20% held out for validation, leaving ~117 training subjects per fold) can exhibit non-trivial seed-to-seed variability.
- The supplementary material reports epochs-to-convergence as single integers with no standard deviation. The probability that all 147 folds of a 12.3 ms/epoch Mamba model "converged" in exactly 58 epochs each is near-zero if early stopping with patience=15 is applied independently per fold.

- **What would change my mind:** (a) Explicitly state the number of random seeds used. If 1, add a sensitivity note acknowledging that fold-wise standard deviations may partially reflect seed-dependent initialisation. If ≥3, state this and confirm that per-fold means were averaged across seeds before computing across-fold statistics. (b) Report epochs-to-convergence as mean ± std across folds. In Supplementary Table S4, change "58" to "58 ± 12" or whatever the data show. (c) Document the number of folds (out of 147) in which each architecture failed to improve beyond random baseline (F1 ≈ 0.50), exhibited NaN gradients, or was rescued by gradient clipping.

### 4. Classical Baseline Comparison Is Retrospective (MODERATE)

The classical signal processing baseline (handcrafted EDA features + SVM, F1 ≈ 0.81) is a retrospective citation from Sanchez-Reolid 2020 (IJNS). This is not a direct experimental comparison — the SVM was not re-evaluated by the current authors under the current pipeline. The table note (††) states the F1 represents "the range of 0.80–0.83 across varying window lengths" with a "representative value" shown at 40 s. Several concerns:

- It is unclear whether the SVM's feature set overlaps with information encoded in the three-channel input (SCR, ΔSCR, Δ²SCR). If the handcrafted features already included derivative-like features (rise time, velocity), the comparison to DLinear (F1 = 0.800) may be more of a tie than the paper implies.
- The SVM's LOSO protocol is cited as "subject-independent" but the original paper's exact fold construction may differ from the current study.
- The note states "per-fold standard deviations are not available for this retrospective comparison" — this means the SVM's variability cannot be compared to the (reported) standard deviations of the DL architectures.

- **What would change my mind:** Re-implement the handcrafted feature extraction (8–10 features: mean SCR, peak count, mean rise time, AUC, NS-SCR frequency, spectral power in 0.2–0.5 Hz band, etc.) from the phasic SCR signal output by the current preprocessing pipeline, train an SVM and Random Forest under the identical 147-fold LOSO protocol, and report F1 with mean ± std. This would convert a retrospective citation into a direct experimental comparison and would take approximately 1–2 hours of computation (SVM training is fast). The paper already has access to the dataset and preprocessing pipeline — this is a low-cost, high-impact addition.

### 5. Wilcoxon Signed-Rank Violation: Acknowledged but Not Remedied (MINOR)

The paper properly acknowledges (Section 3.7, lines 743–748) that LOSO folds with 146/147 overlapping training subjects violate the independence assumption of Wilcoxon signed-rank tests. The transparency is appreciated. However, the guidance that "readers apply their preferred interpretation" effectively delegates statistical judgment to the reader rather than providing a robust alternative.

The central comparison — PatchTST vs. Mamba (p = 0.048 at conventional α, not surviving Bonferroni-Holm) — is a borderline result that the paper uses to drive its primary conclusion ("Mamba provides near-equivalent accuracy at substantially lower cost"). If the p-value is inflated by fold overlap (as the independence violation would suggest), the true Type I error rate may be higher than 0.05, making the PatchTST-vs-Mamba comparison even less significant than reported.

- **What would change my mind:** For the key PatchTST-vs-Mamba comparison only, report the result of a cluster-robust bootstrap (resampling subjects, not folds, with replacement; computing the mean F1 difference across the bootstrapped sample; reporting the 95% CI and empirical p-value). This is computationally trivial (no model retraining needed — just resample the 147-fold F1 vectors). Alternatively, fit a linear mixed-effects model with architecture as a fixed effect and subject as a random intercept, and report the architecture contrast with its 95% CI. Either approach would close this acknowledged gap and substantially strengthen the statistical narrative.

### 6. Embedded Hardware Benchmarks Required for Deployment Claims (MINOR)

The deployment tier labels are now correctly qualified as GPU-relative ("low/mid/high-latency GPU"). The caveat that "absolute latency on embedded hardware will differ substantially" is present. However, a paper whose central contribution is deployment guidance under resource constraints — with explicit reference to "wearable and edge deployment" (line 626) and "smartwatch" (line 628) — should provide at least one data point on deployment-class hardware.

The concern is not about label accuracy (that has been fixed) but about the paper's practical utility for the BSPC audience. A clinician or biomedical engineer reading this paper wants to know: "Can I run Mamba on a Raspberry Pi? On a smartphone? On a wearable microcontroller?" The paper currently answers "Mamba takes 1.5 ms on a Quadro P5000" — a GPU nobody deploys in a wearable.

- **What would change my mind:** Add inference-time benchmarks for the top 3 Pareto-optimal architectures (Mamba, ModernTCN, DLinear) on one deployment-class platform — either an NVIDIA Jetson Orin Nano (representing edge GPU), a Raspberry Pi 5 with ONNX Runtime (representing CPU deployment), or an ARM Cortex-M4 via TensorFlow Lite Micro. Even relative latency (e.g., "Mamba is X× slower than DLinear on a Raspberry Pi 5, consistent with the GPU-relative ordering") would validate the Pareto frontier's portability across hardware classes. If hardware access is the constraint, at minimum add a theoretical analysis: estimate inference time on a target platform using the ratio of FLOPs to the platform's peak GFLOPS, adjusted for memory bandwidth.

---

## Minor Comments

7. **Confusion matrices absent.** The paper reports per-class F1 (supplementary Table S3) but no confusion matrices. For binary arousal classification, a single aggregated confusion matrix for the top 2 architectures would reveal whether errors are symmetric (equal misclassification of calm→stress and stress→calm) or concentrated in one direction. The supplementary notes a "stress-class advantage" (+0.8 pp) but confusion matrices would make this directly interpretable.

8. **No calibration analysis.** A model with F1 = 0.86 but expected calibration error (ECE) > 0.15 produces probability estimates that are unreliable for decision support. Since the paper positions arousal classification for "mental health monitoring" and "biofeedback" applications, calibrated probabilities are important. Computing ECE from saved logits requires no additional experimentation. **What would change my mind:** Report ECE for all architectures in the supplementary material.

9. **Optimal hyperparameters not disclosed anywhere.** The paper states a grid search over 64 configurations per architecture was conducted, and that efficiency metrics were measured using the optimal configuration. The selected hyperparameters (number of layers, embedding dimension, attention heads, etc.) for each architecture are not reported — not in the main text, not in the supplementary. This impedes reproducibility and prevents practitioners from directly deploying the recommended configurations. **What would change my mind:** Add a table to the supplementary listing the selected hyperparameter values for each architecture (at minimum for the Pareto-optimal ones: DLinear, ModernTCN, Mamba, TimesNet, PatchTST).

10. **FLOPs measurement via thop — version and caveats.** The paper reports FLOPs via the `thop` library. The specific version number is not provided. Additionally, `thop` counts operations from the PyTorch computational graph, which may differ from actual hardware-executed operations due to operator fusion (especially relevant for Mamba's hardware-aware scan, which is implemented as a custom CUDA kernel). The paper's own limitations section (line 745) acknowledges this but does not note that Mamba's FLOPs may be particularly affected by the `thop` counting methodology. **What would change my mind:** Add the thop version number and a one-sentence note that Mamba's FLOPs estimate via `thop` may be approximate due to custom CUDA kernel operations.

11. **Window-length curves: interpolation concern.** Figure 7 plots F1-vs-window-length for all architectures as smooth curves with only 12–17 evaluation points. The caption states "Curves are evaluated at selected window lengths (1–15, 20, 25, 30, 35, 40 s)." Drawn as connected lines, these curves imply linear interpolation between evaluation points. The caption should clarify that lines are linear interpolants between evaluated points, and ideally the evaluation points themselves should be marked with dots.

12. **Derivative computation method unspecified.** The paper states (line 94) that "two derivative channels were computed from the phasic signal: the first temporal derivative (ΔSCR) and the second temporal derivative (Δ²SCR)." At 4 Hz sampling, simple finite differences (e.g., forward difference: x[t+1] – x[t]) amplify noise by approximately √2 per differentiation. Whether smoothing was applied before or after differentiation, and whether central/forward/backward differences or Savitzky-Golay filtering was used, materially affects the resulting derivative signals. **What would change my mind:** Add one sentence specifying the differentiation method and any smoothing applied.

---

## Revised Scoring Summary (Round 3 vs Round 2)

| Dimension | Weight | R2 | R3 | Key Driver of Change |
|-----------|--------|-----|-----|---------------------|
| Fairness of Comparison | 30% | 75 | 78 | Transparent disclosure of tuning budget differences; remaining prior-work and single-seed issues well-documented |
| Baseline Selection | 20% | 82 | 85 | Classical baseline now anchors results; BSPC positioning improved; threshold-based detector still absent |
| Evaluation Completeness | 20% | 78 | 80 | Per-class F1 and channel ablation in supplementary; artifact robustness missing but honestly acknowledged |
| Statistical Rigor | 15% | 78 | 82 | p-value corrected; Wilcoxon independence violation disclosed; seed issue remains |
| Analysis & Insights | 15% | 85 | 87 | Channel ablation insight strengthened; classical/DLinear convergence narrative compelling; Pareto frontier actionable |
| **Weighted** | | **80** | **82** | |

---

## Overall Assessment

The manuscript now meets the methodological bar for BSPC with minor remaining issues. The classical baseline anchors the deep learning contribution against a conventional signal processing reference point. The Pareto frontier analysis and channel ablation insights are the paper's strongest contributions. The remaining concerns (artifact robustness, prior-work re-tuning, convergence reporting, embedded benchmarks) are well-understood by the authors and acknowledged in the limitations section. None threatens the paper's central findings, but each would strengthen the contribution.

**Recommendation:** Minor Revision. The authors should address items 1 (artifact experiment), 2 (prior-work tuning sensitivity), and 3 (seed/convergence reporting) before final acceptance. Items 4–6 are recommended but not blocking. Items 7–12 are cosmetic.

The paper has improved meaningfully across three rounds and is close to publishable quality for BSPC.
