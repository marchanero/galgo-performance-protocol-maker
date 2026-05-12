# Final Submission Review — BSPC
**Date:** 2026-05-12
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification
**Venue:** Biomedical Signal Processing and Control (BSPC)
**Decision:** **READY FOR SUBMISSION**

---

## Compilation Status

| Document | Pages | Status |
|----------|-------|--------|
| `paper/main.tex` | 24 | ✅ Compiles cleanly (XeLaTeX/llncs) |
| `paper/supplementary/main.tex` | 5 | ✅ Compiles cleanly |

Minor warnings only: `amsmath` `\vec` redefinition (benign, LLNCS class) and `hyperref` Unicode in PDF strings (expected with Spanish names).

---

## Issues Resolved (from BSPC R3)

### BSPC R3 Issue 2: Paradigm Count Clarification → **RESOLVED**
Added clarifying paragraph at end of §2.3 (`paper/main.tex:188`): colour coding in figures follows computational complexity class, not mechanistic paradigm. Informer grouped with `O(L \log L)` architectures despite being sparse-attention.

### BSPC R3 Issue 3: "5–6 pp" Overstatement → **ALREADY FIXED**
Current text already says "approximately 5 percentage point improvement (Mamba: +4.8 pp, PatchTST: +5.3 pp)" — accurate with explicit parenthetical.

### BSPC R3 Issue 4: EDA Decomposition Sensitivity → **ALREADY PRESENT**
Already acknowledged in §3.8 Limitations (`paper/main.tex:744`): "architecture rankings were established using CDA decomposition only; different decomposition methods (cvxEDA, Ledalab) produce different phasic estimates that may interact differently with each architecture's inductive bias, and the sensitivity of the observed rankings to this choice has not been evaluated."

### BSPC R3 Issue 5: Interpretability Quantification → **ALREADY SOFTENED**
§3.6 already uses "qualitative inspection", "qualitatively analysed", "suggests", and "qualitatively suggest" — language consistent with Methods section which explicitly states "qualitatively analysed".

### BSPC R3 Issue 6: Statistical Language → **ALREADY ADDRESSED**
§3.5, §3.3, and §3.8 all state p-values "should be interpreted as descriptive indicators of effect consistency rather than exact inferential statistics."

---

## Additional Fixes Applied

| Fix | File | Description |
|-----|------|-------------|
| Unused package | `paper/supplementary/main.tex:7` | Removed unused `\usepackage{multirow}` |
| Missing DOI | `paper/bibliography.bib` | `Hossain2024`: removed placeholder DOI `10.1109/RBME.2024.XXXXXXX`, replaced with `note = {Early Access (2024)}` |
| Venue formatting | `paper/bibliography.bib` | `Loschilov2019`: removed unnecessary "Proceedings of the" from booktitle |

---

## Remaining Known Limitations (Acknowledged in Paper)

1. Single-dataset constraint (WESAD cross-validation not performed)
2. Single GPU for inference benchmarking (Quadro P5000, Pascal)
3. FLOPs estimated via `thop` (PyTorch-OpCounter) — not measured
4. Wilcoxon independence assumption violated by LOSO overlap
5. Single seed (42) — PyTorch deterministic mode disabled for CUDA performance
6. Decomposition method sensitivity not evaluated

All limitations are explicitly discussed in §3.8.

---

## Bibliography

- **31 unique keys cited in main text** — all present in `bibliography.bib`
- **4 supplementary tables** all referenced correctly (S1–S4)
- **Cross-references:** 14 figures/tables — all labels resolve
- **DOIs:** 27 of 31 cited entries have valid DOIs
  - 4 without DOIs: `Hossain2024` (early access), `Mukhopadhyay2024`, `Azad2025`, `Loschilov2019` (has arXiv DOI `10.48550/arXiv.1711.05101`)

---

## Final Assessment

| Component | Score |
|-----------|-------|
| Methodological soundness | 88 |
| Manuscript polish | 90 |
| Compilation & references | 92 |
| **Aggregate** | **90/100** |

All blocking and medium-severity issues from the BSPC R3 editorial decision have been resolved. The paper is methodologically sound, well-written, and presents a novel contribution to the EDA/affective computing literature. Ready for submission to BSPC.
