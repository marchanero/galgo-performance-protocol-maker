# galgo-performance-protocol-maker

[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

> **Authors:** José Enrique Herrero Albiar, Eloy García-Pérez, Javier Martínez-López, Alejandro L. Borja, Roberto Sánchez-Reolid, Juan Carlos Pastor Vicedo — Universidad de Castilla-La Mancha (UCLM)

Multi-project research repository for the doctoral compendium of Herrero Albiar. Current project: **Paper 1 — Multimodal passive sensing protocol for cognitive performance in secondary education**, targeting JMIR Research Protocols.

---

## Current Project: JRP Protocol Paper 1

Observational, longitudinal protocol integrating four passive multimodal streams (ambient IoT, EmotiBit wearables, semi-dry EEG, overhead body-pose estimation) with a binary teacher annotation per 5-minute window and monthly PVT external anchor. Deployed over four months in Spanish compulsory secondary education (3rd–4th ESO, ages 14–16) under GDPR Article 9 / LOPDGDD for minors.

| Component | Status |
|-----------|--------|
| Paper | `paper/main.tex` — in progress |
| Target Journal | JMIR Research Protocols |
| Agents | 24 agents calibrated for protocol papers, MMLA, GDPR |
| Data | Pre-execution — tiered access (open aggregated / restricted raw) |
| Scripts | Python: sync validation, signal quality, feature extraction |

---

## Structure

```
galgo-performance-protocol-maker/
├── paper/                        # LaTeX manuscript (Overleaf-synced)
│   ├── main.tex                  # Primary paper
│   ├── Bibliography_base.bib     # References
│   ├── preamble-paper.tex        # XeLaTeX preamble
│   ├── sections/                 # Per-section .tex files
│   └── figuras/                  # Figures
├── data/                         # raw/ and cleaned/
├── scripts/                      # Python (primary)
├── explorations/                 # Research sandbox
├── quality_reports/              # Plans, logs, reviews, scores
├── master_supporting_docs/       # Reference papers and data docs
└── .claude/                      # Agents, skills, rules, references
    ├── agents/                   # 24 agent definitions
    ├── skills/                   # 11 workflow orchestrators
    ├── rules/                    # Quality, invariants, standards
    └── references/               # Domain profile, journals, coding standards
```

---

## Git Sync: Dual-Repo Architecture

This repo syncs `paper/` independently to an Overleaf paper-only repo.

```bash
# Push full repo (agents, scripts, data, paper, everything)
git push origin main

# Push only paper/ to Overleaf
git subtree push --prefix=paper paper main

# Pull Overleaf changes into paper/
git subtree pull --prefix=paper paper main
```

| Remote | URL | Contents |
|--------|-----|----------|
| `origin` | `https://github.com/marchanero/galgo-performance-protocol-maker` | Full repo |
| `paper` | `https://github.com/marchanero/JRP_Protocol_paper1` | `paper/` only |

---

## Compilation

```bash
cd paper && latexmk main.tex
```

Uses XeLaTeX. Requires TeX Live/MacTeX. `paper/latexmkrc` configures the build. On Overleaf, set compiler to XeLaTeX via Menu → Compiler.

---

## Built With

This repository uses the Clo-Author framework for agent-assisted academic research and writing. 24 agents across 11 skills, calibrated via `.claude/references/domain-profile.md`.

## License

MIT License.
