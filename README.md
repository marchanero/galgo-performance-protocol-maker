# A Comparative Study of Emerging Architectures for EDA-based Arousal Classification

[![Paper](https://img.shields.io/badge/paper-ACCEPTED%20(BSPC)-31A354?style=flat-square)](https://github.com/marchanero/BSPC-eda-efficient-transformers)
[![Review](https://img.shields.io/badge/review-5%20rounds-blue?style=flat-square)]()
[![LaTeX](https://img.shields.io/badge/LaTeX-XeLaTeX-orange?style=flat-square)]()
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

> **Authors:** Roberto Sánchez-Reolid, Daniel Sánchez-Reolid, Francisco Javier Celdrán, Antonio Fernández-Caballero — Universidad de Castilla-La Mancha (UCLM) — I3A / TSI

Systematic comparison of eight efficient architectures across five paradigms (patch-based attention, sparse attention, frequency-domain modelling, state space models, and modernised convolutions) for binary arousal classification from EDA signals under strict LOSO validation with 147 participants. Beyond accuracy, we introduce five computational efficiency metrics as primary evaluation dimensions, enabling Pareto-frontier characterisation.

---

## Key Results

| Architecture | Paradigm | F1 | Params | Inference (ms) |
|---|---|---|---|---|
| PatchTST | Patch attention | 0.863 | 152K | 5.4 |
| Mamba | State space model | 0.858 | 48K | 1.5 |
| Informer | Sparse attention | 0.855 | 2.5M | 3.2 |
| FEDformer | Frequency domain | 0.852 | 2.8M | 4.1 |
| ModernTCN | Modernised conv | 0.840 | 96K | 2.3 |
| Classical baseline | Signal processing | 0.81 | — | — |

Mamba achieves F1=0.858 at 1.5 ms inference time, approaching PatchTST accuracy with 3.6× lower latency and 66% fewer parameters.

---

## Structure

```
tsi_eda_paper/
├── paper/                        # Manuscript (source of truth)
│   ├── main.tex                  # Single-file LaTeX (863 lines)
│   ├── bibliography.bib          # 70 references
│   ├── supplementary.tex         # Supplementary material
│   ├── figures/                  # TikZ figures inline in main.tex
│   ├── sections/ preambles/      # Reserved for multi-file setup
│   └── elsarticle_src/           # Elsevier article class + templates
├── data/                         # EDA signals (147 participants)
├── scripts/                      # Python training/evaluation pipeline
├── explorations/                 # Research sandbox
├── quality_reports/              # Plans, logs, reviews, scores
├── master_supporting_docs/       # Reference papers and data docs
└── .claude/                      # Agents, skills, rules, references
```

---

## Compilation

```bash
cd paper && latexmk main.tex
```

Uses XeLaTeX with `elsarticle` document class. Requires TeX Live/MacTeX. `paper/latexmkrc` configures the build.

---

## Built With

This repository was developed using the **Clo-Author** framework (fork of [hugosantanna/clo-author](https://github.com/hugosantanna/clo-author)), adapted for CS/AI & Biomedical Engineering research. The framework provides 23 specialised agents for experiment design, code review, paper writing, TikZ diagramming, and multi-referee peer review simulation — battle-tested through 5 rounds of review on this paper.

## Citation

```bibtex
@article{SanchezReolid2025EfficientEDA,
  title  = {A Comparative Study of Emerging Architectures for EDA-based Arousal Classification},
  author = {S\'{a}nchez-Reolid, Roberto and S\'{a}nchez-Reolid, Daniel and 
            Celdr\'{a}n, Francisco Javier and Fern\'{a}ndez-Caballero, Antonio},
  journal = {Biomedical Signal Processing and Control},
  year   = {2025},
  note   = {Accepted}
}
```

## License

MIT License.
