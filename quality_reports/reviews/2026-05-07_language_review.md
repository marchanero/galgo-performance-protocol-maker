# Language Review — Efficient Transformer Architectures for EDA-based Arousal Classification
**Date:** 2026-05-07
**Reviewer:** language-reviewer
**Author voice:** Extracted from reference_paper.tex (1 paper, 375 lines)
**Score:** 78/100 (advisory)

---

## Author Voice Profile

Extracted from `master_supporting_docs/supporting_papers/reference_paper.tex`:

| Metric | Value |
|--------|-------|
| Median sentence length | ~22 words |
| Spelling | British English ("generalisation", "modelling", "utilises") |
| Passive voice | Moderate (~25-30%) |
| First-person | "we" used in research gap statements, avoided in results |
| Em dash usage | "---" for parenthetical asides, ~1 per paragraph in intro |
| Citation style | Parenthetical dominant (~80%), textual only for key authors |
| Hedging | "may," "can," "potentially" — never "might" or "could possibly" |
| Comparison style | "consistently outperforms," "achieves the best balance" |
| Section openings | Direct topic statements, never rhetorical questions or quotes |

## Grammar Issues

### G1: British/American spelling inconsistency — MINOR
- **Location:** Throughout
- **Issue:** Paper uses British spelling ("generalisation," "characterisation," "modelling") which is consistent with author's prior work, but "utilize" (American) appears where "utilise" (British) is expected.
- **Current:** Not found in main.tex — British spelling is consistent throughout. ✓ No issues.

### G2: Missing subject in sentence fragment — MINOR
- **Location:** Section 1, paragraph 3
- **Current:** "PatchTST achieved the best performance (F1 = 0.852, AUC = 0.912), demonstrating that global dependency modelling through self-attention captures physiologically relevant temporal patterns more effectively than fixed convolutional receptive fields."
- **Assessment:** Grammatically correct. ✓ No issues.

## Style / Voice Issues

### S1: "Moreover" — MINOR
- **Location:** Section 2.3 (Temporal Segmentation)
- **Current:** "Moreover, two segmentation strategies were evaluated."
- **Author's norm:** Author uses "Furthermore" (reference_paper.tex) or direct statements without transitional adverbs. "Moreover" is used 0 times in reference paper.
- **Suggested:** "Two segmentation strategies were evaluated:" (remove adverb entirely, matching author's direct style)
- **Severity:** Minor

### S2: "Furthermore" overuse — MINOR
- **Count:** 2 occurrences in main.tex vs 1 in reference paper (which has fewer words). Slightly above author's norm but acceptable.
- **Locations:** Section 1 and Section 3.2
- **Suggested:** Keep current usage — within acceptable range.

### S3: "Crucially" — MAJOR
- **Location:** Section 1 (last paragraph of introduction)
- **Current:** "Crucially, we elevate computational efficiency..."
- **Author's norm:** Author never uses "Crucially" in reference paper. This is a common AI artifact.
- **Suggested:** "We elevate computational efficiency..." (remove adverb — the importance is self-evident from context)
- **Severity:** Major — AI artifact

### S4: Long sentence density in introduction — MINOR
- **Location:** Section 1, paragraph 5
- **Issue:** The paragraph describing each efficient Transformer variant contains 4 consecutive sentences over 35 words each, while author's norm is mixed lengths.
- **Suggested:** Break the Informer description sentence into two: "The Informer introduced ProbSparse self-attention [citation]. This measures query sparsity through Kullback-Leibler divergence, reducing complexity from O(L²) to O(L log L)."
- **Severity:** Minor

## AI Artifact Detection

| Flagged Term | Count | Locations | Risk |
|-------------|-------|-----------|------|
| "crucially" | 1 | Section 1 | HIGH — not in author's vocabulary |
| "notably" | 0 | — | — |
| "interestingly" | 0 | — | — |
| "remarkably" | 0 | — | — |
| "moreover" | 1 | Section 2.3 | MEDIUM — author prefers "furthermore" or none |
| "furthermore" | 2 | Sections 1, 3.2 | LOW — within acceptable range |
| "in this paper, we" | 1 | Section 1 | LOW — used once, standard in CS |
| "it is worth noting" | 0 | — | — |
| "leverage" | 0 | — | — (was in reference_paper.tex!) |
| "delve" | 0 | — | — |
| "robust" (adj.) | 2 | Sections 1, 2 | LOW — used as technical term, not filler |
| "pivotal" | 0 | — | — |
| "landscape" | 0 | — | — |
| "tapestry" | 0 | — | — |
| "showcase(s)" | 0 | — | — |
| "underscore(s)" | 0 | — | — |
| "holistic" | 0 | — | — |

**AI artifact score: LOW.** Only "crucially" is a clear artifact. The paper reads as human-written academic prose with only minor AI imprint in transitional adverbs.

## Technical Language Issues

### T1: Architecture name casing — MINOR
- **Location:** Section 2.3, ModernTCN subsection
- **Current:** "ModernTCN represents a renaissance..."
- **Assessment:** Correct. Architecture names are consistently capitalized throughout. ✓

### T2: Abbreviation consistency — MINOR
- **Location:** Abstract
- **Current:** "LOSO" used in abstract without expansion
- **Issue:** First use of "Leave-One-Subject-Out (LOSO)" appears in introduction, not abstract. Abstract should either expand or defer to body text.
- **Assessment:** In IEEE/CS style, abstract uses abbreviations without expansion if defined in body. Acceptable. ✓

### T3: Metric notation — MINOR
- **Location:** Throughout
- **Current:** Mix of "$N_{\text{params}}$" and "parameter count" in prose.
- **Assessment:** Consistent — math notation in equations, prose in text. ✓

### T4: "e.g." formatting — MINOR
- **Location:** Section 3.3
- **Current:** "(e.g., NVIDIA Jetson, Google Coral)"
- **Author's norm:** Author uses "e.g.," (with comma after) — consistent with British academic style. ✓

## Readability Assessment

| Metric | Current Paper | Author Norm (reference) |
|--------|--------------|------------------------|
| Median sentence length | ~24 words | ~22 words |
| Passive voice | ~28% | ~25-30% |
| Paragraphs with clear topic sentence | 90%+ | 85%+ |
| Sentences per paragraph (median) | 4.5 | 4 |

**Overall assessment:** The paper's readability closely matches the author's published work. Sentence length is slightly higher (24 vs 22 words median) due to the dense architecture descriptions, but this is inherent to the content. The paper reads as genuine academic prose.

---

## Summary of Suggested Edits

1. **[MAJOR]** Remove "Crucially," from Section 1 (line ~63) — AI artifact, not in author's vocabulary.
2. **[MINOR]** Remove "Moreover," from Section 2.3 — author prefers direct statements without transitional adverbs.
3. **[MINOR]** Break the 35+ word sentences in the efficient Transformer paragraph (Section 1) to improve readability — aligns with author's mixed-length pattern.
4. **[MINOR]** Consider varying paragraph opening patterns in the Introduction — 3 of 5 paragraphs open with topic-subject structure, while author's prior work varies more.

**No grammar errors detected. No spelling inconsistencies. British English is consistent throughout.**

---

## Important Note

The reference paper uses "leverage" (line 75), which would normally be flagged as a potential AI artifact. Since the author themselves uses this word in published work, it is accepted as part of their vocabulary. This demonstrates why voice extraction from the author's corpus is essential — generic AI detection rules would incorrectly flag this term.
