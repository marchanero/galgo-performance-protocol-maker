# Domain Profile

<!--
HOW TO USE: Fill this in manually OR let /discover (interactive interview) generate it.
All agents read this file to calibrate their field-specific behavior.
Delete sections that don't apply. Add sections specific to your field.
If no field is specified, agents default to applied economics.
-->

## Field

**Primary:** Affective Computing / Biomedical Engineering
**Adjacent subfields:** Time-Series Deep Learning, Physiological Signal Processing, Human-Computer Interaction (HCI), Pattern Recognition, Wearable Computing, Health Informatics
**Engineering domain:** Computer Engineering / ICT / Artificial Intelligence

---

## Target Journals (ranked by tier)

<!-- The Orchestrator uses this for journal selection. The Librarian prioritizes these in searches. -->

| Tier | Journals |
|------|----------|
| Top-tier AI/ML | IEEE TPAMI, JMLR, Neural Networks, Nature Machine Intelligence, IJCV |
| Top-tier CS/AI | NeurIPS, ICML, ICLR, CVPR, AAAI, IJCAI |
| Top-tier Affective Computing | IEEE TAC (Transactions on Affective Computing), ACII (Affective Computing and Intelligent Interaction) |
| Top-tier Biomedical | IEEE TBME (Transactions on Biomedical Engineering), IEEE JBHI, Physiological Measurement, Biomedical Signal Processing and Control |
| Strong field | IEEE Sensors Journal, Expert Systems with Applications, ACM Computing Surveys, Information Fusion |
| Specialty | Sensors, IEEE Access, Frontiers in Neuroscience, Biomedical Engineering Online |

---

## Common Data Sources

<!-- The Explorer prioritizes these. The explorer-critic knows their quirks. -->

| Dataset | Type | Access | Notes |
|---------|------|--------|-------|
| WESAD (Wearable Stress and Affect Detection) | Multimodal physiological | Public | 15 subjects, EDA+ECG+EMG, binary labels |
| CASE (Continuously Annotated Signals of Emotion) | Physiological + annotations | Public | 30 subjects, continuous annotations |
| DEAP (Database for Emotion Analysis) | EEG + peripheral signals | Public | 32 subjects, music video stimuli |
| AMIGOS | Multimodal physiological | Public | 40 subjects, short/long videos |
| RECOLA | Multimodal + annotations | Public | 46 subjects, collaborative task |
| CLAS (Cognitive Load, Affect, and Stress) | Physiological signals | Public | 60 subjects, multimodal |
| PMEmo | Physiological signals + music | Public | 457 subjects, music emotion |
| K-EmoCon | Multimodal + annotations | Public | 32 subjects, debate tasks |
| Custom/Proprietary EDA datasets | EDA signals | Restricted | Institutional ethics approval needed |

---

## Common Methodological Approaches

<!-- The Strategist considers these first. The strategist-critic knows field-specific threats. -->

| Approach | Typical Application | Key Concern to Address |
|----------|-------------------|------------------------|
| Lightweight / Efficient Transformers | EDA time-series classification | Model efficiency vs. accuracy trade-off, parameter count, inference latency |
| Convolutional Neural Networks (1D-CNN) | Temporal feature extraction from EDA | Receptive field size, temporal resolution |
| LSTM / BiLSTM | Sequential modeling of physiological signals | Vanishing gradients, training stability |
| Hybrid CNN-Transformer | Multiscale feature extraction | Component balance, overfitting |
| Transfer Learning / Pretraining | Cross-subject / cross-dataset generalization | Domain shift, fine-tuning strategy |
| Self-Supervised Learning | Pretraining on unlabeled physiological data | Pretext task design, representation quality |
| Ablation Studies | Isolating contribution of each architectural component | Controlled comparisons, statistical significance |
| k-Fold Cross-Validation (LOSO) | Subject-independent evaluation | Data leakage, proper stratification |

---

## Field Conventions

<!-- The Coder and Writer follow these. The writer-critic checks for them. -->

- EDA signal preprocessing: 4Hz Butterworth low-pass filter, decomposition into tonic (SCL) and phasic (SCR) components (cvxEDA or Ledalab)
- Standard train/validation/test splits; report performance on held-out test set
- Leave-One-Subject-Out (LOSO) cross-validation as the gold standard for generalization
- Report F1-score, accuracy, and AUC-ROC as primary metrics; include confusion matrices
- Statistical significance testing between models: paired t-test or Wilcoxon signed-rank over folds
- Model efficiency metrics: parameter count (M), FLOPs, inference time (ms/sample), memory footprint (MB)
- Always discuss computational complexity vs. accuracy trade-off
- Reproducibility: report random seeds, hyperparameter search spaces, and training details
- Ablation studies to isolate contributions of each architectural component

---

## Notation Conventions

<!-- The Writer and writer-critic enforce these. -->

| Symbol | Meaning | Anti-pattern |
|--------|---------|-------------|
| X ∈ R^(T×D) | Input EDA time-series with T timesteps and D features | Avoid X without dimensions |
| y | Class label (arousal level: low/high) | Don't use generic "target" |
| f_θ(x) | Model prediction with parameters θ | Avoid ambiguous notation |
| N | Number of subjects / samples | Don't use lowercase n |
| L | Number of classes | Distinguish from Loss L |
| Acc, F1, AUC | Performance metrics | Always define at first use |
| #params, FLOPs, t_inf | Efficiency metrics | Always report with units |

---

## Seminal References

<!-- The Librarian ensures these are cited when relevant. The strategist-critic knows their methods. -->

| Paper | Why It Matters |
|-------|---------------|
| Vaswani et al. (2017) "Attention Is All You Need" | Original Transformer architecture — foundation for all variants |
| Dosovitskiy et al. (2021) "An Image is Worth 16×16 Words" | Vision Transformer (ViT) — adapted to time series patch-based approaches |
| Wang et al. (2023) "Time Series Transformer" | Transformer adaptations for time-series classification |
| Schmidt et al. (2018) "WESAD dataset" | Gold-standard benchmark for wearable stress detection |
| Boucsein (2012) "Electrodermal Activity" | Definitive reference for EDA measurement and interpretation |
| Posada-Quintero & Chon (2020) "EDA-based emotion recognition" | Recent survey of EDA signal processing for affective computing |
| Picard et al. (2001) "Toward Machine Emotional Intelligence" | Foundational work on affective computing |
| Liu et al. (2021) "Swin Transformer" / "Efficient Transformers Survey" | Lightweight/efficient transformer design principles |

---

## Theoretical Foundational References

<!-- The Theorist and theorist-critic default to these anchors when building or reviewing a theory section.
     Only needed if the paper has a formal theory section (convergence proofs, generalization bounds,
     complexity analysis, or formal architecture properties).
     Leave empty to fall back to the generic ML theory defaults. -->

| Topic | Anchor references |
|-------|------------------|
| Attention complexity analysis | Vaswani et al. (2017); Tay et al. (2022) "Efficient Transformers: A Survey" |
| Generalization bounds for deep learning | Bartlett et al. (2017); Neyshabur et al. (2018) |
| Time-series representation learning | Franceschi et al. (2019); Tonekaboni et al. (2021) |
| PAC-Bayesian bounds | McAllester (1999); Dziugaite & Roy (2017) |

---

## Paper Author Team

<!-- Used by the theorist-critic to calibrate respect. If the authors are themselves among the reference
     literature on a topic, the critic avoids lecturing them on their own contributions.
     List author surnames + the topics they are foundational on. -->

| Author | Foundational on |
|--------|----------------|
| [e.g., Vaswani] | [Self-attention, Transformer architecture] |

---

## Field-Specific Referee Concerns

<!-- The domain-referee and methods-referee watch for these. -->

- "Are you comparing against proper baselines (SOTA methods from the last 2-3 years)?"
- "Is LOSO cross-validation used? Within-subject splits artificially inflate performance."
- "Are you reporting both accuracy AND per-class metrics? Imbalanced datasets are common in affective computing."
- "Model efficiency metrics: parameter count, FLOPs, and inference latency must be reported."
- "Is the EDA preprocessing pipeline described with enough detail to reproduce?"
- "Ablation studies: which components actually contribute to the performance gain?"
- "Are statistical significance tests performed between competing models?"
- "Domain shift / cross-dataset generalization: does your model transfer to other datasets?"
- "Is the physiological/behavioral interpretation of results discussed, or are you just reporting numbers?"
- "Reproducibility: are hyperparameters, seeds, and training details fully specified?"

---

## Quality Tolerance Thresholds

<!-- Customize for your domain's standards. Used by quality.md. -->

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| Classification accuracy | ±0.5 pp | Validation set variability across 5-fold CV |
| F1-score | ±0.5 pp | Same as accuracy |
| AUC-ROC | ±0.005 | Standard AUC reporting precision |
| Parameter count | ±1K params | Exact counting, not approximate |
| Inference time | ±0.1 ms | Hardware variability across runs |
| FLOPs | ±1K | Model complexity measurement precision |
