# Requirements Specification: Lightweight Transformers for EDA-based Arousal Classification

**Date:** 2026-05-07
**Status:** DRAFT
**Clarity:** CLEAR

---

## MUST (non-negotiable)

- [MUST] Comparar 5 arquitecturas transformer eficientes: PatchTST (baseline), Informer, Autoformer, FEDformer, DLinear
- [MUST] Mismo dataset de 147 participantes y protocolo controlado que el reference paper
- [MUST] Validación LOSO estricta (Leave-One-Subject-Out)
- [MUST] Mismas 3 channels de entrada: SCR, ΔSCR, Δ²SCR (4 Hz sampling)
- [MUST] Eficiencia computacional como métrica principal (parámetros, FLOPs, tiempo inferencia, memoria) + Accuracy/Precision/Recall/F1/AUC
- [MUST] Análisis de ventana temporal (1-40s)
- [MUST] Test estadístico Wilcoxon signed-rank
- [MUST] Archivo .bib con todas las referencias reales
- [MUST] Formato Springer LNCS (mismo que reference paper)
- [MUST] Compatible con Overleaf (XeLaTeX, latexmkrc)

## SHOULD (expected)

- [SHOULD] Interpretabilidad: mapas de atención alineados con morfología SCR
- [SHOULD] Análisis de ablación de canales (SCR only; SCR+ΔSCR; SCR+ΔSCR+Δ²SCR)
- [SHOULD] Discusión del trade-off eficiencia-accuracy para edge deployment
- [SHOULD] Incluir DLinear como baseline provocador ("are transformers necessary?")

## MAY (nice-to-have)

- [MAY] Comparación con resultados del reference paper (cuando se publique)
- [MAY] Análisis de escalabilidad con tamaño de ventana
- [MAY] Visualizaciones de consumo energético estimado

---

## Selected Architectures & Rationale

| Architecture | Mechanism | Complexity | Reference | Rationale for EDA |
|---|---|---|---|---|
| PatchTST | Patch tokenization | O(N²), N≪L | Wang et al., 2023 | Baseline; best in reference paper (F1=0.852) |
| Informer | ProbSparse attention | O(L log L) | Zhou et al., AAAI 2021 | Canonical efficient transformer; selective attention |
| Autoformer | Auto-Correlation + decomposition | O(L log L) | Wu et al., NeurIPS 2021 | Progressive decomposition aligns with EDA phasic/tonic |
| FEDformer | Frequency Enhanced | O(L) | Zhou et al., ICML 2022 | Only linear-complexity candidate; frequency domain for EDA |
| DLinear | Simple linear | O(L) | Zeng et al., AAAI 2023 | Provocative baseline: do we even need transformers? |

## Dataset

- 147 participants, controlled laboratory protocol
- EDA at 4 Hz, 40s effective segments
- Binary arousal classification (calm vs. stress)
- 3 channels: SCR, ΔSCR, Δ²SCR

## Training Protocol

- AdamW, lr=1e-3, cosine annealing
- Batch size 32, max 100 epochs, early stopping patience=15
- Dropout 0.1-0.3, weight decay 1e-4, gradient clipping norm=1.0
- Hyperparameter search: L∈{1,2,3,4}, H∈{1,2,4,8}, D∈{16,32,64,128}
- Z-score normalization per fold
