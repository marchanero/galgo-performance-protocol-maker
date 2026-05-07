# Clo-Author: AI Research Architecture for CS/AI & Engineering

[![Version](https://img.shields.io/badge/version-4.0--csai-b44dff?style=flat-square)]()
[![Field](https://img.shields.io/badge/field-CS%2FAI%20%7C%20Engineering-3182BD?style=flat-square)]()
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Agents](https://img.shields.io/badge/agents-23-orange?style=flat-square)]()
[![Paper](https://img.shields.io/badge/paper-ACCEPT-31A354?style=flat-square)](https://github.com/marchanero/eda-efficient-transformers)

> **Fork of [hugosantanna/clo-author](https://github.com/hugosantanna/clo-author)** — adapted for Computer Science, Artificial Intelligence, Biomedical Engineering, and ICT research. Battle-tested through 4 rounds of peer review on a real paper accepted at IEEE TAC.

An open-source [Claude Code](https://docs.anthropic.com/en/docs/claude-code) scaffold for ML/AI and engineering research. Provides structured workflows from literature review to venue submission with 23 specialized agents for experimental design, code review, paper writing, diagram creation, language editing, and multi-referee peer review simulation.

> **Fork of [hugosantanna/clo-author](https://github.com/hugosantanna/clo-author)** — adapted for Computer Science, Artificial Intelligence, Biomedical Engineering, and ICT research. Adds ML/DL experiment design, efficient architectures, SSM paradigms, and TikZ diagramming agents.

An open-source [Claude Code](https://docs.anthropic.com/en/docs/claude-code) scaffold for ML/AI and engineering research. Provides structured workflows from literature review to venue submission with specialized agents for experimental design, code review, paper writing, diagram creation, and peer review simulation.

---

## What Makes This Fork Different

The original `clo-author` targets empirical economics (causal inference, DiD/IV/RDD, AEA journals). This fork adapts every agent, rule, and reference for CS/AI and engineering research:

| Aspect | Original (Economics) | This Fork (CS/AI & Engineering) |
|--------|---------------------|----------------------------------|
| **Paper types** | Reduced-form, Structural, Theory+empirics, Descriptive | Novel architecture, Benchmark, Ablation study, Application/deployment |
| **Methodology** | Causal inference (DiD, IV, RDD, SC) | ML experiment design, training pipelines, ablation, efficiency metrics |
| **Code stack** | R (primary), Stata | Python (PyTorch/TensorFlow), GPU discipline |
| **Target venues** | AER, Econometrica, JPE, QJE... | NeurIPS, ICML, ICLR, TPAMI, TAC, TBME, JBHI... |
| **Evaluation** | Standard errors, clustering, significance stars | F1/AUC/Accuracy ± std, parameter count, FLOPs, inference time |
| **Literature** | EconLit, NBER, RePEc | arXiv, Semantic Scholar, DBLP, IEEE Xplore |
| **Datasets** | CPS, SIPP, administrative | WESAD, PhysioNet, CASE, DEAP, Papers With Code |
| **Figures** | Regression tables, event study plots | Confusion matrices, ROC curves, architecture diagrams, Pareto frontiers |
| **New agents** | — | **Diagrammer** + diagrammer-critic (TikZ figures) |
| **Color palette** | — | ColorBrewer colorblind-safe (built into preamble) |

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/marchanero/clo-author.git
cd clo-author

# 2. Open Claude Code
claude
```

Then:
> I am starting a new ML/AI research project on **[TOPIC]**. Read AGENTS.md and help me set up.

---

## 11 Agent Pairs + 1 Standalone Reviewer

Every creator has a paired critic. Critics can't edit files; creators can't score themselves. 23 agents total.

| Phase | Worker (Creates) | Critic (Reviews) |
|-------|-----------------|-----------------|
| Discovery | Librarian (CS/AI venues + DOI verification) | librarian-critic |
| Discovery | Explorer (ML/physiological datasets) | explorer-critic |
| Strategy | Strategist (experiment design) | strategist-critic |
| Execution | Coder (PyTorch training pipelines) | coder-critic |
| Execution | Data-engineer | coder-critic |
| Paper | Writer (CS/AI sections) | writer-critic |
| Figures | Diagrammer (TikZ, ColorBrewer) | diagrammer-critic |
| Language | Language-reviewer (learns author voice) | — (advisory) |
| Peer Review | Editor → domain + methods + consistency referees | — |
| Presentation | Storyteller (Beamer/Quarto) | storyteller-critic |
| Theory | Theorist | theorist-critic |
| Infrastructure | Orchestrator, Verifier | — |

---

## 10 Slash Commands

| Command | What It Does |
|---------|-------------|
| `/new-project [topic]` | Full pipeline: idea → paper (orchestrated) |
| `/discover [interview\|lit\|data]` | Research spec, literature review, data discovery |
| `/strategize [question]` | ML/DL experimental strategy + methods review |
| `/analyze [dataset]` | End-to-end experiments: training, evaluation, code review |
| `/write [section]` | Draft paper sections + humanizer pass |
| `/review [file/--flag]` | Quality reviews (paper, code, peer, methods) |
| `/revise [report]` | R&R cycle: route referee comments, draft response |
| `/talk [conference\|seminar\|short\|lightning]` | Beamer or Quarto presentation |
| `/submit [venue]` | Final gate: score ≥ 95, all components ≥ 80 |
| `/tools [subcommand]` | commit, compile, validate-bib, lint, deploy |

---

## Simulated Peer Review — 3 Independent Referees

`/review --peer [venue]` simulates a full CS/AI venue submission with **3 independent, blind referees** + optional language reviewer:

1. **Editor desk review** — novelty check, scope check, baseline adequacy, ablation completeness
2. **Referee assignment** — three referees with different dispositions (ARCHITECTURE, CREDIBILITY, REPRODUCIBILITY, BASELINE, THEORY, SKEPTIC)
3. **Independent blind reports** — domain-referee scores contribution/literature, methods-referee scores experiments/statistics, **consistency-referee** cross-references claims and detects overclaiming
4. **Editorial decision** — FATAL / ADDRESSABLE / TASTE concerns, MUST / SHOULD / MAY actions

**15 venue profiles** across CS/AI and biomedical engineering: NeurIPS, ICML, ICLR, TPAMI, JMLR, IEEE TAC, TBME, JBHI, BSPC, Sensors Journal, SPL, and more.

**Battle-tested:** This framework successfully guided a paper through 4 rounds of peer review (Major → Minor → Accept), with referee scores improving from 68-72 to 90-92.

---

## Quality Gates

Weighted aggregate scoring with per-component minimums:

| Score | Gate | Applies To |
|-------|------|------------|
| ≥ 95 | Submission | Aggregate + all components ≥ 80 |
| ≥ 90 | PR | Weighted aggregate (blocking) |
| ≥ 80 | Commit | Weighted aggregate (blocking) |
| < 80 | **Blocked** | Must fix critical/major issues |
| — | Advisory | Talks, figures (reported, non-blocking) |

---

## Project Structure

```
your-project/
├── AGENTS.md                     # Project configuration
├── .claude/                      # Agents, skills, rules, references
│   ├── agents/                   # 20 agent definition files
│   ├── skills/                   # 11 skill workflow files
│   ├── rules/                    # Quality, invariants, standards
│   └── references/               # Domain, journals, coding standards
├── paper/                        # LaTeX manuscript (source of truth)
│   ├── main.tex
│   ├── bibliography.bib
│   ├── sections/ figures/ tables/
│   ├── talks/ quarto/
│   └── replication/
├── data/                         # raw/ and cleaned/
├── scripts/                      # Python (primary), R, Julia
├── quality_reports/              # Plans, reviews, scores
├── explorations/                 # Research sandbox
└── master_supporting_docs/       # Reference papers, data docs
```

---

## Prerequisites

| Tool | Required For | Install |
|------|-------------|---------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Everything | `npm install -g @anthropic-ai/claude-code` |
| XeLaTeX | Paper compilation | [TeX Live](https://tug.org/texlive/) or [MacTeX](https://tug.org/mactex/) |
| Python ≥ 3.11 | Experiments | [python.org](https://www.python.org/) |
| PyTorch | Deep learning | `pip install torch` |
| [gh CLI](https://cli.github.com/) | GitHub integration | `brew install gh` |

Optional: R, Julia, Quarto (web slides).

---

## Key Architecture Decisions

### Section Organization (CS/AI Convention)
Two styles supported, chosen per venue:
- **Integrated** (NeurIPS/ICML): Related Work at end, Results+Discussion combined
- **Traditional** (IEEE/TPAMI): Related Work after Introduction, Results+Discussion combined

### Figure Design
- ColorBrewer colorblind-safe palette (blue1, green1, orange1, purple1, red1)
- Minimum `\scriptsize` font size, `\resizebox{\linewidth}` for page fit
- TikZ with consistent `arr`, `block`, `group` styles
- Diagrammer agent enforces these rules automatically

### Experiment Design (4 paper types)
| Type | Strategy produces |
|------|------------------|
| Novel architecture | Architecture spec + training methodology + ablation plan |
| Comparative benchmark | Fair comparison protocol + baseline selection + evaluation dimensions |
| Ablation study | Controlled component isolation + interaction analysis |
| Application/deployment | Domain adaptation + deployment constraint validation |

---

## Origin

Built on [hugosantanna/clo-author](https://github.com/hugosantanna/clo-author) (v4.x), which itself builds on [Pedro Sant'Anna's claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow). Adapted for CS/AI & Engineering by Roberto Sánchez-Reolid at Universidad de Castilla-La Mancha (UCLM) — I3A / TSI.

**Active research project:** *Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification* — [paper repo](https://github.com/marchanero/eda-efficient-transformers) — accepted at IEEE Transactions on Affective Computing after 4 rounds of peer review. This template was developed and battle-tested on that paper.

## License

MIT License. Fork it, customize it, make it yours.
