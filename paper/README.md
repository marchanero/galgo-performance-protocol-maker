# JRP Protocol Paper 1 — Multimodal Passive Sensing of Cognitive Performance

**Status:** Ready for submission — CEIS approved, JMIR compliant  
**Target Journal:** JMIR Research Protocols (JRP)  
**Paper Type:** Pre-execution study protocol  
**Authors:** Herrero Albiar, García-Pérez, Martínez-López, Borja, Sánchez-Reolid, Pastor Vicedo  
**Ethics:** CEIS-UCLM (reference CEIS-738323-C7M2)

---

## Scope

Observational, longitudinal protocol integrating four passive multimodal streams (ambient IoT, EmotiBit wearables, semi-dry EEG, overhead body-pose estimation) with a BOSS (Behavioral Observation of Students in Schools) 5-code annotation system applied by the teacher via an ad-hoc application when a transformer-like encoder detects changes in classroom dynamics. A monthly PVT provides external convergent validation. Deployed over four months in Spanish compulsory secondary education (3rd–4th ESO, ages 14–16) under GDPR Article 9 / LOPDGDD for minors. The protocol establishes the measurement infrastructure for an eventual autonomous attention monitoring system.

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
| Structured Abstract | `sections/abstract_structured.tex` | Background, Objective, Methods, Results, Conclusions (≤450 words) |
| Introduction | `sections/introduction.tex` | Gap, technology review, 4 conjunctive properties, 4 hypotheses (H1-H4) |
| Methods | `sections/methods.tex` | Study design, population, sensor stack, BOSS annotation, PVT, data pipeline, Data Analysis Plan (4 stages), ethics |
| Results | `sections/results.tex` | Current status, 5 method validation protocols, anticipated characterisation |
| Discussion | `sections/discussion.tex` | Anticipated findings, autonomous system vision, strengths, limitations, comparison, construct validity, falsifiability |
| End Sections | `sections/declaration_competing_interests.tex` | Acknowledgements, Funding, CRediT, Conflicts of Interest, Abbreviations (23 terms) |
| Data Availability | `sections/data_availability.tex` | Tiered access: open code + aggregated features / restricted raw signals |
| Privacy Appendix | `sections/privacy_appendix.tex` | Operational privacy pipeline (72h video deletion, audio disable, pseudonymisation) |

---

## Figures

| File | Section | Description |
|------|---------|-------------|
| `figuras/arquitectura_galgo.png` | Methods | High-level architecture of the synchronised multimodal IoT platform |
| `figuras/dashboard.png` | Discussion | Proof-of-concept teacher dashboard |

---

## Key Features

- **4 pre-specified hypotheses** (H1 acquisition feasibility, H2 multimodal prediction, H3 fusion gain, H4 ground-truth quality)
- **BOSS 5-code annotation** (AET, PET, OFT-P, OFT-M, OFT-V) via transformer-like encoder + teacher app
- **Specific ML architecture** (XGBoost + 1D-CNN + TCN → logistic regression meta-learner)
- **Operational privacy-by-design** (72h video deletion with SHA-256 attestation, audio disabled at hardware level)
- **Falsifiability thresholds** (pre-committed corrigendum if platform fails to deliver)
- **JMIR compliant** (AMA numeric citations, structured abstract ≤450w, sentence case headings, CRediT, Funding, Abbreviations)

---

## Revision Log

### Version 3 — Pre-submission (2026-06-16)
- BOSS 5-code system replaces binary teacher label
- Transformer-like encoder for video event detection
- Teacher annotates via ad-hoc app (event-driven, not fixed 5-min)
- Data Analysis Plan restructured (4 stages, signal processing leads)
- Autonomous system vision added (teacher-free once validated)
- CEIS-UCLM reference inserted (CEIS-738323-C7M2)
- JMIR submission checklist completed (Funding, AI disclosure, Abbreviations)
- 6 new references added (Wargocki 2020, Barel 2022a/b, González-Fernández 2023, Prinsloo 2023, Hernández-Mustieles 2024)
- 3 BOSS references added (Shapiro 2011, Alperin 2023, Volpe 2023)
- All desk-reject risks resolved
- 47 pages, ~9,000 words, compiles clean

### Version 1 — Initial draft (2026-06-05)
- First complete draft: structured abstract, 4 modalities, MQTT/QoS 2 pipeline, binary teacher label, PVT, SAP, anticipated results, privacy appendix

### Pending
- ORCID Herrero Albiar
- Protocol registration on OSF
- GitHub URL and Zenodo DOI
