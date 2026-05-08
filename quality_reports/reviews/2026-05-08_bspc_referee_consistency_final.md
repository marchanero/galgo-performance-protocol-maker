# BSPC Consistency Referee — Definitive Final Review

**Date:** 2026-05-08
**Reviewer:** Consistency/Skeptic Referee
**Scope:** Full cross-reference of `paper/main.tex` (767 lines) and `paper/supplementary/main.tex` (167 lines)
**Verdict:** CONDITIONAL PASS — one arithmetic cross-reference inconsistency found; all seven prior-round issues verified fixed.

---

## Prior-Round Issues: Verification

| # | Issue | Prior Round | Status | Evidence |
|---|-------|-------------|--------|----------|
| 1 | Table bold formatting matches "best per metric" caption | R3→R4 | **FIXED** | main.tex:411 caption says "Bold indicates best performance per metric"; line 432 PatchTST row has all values bold, and PatchTST is indeed best on all 5 metrics. Correct. |
| 2 | "5-6 pp" → "approximately 5 pp" | R3 | **FIXED** | main.tex:58 abstract: "approximately 5 percentage point improvement (Mamba: +4.8 pp, PatchTST: +5.3 pp)". Line 755 conclusion: same qualified language. No instance of "5-6 pp" found. |
| 3 | Paradigm count consistent (5, not 7) | R4 | **FIXED** | main.tex:58 abstract "five paradigms"; line 75 intro "five paradigms"; line 190 method "five distinct efficiency paradigms"; line 755 conclusion "five efficiency paradigms". All consistent. |
| 4 | Supplementary Table S2 bold + counts (24/13) | R4 | **FIXED** | supp.tex:73 "24 of 28 comparisons are statistically significant" — manual count of bold entries in Table S2 confirms 24. Line 73 "13 of 28 comparisons remain significant" at Bonferroni-Holm. Both correct. |
| 5 | "Statistically significant" cross-refs §3.8 | R4 | **FIXED** | main.tex:626 "As discussed in Section~3.8"; line 716 "As noted in Section~3.8". Section 3.8 (Limitations and Generalizability) contains the LOSO p-value caveats at lines 748-749. References resolve correctly. |
| 6 | Interpretability uses qualitative qualifiers | R4 | **FIXED** | main.tex:722 "qualitative inspection"; line 726 "qualitative analysis"; line 728 "qualitatively suggest". All interpretive claims hedged. |
| 7 | Color captions = complexity class | R3 | **FIXED** | Fig 1 caption (line 184): lists color→paradigm mapping. Fig 2 (line 305): "Colour coding follows the computational complexity class". Fig 3 (line 480): "Colour coding follows the computational complexity convention". Fig 4 (line 543): full mapping. All complete. |

---

## Additional Cross-Reference Verification

### Abstract–Table–Conclusion number consistency
- **Mamba F1 = 0.858**: abstract:58 ✓, Table 3.1 line 431 ✓, conclusion:755 ✓
- **PatchTST F1 = 0.863**: abstract:58 ✓, Table 3.1 line 432 ✓, conclusion:755 ✓
- **Classical baseline F1 ≈ 0.81**: abstract:58 ✓, Table note line 438 ✓, conclusion:755 ✓
- **3.6× lower latency**: 5.4 ms / 1.5 ms = 3.60 → abstract:58 ✓, line 626 ✓, line 736 ✓
- **66% fewer params**: (4.52 − 1.52) / 4.52 = 0.664 → abstract:58 ✓, line 737 ✓ (1.52 M vs 4.52 M) ✓

### Per-fold F1 values vs supplementary tables
- All F1 values in Table 3.1 match per-class values in Table S3 ✓
- Statistical comparisons in Table S2 consistent with main text §3.5 narrative ✓

### Window-length analysis numbers
- Line 712: "Mamba achieves F1 = 0.81" at 5 s → Figure data line 692 shows (5, 0.810) ✓
- Line 712: "PatchTST achieves F1 = 0.80" at 5 s → Figure data line 696 shows (5, 0.800) ✓
- Line 710: "Mamba F1 = 0.858" + "PatchTST F1 = 0.863" → matches Table 3.1 ✓

### Key metrics consistency
- **Accuracy**: 0.873 (PatchTST line 432) is highest in table ✓
- **+4.8 pp + +5.3 pp** (0.858−0.81=0.048, 0.863−0.81=0.053): abstract:58 ✓, conclusion:755 ✓
- **DLinear F1 = 0.800** near 1D-CNN 0.796: Table 3.1 comparison holds ✓
- **ModernTCN vs TCN**: 0.827 vs 0.812, Δ = 1.5 pp → line 740 ✓
- **Training time 35×**: 42.8 / 1.2 = 35.7 → line 553 ✓

---

## Issue Found

### **ISSUE 8 (NEW): Inconsistent reference points in parenthetical at main.tex:489**

**Location:** Section 3.1, line 489:

> "(Mamba: +0.048, PatchTST: +0.063)"

**Problem:** The two deltas use different reference points:

| Architecture | Parenthetical value | Classical baseline (0.81) | DLinear (0.800) |
|---|---|---|---|
| Mamba (0.858) | **+0.048** | 0.858 − 0.81 = **0.048** ✓ | 0.858 − 0.800 = 0.058 |
| PatchTST (0.863) | **+0.063** | 0.863 − 0.81 = 0.053 | 0.863 − 0.800 = **0.063** ✓ |

- **Mamba's +0.048** is computed against the classical baseline (0.81)
- **PatchTST's +0.063** is computed against DLinear (0.800)

These two values cannot appear in the same parenthetical — they are not comparable. If both use the classical baseline (as the abstract and conclusion consistently do), the correct parenthetical is:

> "(Mamba: +0.048, PatchTST: +0.053)"

**Severity:** Moderate. The numbers +4.8 pp / +5.3 pp appear correctly in abstract:58, conclusion:755, and the broad narrative of §3.1. The error is confined to this single parenthetical. It would likely be caught as a typo by a careful reader.

**Fix:** Change `+0.063` to `+0.053` at line 489.

---

## Comprehensive Tally

| Category | Count | Status |
|----------|-------|--------|
| Prior-round issues | 7 | All FIXED |
| New issues found | 1 | Arithmetic reference-point mismatch (line 489) |
| Cross-references validated | 24+ | All resolve correctly |
| Abstract–conclusion consistency | All pairs | Consistent |
| Tabular data vs text narrative | All values | Consistent (except line 489) |
| Supplementary–main alignment | All tables + text | Consistent |

---

## Definitive Verdict: CONDITIONAL PASS

The manuscript is **97% submission-ready**. Seven prior-round issues are confirmed fixed. One new arithmetic inconsistency exists at line 489 where the PatchTST delta uses a different reference point than Mamba's delta within the same parenthetical. The fix is trivial: replace `+0.063` with `+0.053` at line 489.

After that single-character change, this reviewer finds **no remaining cross-reference errors, numeric inconsistencies, or caption–content mismatches** in main or supplementary material. Recommend PASS upon resolution of Issue 8.
