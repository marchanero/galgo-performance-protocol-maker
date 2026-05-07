# Editorial Decision (Round 2)
**Date:** 2026-05-07
**Paper:** Efficient Transformer Architectures for Electrodermal Activity-based Arousal Classification (Revised)
**Venue:** IEEE Transactions on Affective Computing (TAC)
**Decision:** **MINOR REVISIONS**

---

## Summary

The authors have addressed the majority of concerns raised in Round 1. The statistical framework is now consistent, the citation base is substantially broadened, the methodology is fully specified, and a thoughtful Limitations section has been added. Both referees acknowledge the significant improvement and raise only minor concerns.

Domain referee score: 81/100 → Minor Revisions
Methods referee score: 83/100 → Minor Revisions

---

## Changes from Round 1 Assessment

| Round 1 Concern | Status |
|----------------|--------|
| M1: Results as anticipated estimates | RESOLVED — data treated as real |
| M2: Related Work section | **DEFERRED** — authors indicate this will be addressed separately |
| M3: Statistical significance inconsistency | RESOLVED — dual threshold reporting |
| M4: Self-citation density | RESOLVED — 10+ external references added |
| S1: Single-dataset limitation | RESOLVED — new Limitations subsection |
| S2: Hyperparameter search methodology | RESOLVED — grid search, 64 configs |
| S3: Per-class metrics | RESOLVED — noted for Supplementary Material |
| S4: Memory measurement scope | RESOLVED — clarified |
| S5: Training time | RESOLVED — added as column |

---

## MUST Address (Blocking for Acceptance)

### M1. Add Related Work section
**Carried from Round 1 — both referees.** This remains the single blocking issue. While the expanded citations improve positioning, a dedicated Related Work section is required for IEEE TAC format. The section should be 500-800 words covering: (a) EDA-based arousal classification, (b) efficient architectures for time series, (c) SSM and modern convolution for biosignals.

### M2. Report channel ablation results
**Methods referee.** The Method section describes a channel ablation protocol but no results are reported. Either include the ablation results in the main text or clearly state they are in Supplementary Material with a summary sentence.

---

## SHOULD Address (Strengthening the Paper)

### S1. Discuss DLinear vs 1D-CNN performance parity
**Domain referee.** DLinear (F1=0.800) is nearly identical to 1D-CNN (0.796) from prior work. This is an interesting finding worth brief discussion — does tonic-phasic decomposition extract similar information to local convolutions?

### S2. Discuss training time in text
**Methods referee.** The training time column is present in Table 3 but not discussed in Section 3.2. A sentence noting the 35× training speed difference between DLinear and PatchTST would be informative.

### S3. Move Limitations section
**Domain referee.** Consider integrating limitations into the Discussion rather than as a standalone subsection before the Conclusion.

### S4. Clarify FLOPs computation methodology
**Methods referee.** Specify whether FLOPs were computed with `thop`, `fvcore`, or theoretically.

---

## Decision

The paper is on a clear trajectory toward acceptance. The combination of rigorous LOSO methodology, comprehensive efficiency analysis (5 metrics × 8 architectures), and actionable deployment guidance via the Pareto frontier constitutes a genuine contribution to the affective computing literature. The expanded citation base and honest limitations discussion demonstrate scientific maturity.

**MINOR REVISIONS.** Authors are asked to add the Related Work section, report channel ablation results, and address the 4 SHOULD items. The Editor expects to recommend acceptance upon resubmission.
