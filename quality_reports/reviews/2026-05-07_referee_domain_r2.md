# Domain Referee Report (Round 2)
**Date:** 2026-05-07
**Paper:** Efficient Transformer Architectures for Electrodermal Activity-based Arousal Classification (Revised)
**Field:** Affective Computing / Biomedical AI / Time-Series Deep Learning
**Referee:** Domain Expert (Disposition: BASELINE — Round 2)
**Recommendation:** Minor Revisions
**Overall Score:** 81/100

---

## Summary

The authors have substantially improved the manuscript in response to the initial review. The addition of external EDA and affective computing references (Posada-Quintero 2020, Greco 2017, Ganapathy 2021, Picard 2001) significantly strengthens the literature positioning. The new "Limitations and Generalizability" subsection demonstrates scientific maturity and honesty. The remaining issues are minor and do not threaten the paper's contribution.

---

## Dimension Scores

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Contribution & Novelty | 30% | 78 | Improved with external citations; SSM/2D paradigms remain novel for EDA; Pareto frontier is the key contribution |
| Literature Positioning | 25% | 72 | Much improved with external refs; still needs Related Work section |
| Substantive Arguments | 20% | 85 | Deployment narrative is compelling; Pareto analysis directly informs practice; physiological interpretation is solid |
| External Validity | 15% | 80 | Limitations section honestly acknowledges single-dataset constraint; LOSO provides strong internal validity |
| Venue Fit | 10% | 88 | Strong fit for IEEE TAC; practical deployment question well-addressed |
| **Weighted** | 100% | **81** | |

---

## Changes Evaluated from Round 1

### M2 (Related Work) — NOT YET ADDRESSED
The Related Work section remains absent. This was identified as FATAL in Round 1. The expanded citations in the introduction partially mitigate this but do not replace a dedicated section where the reader can find organized positioning against prior work. This is now the primary remaining structural issue.

### M4 (Self-citation density) — ADDRESSED
The addition of Posada-Quintero, Greco, Ganapathy, Picard, Zhu, Tay, IsmailFawaz, and Loshchilov substantially broadens the citation base. The paper no longer reads as primarily citing the authors' own work. Self-citations remain appropriate for the prior work [13] which established the LOSO protocol.

### S1 (Single-dataset limitation) — ADDRESSED
The new Limitations subsection (Section 3.7) is well-written and thoughtfully addresses dataset, hardware, and statistical methodology constraints. The acknowledgment of the Wilcoxon test's independence assumption violation with LOSO is particularly appreciated — this level of methodological transparency is rare in the affective computing literature.

---

## Minor Comments

1. **Limitations placement:** The "Limitations and Generalizability" subsection (3.7) appears between "Interpretability Insights" (3.6) and "Comparison with Prior Work" (3.8). Consider moving it after the comparison or integrating it into the Discussion narrative. In its current position, it interrupts the flow from results to implications.

2. **WESAD mention:** The limitations section mentions WESAD as a candidate for cross-dataset validation. If WESAD data is not available for this submission, consider noting whether the WESAD protocol (stress induction via Trier Social Stress Test) would provide complementary stress elicitation to the current audiovisual stimulus protocol.

3. **DLinear interpretation:** The results show DLinear achieving F1 = 0.800, which is competitive with 1D-CNN (0.796) from prior work [13]. This is an interesting finding that could be discussed more explicitly: does this suggest that the tonic-phasic decomposition captured by DLinear and the local feature extraction of 1D-CNN extract similar information from EDA signals?

4. **Figure 6 axis limits:** The y-axis starts at 0.68, which compresses the visual difference between architectures at plateau values. Consider starting at 0.70 or using a break in the axis to better display the 0.80-0.87 range where architectures differentiate.

5. **Per-class F1 note:** The paper mentions per-class F1 scores are "reported in the Supplementary Material." Ensure this supplementary file is included with the submission.

---

## Overall Assessment

The revision is substantially improved. The paper makes a clear, well-motivated contribution to the affective computing literature through its systematic comparison of 8 architectures under rigorous LOSO evaluation and its actionable deployment guidance via the Pareto frontier. Once the Related Work section is added and the minor structural issues are addressed, the paper meets the bar for publication in IEEE TAC.
