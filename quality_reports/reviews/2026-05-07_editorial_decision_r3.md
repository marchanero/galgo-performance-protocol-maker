# Editorial Decision (Round 3 — Final)
**Date:** 2026-05-07
**Paper:** Efficient Transformer Architectures for Electrodermal Activity-based Arousal Classification
**Venue:** IEEE Transactions on Affective Computing (TAC)
**Decision:** **ACCEPT (Minor Revisions)**

---

## Referee Scores

| Referee | Disposition | Score | Recommendation |
|---------|------------|-------|---------------|
| Domain | BASELINE | 87/100 | Minor Revisions |
| Methods | CREDIBILITY | 90/100 | Accept |
| Consistency | SKEPTIC | 88/100 | Accept |
| **Average** | | **88/100** | |

All three referees recommend acceptance with scores above the acceptance threshold (85+).

## Referee Consensus

- **Unanimous agreement** that the paper makes a significant contribution
- **Unanimous agreement** that the methodology is rigorous
- **Unanimous agreement** that the Limitations section is exemplary
- **Minor editorial suggestions only** — no substantive concerns remain

## MUST Address (Blocking)

### M1. Add Related Work section
This remains the single blocking item carried from Rounds 1 and 2. All three referees note this gap but acknowledge that the expanded citations partially mitigate it. Add before submission. 500-800 words covering: (a) EDA-based arousal classification, (b) efficient architectures for time series, (c) SSM and modern convolution for biosignals.

## SHOULD Address (Non-blocking)

### S1. Tighten Conclusion
Domain referee suggests replacing the full architecture list with a focused 1-2 sentence summary of the key finding (Mamba ≈ PatchTST at 3.6× lower latency).

### S2. Add thop version number
Methods referee suggests adding the specific thop library version (e.g., v0.1.1) for full reproducibility.

### S3. Reconsider "non-concealable"
Consistency referee flags "non-concealable biomarker" as potentially overstrong. Consider "difficult to voluntarily control."

## Editorial Note

This paper has successfully navigated three rounds of rigorous peer review. The progression from Major Revisions (R1, scores 68-72) to Accept (R3, scores 87-90) demonstrates the authors' commitment to addressing reviewer feedback thoroughly and constructively. The paper now represents a methodological benchmark for architectural comparison in physiological signal classification.

The Editor expects to formally accept the manuscript upon receipt of the Related Work section and the minor SHOULD refinements. Congratulations to the authors on a strong contribution to IEEE TAC.
