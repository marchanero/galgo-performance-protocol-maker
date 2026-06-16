# Protocol-Specialist Referee Report

**Paper:** Multimodal Passive Sensing of Cognitive Performance in Spanish Compulsory Secondary Education Classrooms: Protocol for an Observational, Longitudinal Study  
**Target Journal:** JMIR Research Protocols  
**Calibrated to:** JMIR Research Protocols + MMLA/education/sensing domain (domain-profile.md)

---

## Dimension Scores

| # | Dimension | Score | Notes |
|---|-----------|-------|-------|
| 1 | Research Question & Hypotheses | 78/100 | 4 pre-specified hypotheses are a strength. H1-H4 are directional, falsifiable, with declared consequences. Gap: the overarching research question ("can we passively measure cognitive performance?") is implicit but never stated as a single sentence. |
| 2 | Study Design | 76/100 | Observational longitudinal with comparison group is appropriate. Population, setting, recruitment well described. Gap: sample size is window-based (~16,000 windows) but participant count is indeterminate ("class-complete"). A reviewer will ask: how many students is that? EEG sample (16 sessions) is honestly acknowledged as underpowered. |
| 3 | Pre-registration & Transparency | 45/100 | This is the weakest dimension. Protocol is NOT registered (OSF/ClinicalTrials.gov). No SPIRIT statement. No PRISMA-P for the scoping review (scoping review is no longer claimed as protocol methodology). IRRD is placeholder. Ethics reference is pending. These are desk-reject risks at JMIR. |
| 4 | Ethics & Data Governance | 75/100 | Privacy appendix (A-F) is operationally verifiable — SHA-256 hashes, governance logs, AES-256-GCM, 72h video deletion. This is excellent. Gap: no independent data monitor. Who enforces the privacy guarantees? CEIS reference pending blocks this dimension from scoring higher. |
| 5 | Statistical Analysis Plan | 80/100 | 4-stage Data Analysis Plan is coherent. Signal processing → validation → descriptive → fusion. SAP pre-specifies: Spearman's ρ, complete-case analysis, missing data reporting, hierarchical data structure. ML architecture is specific (XGBoost + 1DCNN + TCN → LR). Gap: no minimal detectable effect calculation for H2 or H3. |
| 6 | Anticipated Results & Discussion | 82/100 | Abstract Results = pure status/timeline ✓ (JMIR convention). Discussion has: anticipated findings, downstream applications (brief, scientific), strengths, comparison, construct validity, falsifiability, 7 limitations, conclusions. Strengths: falsifiability thresholds are rare and commendable. Limitations are honest and specific. |
| 7 | Format Compliance | 85/100 | Structured abstract (363w <450) ✓. AMA numeric citations ✓. Sentence case headings ✓. CRediT ✓. Data availability ✓. IRRD placeholder ✓. Gap: no "Protocol" label before title (JMIR may typeset this; not blocking). No SPIRIT checklist. |

---

## WEIGHTED TOTAL

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| 1. RQ & Hypotheses | 78 | 0.20 | 15.60 |
| 2. Study Design | 76 | 0.20 | 15.20 |
| 3. Pre-registration | 45 | 0.10 | 4.50 |
| 4. Ethics & Governance | 75 | 0.15 | 11.25 |
| 5. SAP | 80 | 0.15 | 12.00 |
| 6. Results & Discussion | 82 | 0.10 | 8.20 |
| 7. Format | 85 | 0.10 | 8.50 |
| **TOTAL** | | | **75.25/100** |

---

## Major Concerns

### MC1. Protocol not registered (dimension 3 — 45/100)
JMIR "strongly recommends" protocol registration. PLoS ONE requires it. BMJ Open requires it. Without registration, this paper is not following the most basic transparency norm for protocol papers. **Register on OSF (osf.io) — free, takes 5 minutes.** Add the registration number to the abstract and methods.

**What would change my mind:** OSF registration link in the manuscript.

### MC2. Ethics reference is PENDING (dimension 4)
A protocol paper cannot be published without ethics approval. If the CEIS-UCLM evaluation is genuinely pending, the paper should state that clearly and consistently. Currently the language is unified across files, which is good, but the substance (no reference number) remains.

**What would change my mind:** CEIS-UCLM reference number in the manuscript.

### MC3. Overarching research question is implicit (dimension 1)
The paper states 4 hypotheses but never articulates the single question that ties them together. I had to infer it. Add one sentence to the Introduction: "The overarching research question is whether a multimodal passive sensing platform can [measure/predict/characterise] cognitive performance in ordinary secondary education classrooms."

**What would change my mind:** A single, explicit research question sentence in the Introduction.

---

## Minor Concerns

### m1. No SPIRIT statement
While SPIRIT is designed for clinical trials, JMIR recommends it for all protocols. A brief sentence acknowledging SPIRIT (even if noting it was consulted but the protocol is observational) shows awareness.

### m2. EEG sample not explicitly in the abstract
The abstract mentions EEG but not that it's one participant per week for 16 sessions. For transparency, consider adding "on one participant per week" to the abstract Methods.

### m3. Comparison group rationale could be stronger
The comparison group provides PVT and teacher labels without sensors. The methods now specify this clearly, but the value proposition is: "within-school reference for label and PVT distributions." This is thin. Consider adding what specific question the comparison group answers.

---

## Recommendation

**MAJOR REVISIONS** (75.25/100)

The paper is substantially stronger than a typical first-submission protocol. The 4 hypotheses, operational privacy appendix, specific ML architecture, and falsifiability thresholds are genuine methodological contributions. However, **no protocol can be published without (a) ethics approval and (b) pre-registration.** These are basic transparency norms, not editorial preferences. Resolve MC1-MC3 and this paper is ready for submission.

---

## What I Particularly Like

1. **Falsifiability thresholds** — stating what happens if H1 fails (platform redesign before ML) is rare and scientifically honest
2. **Privacy appendix** — operational, verifiable, with hashes and logs. This is how privacy should be documented
3. **4-stage Data Analysis Plan** — leads with signal processing, which is the paper's real strength
4. **Specific ML architecture** — XGBoost + 1DCNN + TCN → LR is pre-registerable; no algorithm shopping
5. **Honest limitations** — 7 specific, substantive limitations, not generic "more research needed"

These 5 items distinguish this protocol from the median JMIR submission.
