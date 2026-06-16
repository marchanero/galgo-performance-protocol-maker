# SKEPTIC AGENT REVIEW — 2026-06-16

**Disposition:** SKEPTIC — looking for reasons to REJECT
**Paper:** Multimodal Passive Sensing Protocol, JMIR Research Protocols

---

## VERDICT: MAJOR REVISIONS

This paper should be sent back to authors. The idea is interesting but the execution has 5 fatal weaknesses and several serious gaps. I would not accept in current form.

---

## 🚨 FATAL ISSUES (5)

### F1. This is not a protocol — it is a measurement validation plan with no data.
A protocol describes a study DESIGN: hypotheses, recruitment plan, power analysis, randomization, blinding, statistical comparisons. This paper describes hardware and signal processing. Where are the study hypotheses? What is the primary comparison? How many participants do you need for that comparison? "Class-complete enrolment" is not a sample size justification — it's avoidance of one. 

**What would change my mind:** State explicit, falsifiable hypotheses (even descriptive ones). Justify the participant sample size for the primary outcome — the PVT-teacher label correlation — with a minimal detectable effect calculation. 

### F2. Your "ground truth" is a single teacher pressing a button every 5 minutes.
A binary label from one teacher, with no inter-rater reliability, is your primary outcome? And you're building "multimodal fusion models" on this? This is garbage-in-garbage-out. A single-annotator binary scheme compresses the entire construct of "cognitive performance" into one bit from one person. You acknowledge this in limitations (good) but then proceed to build an entire AI architecture on it (contradictory). Either the label is reliable enough for AI models (in which case the limitation is exaggerated) or it's too noisy (in which case the AI section is premature). Pick one.

**What would change my mind:** Either remove the AI fusion section and frame this purely as a measurement validation protocol, OR commit to multi-annotator labels before any AI model is trained.

### F3. The AI fusion section belongs in a grant proposal, not a protocol paper.
Section "Multimodal fusion and predictive modelling" is a vision statement: "gradient-boosted trees... convolutional networks... graph-based models... meta-learner." This is not a protocol commitment — it's a list of ML algorithms you might try. A protocol should pre-specify the EXACT model class, not enumerate the entire scikit-learn catalogue. "Full pre-analysis plans... are declared in the subsequent compendium articles" — so this protocol commits to nothing. What is the reader supposed to extract from this section?

**What would change my mind:** Specify exactly ONE model architecture that will be tested. Pre-register it. Remove the algorithm shopping list.

### F4. You claim "four conjunctive conditions" as novelty — but condition (c) and (d) are subjective.
- Condition (c): "on-site or institutional-server processing under European data-protection guarantees for minors." This is not a technical contribution, it's a compliance requirement. GDPR applies to all research with minors in the EU. You didn't invent it.
- Condition (d): "anchoring to an external, independently validated attentional benchmark." The PVT is well-established — using it as a benchmark is good practice, not a novel condition.

So you're really left with (a) integrating 4 modalities and (b) doing it longitudinally. Is that enough for a protocol paper? The integration is an engineering achievement, not a scientific contribution.

**What would change my mind:** Reframe conditions (c) and (d) as protocol commitments, not novelty claims. The true novelty is (a) + (b) + privacy-by-design — which is 3 conditions, not 4.

### F5. No ethics reference, no ORCID, no registration.
The paper states ethics evaluation is "pending." You cannot publish a protocol that hasn't been approved. What if the ethics committee rejects it? The entire paper becomes void. This alone is reason to reject until approval is obtained.

---

## 🔴 SERIOUS ISSUES (4)

### S1. "Class-complete enrolment" masks the real sample.
A Spanish ESO class has ~25 students. All need both parental consent + minor assent. Real uptake with opt-in consent for biometric data of minors? Maybe 60-70%. That's ~15-17 students, not 25. Your sample size calculations should use realistic uptake estimates, not maximal class size.

### S2. EEG: 16 sessions is a descriptive case series, not a study.
16 individual EEG recordings over 4 months, one participant per week. This is so underpowered it barely qualifies as pilot data. Yet the Data Analysis Plan describes EEG processing with 5 frequency bands, ICA, inter-channel coherence — for 160 windowed observations. This is massive over-engineering for a negligible sample. Either increase EEG sampling or downgrade EEG analysis promises.

### S3. Comparison group without sensors is nearly useless.
The comparison group gives you teacher labels + PVT data. Both groups get the same outcomes. So what exactly are you comparing? You have no sensor data from the comparison group, so you cannot attribute any multimodal differences to your platform vs. a control condition. The comparison only tells you whether PVT distributions differ between two classes — which could be due to any between-class factor (teacher, schedule, classroom layout).

### S4. The privacy appendix is operationally precise — but who will enforce it?
Appendix A through F describes a privacy-by-design pipeline with SHA-256 hashes, governance logs, AES-256-GCM encryption, and independent audits. This is commendably detailed. But the protocol does not state WHO will perform these operations, whether this person is independent from the research team, or what happens if the governance log detects a violation. Without an independent data monitor, the privacy guarantees are self-policed.

---

## 🟡 MINOR

| # | Issue |
|---|-------|
| M1 | "2400px" or similar artifact appears... actually I don't see it. Ignore. |
| M2 | Results validation says "engineering documentation of the UCLM smart-classroom platform" — this is an internal document. Not a citable reference. |
| M3 | Dashboard caption says "accelerometry" but the sensor is "9-axis IMU" — use consistent terminology. |
| M4 | Conclusions section is too similar to the abstract. Add one unique sentence. |
| M5 | No discussion of what happens if the environmental mote fails during the 4-month deployment. Redundancy? |

---

## SCORE

| Category | Score |
|----------|-------|
| Novelty / contribution | 45/100 |
| Methodological rigor | 55/100 |
| Internal consistency | 65/100 |
| Feasibility / realism | 50/100 |
| Writing / clarity | 70/100 |
| **OVERALL** | **57/100** |

**Recommendation:** MAJOR REVISIONS. The paper has potential but needs: (1) real ethics approval, (2) explicit hypotheses, (3) realistic sample size, (4) either commit to specific AI models or remove the fusion section, (5) tone down novelty claims about GDPR compliance and PVT usage.
