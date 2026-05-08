# Self-Citation Analysis — BSPC Submission
**Date:** 2026-05-08
**Paper:** Efficient and Modern Architectures for EDA-based Arousal Classification

---

## Summary

| Metric | Value | Threshold | Assessment |
|--------|-------|-----------|------------|
| Unique self-cited papers | 3 of 38 keys | < 20% OK | ✅ 7.9% — acceptable |
| Self-cite instances | 23 of 39 commands | < 30% typical | ⚠️ **59% — high** |
| Most-cited self-paper | SanchezReolid2022 (12×) | — | Needs consolidation |
| Second most-cited | sanchez2020deep (9×) | — | Partially justified by baseline |

---

## Breakdown by Paper

### SanchezReolid2022 — 12 instances
*Prior comparison paper (5 DL architectures, same dataset + LOSO protocol)*

| Line | Context | Verdict |
|------|---------|---------|
| §1 L69 | "In prior work... we compared five architectures" | ✅ Keep — establishes context |
| §1 L75 | "identical 147-participant dataset and LOSO protocol as our prior work" | ✅ Keep — necessary |
| §1 L75 (same cite cmd) | Duplicated in same sentence | ⚠️ Remove duplicate |
| §2.1 L82 | "described in previous work" (dataset protocol) | ⚠️ Use sanchez2020deep instead (dataset paper) |
| §2.2 L88 | "pipeline established in our prior work" | ⚠️ Use sanchez2020deep instead (dataset protocol) |
| §2.2 L94 | "consistency with reference study" | ⚠️ Could merge with prior cite |
| §2.4 L312 | "PatchTST serves as top-performing baseline from prior work" | ✅ Keep — direct comparison |
| §3.1 L437 | Table 2 footnote — "Results reproduced from..." | ✅ Keep — table note |
| §3.1 L482 | "pattern observed in our prior work" | ⚠️ Remove — not essential |
| §3.4 L698 | Fig 7 caption: "Grey curves reproduce prior work" | ✅ Keep — figure credit |
| §3.6 L718 | "known to encode diagnostically relevant information" | ⚠️ Remove — generic claim |
| §3.7 L729 | "our prior evaluation of five architectures" | ✅ Keep — comparison context |
| §3.7 L735 | "TCN baseline from prior work" | ✅ Keep — comparison context |

**Recommended: Reduce from 12 → 8 instances** (remove 4 redundant ones)

### sanchez2020deep — 9 instances
*Deep-SVM paper + dataset protocol*

| Line | Context | Verdict |
|------|---------|---------|
| §1 L65 | Part of multi-cite with LongTermVariability + Hossain2024 | ⚠️ Remove — dataset paper not needed in intro sentence |
| §2.1 L82 | "described in a previous paper" (dataset) | ✅ Keep as primary dataset reference |
| §2.2 L94 | In preprocessing justification paragraph | ⚠️ Redundant with SanchezReolid2022 — keep only one |
| §3.1 L489 | Classical baseline discussion | ✅ Keep — defines baseline value |
| §3.1 L489 | Same sentence, same cite | ⚠️ Remove duplicate |
| §3.7 L733 | Classical baseline comparison | ✅ Keep — essential for argument |
| §3.7 L733 | Same paragraph, repeated | ⚠️ Consolidate to once per paragraph |
| §3.8 L739 | "enables direct comparison with prior work" | ⚠️ Use SanchezReolid2022 instead |
| §5 L751 | Conclusion: "F1 ≈ 0.81 on same dataset" | ✅ Keep — summarizes key finding |

**Recommended: Reduce from 9 → 5 instances** (remove 4 redundant ones)

### sanchez2022one — 2 instances

| Line | Context | Verdict |
|------|---------|---------|
| §1 L67 | "1D-CNNs processing raw SCR waveforms" | ✅ Keep — related work |
| §2.2 L95 | "information about the rate and pattern of phasic change" | ✅ Keep — derivative channel justification |

**✅ Acceptable — no reduction needed.**

---

## Recommended Actions

| # | Action | Reduction |
|---|--------|-----------|
| 1 | Remove duplicate cites in same sentence / paragraph | -5 instances |
| 2 | Use `sanchez2020deep` for dataset protocol, `SanchezReolid2022` for architecture comparison only | Clarity + reduce overlap |
| 3 | Remove generic/boilerplate self-cites (e.g., "as in prior work" without specific claim) | -3 instances |
| 4 | Consolidate multiple cites to same paper within single paragraph | -2 instances |
| **Total reduction** | | **23 → 13 instances (59% → ~33%)** |

---

## Verdict

**Not a rejection-level problem**, but the current 59% self-citation rate would draw attention from BSPC reviewers. The high count is partially justified (paper builds on prior protocol + classical baseline from same dataset), but 23 out of 39 citation commands is excessive. Reducing to ~13 instances (33%) would bring it within typical norms while preserving all essential citations.

Recommended: apply the reductions above before submission. Focus especially on removing duplicate citations within the same sentence and replacing generic "as in prior work" cites with more specific references or simply stating the fact without a citation when it's been established earlier in the paper.
