# Agent Review — Round 1 (2026-06-05)

**Paper:** Multimodal Passive Sensing of Cognitive Performance in Spanish Compulsory Secondary Education Classrooms: Protocol for an Observational, Longitudinal Study  
**Target:** JMIR Research Protocols  
**Word count:** 8,472 / 10,000 (under limit)

---

## Scores

| Agent | Score | Recommendation |
|-------|-------|---------------|
| domain-referee | 70/100 | Major Revisions |
| methods-referee | 73/100 | Major Revisions |
| consistency-referee | 59/100 | Major Revisions |
| language-reviewer | 63/100 | Advisory (format-blocking) |

**Editor (JMIR):** PASS desk review

---

## BLOCKING (desk reject or certain rejection if not fixed)

| # | Issue | Section | Effort |
|---|-------|---------|--------|
| 1 | Abstract 526 words → 450 max (JMIR structured abstract limit) | abstract_structured.tex | Low |
| 2 | Citation style author-year → AMA numbered (JMIR requires [1], not Author, Year) | preamble-paper.tex | Low |
| 3 | All section headings Title Case → sentence case (JMIR/AMA requirement) | methods.tex, results.tex, discussion.tex | Medium |
| 4 | ORCID Borja duplicated from García-Pérez (0009-0008-0277-2414 → 0000-0003-2880-0678) | main.tex:30 | 1 line |
| 5 | ORCID Herrero Albiar placeholder (0000-0000-0000-0000) | main.tex:27 | 1 line |
| 6 | Sync latency inconsistency: Abstract <15ms "guarantee" vs Methods/Results ≤100/≤50ms acceptance criteria | abstract, methods, results | Low |
| 7 | "Zero packet loss" unverifiable (MQTT QoS 2 ≠ physical-layer guarantee) | abstract, methods | Low |
| 8 | VPN contradiction: Tailscale/WireGuard (Methods) vs institutional mutual-TLS (Privacy Appx D) | methods.tex:68, privacy_appendix.tex:36 | Medium |
| 9 | Environmental Mote as "temporal master" (fig caption) contradicts NTP text in pipeline subsection | methods.tex:24-26, methods.tex:64 | 1 line |
| 10 | Present-tense empirical language: "yields a measured", "achieving" → bench-test language | methods.tex:64-66 | Low |

---

## HIGH PRIORITY (flagged by ≥2 referees)

| # | Issue | Δ Words |
|---|-------|----------|
| 11 | Scoping review methodology undocumented (databases, search, PRISMA flow, criteria) | +350 |
| 12 | Downstream AI/dashboard section too speculative → condense or move to Appendix | −300 |
| 13 | SAP underspecified: correlation type, hierarchical data structure, missing data strategy | +95 |
| 14 | PRISMA-ScR checklist missing (JMIR recommends reporting guideline checklists) | +200 |
| 15 | EmotiBit sampling rates not specified in Methods | +30 |
| 16 | 15+ missing citations (Fuentes-Martinez 2023, Wargocki 2020, PVT-adolescent, MMLA, GDPR) | +200 |
| 17 | Protocol not registered (OSF/ClinicalTrials.gov) | +10 |

---

## LANGUAGE / FORMAT (language-reviewer)

| # | Issue | Severity |
|---|-------|----------|
| L1 | AI-vocabulary: "leveraging", "ecosystem", "crucial", "serves as" (×2), "Additionally" | Major |
| L2 | Downstream AI section reads as promotional/product-pitch | Critical |
| L3 | "TVOCs" undefined, appears in figure caption but not in Methods sensor list | Minor |
| L4 | "in principle" vs "approved" — ethics approval status inconsistent | Minor |

---

## CONSISTENCY (consistency-referee specifics)

| # | Issue |
|---|-------|
| C1 | TVOC not listed in Methods environmental sensor variables but appears in Results and dashboard |
| C2 | Comparison group instrumentation not specified (full stack vs reduced set?) |
| C3 | IMU: "9-axis" (Methods) vs "tri-axial" (all other sections) |
| C4 | Live RTSP camera feed in dashboard not addressed in Privacy Appendix |
| C5 | "AI fusion engine" in architecture diagram has no corresponding Methods subsection |
| C6 | Dashboard labels "TVOCs" / "ambient noise" vs protocol measuring SPL (dBFS) |

---

## Net word budget impact

| Category | Δ |
|----------|---|
| Blocking fixes (1-10) | +80 |
| High priority fixes (11-17, net of dashboard trim) | +285 |
| **Total net** | **8,472 → ~8,840** (1,160 under 10,000 limit) |
