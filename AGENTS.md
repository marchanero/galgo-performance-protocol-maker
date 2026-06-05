# AGENTS.MD -- CS/AI & Engineering Research Template

<!-- 
  TEMPLATE: Replace bracketed placeholders with your project info.
  Agents load this file every session — keep it under ~150 lines.
  
  ADAPTING: Change the "Field" line to calibrate all agents.
  See .claude/references/domain-profile.md for field-specific defaults.
  See .claude/references/journal-profiles.md for venue profiles.
-->

**Project:** [YOUR-PROJECT-NAME]
**Institution:** [YOUR-INSTITUTION]
**Field:** [YOUR-FIELD]
**Branch:** main

---

## Core Principles

- **Plan first** — enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** — compile and confirm output at the end of every task
- **Single source of truth** — Paper `main.tex` is authoritative; talks and supplements derive from it
- **Quality gates** — weighted aggregate score; nothing ships below 80/100; see `quality.md`
- **Worker-critic pairs** — every creator has a paired critic; critics never edit files
- **Auto-memory** — corrections and preferences saved via Claude Code's built-in memory system

---

## Getting Started

1. Fill in the bracketed placeholders at the top of this file
2. Run `/discover interview [topic]` to build your research specification
3. Or run `/new-project [topic]` for the full orchestrated pipeline

---

## Folder Structure

```
[YOUR-PROJECT]/
├── AGENTS.MD                    # This file
├── .claude/                     # Agents, skills, rules, references
│   ├── agents/                  # 20 agent definitions
│   ├── skills/                  # 11 workflow orchestrators
│   ├── rules/                   # Quality, invariants, standards
│   └── references/              # Domain, journals, coding standards
├── paper/                       # LaTeX manuscript (source of truth)
│   ├── main.tex                 # Primary paper file
│   ├── bibliography.bib         # Project bibliography
│   ├── sections/ figures/
│   ├── preambles/
│   └── supplementary/
│   # Removed but documented for future use:
│   #   tables/ talks/ quarto/ replication/
├── data/                        # raw/ and cleaned/
├── scripts/                     # Python (primary), R, Julia
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

## Output Organization

Output organization: by-script

---

## Current Project State

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| Paper | `paper/main.tex` | not started | [describe your paper] |
| Bibliography | `paper/bibliography.bib` | empty | [describe references] |
| Data | `data/` | empty | [describe your dataset] |
| Scripts | `scripts/` | empty | [describe your pipeline] |
| Agents | `.claude/agents/` | 24 agents | All adapted for CS/AI & Engineering |
