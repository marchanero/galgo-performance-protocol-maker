---
name: write
description: Draft academic paper sections using paragraph-level argument moves. Cleanup pass strips AI patterns after drafting. Replaces /draft-paper and /humanizer.
argument-hint: "[section or mode: intro | strategy | results | conclusion | abstract | full | humanize | style-guide] [file path (optional)]"
allowed-tools: Read,Grep,Glob,Write,Edit,Task
---

# Write

Draft paper sections, apply a cleanup pass, or extract a personal style guide from prior papers by dispatching the **Writer** agent.

**Input:** `$ARGUMENTS` — section name or mode, optionally followed by file path.

---

## Modes

### `/write [section]` — Draft Paper Section
Draft a specific section: `intro`, `strategy`, `results`, `conclusion`, `abstract`, or `full`.

**Agent:** Writer
**Output:** LaTeX section file in paper/sections/

Workflow:

#### 1. Context Gathering

Before drafting, read all available context:
1. Read existing paper draft in `paper/` (if it exists)
2. Read `master_supporting_docs/` for notes, outlines, research specs
3. Read most recent `quality_reports/research_spec_*.md` or `quality_reports/lit_review_*.md`
4. Read `.claude/references/domain-profile.md` for field conventions
5. Check `Bibliography_base.bib` for available citations
6. Scan `paper/tables/` and `paper/figures/` for generated output
7. Read `quality_reports/results_summary.md` if it exists (from Coder)

#### 2. Paper Type Detection

Before routing, identify the paper type from the strategy memo or existing draft:
- **Novel architecture** — New model or architectural component
- **Comparative benchmark** — Systematic comparison of existing methods
- **Ablation study** — Isolating contributions of design choices
- **Application / deployment** — Domain adaptation or deployment validation

This determines which section templates the Writer uses.

#### 3. Section Routing

Based on `$ARGUMENTS`:
- **`full`**: Draft all sections in sequence. For conferences (integrated style): Intro → Method → Experimental Setup → Results and Discussion → Related Work → Conclusion. For journals (traditional style): Intro → Related Work → Method → Experimental Setup → Results and Discussion → Conclusion. Pause between major sections for user feedback.
- **`intro`**: Draft introduction (most common request)
- **`method` or `strategy`**: Draft method/architecture section or experimental setup
- **`related-work` or `lit`**: Draft related work section (placement-aware: end-of-paper for integrated style, post-intro for traditional)
- **`results`**: Draft results and discussion — combined section with inline interpretation (default) or just results if journal requires split
- **`discussion`**: Draft standalone discussion section (only if results and discussion are split — rare in CS/AI)
- **`conclusion`**: Draft conclusion — brief in integrated style (interpretation already done in Results+Discussion), slightly longer if standalone Discussion was used
- **`abstract`**: Draft abstract (must have other sections first)
- **`experiments`**: Draft experimental setup section only (datasets, protocol, metrics, baselines)
- **No argument**: Ask user which section to draft

#### 4. Dispatch Writer

Dispatch Writer with paper type and argument-move templates for the target section. The writer drafts using paragraph types (motivation, result statement, mechanism, etc.), applies design-specific moves, then runs the cleanup pass. Save to `paper/sections/[section].tex`.

#### 5. Quality Self-Check

Before presenting the draft:
- [ ] Paper type identified and correct template used
- [ ] Section organization matches target venue conventions (integrated vs traditional)
- [ ] Every paragraph has an identifiable purpose (argument move type)
- [ ] Findings lead sentences — not buried after setup
- [ ] Each result is followed by its interpretation (Results+Discussion integrated)
- [ ] Paper-type-specific elements present (see writer.md per type)
- [ ] Every displayed equation is numbered (`\label{eq:...}`)
- [ ] All `\cite{}` keys exist in `Bibliography_base.bib`
- [ ] Introduction contribution paragraph names specific papers
- [ ] Metric values stated with numbers and precision (±std across folds)
- [ ] Efficiency claims backed by numbers (params, FLOPs, inference time)
- [ ] No banned hedging phrases
- [ ] Notation consistent throughout
- [ ] All tables/figures referenced actually exist in `paper/tables/` or `paper/figures/`

#### 6. Present to User

Present each section for feedback. Flag items that need attention:
- **TBD items:** Where empirical results are needed but not yet available
- **VERIFY items:** Citations that need user confirmation
- **PLACEHOLDER items:** Effect sizes awaiting final estimates

### `/write style-guide [paper-dir]` — Extract Personal Voice

One-shot extraction of the user's writing voice from their published or drafted papers. Produces `.claude/references/personal-style-guide.md`, which the writer auto-loads on every subsequent invocation.

**When to run:**
- Once at the start of a project, after pointing at a directory of the user's prior papers
- After publishing a new paper that shifts voice (re-run to refresh the profile)

**Input:** `$ARGUMENTS` — path to a directory containing prior papers (.tex or .pdf). If omitted, defaults to `master_supporting_docs/` and scans for .tex/.pdf files.

**Agent:** Writer (style-extraction mode)
**Output:** `.claude/references/personal-style-guide.md`

Workflow:
1. **Discover corpus.** List .tex and .pdf files in the target directory. If fewer than 2 papers found, flag and ask before proceeding (style extraction on a single paper overfits).
2. **Sample strategically.** For each paper, extract:
   - The full introduction
   - The first two paragraphs of each major section
   - The abstract and conclusion
   - A random sample of 5–10 results-section paragraphs
   This keeps context usage bounded while capturing voice variation across sections.
3. **Extract patterns.** The Writer (in style-extraction mode) produces quantitative and qualitative patterns:
   - Sentence-length distribution (median, 10th–90th pct)
   - Passive-voice frequency, first-person-plural frequency, em dash rate
   - Paragraph opening and closing moves
   - Section-architecture patterns (how introductions open, how results lead)
   - Lexicon: words used repeatedly, words demonstrably avoided
   - Hedging and comparison patterns
   - Citation conventions (textual vs. parenthetical split; papers-per-claim)
   - Tone markers and anti-patterns already stripped
4. **Write to `.claude/references/personal-style-guide.md`.** Fill every template section with quoted examples from the corpus. Never invent patterns — if a section has no evidence, write "[insufficient corpus evidence]".
5. **Present summary.** One-paragraph recap of the voice profile: sentence length, passive rate, signature lexicon, distinguishing tone markers. User confirms before the guide takes effect on subsequent `/write` calls.

Principles for the extraction:
- **Ground every claim in the corpus.** Each pattern must have at least one quoted example.
- **Extract, don't prescribe.** The guide records the author's observed behavior, not what the Writer thinks is good style.
- **Don't duplicate `domain-profile.md`.** The style guide is about voice; the domain profile is about field conventions.
- **Don't override working-paper-format invariants.** Voice doesn't trump INV-1..21.

### `/write humanize [file]` — Cleanup Pass Only
Strip AI writing patterns from existing text without rewriting content.

**Agent:** Writer (cleanup mode)
**Output:** Edited file with AI patterns removed

Strips 24 patterns across 4 categories:
- Structural: forced narrative arcs, artificial progression
- Lexical: "delve, leverage, nuanced, robust"
- Rhetorical: rule-of-three, negative parallelisms, em dash overuse
- Formatting: excessive bullet points, promotional language

---

## Section Standards

**Two organization styles — see writer.md for full details and templates.**

| Section | Length | Integrated Style (Conferences) | Traditional Style (Journals) |
|---------|--------|-------------------------------|------------------------------|
| Introduction | 800-1200 | Motivation, gap, approach, contributions, roadmap | Same |
| Related Work | 500-800 | **After Experiments**, before Conclusion; contrasts with what was shown | **After Introduction**, before Method; establishes context first |
| Method | 1000-2000 | Component walkthrough + training methodology | Same |
| Experimental Setup | 400-600 | Datasets, metrics, baselines, hyperparameters | Same |
| Results and Discussion | 800-1500 | **Combined section** — results with inline interpretation + synthesis at end | **Combined** (default for IEEE TAC/TBME/JBHI) or **split** if venue requires |
| Conclusion | 200-400 | Brief takeaway (discussion already done) | Slightly longer (discussion was integrated or separate) |

**When splitting Results and Discussion (rare, venue-dependent):**
- Results (600-1000 words): What was found — minimal interpretation
- Discussion (400-600 words): Why + what it means — synthesis, limitations, implications

---

## LaTeX Conventions

- `\citet{}` for textual citations ("Vaswani et al. (2017) proposed...")
- `\citep{}` for parenthetical citations ("...as shown in prior work \citep{vaswani2017attention}")
- `booktabs` rules (`\toprule`, `\midrule`, `\bottomrule`) — never `\hline`
- Notation protocol: `Y_{it}`, `D_{it}`, `\gamma_i`, `\delta_t`, `\varepsilon_{it}`

---

## Principles
- **This is the user's paper, not Claude's.** Match their voice and style.
- **Never fabricate results.** Use TBD placeholders.
- **Citations must be verifiable.** Only cite confirmed papers.
- **Argument moves first, cleanup second.** Draft with structure, then strip AI patterns.
