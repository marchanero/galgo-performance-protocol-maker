# Final Peer Review — Consolidated Decision
**Date:** 2026-05-07
**Paper:** Efficient and Modern Architectures for Electrodermal Activity-based Arousal Classification
**Venue:** IEEE Transactions on Affective Computing (TAC)
**Decision:** **ACCEPT**

---

## Referee Scores (Final Round)

| Referee | Disposition | Score | Recommendation |
|---------|------------|-------|---------------|
| Domain | BASELINE | 92/100 | Accept |
| Methods | CREDIBILITY | 93/100 | Accept |
| Consistency | SKEPTIC | 92/100 | Accept |
| Language | — | 91/100 | Accept (advisory) |
| **Average** | | **92/100** | |

---

## What Was Checked (This Round)

1. **Data consistency** — All tables, figures, and text cross-verified. Zero numerical discrepancies after Fig 6 plateau offset was explained (sliding vs non-overlapping windows).
2. **Cross-references** — 9 `\ref{}` labels all resolve. 31 `\cite{}` keys all in bibliography. Zero broken references.
3. **Results language** — All speculative/conditional language removed. Results section now reports findings declaratively.
4. **Supplementary integrity** — All 4 tables (S1-S4) cited in main text. Numerical ranges corrected to match actual data.
5. **Figure captions** — All match plot content. Pareto thresholds (1.5ms/4ms) consistent across caption, plot, and body text.
6. **Abstract precision** — "matching" → "approaching" to reflect the statistically significant 0.005 F1 difference.
7. **DOIs** — 31 cited entries have verified DOIs. Remaining uncited entries left as-is.
8. **Supplementary further reading** — 14 additional references organized by category.

---

## Paper Statistics

| Metric | Value |
|--------|-------|
| Lines | 763 |
| Sections | 4 |
| Subsections | 13 |
| Figures | 6 |
| Tables (body) | 3 |
| Tables (supplementary) | 4 |
| Citations | 31 (all verified) |
| Estimated pages (LNCS) | 16-18 |

---

## Strengths (Unanimous)

1. **Methodological rigor** — LOSO with 147 participants, equal hyperparameter tuning budget (64 configs), 5 complementary efficiency metrics, honest limitations section.
2. **Novel comparison** — First systematic evaluation of Transformers, SSMs, and modernised convolutions for EDA under LOSO.
3. **Practical value** — Pareto frontier directly informs architecture selection for edge deployment. Channel ablation provides actionable input design guidance.
4. **Presentation quality** — 6 publication-quality figures with consistent ColorBrewer palette, clean table design, well-organized supplementary material.
5. **Transparency** — Limitations section honestly addresses single-dataset constraint, hardware dependency, and Wilcoxon test assumptions.

## No Remaining Issues

All concerns from previous rounds have been resolved. The paper is methodologically sound, internally consistent, and well-written. No blocking issues remain.

## Editorial Note

This paper successfully navigated 5 rounds of peer review, progressing from Major Revisions (R1, 68-72) to Accept (R5, 91-93). The authors' thorough and constructive engagement with reviewer feedback has produced a manuscript that sets a methodological standard for architectural comparison in physiological signal classification. 

**ACCEPT. Ready for submission.**
