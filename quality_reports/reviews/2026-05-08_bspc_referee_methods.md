# Methods Referee Report
**Date:** 2026-05-08
**Venue:** Biomedical Signal Processing and Control (BSPC)
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification
**Paper type:** Comparative Benchmark
**Disposition:** CREDIBILITY
**Calibrated to:** BSPC
**Recommendation:** Major Revision
**Overall Score:** 65/100

## Summary

This paper presents a systematic comparison of eight deep learning architectures (Transformers, SSM, modernised convolutions, and a linear baseline) for binary EDA arousal classification under LOSO validation with 147 participants. The joint evaluation of classification performance and five computational efficiency metrics is a methodologically sound framing, and the Pareto frontier analysis yields actionable deployment guidance. However, the manuscript reads as a CS/ML benchmarking paper that happens to use EDA signals, not as a biomedical signal processing contribution. Three critical gaps undermine its fit for BSPC: (i) no comparison against traditional biomedical signal processing baselines, (ii) no robustness analysis to signal quality degradation or motion artefacts despite EDA's well-documented susceptibility to both, and (iii) the preprocessing pipeline—although well-structured—lacks physiological or signal-theoretic justification for several parameter choices.

## Dimension Scores

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Fairness of Comparison | 30% | 62 | Equal tuning budget per architecture is commendable, but prior-work baselines were tuned with only 24 configurations vs. 64 for the new architectures, biasing the comparison in favour of the new models. Single-seed training conflates fold and seed variability. |
| Baseline Selection | 20% | 48 | Strong internal ML baselines (DLinear, ModernTCN) but no traditional signal processing baselines whatsoever—a critical omission for BSPC. No feature-engineering + classical-ML pipeline. No simple threshold-based SCR detector. Prior-work baselines are ~4 years old. |
| Evaluation Completeness | 20% | 68 | Five classification metrics plus five efficiency metrics. Per-class F1 and channel ablation in supplementary material. Missing: signal-quality / artefact-robustness analysis, confusion matrices, calibration error, and demographic stratification. |
| Statistical Rigor | 15% | 66 | Wilcoxon + Bonferroni-Holm is the right framework. Effect sizes (ΔF1 pp) reported alongside p-values. Weakened by (a) acknowledged but unresolved violation of independence within LOSO folds, (b) unspecified number of training seeds, and (c) inconsistent characterisation of the PatchTST–Mamba p-value across the text. |
| Analysis & Insights | 15% | 74 | Pareto frontier characterisation and channel-ablation findings are insightful and actionable. Interpretability analysis links learned representations to SCR physiology reasonably. Missing: failure-mode analysis, architecture × window-length interaction discussion for all eight models, and any analysis of how preprocessing choices interact differentially with each paradigm. |
| **Weighted** | 100% | **65** | |

## Sanity Check Results

| Check | Result | Detail |
|-------|--------|--------|
| Baseline consistency | **PARTIAL PASS** | PatchTST F1 0.863 vs prior 0.852 is explained (64 vs 24 configs + Δ²SCR channel). However, the prior-work baselines (1D-CNN, TCN, InceptionTime, TST) were tuned with only 24-configuration budgets, while the eight candidate architectures received 64 — a 2.7× tuning advantage. The table note discloses the PatchTST discrepancy but not this systematic imbalance. |
| Performance plausibility | **PASS** | F1 range (0.800–0.863) is within plausible bounds for binary EDA arousal classification under strict LOSO with 147 subjects and 40s windows. The hierarchy (SSM/attention > frequency > convolution > linear) aligns with known paradigm capabilities. |
| Model convergence | **LIKELY PASS** | Reported epochs-to-convergence (32–85 across architectures) are specific and consistent with architectural complexity. However, convergence criteria are described only as "early stopping (patience = 15) based on validation loss"—no mention of whether any architectures or folds exhibited pathological training behaviour (divergence, loss plateaus, NaN gradients). |
| Equal tuning budget | **QUALIFIED PASS** | 64 configurations per architecture is stated. However, the per-architecture search spaces differ substantially in cardinality—e.g., PatchTST spans ~768 unique combinations while DLinear spans ~320—so 64 trials explore different fractions of each space. This is inherent to grid search across heterogeneous search spaces but should be acknowledged. |
| Deployment metrics | **CONCERN** | Inference times are measured (1,000 forward passes on Quadro P5000), which is appropriate. BUT: the deployment-region thresholds (<1.5 ms wearable, 1.5–4 ms edge, ≥4 ms cloud) are defined on a workstation-class GPU with 2560 CUDA cores. Describing 1.5 ms on a Quadro P5000 as "wearable/microcontroller region" (line 619) conflates a desktop GPU with embedded hardware and misleads practitioners about deployability. |

## Major Comments

### 1. No Traditional Signal Processing Baselines (CRITICAL)
The paper compares eight deep learning architectures but includes zero traditional EDA signal processing methods. For BSPC, a comparison against established biomedical signal processing approaches is expected—not merely adjacent ML models. Missing baselines include: (a) threshold-based SCR detection (e.g., trough-to-peak) followed by a statistical classifier, (b) handcrafted EDA features (e.g., mean SCR amplitude, peak count, rise time, AUC) fed into SVM or Random Forest, and (c) classical frequency-domain approaches (e.g., spectral power features from SCR). At minimum, a feature-engineered pipeline with a linear classifier would provide a non-learned signal-processing anchor to contextualise the deep learning gains. Without these, the reader cannot determine whether the reported F1 = 0.80–0.86 range represents a genuine advance over conventional EDA analysis or merely the cost of using neural networks for a problem that simpler methods could solve adequately.

- **What would change my mind:** Addition of at least two traditional signal processing pipelines—(i) a feature-engineering approach with classical ML (e.g., 8–10 handcrafted SCR features + RF/SVM) and (ii) a simple threshold-based or template-matched SCR detector—evaluated under the identical LOSO protocol, preprocessing pipeline, and input window durations. If these achieve F1 substantially below 0.80, the deep learning gap is validated; if they approach 0.80, the contribution of the deep architectures must be re-contextualised.

### 2. Zero Robustness Analysis to Signal Quality and Artefacts (CRITICAL)
EDA signals are notoriously susceptible to motion artefacts, electrode contact pressure changes, and environmental noise—yet the paper contains no analysis of how any architecture degrades under these conditions. The dataset was collected under controlled laboratory conditions; this is acknowledged (line 739) but not addressed experimentally. The paper's own FEDformer discussion (line 323) speculates that "sparse Fourier mode selection provides implicit denoising, attenuating high-frequency acquisition artefacts"—but this claim is never tested. Similarly, Mamba's selective state-space mechanism is posited to filter noise content-adaptively, which could be tested by injecting synthetic artefacts of varying severity. For a BSPC audience, a benchmark paper that evaluates architectures only on clean laboratory data has limited translational value for real-world biomedical deployment.

- **What would change my mind:** An experiment—even synthetic—that simulates real-world signal degradation. At minimum: inject white noise at varying SNR levels (e.g., 20 dB, 10 dB, 0 dB), simulate motion-artefact transients (large-amplitude square-wave perturbations), and/or simulate electrode-contact dropout, then report F1 degradation curves for all architectures. This would directly validate or refute the implicit denoising claims and provide BSPC-relevant deployment guidance.

### 3. Preprocessing Pipeline Lacks Parameter Justification
While the preprocessing structure (FIR filter → Gaussian smoothing → CDA → derivatives → z-score) is clearly described, none of the parameter choices are justified by EDA physiology or signal theory:

- **Low-pass FIR at 4 Hz:** At a sampling rate of 4 Hz, the Nyquist frequency is 2 Hz. A 4 Hz cutoff exceeds Nyquist and therefore does not attenuate aliased content as expected—if the signal were sampled at 4 Hz, frequencies above 2 Hz have already been aliased. The filter order, passband ripple, and stopband attenuation are unspecified. Why an FIR filter specifically? Why not an IIR Butterworth?
- **Gaussian smoothing:** Sigma/bandwidth unspecified. How does the chosen sigma relate to the frequency content of typical SCR waveforms (0.2–0.5 Hz dominant)?
- **CDA implementation:** The specific CDA algorithm is unnamed. Ledalab's CDA differs from cvxEDA and from the Benedek-Kaernbach method—different decompositions produce different SCR waveforms. The paper says "following the pipeline established in our prior work," but the prior work [SanchezReolid2022] should be summarised rather than requiring BSPC readers to cross-reference.
- **Derivative computation:** How are first and second temporal derivatives computed at 4 Hz? Simple finite differences amplify noise—is smoothing applied before/after? The choice of derivative computation interacts with the 250 ms sample interval.

- **What would change my mind:** A short table summarising each preprocessing parameter, its chosen value, and a one-sentence physiological or signal-theoretic justification for the choice. Example: "Gaussian σ = 0.5 s → matches the ~0.3–0.5 s rise time of a typical SCR half-wave." Include the CDA implementation name (Ledalab / cvxEDA / custom). State the FIR filter order and justify the 4 Hz cutoff given the 2 Hz Nyquist bound.

### 4. Deployment Thresholds Defined on Wrong Hardware Class
The deployment regions in Figure 5 (wearable < 1.5 ms, mobile/edge 1.5–4 ms, cloud ≥ 4 ms) are defined from latency measurements on an NVIDIA Quadro P5000—a Pascal-generation workstation GPU with 2560 CUDA cores and 16 GB GDDR5X. This hardware has no relationship to a wearable microcontroller (e.g., ARM Cortex-M4 running TensorFlow Lite Micro) and only a loose relationship to a mobile SoC (e.g., Qualcomm Snapdragon with Hexagon DSP). The claim that Mamba "falls within the wearable/microcontroller region" at 1.5 ms on a Quadro P5000 is technically precise but pragmatically misleading: the same model on a Cortex-M4 could require 50–500× longer, depending on fixed-point quantisation and memory bandwidth.

- **What would change my mind:** Either (a) re-label the regions to reflect the actual hardware used (e.g., "low-latency GPU," "mid-latency GPU," "high-latency GPU"), removing all references to wearable/microcontroller deployment; or (b) add at least one benchmark point on actual embedded hardware (NVIDIA Jetson Orin Nano, Raspberry Pi 5 with ONNX Runtime, or an ARM Cortex-M4 with TFLite Micro) and recalibrate the thresholds accordingly.

### 5. Prior-Work Baselines Not Tuned on Equal Budget
The main results table (Table 2) places prior-work architectures (1D-CNN, TCN, InceptionTime, TST, PatchTST from [SanchezReolid2022]) alongside the new architectures. The table note reveals that the prior-work PatchTST was tuned with 24 configurations, while the new architectures received 64. This 2.7× difference in tuning budget likely gives the newly evaluated architectures an advantage. Worse, the prior-work 1D-CNN, TCN, InceptionTime, and TST may be systemically undertuned relative to the new candidates. The authors note only the PatchTST discrepancy but not the broader imbalance.

- **What would change my mind:** A full re-run of at minimum the strongest prior baseline (TST) with the 64-configuration budget and identical preprocessing, reported in the main results table. Alternatively, a sensitivity analysis showing that the ordering of architectures is preserved when all models are retrained with a reduced 24-configuration budget.

## Minor Comments

6. **Seed specification missing (line 343–345):** The paper does not state whether multiple random seeds were used. The standard deviation reported in Table 2 is across 147 LOSO folds. If a single seed was used, these standard deviations conflate fold-to-fold variability with the particular random initialisation. Specify the number of seeds and, if >1, report across-fold standard deviations with seed-averaged per-fold means.

7. **Wilcoxon independence assumption:** The paper properly acknowledges that LOSO folds with 146/147 overlapping training subjects violate the independence assumption of the Wilcoxon signed-rank test (line 743–745). The transparency is appreciated, but the subsequent recommendation that "readers apply their preferred interpretation" is an abdication of statistical responsibility. At minimum, report the results of a cluster-robust bootstrap or a mixed-effects model that accounts for the nested data structure, even if only for the key PatchTST-vs-Mamba comparison.

8. **p-value characterisation inconsistency:** Line 622 (Results) states "The 0.005 F1 difference between Mamba and PatchTST is not statistically significant (p = 0.048)"—but p = 0.048 IS significant at α = 0.05. Line 711–712 correctly clarifies that this is significant at the conventional level but not at the Bonferroni-Holm corrected level. The line 622 claim is contradicted by the paper's own statistical framework and must be corrected.

9. **Model convergence reporting:** Table S4 reports "epochs to converge" as fixed integers (32, 45, 58, etc.). Did all 147 folds converge in exactly the same number of epochs? If these are averages, report as mean ± std. If some folds failed to converge for any architecture, this must be disclosed.

10. **Cross-dataset evaluation recommended:** The paper cites WESAD (line 739) and identifies single-dataset evaluation as a limitation. However, WESAD contains EDA data from only 15 subjects under different conditions—evaluating the top-3 architectures (Mamba, PatchTST, TimesNet) on WESAD would provide a preliminary out-of-distribution test that substantially strengthens the generalisability claim, even if full LOSO is impossible with 15 subjects.

## Technical Suggestions

1. **Add a confusion matrix figure** for the top-performing architectures (Mamba, PatchTST) aggregated across all folds. This would reveal whether errors are concentrated in specific arousal states or signal types.

2. **Report expected calibration error (ECE)** for each architecture. A model with F1 = 0.86 but poorly calibrated probabilities (e.g., ECE > 0.15) is less useful for decision support than a calibrated model with slightly lower F1.

3. **Add signal-quality robustness experiment:** Inject synthetic motion artefacts (transient high-amplitude perturbations spanning 0.5–2 s) at random positions and measure F1 degradation. This is implementable without additional data collection and directly addresses the BSPC audience's primary concern.

4. **Add a traditional SCR feature extraction + classifier baseline:** Compute 8–10 features per window (mean SCR amplitude, peak count, mean rise time, AUC, number of SCRs detected by trough-to-peak, mean peak amplitude, median inter-response interval, spectral power in 0.2–0.5 Hz band) from the phasic SCR signal, apply RF/SVM, and report under identical LOSO. If this achieves F1 > 0.75, the deep learning delta shrinks considerably; if F1 < 0.70, the deep learning advantage is validated as substantial.

5. **Document per-fold convergence behaviour:** At minimum, report the number of LOSO folds for which each architecture failed to improve beyond the random baseline (F1 ≈ 0.50), diverged, or required gradient-clipping intervention.

6. **Clarify derivative computation:** State explicitly whether ΔSCR and Δ²SCR are computed via finite differences (forward, backward, or central), Savitzky-Golay filtering, or another method, and whether smoothing was applied before or after differentiation—this is critical for noise amplification at 4 Hz sampling.
