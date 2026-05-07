# Desk Review (Round 2)
**Date:** 2026-05-07
**Paper:** Efficient Transformer Architectures for Electrodermal Activity-based Arousal Classification (Revised)
**Reviewer:** Editor (IEEE TAC — Transactions on Affective Computing)
**Decision:** SEND TO REFEREES

---

## Changes Since Round 1

The authors have addressed several issues raised in the initial desk review:
- Broadened citation base with external EDA references (Posada-Quintero 2020, Greco 2017, Ganapathy 2021, Picard 1997/2001, Zhu 2024)
- Added AdamW citation (Loshchilov 2019)
- Added efficient transformers survey (Tay 2022) and time series classification survey (IsmailFawaz 2019)
- Clarified statistical significance framework (raw α=0.05 primary, Bonferroni-Holm secondary)
- Added "Limitations and Generalizability" subsection
- Specified hyperparameter search methodology (grid search, 64 configs)
- Added per-class metrics note and training time column
- Clarified memory measurement scope

The most significant remaining gap is the absence of a Related Work section (M2 from Round 1), which the authors have deferred.

## Novelty Check (Re-confirmed)

Web search confirms that no existing work combines PatchTST, Informer, Autoformer, TimesNet, FEDformer, Mamba, ModernTCN, and DLinear for EDA classification under LOSO. The expanded citation list strengthens the positioning.

## Quality Floor Assessment

The paper has improved since Round 1:
- Methodology section is more complete (search budget, memory scope, training time)
- Statistical framework is consistent
- Limitations are honestly discussed
- External citations provide better context

## Concerns

1. **Related Work section still missing.** This is the single largest structural gap. Without it, the reader cannot assess how this work fits into the broader literature. However, the expanded citations in the introduction partially mitigate this concern.

2. **Self-citation density is reduced but still noticeable** — the paper cites [13] (SanchezReolid2022) approximately 6 times. While this is justified (direct prior work on same protocol), additional external EDA references would further strengthen positioning.

3. **The Limitations section is a strong addition** but should be integrated into the Discussion rather than appearing as a standalone subsection before the Conclusion. In IEEE TAC format, limitations are typically discussed within the broader interpretation of results.

## Desk Decision

The revision addresses most Round 1 concerns. The paper is methodologically sound, well-structured, and makes a clear contribution. The remaining issues (Related Work, limitation placement) are addressable.

**SEND TO REFEREES.** Assigning the same referees from Round 1 to evaluate the revision.

## Referee Assignment

- **Referee 1 (Domain):** Disposition = BASELINE (same as Round 1)
- **Referee 2 (Methods):** Disposition = CREDIBILITY (same as Round 1)
