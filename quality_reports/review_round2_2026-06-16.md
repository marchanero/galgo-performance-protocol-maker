# Agent Review — Round 2 (2026-06-16)

**Paper:** Multimodal Passive Sensing of Cognitive Performance in Spanish Compulsory Secondary Education Classrooms: Protocol for an Observational, Longitudinal Study  
**Target:** JMIR Research Protocols  
**Word count:** ~9,989 / 10,000 (tight)
**Previous round:** 10 blocking + 7 high-priority issues (Round 1, 2026-06-05)

---

## Round 1 Resolution Status

| # | Issue | Status |
|---|-------|--------|
| 1 | Abstract 526→450 words | PENDING (blocking) |
| 2 | Citation style author-year→AMA | PENDING (blocking) |
| 3 | Headings Title Case→sentence case | PENDING (blocking) |
| 4 | ORCID Borja duplicated | PENDING (blocking) |
| 5 | ORCID Herrero placeholder | PENDING (blocking) |
| 6 | Sync latency inconsistency | PENDING (blocking) |
| 7 | "Zero packet loss" unverifiable | PENDING (blocking) |
| 8 | VPN contradiction | PENDING (blocking) |
| 9 | Environmental Mote ≠ temporal master | PENDING (blocking) |
| 10 | Present-tense empirical language | PENDING (blocking) |
| 11 | Scoping review methodology undocumented | **RESOLVED** |
| 12 | Downstream AI/dashboard → Appendix | DEFERRED |
| 13 | SAP underspecified | **RESOLVED** |
| 14 | PRISMA-ScR checklist missing | **RESOLVED** |
| 15 | EmotiBit sampling rates missing | **RESOLVED** |
| 16 | 15+ missing citations | **RESOLVED** (6 added) |
| 17 | Protocol not registered | PENDING |

---

## DOMAIN-REFEREE

**Score: 72/100 → Major Revisions**

### Strengths
- The four-conjunctive-conditions gap is now clearly articulated and flows naturally from the literature review
- Scoping review methodology is appropriately referenced to the PRISMA-ScR appendix without cluttering the introduction
- New references (Wargocki 2020, Barel 2022, González-Fernández 2023, Prinsloo 2023, Hernández-Mustieles 2024) substantially strengthen the evidential base
- PVT validation in school-age populations is now explicitly supported by three new references

### Critical gaps
1. **Protocol registration missing** — No OSF/ClinicalTrials.gov registration. JMIR requires this. Blocking for submission.
2. **Comparison group instrumentation unspecified** — What sensors does the comparison group receive? Full stack? Only PVT? This is critical for interpreting the design. Mentioned but not defined.
3. **Ethics reference is [PENDING]** — CEIS-UCLM reference number and IRRID are placeholders. Must be resolved before submission.
4. **Data availability URLs are [PENDING]** — GitHub URL exists but Zenodo DOI is placeholder. Blocking.
5. **"Under review" reference in PRISMA-ScR appendix** — Item 15 says "Full characteristics reported in the companion scoping-review article (under review)" — this references an unpublished work. Either remove or change to "available from the corresponding author upon request."

### Missing domain coverage
- No discussion of the Hawthorne effect in a classroom where students are visibly monitored for 4 months
- Teacher annotation fatigue over 4 months not addressed (a single teacher annotating every 5 minutes for months)
- Comparison group may alter behavior knowing they're being compared — no contamination control discussed
- No mention of school calendar effects (exam periods, holidays, seasonal variation)

---

## METHODS-REFEREE

**Score: 74/100 → Major Revisions**

### Strengths
- EmotiBit sampling rates now specified (PPG 25 Hz, EDA 15 Hz, temp 25 Hz, IMU 100 Hz) — previously a gap
- SAP now specifies correlation type (Spearman's ρ), hierarchical structure (4 levels), and missing data strategy (complete-case, imputation deferred)
- Falsifiability thresholds in Discussion are excellent — rare and commendable in protocol papers
- Privacy-by-design appendix is operationally verifiable, not merely aspirational

### Critical issues
1. **"Zero packet loss" claim is physically unverifiable** — MQTT QoS 2 guarantees exactly-once delivery at the application layer but does not guarantee zero packet loss at the physical/link layer. The claim should be softened to "zero application-layer message loss" or "guaranteed exactly-once delivery."

2. **Sync latency: <15 ms claim vs <100 ms acceptance criterion** — The pipeline section claims a measured end-to-end error below 15 ms, but the validation section sets acceptance at ≤100 ms. These numbers are inconsistent. If the bench test achieved <15 ms, that should be reported clearly as bench-test results, not as a deployment guarantee.

3. **VPN contradiction persists** — Methods (line 68) describes Tailscale/WireGuard mesh VPN. Privacy Appendix D describes "institutional VPN with mutual-TLS authentication." These are different architectures. WireGuard uses Noise protocol, not mutual TLS. Must reconcile or choose one.

4. **Temporal master inconsistency persists** — Figure caption says "Environmental Mote acts as temporal master" but pipeline text describes NTP-based timestamping where all nodes discipline against an NTP server. The environmental mote is not a temporal master in an NTP-disciplined system. Either fix the figure caption or clarify the architecture.

5. **EmotiBit validation gap** — The paper cites the EmotiBit as validated (Montgomery 2024, Sindermann 2024) but acknowledges that "residual quality loss is expected" in adolescents (Discussion). The protocol should specify which EmotiBit-derived features are validated for adolescent wrist-worn use vs. which are exploratory.

### Methods compliance
- **JMIR SPIRIT checklist**: Not mentioned. JMIR Research Protocols recommends SPIRIT for clinical trial protocols. While this is observational, a SPIRIT adaptation or explicit waiver should be included.
- **Sample size justification**: Window-level (~10³ per participant) is valid for descriptive analysis but the EEG sample (~16 sessions) is acknowledged as underpowered. This is honest but could be strengthened with a minimal detectable effect calculation for the PVT-teacher-label correlation.

---

## CONSISTENCY-REFEREE

**Score: 68/100 → Major Revisions**

### Cross-reference audit
- All `\Cref{}` references resolve correctly ✓
- All `\ref{}` references resolve correctly ✓
- Bibliography keys match citations ✓ (verified 6 new references in .bbl)

### Terminology inconsistencies

| Term | Usage A | Usage B | Recommendation |
|------|---------|---------|---------------|
| IMU axes | "9-axis" (Methods:36) | "tri-axial accelerometry" (Intro:9, Abstract:15) | Standardize to "9-axis IMU (tri-axial accelerometer, gyroscope, magnetometer)" |
| TVOC | Appears in dashboard caption (Discussion) | Not listed in Methods environmental variables | Remove or add to Methods sensor list |
| SPL | "sound pressure level" (Intro) / "dBFS" (Methods:32) / "dB SPL" (Methods:32) / "ambient noise" (dashboard caption) | dBFS is digital full-scale; dB SPL is acoustic pressure — different units. Unify. |
| EEG frequencies | "Alpha, Beta, and Theta" (Methods:38) | "Theta" misspelled — should be "Theta" (already correct in some instances). Verify consistent spelling. |
| Groups | "group A" (Methods:5), "instrumented group" (throughout), "3rd-of-ESO group" | No formal group naming convention. Use consistent labels. |

### Structural issues
- **Dashboard section (Discussion 7-18)** advertises a product ("Galgo-Hub proof of concept") with features not addressed in Methods (live RTSP feed, attention heat maps, prescriptive alerts). This reads as promotional and creates a consistency gap between what the protocol measures and what the dashboard claims to do.
- **AI fusion engine** appears in Figure 1 caption but has no corresponding Methods subsection describing which algorithms, what input features, or what output format. Either remove from the figure or add a Methods subsection.

### Numerical/logic inconsistencies
- **<15 ms sync** (Methods:64, Abstract:16) vs **≤100/≤50 ms acceptance** (Methods:64, Results:15, Methods validation:14-15). If the measured error is <15 ms, the acceptance criterion of 100 ms is oddly generous. The acceptance threshold should be stated as a protocol requirement, and the <15 ms figure should be clearly labeled as bench-test performance.
- **EEG sample**: ~16 individual sessions is correct (4 months × ~4 weeks/month × 1 participant/week), but the rotation across 4 weekly sessions means each of the 4 participants per month gets 1 recording, not 4 sessions each. Clarify: ~16 total, ~4 per participant.

---

## EDITOR (JMIR Desk Review)

**Verdict: CONDITIONAL PASS — 8 must-fix items before submission**

### JMIR compliance checklist

| Requirement | Status |
|-------------|--------|
| Word count <10,000 | ✓ ~9,989 |
| Structured abstract | ✓ Format correct |
| Abstract word count ≤450 | ✗ Currently ~526 words — **BLOCKING** |
| AMA numbered citations | ✗ Currently author-year (biblatex style=authoryear) — **BLOCKING** |
| Sentence case headings | ✗ Currently Title Case — **BLOCKING** |
| IRRID assigned | ✗ Placeholder — **BLOCKING** |
| Ethics reference provided | ✗ [PENDING] — **BLOCKING** |
| Data availability with URLs | ✗ Zenodo DOI [PENDING] — **BLOCKING** |
| Author ORCIDs complete | ✗ 2 errors (duplicate, placeholder) — **BLOCKING** |
| Competing interests declared | ✓ |
| CRediT author contributions | ✗ Missing — JMIR requires CRediT |
| Supplementary files referenced in text | ✓ PRISMA-ScR appendix |
| PRISMA-ScR checklist included | ✓ |
| Protocol registration number | ✗ Not registered — **BLOCKING** |

### 8 Must-fix items (all inherited from Round 1, still pending)
1. Abstract: 526 → 450 words
2. Citation style: authoryear → AMA numbered
3. Headings: Title Case → sentence case
4. ORCID Borja: 0009-0008-0277-2414 → 0000-0003-2880-0678
5. ORCID Herrero: 0000-0000-0000-0000 → real ORCID
6. Ethics reference: [PENDING] → real CEIS-UCLM ref
7. IRRID: placeholder → real identifier (JMIR assigns upon submission; note "assigned upon submission" is acceptable)
8. Protocol registration: register on OSF or ClinicalTrials.gov

---

## LANGUAGE-REVIEWER

**Score: 65/100 (advisory, format-blocking)**

### AI vocabulary (flagged)

| Term | Instances | Recommendation |
|------|-----------|----------------|
| "leveraging" | Methods (MQTT paragraph was removed in round 1) | ✓ Already cleaned |
| "ecosystem" | Methods:19 ("distributed Internet of Things (IoT) ecosystem") | Replace: "distributed IoT architecture" |
| "crucial" | Methods:66 ("crucial for high-frequency") | Replace: "important for" or "required for" |
| "serves as" | Discussion:8, Results:56-57 | Replace with direct verbs |
| "Additionally" | Dashboard caption | Remove or replace with "The dashboard also" |

### Promotional language
- Discussion 7-11 reads as a product pitch for the Galgo-Hub dashboard: "thermal stress disambiguation," "cognitive overload detection," "classroom disruption scenario" with specific ppm thresholds and EEG band patterns. These are speculative use cases, not protocol commitments. JMIR reviewers will flag this as marketing, not science.
- "the AI can isolate" (Discussion:9) attributes agency to a system that doesn't exist yet.

### Grammar and style
- Mix of British ("characterise," "behavioural") and American English ("characterize" appears nowhere — consistent British English ✓)
- "in principle" (Abstract:13) vs "approved" (Abstract:17) — approval status is inconsistent in the abstract
- "TVOCs" undefined abbreviation in dashboard figure caption

### JMIR format violations
- Abstract exceeds 450 word limit (the most common desk-reject reason at JMIR)
- Citation style is author-year; JMIR uses AMA numbered
- Section headings in Title Case; JMIR requires sentence case

---

## VERIFIER

**Status: PASS ✓** (compiles with `latexmk -pdf -interaction=nonstopmode main.tex`)
- 51 pages, no LaTeX errors
- All cross-references resolve
- All citations resolve
- All figures render
- Bibliography compiles

---

## WEIGHTED AGGREGATE SCORE

| Agent | Score | Weight | Weighted |
|-------|-------|--------|----------|
| domain-referee | 72 | 0.25 | 18.0 |
| methods-referee | 74 | 0.25 | 18.5 |
| consistency-referee | 68 | 0.20 | 13.6 |
| editor | PASS* | 0.15 | -- |
| language-reviewer | 65 | 0.10 | 6.5 |
| Verifier | 100 | 0.05 | 5.0 |
| **TOTAL** | | | **61.6/100** |

*Editor: CONDITIONAL PASS — score not applicable until blocking items resolved

**Verdict: MAJOR REVISIONS**  
**Gate: Does not meet 80/100 commit threshold**

---

## PRIORITY ROADMAP

### BLOCKING (must fix before JMIR submission)
| # | Issue | Section | Effort |
|---|-------|---------|--------|
| B1 | Abstract 526 → 450 words | abstract_structured.tex | Low |
| B2 | Citation style → AMA numbered | preamble-paper.tex | Low |
| B3 | Headings → sentence case | all sections | Medium |
| B4 | Fix 2 ORCID errors | main.tex | 1 line each |
| B5 | Fix ethics reference placeholder | main.tex + methods.tex | 1 line |
| B6 | Register protocol (OSF/ClinicalTrials) | External | 1 action + 1 line |
| B7 | Add CRediT author statement | main.tex or new section | Low |
| B8 | Add SPIRIT compliance statement or waiver | methods.tex | Low |

### HIGH PRIORITY (Round 2 — new findings)
| # | Issue | Δ Words |
|---|-------|----------|
| H1 | Soften "zero packet loss" → "exactly-once delivery" | −5 |
| H2 | Reconcile sync latency claims (<15ms bench vs ≤100ms criterion) | +20 |
| H3 | Fix VPN contradiction (WireGuard vs mutual-TLS) | +30 |
| H4 | Fix temporal master inconsistency (figure caption) | 1 line |
| H5 | Specify comparison group instrumentation | +40 |
| H6 | Standardize IMU/accelerometry terminology | 5 lines |
| H7 | Fix TVOC/SPL/dBFS terminology inconsistencies | +15 |
| H8 | Move speculative dashboard use cases to Appendix or tone down | −200 |
| H9 | Fix AI vocabulary (ecosystem, crucial, serves as) | −10 |
| H10 | Remove "under review" reference in PRISMA-ScR appendix item 15 | 1 line |
| H11 | Discuss Hawthorne effect and annotation fatigue | +80 |

### ADVISORY (improve but non-blocking)
| # | Issue |
|---|-------|
| A1 | Add EmotiBit adolescent validation caveat detail |
| A2 | Calculate minimal detectable effect for PVT-teacher correlation |
| A3 | Address school calendar effects on data |
| A4 | Reconcile EEG sampling frequency band naming ("Theta" spelling) |
| A5 | Add school selection criteria to Setting subsection |

---

## Net Word Budget Impact

| Category | Δ |
|----------|---|
| Blocking fixes (B1-B8, net) | +30 |
| High priority (H1-H11, net of dashboard trim) | −15 |
| **Total net** | **~9,989 → ~10,004** (borderline — need ~15 words of trimming) |
