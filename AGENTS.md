# AGENTS.MD — Multi-Project Research Repository

**Repository:** galgo-performance-protocol-maker
**Institution:** Universidad de Castilla-La Mancha (UCLM) — I3A / TSI
**Branch:** main

---

## Git Sync: Dual-Repo Architecture

This repo hosts multiple projects. The `paper/` directory is synced independently to a paper-only Overleaf repo.

| Remote | URL | Pushes |
|--------|-----|--------|
| `origin` | `https://github.com/marchanero/galgo-performance-protocol-maker.git` | Full repo (root + all projects) |
| `paper` | `https://github.com/marchanero/JRP_Protocol_paper1.git` | `paper/` only (Overleaf sync) |

```bash
# Push full repo (agents, scripts, data, paper, everything)
git push origin main

# Push only paper/ to paper-only remote (Overleaf)
git subtree push --prefix=paper paper main

# Pull paper-only remote into paper/ (if Overleaf has newer changes)
git subtree pull --prefix=paper paper main
```

> **⚠️ IMPORTANT:** Never force-push to the paper remote — it breaks Overleaf sync. If rebasing is needed, use manual clone + copy + normal push.

---

## Core Principles

- **Plan first** — enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** — compile and confirm output at the end of every task
- **Single source of truth** — Paper `main.tex` is authoritative; talks and supplements derive from it
- **Quality gates** — weighted aggregate score; nothing ships below 80/100; see `.claude/rules/quality.md`
- **Worker-critic pairs** — every creator has a paired critic; critics never edit files
- **Auto-memory** — corrections and preferences saved via Claude Code's built-in memory system

---

## Folder Structure

```
galgo-performance-protocol-maker/
├── AGENTS.MD                    # This file
├── .claude/                     # Agents, skills, rules, references
│   ├── agents/                  # 24 agent definitions
│   ├── skills/                  # 11 workflow orchestrators
│   ├── rules/                   # Quality, invariants, standards
│   └── references/              # Domain, journals, coding standards
├── paper/                       # LaTeX manuscript → synced to paper remote
│   ├── main.tex                 # Primary paper file
│   ├── Bibliography_base.bib    # Project bibliography
│   ├── preamble-paper.tex       # LaTeX preamble
│   ├── sections/                # Per-section .tex files
│   ├── figuras/                 # Figures (PNG, PDF)
│   └── latexmkrc                # XeLaTeX build config
├── data/                        # raw/ and cleaned/
├── scripts/                     # Python (primary)
├── quality_reports/             # Plans, logs, reviews, scores
├── explorations/                # Research sandbox
└── master_supporting_docs/      # Reference papers and data docs
```

---

## Commands

```bash
# Paper compilation (latexmk with XeLaTeX)
cd paper && latexmk main.tex

# Talk compilation
cd paper/talks && latexmk talk.tex

# Clean auxiliary files
cd paper && latexmk -c
```

> `paper/latexmkrc` configures XeLaTeX, TEXINPUTS, and BIBINPUTS.
> On Overleaf, set compiler to XeLaTeX via Menu → Compiler.

---

## Quality Thresholds

| Score | Gate | Applies To |
|-------|------|------------|
| 80 | Commit | Weighted aggregate (blocking) |
| 90 | PR | Weighted aggregate (blocking) |
| 95 | Submission | Aggregate + all components >= 80 |
| -- | Advisory | Talks, figures (reported, non-blocking) |

---

## Skills Quick Reference

| Command | What It Does |
|---------|-------------|
| `/new-project [topic]` | Full pipeline: idea → paper (orchestrated) |
| `/discover [mode] [topic]` | Discovery: interview, literature, data, ideation |
| `/strategize [mode] [question]` | ML experiment design, pre-reg plan, theory analysis |
| `/analyze [dataset]` | End-to-end experiments: training, evaluation, review |
| `/write [section]` | Draft paper sections + humanizer pass |
| `/review [file/--flag]` | Quality reviews (paper, code, peer, methods) |
| `/revise [report]` | R&R cycle: classify + route referee comments |
| `/talk [mode] [format]` | Create/audit/compile Beamer or Quarto talks |
| `/submit [mode]` | Venue targeting → package → audit → final gate |
| `/tools [subcommand]` | commit, compile, validate-bib, lint, deploy, learn |
| `/checkpoint [--flag]` | Session handoff: memory + report + research journal |

---

## Current Project: JRP Protocol Paper 1

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| Paper | `paper/main.tex` | in progress | Multimodal passive sensing of cognitive performance in secondary education — observational longitudinal protocol |
| Target Journal | — | JMIR Research Protocols | Pre-execution study protocol |
| Authors | — | Herrero Albiar, García-Pérez, Martínez-López, Borja, Sánchez-Reolid, Pastor Vicedo | UCLM doctoral compendium (Paper 1) |
| Keywords | — | multimodal learning analytics, cognitive performance, EEG, ambient sensing, body-pose estimation, PVT, GDPR minors | |
| Data | `paper/sections/data_availability.tex` | PENDING URLs | Tiered access: open code + aggregated features / restricted raw signals |
| Analysis | `scripts/` | not started | Feature extraction, sync validation, statistical analysis plan |
| Agents | `.claude/agents/` | 24 agents | Calibrated via `.claude/references/domain-profile.md` |
