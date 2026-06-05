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

### Agent Review — 2026-06-05 (Round 1)
- **Full report:** `quality_reports/review_round1_2026-06-05.md`
- **Reviewers:** domain-referee (70/100), methods-referee (73/100), consistency-referee (59/100), language-reviewer (63/100), editor (PASS desk review)
- **Recommendation:** Major Revisions
- **10 blocking issues** identified (JMIR compliance: abstract word count, citation style, heading case, ORCID errors, sync latency inconsistency, zero packet loss, VPN contradiction, temporal master mismatch, empirical language)
- **7 high-priority issues** (scoping review methodology, AI/dashboard section, SAP specificity, missing citations, protocol registration)
- **Net word budget:** ~8,840 words after fixes (1,160 under JMIR's 10,000 limit)

### Alternate journals considered
| Journal | IF | Fit | Notes |
|---------|-----|-----|-------|
| BMJ Open | 2.9 | Published closest precedent (Palacios Temprano 2020) | Accepts protocols |
| Sensors (MDPI) | 3.4 | Max MMLA+sensor thematic fit | No protocol article type |
| PLoS ONE | 3.7 | Multidisciplinary, accepts protocols | Broad reach |
| BJET | 5.5 | Highest IF, EdTech prestige | May require empirical data |
| **JMIR Research Protocols** | **1.7** | **Current target** | **Protocol-specific journal** |

---
