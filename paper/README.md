# JRP Protocol Paper 1 — Multimodal Passive Sensing of Cognitive Performance

**Status:** in progress — agent review completed (3 referees), corrections pending
**Target Journal:** JMIR Research Protocols (JRP)
**Paper Type:** Pre-execution study protocol
**Authors:** Herrero Albiar, García-Pérez, Martínez-López, Borja, Sánchez-Reolid, Pastor Vicedo

---

## Scope

Observational, longitudinal protocol integrating four passive multimodal streams (ambient IoT, EmotiBit wearables, semi-dry EEG, overhead body-pose estimation) with a binary teacher annotation per 5-minute window and monthly PVT external anchor. Deployed over four months in Spanish compulsory secondary education (3rd–4th ESO, ages 14–16) under GDPR Article 9 / LOPDGDD for minors.

---

## Compilation

```bash
latexmk main.tex
```

- **Engine:** XeLaTeX (configured in `latexmkrc`)
- Clean auxiliary files: `latexmk -c`

---

## Manuscript Structure (JMIR format)

| Section | File | Content |
|---------|------|---------|
| Structured Abstract | `sections/abstract_structured.tex` | Background, Objective, Methods, Results, Conclusions (300–400 words) |
| Introduction | `sections/introduction.tex` | Four conjunctive gaps in multimodal sensing, dataset scoping review, protocol overview |
| Methods | `sections/methods.tex` | Study design, population, sensor stack (ambient, EmotiBit, EEG, vision), data pipeline, teacher label, PVT, statistical analysis plan, ethics |
| Results | `sections/results.tex` | Anticipated measurement validation, planned descriptive output |
| Discussion | `sections/discussion.tex` | Principal anticipated findings, downstream AI fusion, strengths, limitations, comparison with prior work |
| Competing Interests | `sections/declaration_competing_interests.tex` | Declaration |
| Data Availability | `sections/data_availability.tex` | Tiered-access: open code + aggregated features / restricted raw signals |
| Privacy Appendix | `sections/privacy_appendix.tex` | Operational privacy pipeline (72h video deletion, audio disable, pseudonymisation) |

---

## Figures

| File | Section | Description |
|------|---------|-------------|
| `figuras/arquitectura_galgo.png` | Methods | High-level architecture of the synchronised multimodal IoT platform |
| `figuras/dashboard.png` | Discussion | Galgo-Hub proof-of-concept teacher dashboard |

---

## Revision Log

### Version 1 — Initial draft
- **Date:** 2026-06-05
- **Description:** First complete draft of the JRP protocol manuscript. Structured abstract, full Methods section (4 modalities, MQTT/QoS 2 pipeline, teacher label, PVT, SAP), anticipated Results, Discussion with downstream AI fusion use cases (thermal stress, cognitive overload, classroom disruption), privacy appendix, data availability.
- **Pending:** CEIS-UCLM reference number, consent campaign completion, GITHUB URL, Zenodo DOI, IRRID.

### Agent Review — 2026-06-05
- **Reviewers:** domain-referee (73/100), methods-referee (76/100), consistency-referee (71/100)
- **Recommendation:** Major Revisions

**Issues flagged by all 3 referees:**
1. Sync latency inconsistency: Abstract claims `<15 ms guarantee`, Methods/Results use `≤100 ms / ≤50 ms` acceptance criteria.
2. "Zero packet loss" claim not verifiable — MQTT QoS 2 provides exactly-once delivery, not physical-layer loss guarantees. No packet-loss validation protocol described.
3. ORCID duplication for Alejandro L. Borja (displays García-Pérez's ORCID).
4. Scoping review cited as foundational warrant 4+ times but methodology not documented in paper — referee cannot verify the conjunctive-gap claim.
5. Downstream AI fusion / dashboard section too speculative for pre-execution protocol.

**Domain referee (73):** 15+ papers missing from citations (Fuentes-Martinez 2023, Wargocki 2020, PVT-adolescent studies: González-Fernández 2021, DiFrancesco 2019, Ballester 2015). Protocol not registered (ClinicalTrials.gov/OSF). No JRP editorial cited (Eysenbach 2004).

**Methods referee (76):** SAP under-specified — correlation coefficient type unnamed, hierarchical data structure not acknowledged, missing data handling limited to reporting. EmotiBit sampling rates not specified. DPIA status: filed vs approved. 4:1 session imbalance between groups not discussed as analytical confound.

**Consistency referee (71):** VPN architecture contradiction (Tailscale/WireGuard in Methods vs institutional mutual-TLS in Privacy Appendix). IMU specification inconsistent (9-axis in Methods vs tri-axial in all other sections). Live RTSP camera feed on dashboard not documented in privacy appendix. "AI fusion engine" in architecture diagram has no corresponding Methods subsection.

### Alternate journals considered
| Journal | IF | Fit | Notes |
|---------|-----|-----|-------|
| BMJ Open | 2.9 | Published closest precedent (Palacios Temprano 2020) | Accepts protocols |
| Sensors (MDPI) | 3.4 | Max MMLA+sensor thematic fit | No protocol article type |
| PLoS ONE | 3.7 | Multidisciplinary, accepts protocols | Broad reach |
| BJET | 5.5 | Highest IF, EdTech prestige | May require empirical data |
| **JMIR Research Protocols** | **1.7** | **Current target** | **Protocol-specific journal** |

---
