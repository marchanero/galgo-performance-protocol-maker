---
name: strategize
description: Design identification strategy, pre-analysis plan, or formal theory section. Dispatches Strategist / Theorist (proposer) and the paired critic (validator). Replaces /identify and /pre-analysis-plan.
argument-hint: "[mode: strategy | pap | pap interactive | theory] [research question or spec path]"
allowed-tools: Read,Grep,Glob,Write,Task
---

# Strategize

Design an experimental strategy (novel architecture, benchmark, ablation, or deployment) by dispatching the **Strategist** and its paired critic.

**Input:** `$ARGUMENTS` — mode keyword followed by research question or path to research spec.

---

## Modes

### `/strategize [question]` or `/strategize strategy [question]` — Experimental Strategy
Design the ML/DL experimental strategy.

**Agents:** Strategist → strategist-critic
**Output:** Strategy memo + experimental design + ablation plan + baseline selection

Workflow:
1. **Pre-Strategy Report (mandatory).** Before proposing any strategy, the Strategist must output a structured report proving it read the discovery inputs:

```markdown
## Pre-Strategy Report
**Research spec:** [path or "not found"]
**Literature review:** [path or "not found"]
**Data assessment:** [path or "not found"]
**Domain profile:** [loaded / not found]

**Research question:** [one sentence from spec]
**Key findings from literature:**
- [What architectures/methods have been used for this task]
- [What gaps remain]
**Available data:**
- [Dataset name] — [subjects, samples, classes, access]
**Task type:** [classification / regression / representation learning]
**Candidate paper type from domain profile:** [novel architecture / benchmark / ablation / application]

Proceeding to strategy design.
```

If research spec, literature review, or data assessment are missing, the Strategist proceeds with ASSUMED placeholders — but flags each clearly.

2. Read .claude/references/domain-profile.md for common identification strategies in the field
3. Dispatch Strategist to produce:
   - Strategy memo: paper type, architecture design, training methodology, evaluation strategy
   - Experimental design: detailed protocol (splits, metrics, baselines, tuning)
   - Ablation plan: ordered list of ablations with justification
   - Baseline selection: which baselines and why; tuning budget allocation
4. Dispatch strategist-critic to review through 4 phases:
   - Phase 1: Claim identification (paper type, approach, task, dataset)
   - Phase 2: Core experimental design (assumption checks, sanity checks)
   - Phase 3: Experimental execution soundness (data integrity, training integrity, statistical rigor)
   - Phase 4: Polish and completeness (robustness, sensitivity, citations)
5. If CRITICAL issues found, iterate (max 3 rounds per three-strikes)
6. Save memo to `quality_reports/strategy_memo_[topic].md`
7. Save review to `quality_reports/strategy_memo_[topic]_review.md`
8. **Save decision record** → `quality_reports/decisions/strategy_[topic].md`
   Record:
   - **Decision:** The chosen paper type (novel architecture, benchmark, ablation, application)
   - **Alternatives:** Other paper types or approaches considered
   - **Why rejected:** For each alternative, the specific reason
   - **Key design choices:** Architecture components, experimental protocol, baseline selection
   - **What would invalidate:** What findings would force a redesign (poor baseline reproduction, implausible results, data limitations)

### `/strategize preregister [spec]` — Pre-Registration Plan

Draft a pre-registration plan for ML experiments.

**Input:** `$ARGUMENTS` — path to research spec file, a topic, or `interactive` for guided interview.

- If `$ARGUMENTS` includes a file path: read it (research spec from `/discover interview`)
- If `$ARGUMENTS` includes `interactive`: conduct the guided interview (see below)
- Otherwise: treat as topic and draft with ASSUMED placeholders marked clearly

**Agents:** Strategist (in pre-reg mode)
**Output:** Pre-registration plan document

#### Interactive Pre-Reg Interview (6-Question Guided Flow)

When invoked as `/strategize preregister interactive`, ask these questions one at a time:

1. **What is the research question/hypothesis?**
2. **What is the paper type?** (novel architecture / benchmark / ablation / application)
3. **What datasets and evaluation protocol?** (name, splits, LOSO if subject-dependent)
4. **What is the primary metric and expected effect size?**
5. **What baselines will be compared?** (with justification for each)
6. **What ablation studies are pre-specified?** (with expected outcomes)

After all 6 answers are collected, proceed to drafting.

#### Pre-Reg Sections

1. **Study overview** — research question, paper type, task, dataset
2. **Architecture/method description** — key design elements before experiments
3. **Evaluation protocol** — data splits, metrics hierarchy (primary/secondary), cross-validation
4. **Baselines** — selection criteria, tuning budget, implementation details
5. **Ablation plan** — pre-specified ablations with hypotheses
6. **Statistical analysis plan** — significance tests, multiple comparison corrections
7. **Hardware and implementation** — framework, GPU, seeds, training details

---

### `/strategize theory [target]` — Formal Analysis Section

Produce a formal analysis of architecture properties: complexity analysis, convergence proofs, generalization bounds, or formal comparisons.

**When to use:**
- Paper type is **novel architecture** with formal claims (convergence guarantees, complexity bounds)
- Need formal proof of efficiency claim (e.g., O(n log n) attention complexity)
- Generalization bounds or theoretical guarantees for the proposed method

**Skip this mode** for applied/empirical papers that don't make formal mathematical claims.

**Input:** `$ARGUMENTS` — research question, path to strategy memo, or path to architecture description.

**Agents:** Theorist → theorist-critic
**Output:** Theory memo + assumptions.tex + results.tex + proofs.tex + notation glossary

Workflow:
1. **Pre-Theory Report (mandatory).** Before writing any math, the Theorist must output a structured report:

```markdown
## Pre-Theory Report
**Paper type:** [novel architecture / methods contribution]
**Theoretical object(s) to produce:** [complexity bound / convergence proof / generalization bound / formal comparison]
**Architecture components to analyze:** [attention mechanism, positional encoding, etc.]
**Assumptions anticipated:** [e.g., bounded inputs, Lipschitz continuity, i.i.d. samples]
**Input dimensions:** [T timesteps, D features, H heads, L layers]
**Parameterization:** [d_model, n_heads, etc.]

Proceeding to theory drafting.
```

2. Dispatch **Theorist** to produce formal analysis.
3. Dispatch **theorist-critic** to review through 4 phases.
4. Save outputs to `quality_reports/theory/[topic]/`.

---

## Principles

- **Strategist proposes, strategist-critic critiques.** Adversarial pairing catches design flaws early.
- **Strategy memo is the contract.** Once approved, the Coder implements it faithfully.
- **Catch problems before training.** A flawed experimental design caught now saves weeks of wasted compute.
- **Multiple strategies are OK.** Present trade-offs and let the user choose.
- **The user decides.** If Strategist and strategist-critic disagree after 3 rounds, the user resolves it.
- **Pre-specification is the point.** Pre-registered experiments prevent p-hacking and cherry-picking.
- **Be honest about what's exploratory.** Label secondary analyses and ad-hoc ablations clearly.
- **Reproducibility requires documentation.** Every design choice must be recorded.
