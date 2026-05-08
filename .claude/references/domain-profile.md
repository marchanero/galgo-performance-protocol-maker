# Domain Profile

<!--
HOW TO USE: Calibrated for Roberto Sánchez-Reolid's research group (UCLM — I3A / TSI).
All agents read this file to calibrate their field-specific behavior.
-->

## Field

**Primary:** Affective Computing / Biomedical Engineering / Time-Series Deep Learning
**Adjacent subfields:** Physiological Signal Processing (EDA), Wearable Computing, Health Informatics, Pattern Recognition, State Space Models, Efficient Transformers
**Engineering domain:** Computer Engineering / ICT / Artificial Intelligence

## Research Group Context

- **Institution:** Universidad de Castilla-La Mancha (UCLM) — I3A / TSI
- **Core dataset:** 147 healthy participants (aged 18–44), controlled laboratory protocol (audiovisual stimuli: calm vs. stress), EDA at 4 Hz, 40-second effective windows after trimming 4s onset + 3s offset from 47s stimuli
- **Gold standard protocol:** Leave-One-Subject-Out (LOSO), 147 folds — test subject fully excluded from training, validation, AND normalization
- **Typical input:** SCR + ΔSCR + Δ²SCR (3 channels, T = 4n, 4 Hz)
- **Core architecture papers:** Deep-SVM (IJNS 2020), 1D-CNN (BSPC 2022), 5-architecture comparison (reference paper), current 8-architecture paper
- **Self-citation sensitivity:** Keep below ~35% of total cite instances. Remove duplicate cites in same sentence, avoid generic "as in prior work" without specific claim. Use `sanchez2020deep` for dataset protocol, `SanchezReolid2022` for architecture comparison context.

---

## Target Journals (ranked by tier)

| Tier | Journals |
|------|----------|
| Top-tier Affective Computing | IEEE TAC (Transactions on Affective Computing) |
| Top-tier Biomedical Signal Processing | BSPC (Biomedical Signal Processing and Control), IEEE TBME, IEEE JBHI |
| Strong field | IEEE Sensors Journal, Physiological Measurement, Expert Systems with Applications |
| Specialty / Outreach | Sensors, IEEE Access, Frontiers in Neuroscience |

---

## Common Data Sources

| Dataset | Type | Access | Notes |
|---------|------|--------|-------|
| UCLM custom (147 subjects) | EDA only | Institutional | Primary dataset. 147 participants, calm/stress, 4 Hz, 40s windows. LOSO protocol. |
| WESAD | Multimodal | Public | 15 subjects, EDA+ECG+EMG, binary stress labels. Good for cross-dataset validation. |
| CASE | Physiological | Public | 30 subjects, continuous annotations |
| DEAP | EEG+peripheral | Public | 32 subjects, music video stimuli |
| AMIGOS | Multimodal | Public | 40 subjects, short/long videos |

## Author's Own Published Work (Self-Citation Pool)

| Key | Paper | Journal | Year | Use for |
|-----|-------|---------|------|---------|
| `sanchez2020deep` | Deep SVM for stress from EDA | Int. J. Neural Systems | 2020 | Dataset protocol, classical baseline (F1 0.80-0.83) |
| `sanchez2022one` | 1D-CNN for EDA arousal | BSPC | 2022 | 1D-CNN baseline, derivative channels justification |
| `SanchezReolid2022` | 5-architecture comparison (1D-CNN, TCN, InceptionTime, TST, PatchTST) | — | 2022 | Reference paper. Prior DL baselines, LOSO protocol, architecture comparison context |

---

## Common Methodological Approaches

| Approach | Typical Application | Key Concern to Address |
|----------|-------------------|------------------------|
| Efficient Transformers (Informer, Autoformer, FEDformer, PatchTST) | EDA time-series classification | O(N²) vs O(L log L) vs O(L) complexity; attention interpretability |
| State Space Models (Mamba/Bi-Mamba) | Physiological sequence modeling | Competitive accuracy at O(L) complexity; content-dependent gating |
| Modernised Convolutions (ModernTCN) | Temporal feature extraction | Large kernels, inverted bottlenecks vs. attention mechanisms |
| Linear Baselines (DLinear) | Efficiency floor | Trend-seasonal decomposition matches 1D-CNN — confirms non-linear temporal modeling necessity |
| Handcrafted Features + SVM/RF | Classical signal processing baseline | Anchors DL gains; expected by BSPC reviewers |
| Ablation Studies (channel, window length) | Isolating component contributions | Derivative channels; minimal temporal interval |
| LOSO Cross-Validation | Subject-independent evaluation | Z-score within-fold only; same-subject windows preserved together |
| Pareto Frontier Analysis | Accuracy-efficiency trade-off | 5 efficiency metrics: params, FLOPs, t_inf, M_peak, t_train |

---

## Field Conventions

- **EDA preprocessing:** FIR low-pass + Gaussian smoothing + CDA decomposition (cite cvxEDA [Greco2016] and Ledalab [Benedek2010] as alternatives)
- **Derivative channels:** ΔSCR (velocity) and Δ²SCR (acceleration) computed from phasic SCR
- **SPR Guidelines:** Always cite SPR2012EDA for methodological choices
- **LOSO is gold standard:** Within-subject splits artificially inflate performance in EDA
- **Metrics:** F1, Acc, Prec, Rec, AUC — report mean ± std across 147 LOSO folds
- **Efficiency is primary:** params (M), FLOPs (M), t_inf (ms), M_peak (MB), t_train (s/epoch)
- **Statistical tests:** Wilcoxon signed-rank on per-fold F1; Bonferroni-Holm correction for 28 pairwise comparisons. **Caveat:** LOSO violates independence assumption — state that p-values are "descriptive indicators of effect consistency"
- **Deployment tiers:** Use GPU-relative language (low/mid/high-latency GPU), not wearable/mobile/cloud unless benchmarked on actual embedded hardware
- **Classical baseline:** Handcrafted SCR features + SVM is expected at BSPC; report even if retrospective
- **Self-citations:** Keep to ~35% max; don't cite same paper twice in same sentence; use `sanchez2020deep` for dataset protocol, not `SanchezReolid2022`
- **Table formatting:** booktabs, threeparttable for footnotes. Bold = best per metric (verify numbers match bolding!)
- **Figures:** TikZ with ColorBrewer colorblind-safe palette. 6-figure typical count.
- **Reproducibility:** Report seeds, hyperparameter search space, optimal configs, epochs to convergence (mean ± std across folds)
- **Overleaf sync:** Use `git subtree push --prefix=paper overleaf main` — NEVER force push (breaks sync). If rebasing, use manual clone + copy + normal push.

---

## BSPC Journal Calibration (Key Lessons)

- **Classical signal processing baseline is mandatory** — handcrafted EDA features + SVM/RF anchors DL gains. Without it, paper reads as ML benchmark, not biomedical signal processing.
- **Preprocessing must be physiologically justified** — why FIR at 4 Hz? Why Gaussian σ? Why CDA over cvxEDA/Ledalab?
- **Cite BSPC papers in introduction** — aim for 5-8 BSPC journal references in related work. Shows venue awareness.
- **Artifact handling** — EDA is noise-sensitive. At minimum, acknowledge limitation. Stronger: inject synthetic noise experiment.
- **Deployment claims** — GPU benchmarks ≠ wearable deployment. Use honest GPU-relative language.
- **Interpretability** — Qualitative observations are fine IF labeled as qualitative. Don't promise "quantification" in Methods then deliver narrative in Results.
- **Paradigm/color consistency** — If figures group by complexity class, captions must say so (not "by paradigm"). Count must be consistent across abstract, intro, figures.

## BSPC Referee Pet Peeves

| Critical (they scrutinize) | Constructive (they reward) |
|---------------------------|---------------------------|
| Missing classical signal processing baselines | Thorough preprocessing documentation with physiological justification |
| Deployment claims without embedded hardware evidence | Honest limitations and GPU-relative language |
| "First"/"novel" claims without literature verification | Self-citation restraint + BSPC journal references |
| "Significantly better" without stats or with violated test assumptions | Pareto frontier analysis with multiple efficiency dimensions |

---

## Notation Conventions

| Symbol | Meaning | Anti-pattern |
|--------|---------|-------------|
| X ∈ R^(T×C) | Input with T timesteps and C channels | Avoid X without dimensions |
| T = 4n | Timesteps for n-second window at 4 Hz | Don't forget factor |
| C = 3 | Channels: SCR, ΔSCR, Δ²SCR | |
| N_params | Parameter count (millions) | Always with units |
| t_inf | Inference time (ms) | Batch size = 1 |
| M_peak | Peak GPU memory (MB) | |
| p_BH | Bonferroni-Holm corrected threshold | For 28 pairwise comparisons |

---

## Seminal References

| Paper | Why It Matters |
|-------|---------------|
| Boucsein (2012) "Electrodermal Activity" | Definitive EDA reference |
| Greco et al. (2016) "cvxEDA" (IEEE TBME) | Standard EDA decomposition method |
| Benedek & Kaernbach (2010) "Ledalab" (J. Neurosci. Meth.) | Alternative EDA decomposition |
| SPR Ad Hoc Committee (2012) "Publication recommendations for EDA" | Methodological guidelines for EDA |
| Posada-Quintero & Chon (2020) "EDA innovations" (Sensors) | Recent EDA signal processing survey |
| Schmidt et al. (2018) "WESAD" | Gold-standard wearable stress benchmark |
| Vaswani et al. (2017) "Attention Is All You Need" | Original Transformer |
| Wen et al. (2023) "Transformers in Time Series: A Survey" | Time-series Transformer taxonomy |
| Tay et al. (2022) "Efficient Transformers: A Survey" | Efficiency mechanisms |
| Mamba (Gu & Dao 2023) | Selective state space models |
| PatchTST (Nie et al. 2023, ICLR) | Patch-based time-series Transformer |

---

## Quality Tolerance Thresholds

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| Classification accuracy | ±0.5 pp | LOSO fold variability across 147 subjects |
| F1-score | ±0.5 pp | Same |
| AUC-ROC | ±0.005 | Standard reporting precision |
| Parameter count | ±0.1 M | Rounding for readability |
| Inference time | ±0.1 ms | Hardware variability |
| FLOPs | ±1 M | thop library estimation tolerance |

---

## Paper Author Team (from ORCID/Crossref)

**Primary author:** Roberto Sánchez-Reolid (ORCID: `0000-0003-4455-370X`)
- **Affiliation:** UCLM — I3A / Dpto. Sistemas Informáticos
- **Total publications:** 21 (2018–2026), 5 as first author
- **Core lines:** Affective computing (EDA), physiological signal processing (EEG, fNIRS), deep learning time-series, computer vision (defect classification), neuroarchitecture, XR, speech emotion

**Key co-authors:**
| Author | ORCID | Research line |
|--------|-------|---------------|
| Antonio Fernández-Caballero | `0000-0002-8211-0398` | Affective computing, ambient intelligence |
| Daniel Sánchez-Reolid | `0000-0003-3612-1261` | EEG, emotion recognition, BCI |
| Francisco López de la Rosa | — | Computer vision, CNN, defect detection |
| José L. Gómez-Sirvent | — | Neuroarchitecture, XR, emotion recognition |
| Arturo Martínez-Rodrigo | — | Digital health, physiological signals |

**EDA papers (same 147-subject dataset):**
| Year | Title | Journal | Bib key | First author? |
|------|-------|---------|---------|---------------|
| 2020 | Deep SVM for stress from EDA | Int. J. Neural Systems | `sanchez2020deep` | ✅ |
| 2022 | 1D-CNN for EDA arousal | BSPC | `sanchez2022one` | ✅ |
| 2022 | ML for stress from EDA (scoping review) | Sensors | `SanchezReolid2022` | ✅ |
| 2025 | Efficient architectures for EDA (current) | (this paper) | — | ✅ |
