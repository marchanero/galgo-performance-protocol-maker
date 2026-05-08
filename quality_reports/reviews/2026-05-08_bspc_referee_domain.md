# Domain Referee Report
**Date:** 2026-05-08
**Venue:** Biomedical Signal Processing and Control (BSPC)
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification
**Disposition:** ARCHITECTURE
**Calibrated to:** BSPC (biomedical signal processing + control systems)
**Recommendation:** Major Revisions
**Overall Score:** 66/100

## Summary

This paper benchmarks eight deep learning architectures spanning Transformers, state space models, and modernised convolutions for binary arousal classification from EDA signals under LOSO validation with 147 participants. The Pareto frontier analysis and five complementary efficiency metrics provide actionable deployment guidance. However, the paper evaluates DL architectures against only other DL architectures, omitting the classical EDA signal processing baselines (hand-crafted feature engineering + traditional classifiers) that would anchor the contribution in the biomedical signal processing literature. The preprocessing pipeline is adopted from prior work without critical justification for its specific components relative to EDA physiology. As submitted, the paper reads as an ML benchmarking study retrofitted to a physiological application, rather than a biomedical signal processing contribution that happens to use modern architectures. The core computational results are sound and the Pareto analysis is genuinely useful, but the paper needs to engage substantially more with how EDA signals are classically processed and interpreted in the biomedical engineering community before it meets the BSPC bar.

## Dimension Scores
| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Contribution & Novelty | 30% | 65 | First EDA benchmark for SSM/modernConv, but no novel architecture or signal processing method; Pareto frontier is the main contribution |
| Literature Positioning | 25% | 58 | Well-situated in DL/time-series literature; poorly positioned in classical EDA signal processing — cvxEDA, Ledalab, SPR guidelines absent |
| Substantive Arguments & Interpretation | 20% | 72 | Pareto analysis and channel ablation are strong; physiological interpretation of preprocessing is thin; interpretability results lack quantitative support |
| External Validity & Generalizability | 15% | 68 | LOSO provides strong internal validity; single lab dataset limits generalizability; no ambulatory/clinical validation |
| Venue Fit for BSPC | 10% | 75 | EDA topic fits BSPC; missing classical signal processing comparisons weaken the fit; currently closer to an ML venue |
| **Weighted** | 100% | **66** | |

## Major Comments

### 1. Absence of classical EDA signal processing baselines (CRITICAL — ARCHITECTURE pet peeve)

The paper compares eight DL architectures exclusively against prior DL architectures (1D-CNN, TCN, InceptionTime, TST, PatchTST from the authors' prior work). At no point are these architectures benchmarked against how EDA signals are classically processed and classified in the biomedical signal processing community — namely, hand-crafted feature extraction (SCR amplitude, rise time, half-recovery time, frequency of NS-SCRs, AUC, etc. from the trough-to-peak analysis framework codified in Boucsein 2012) paired with traditional classifiers (SVM with RBF kernel, Random Forest, Logistic Regression with L1/L2 regularisation, Linear Discriminant Analysis).

This is a critical omission for BSPC. The canonical approach in biomedical signal processing is to extract physiologically interpretable features and determine whether deep learning provides marginal gains beyond that well-understood baseline. Without it, the reader cannot judge whether the 8--10 percentage point F1 gap between DLinear (0.800) and Mamba/PatchTST (0.858/0.863) represents a genuine advance over what a domain expert could achieve with classical feature engineering, or whether both DL and classical approaches converge to similar performance ceilings.

The inclusion of DLinear as a "linear baseline" is welcome but not sufficient — DLinear operates on raw/decomposed signal values, not on physiologically motivated features. Hand-crafted EDA features encode domain knowledge about SCR morphology (amplitude, latency, rise time, recovery slope) that a linear model on raw time points cannot capture.

- **What would change my mind:** Add a classical EDA feature engineering baseline: extract standard SCR features (amplitude, rise time, half-recovery time, AUC, NS-SCR frequency, mean SCL, etc.) from each 40 s window, as defined in Boucsein (2012) and the SPR publication guidelines. Train at least two classifiers (e.g., SVM with RBF kernel, Random Forest) under the identical LOSO protocol with the same feature set. Report these results alongside Table~2. Even a simple SCR amplitude threshold classifier would contextualise the performance ceiling. If the feature-engineered baseline approaches DLinear, the narrative about the necessity of deep temporal modelling becomes more compelling; if it approaches Mamba/PatchTST, the contribution needs reframing.

### 2. Preprocessing pipeline lacks explicit physiological justification for EDA-specific components (CRITICAL — CONSTRUCTIVE pet peeve)

The preprocessing pipeline (Section 2.2, lines 87--103) describes: low-pass FIR filter (4 Hz) → Gaussian smoothing → CDA decomposition → derivative channels → windowing → Z-score normalisation. Each step needs explicit physiological motivation linked to EDA signal characteristics and sympathetic nervous system (SNS) physiology:

**(a) Low-pass FIR filter at 4 Hz:** Why 4 Hz? EDA signals are acquired at 4 Hz, making the Nyquist frequency 2 Hz. A 4 Hz cutoff provides no anti-aliasing benefit. Was the cutoff determined empirically or chosen to match the prior work? Given that EDA spectral power is concentrated below 1 Hz (Boucsein 2012, Ch. 2), what is the justification for a cutoff at 4 Hz rather than 1--2 Hz? If the filter is meant to attenuate high-frequency acquisition noise, what is the noise spectrum of the acquisition hardware? The filter order and design method (window type, passband/stopband specs) are also absent.

**(b) Gaussian smoothing parameters:** No σ value or kernel width is specified. Gaussian smoothing is an ad-hoc denoising step when physiological signals have well-characterised noise sources (motion artifacts, electrode contact noise, thermal drift, quantisation noise). What specific noise source does Gaussian smoothing target, and why is it preferred over, e.g., a median filter for motion artifact removal or wavelet denoising for non-stationary noise? The interaction between the FIR filter and subsequent Gaussian smoothing (effectively double-filtering) is not discussed.

**(c) CDA vs. cvxEDA/Ledalab:** The paper uses Continuous Decomposition Analysis (CDA) from prior work, but does not justify this choice against the two most widely used EDA decomposition methods: cvxEDA (Greco et al. 2016, IEEE TBME) and Ledalab (Benedek & Kaernbach 2010, J. Neurosci. Methods). cvxEDA formulates decomposition as a convex optimisation problem with physiologically grounded constraints (non-negative SCRs, sparse phasic driver), while Ledalab uses non-negative deconvolution with an a priori SCR shape. Different decomposition methods produce different phasic estimates, which may interact differently with downstream architectures. Has the choice of CDA been validated against these alternatives for the specific task of arousal classification?

**(d) Derivative channels — ΔSCR and Δ²SCR:** These are well-motivated (velocity and acceleration of SNS activation), but the justification could be strengthened by noting that SCR rise time and slope are established features in classical EDA analysis (Boucsein 2012, Ch. 3.2.2). The gap is that derivative channels approximate these classical features but in a purely data-driven way — whether the approximations capture the same information as explicit feature computation is untested.

- **What would change my mind:** Add a subsection or expanded paragraph within Section 2.2 that explicitly links each preprocessing step to (i) the specific EDA signal characteristic it addresses (e.g., "Gaussian smoothing with σ = X attenuates electrode contact noise, which manifests as high-frequency fluctuations above Y Hz"), (ii) the SNS physiological rationale (e.g., "CDA is chosen over cvxEDA because the continuous formulation better preserves the smoothness of tonic drift during the 40 s window"), and (iii) evidence from the EDA literature supporting the choice. A sensitivity analysis comparing at least two decomposition methods (CDA vs. cvxEDA) on a subset of architectures would substantially strengthen this section.

### 3. Interpretability claims require quantitative support

The interpretability subsection (3.6, lines 715--725) makes several claims that are described qualitatively but lack the quantitative evidence that a BSPC audience would expect:

**(a)** "Attention weight distributions concentrate on SCR onset and rising phases" — no attention heatmaps or aggregate onset-phase attention ratios are shown. For a BSPC reader, the natural question is: _what proportion of total attention mass falls within the onset/rise region vs. baseline/decay?_ Without this, the claim is unfalsifiable.

**(b)** "TimesNet's period discovery mechanism identifies dominant periods in the 2--5 second range" — no distribution of discovered periods is shown across folds or participants. The variability of these periods across subjects (given known inter-subject SCR duration variability) is relevant.

**(c)** "Mamba's discretised state transition matrices reveal emphasis on SCR onset regions" — this is described but no transition matrix visualisation or quantitative metric is provided. How is "emphasis" measured? Eigenvalue analysis? Gate activation statistics?

**(d)** The gradient-based saliency analysis ($S = |\partial \hat{y} / \partial \mathbf{X}|$) for Mamba and ModernTCN — saliency on recurrent/SSM models has known reliability issues (Adebayo et al. 2018, "Sanity Checks for Saliency Maps"). SmoothGrad or Integrated Gradients would be more appropriate for Mamba with its selective gating.

- **What would change my mind:** Provide at minimum (i) an aggregate attention/Saliency heatmap for the top-2 architectures (Mamba, PatchTST) showing temporal distribution across the 40 s window with SCR onset/peak annotations from representative trials, (ii) a histogram of TimesNet-discovered periods, and (iii) a quantitative metric for "onset region emphasis" (e.g., percentage of attention mass within ±2 s of detected SCR onsets). Report the physiological results in a dedicated figure.

### 4. The channel ablation claim that SSMs "learn temporal derivative information implicitly" requires stronger evidence

The finding that DLinear and ModernTCN gain +2.7--2.8% F1 from derivative channels while attention/SSM architectures gain +1.8--1.9% (Section 3.6, line 725) is interesting. The inference that SSM/attention models "partially learn temporal derivative information implicitly" is plausible but not uniquely supported by this data.

Alternative explanations exist: (a) SSM/attention models have higher total capacity (more parameters, deeper representations) and can therefore better utilise the raw SCR signal without needing explicit derivative encoding — the gain from derivative channels is smaller simply because the baseline (SCR-only) performance is already higher, leaving less room for improvement (ceiling effect); (b) the derivative channels provide redundant information that multi-layer non-linear transformations can reconstruct but do not necessarily "learn" in the sense of explicitly computing derivatives; (c) patch tokenisation (PatchTST) or state-space recurrence (Mamba) may encode local temporal context in ways that correlate with but do not functionally replace derivative computation.

- **What would change my mind:** Conduct a probing analysis: train a linear probe to predict ΔSCR from the internal representations of each architecture (after the encoder, before the classification head). If SSM/attention representations encode derivative information with higher fidelity than ModernTCN/DLinear representations, the "implicit learning" claim is supported. Report the probe's $R^2$ for ΔSCR prediction across architectures. Without this, the claim should be softened to an observation about differential benefit rather than an inference about mechanism.

## Minor Comments

5. **Sampling rate of 4 Hz is very low for EDA.** The paper notes this as the acquisition frequency (line 82) but does not discuss its implications. At 4 Hz, the temporal resolution is 250 ms. Individual SCR components (especially the rapid onset) may be under-sampled — a typical SCR onset can rise within 500--1000 ms. While 4 Hz is sufficient to capture the waveform envelope (Boucsein 2012 recommends ≥ 10 Hz for morphologically detailed SCR analysis), the paper should acknowledge that fine-grained SCR dynamics (pre-ejection period, precise latency) are not resolvable at this rate. Whether this under-sampling explains any of the DLinear-vs.-Transformer performance gap is worth considering.

6. **Motion artifact handling is not discussed.** EDA signals from controlled laboratory conditions still contain artifacts (electrode pressure changes, hand movements, temperature fluctuations). The paper does not describe any artifact detection or rejection step. Was artifact-free signal segments guaranteed by the experimental protocol? If so, this should be stated. If not, the interaction between artifact presence and architecture robustness (SSM gating may be more resilient to artifacts than attention) should be noted as a limitation.

7. **The `O(L log L)` complexity assignment for Informer, Autoformer, and TimesNet is inconsistent with practical measurements.** Table 1 assigns $O(L \log L)$ to Informer, but the original Informer paper claims $O(L \log L)$ only for ProbSparse attention with self-attention distilling; without distilling across all layers, the complexity approaches $O(L^2)$ in the worst case. Similarly, Autoformer's auto-correlation mechanism has $O(L \log L)$ theoretical complexity but the constant factor from two FFTs per layer is substantial — this aligns with the measured Autoformer being the most expensive of the $O(L \log L)$ group (3.84M parameters, 4.2 ms inference). A clarifying note about worst-case vs. practical complexity would help.

8. **The deployment region thresholds (1.5 ms, 4 ms) lack hardware justification.** The thresholds in Figure 5 (line 619) define "wearable," "mobile/edge," and "cloud/server" regions based on inference time on a single Quadro P5000 GPU. However, a 1.5 ms threshold for "wearable" is optimistic for actual wearable processors — an ARM Cortex-M4 at 100 MHz with 256 KB SRAM would not achieve 1.5 ms inference for Mamba (1.52M parameters). The thresholds are specific to a workstation-class GPU (Pascal, 2560 CUDA cores, 16 GB VRAM) which is not representative of wearable or even mobile hardware. At minimum, note that these thresholds are relative to the benchmark GPU and would shift on target hardware.

9. **Unused bibliography entries clutter the bib file.** The .bib file contains 46 entries of which approximately 15 are uncited in the main text or supplementary material. For BSPC submission, journal editors typically prefer lean bibliographies. Trim or move to a "Further Reading" appendix.

10. **The term "modernised convolution" is imprecise.** ModernTCN uses depthwise separable convolutions with inverted bottlenecks, Squeeze-and-Excitation, and large kernels — all of which were introduced in MobileNetV2 (Sandler et al. 2018) and SENet (Hu et al. 2018). The "modernisation" is in applying these established computer vision techniques to 1D time series, not in inventing new convolutional primitives. Consider "depthwise-separable TCN" or "MobileNet-style TCN" for precision.

## Missing Literature

The paper is well-cited in the DL/time-series domain but has significant gaps in the EDA signal processing and biomedical engineering literature:

- **Greco, A., Valenza, G., Lanata, A., Scilingo, E.P., & Citi, L. (2016).** "cvxEDA: A convex optimization approach to electrodermal activity processing." *IEEE Transactions on Biomedical Engineering*, 63(4), 797--804. — The most widely cited algorithmic EDA decomposition method; should be discussed as an alternative to CDA.

- **Benedek, M. & Kaernbach, C. (2010).** "A continuous measure of phasic electrodermal activity." *Journal of Neuroscience Methods*, 190(1), 80--91. — Ledalab; foundational for non-negative deconvolution of SCRs.

- **Bach, D.R., Flandin, G., Friston, K.J., & Dolan, R.J. (2010).** "Modelling event-related skin conductance responses." *International Journal of Psychophysiology*, 75(3), 349--356. — Psi-based SCR modeling with physiologically grounded response functions.

- **Kleckner, I.R., et al. (2018).** "Methodological recommendations for electrodermal activity data analysis." *Psychophysiology*, 55(1), e12971. — SPR publication guidelines for EDA signal processing; citation needed for methodological choices.

- **Posada-Quintero, H.F. & Chon, K.H. (2020).** "Innovations in electrodermal activity data collection and signal processing: A systematic review." *Sensors*, 20(2), 479. — Already cited; should be used to motivate preprocessing choices.

- **Braithwaite, J.J., Watson, D.G., Jones, R., & Rowe, M. (2013).** "A guide for analysing electrodermal activity (EDA) & skin conductance responses (SCRs) for psychological experiments." — Widely used practical guide for EDA feature extraction; relevant for the classical baseline.

## Questions for the Authors

1. **Why was CDA chosen over cvxEDA or Ledalab for phasic decomposition?** What are the quantitative differences in the phasic signal produced by these three methods on the 147-participant dataset, and have you verified that the architecture rankings are robust to the choice of decomposition method?

2. **What classification performance is achievable with classical EDA features (SCR amplitude, rise time, AUC, NS-SCR frequency, mean SCL) + an SVM or Random Forest classifier under the identical LOSO protocol?** If the authors do not have these numbers, could they provide a reasoned estimate of where the classical baseline would fall relative to DLinear (F1 = 0.800)?

3. **At the 4 Hz sampling rate, what is the temporal precision of detected SCR onsets?** Given that individual SCRs can onset and peak within 1--2 seconds (corresponding to only 4--8 samples), can the patch tokenisation and attention mechanisms reliably distinguish onset-phase from peak-phase dynamics, or are they primarily detecting the overall presence/absence of a phasic response?

4. **Does the preprocessing pipeline include any artifact rejection?** If motion artifacts or electrode contact noise are present in the data, how do the architectures differ in robustness to these artifacts? Mamba's selective gating mechanism could theoretically suppress artifact-corrupted time steps — was this empirically observed?

5. **For the Mamba interpretability analysis, you mention examining "discretised state transition matrices."** Can you provide the specific metric used to quantify SCR onset emphasis (e.g., eigenvalue magnitude at onset-adjacent time steps, gate activation statistics) and report it quantitatively?

6. **The paper positions channel-independent encoding as a feature of PatchTST (line 311).** Do any of the other architectures employ channel mixing at the input stage, and could this explain any portion of the observed performance differences? For example, TimesNet's 2D reshaping operates on multi-channel inputs jointly — does this introduce any subject-specific channel correlation that could be affected by inter-subject variability?
