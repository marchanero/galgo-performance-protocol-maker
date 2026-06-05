# Domain Profile

<!--
HOW TO USE: Calibrated for the JRP Protocol Paper 1 (Herrero Albiar, UCLM doctoral compendium).
All agents read this file to calibrate their field-specific behavior.
This file is the single source of truth for project scope.
-->

## Field

**Primary:** Multimodal Learning Analytics / Educational Technology / Physiological Signal Processing
**Adjacent subfields:** Ambient Sensing (IoT), EEG Signal Processing, Body-Pose Estimation, Psychomotor Vigilance, Data Privacy (GDPR for minors)
**Paper type:** Pre-execution study protocol (observational, longitudinal, descriptive)
**Target journal:** JMIR Research Protocols (JRP)

## Research Group Context

- **Institution:** Universidad de Castilla-La Mancha (UCLM) — multiple departments (I3A, TSI, EIEAC, Didáctica de la Educación Física)
- **Doctoral compendium:** Herrero Albiar, José Enrique — Programa de Investigación en Humanidades, Artes y Educación
- **Core dataset:** Multimodal classroom sensing (4 modalities) over 4 months in secondary education (3rd–4th ESO, ages 14–16)
- **Modalities:** (i) Ambient IoT platform (T, RH, CO2, PM2.5, PM10, illuminance, SPL at 15 Hz), (ii) EmotiBit wristbands (HR, HRV, EDA, skin temp, 3-axis accelerometry; 6 rotating units), (iii) 32-channel semi-dry EEG at 256 Hz (Bitbrain Versatile; 1 participant/week), (iv) 4K dual-lens overhead camera (body-pose features only; raw video deleted within 72h)
- **Label:** Binary teacher annotation per 5-minute window (on-task/off-task)
- **External anchor:** Psychomotor Vigilance Task (PVT) monthly + end-of-session 0–10 global rating
- **Synchronisation:** MQTT QoS 2 + source-based NTP timestamping; inter-modality alignment <15 ms, zero packet loss
- **Ethics:** CEIS-UCLM approved; GDPR Article 9 / LOPDGDD for special-category data of minors; tiered data access (open aggregated features / restricted raw signals)
- **No ML models trained yet** — this protocol characterizes the measurement platform before any predictive modeling. Subsequent compendium articles will analyze multimodal predictive performance, feature selection, and minimal sensor subsets.

---

## Target Journal: JMIR Research Protocols

**Scope:** Pre-execution study protocols and grant proposals. Accepts protocols with statistical analysis plans and anticipated results.

**Section ordering (mandatory):**
1. Introduction
2. Methods (Study Design, Setting, Population, Procedures, Outcomes, Data Collection, Statistical Analysis Plan, Sample Size, Ethics & Data Governance)
3. Results (Anticipated / Expected)
4. Discussion (Principal Anticipated Findings, Strengths, Limitations, Comparison with Prior Work, Conclusions)
5. Acknowledgements & CRediT
6. Conflicts of Interest
7. Data Availability
8. Multimedia Appendix
9. References

**Key JMIR conventions:**
- Structured abstract required (Background / Objective / Methods / Results / Conclusions)
- IRRID (International Registered Report Identifier) line after abstract
- No separate "Related Work" section — literature is integrated into Introduction
- Anticipated results only — no empirical data collection completed at time of submission
- Privacy-by-design documentation expected for protocols involving special-category data

**JMIR referee expectations (from Eysenbach 2004 [1]):**
- Protocols are reviewed for methodology quality and completeness, not for results
- Peer review focuses on: study design soundness, population justification, sample size rationale, ethical governance, data management plan, statistical analysis plan
- "Peer-review only" option available — authors can opt for expert review without mandatory publication
- Reviewers assess whether the protocol "would produce valid evidence if executed as described"

---

## Data Characteristics

| Stream | Variables | Sampling | Access tier |
|--------|-----------|----------|-------------|
| Ambient IoT | T, RH, CO2, PM2.5, PM10, illuminance, SPL | 15 Hz (derived 1/60 Hz aggregates per 5-min window) | Open (aggregated features) |
| EmotiBit | HR, HRV, EDA, skin temp, 3-axis accel | Per-sensor native rates (EDA/ACC ~15–100 Hz) | Restricted (raw) / Open (aggregated) |
| EEG | 32-channel raw EEG, Alpha/Beta/Theta PSD | 256 Hz | Restricted |
| Body-pose | Head/trunk/limb keypoints, head orientation, gross motor, posture indicators | Derived from 4K video (frame-level) | Open (numeric features only) |
| Teacher label | Binary on-task/off-task per 5-min window | 1 per 5-min window | Open (anonymised) |
| PVT | Reaction time, lapses, mean/median RT | Monthly pre/post session | Open |

---

## Key Methodological Conventions

- **Unit of analysis:** 5-minute time window (not participant, not session)
- **Synchronisation:** MQTT QoS 2 (exactly-once delivery) + NTP-disciplined timestamping; acceptance criterion: inter-modality offset ≤100 ms (ambient-camera), ≤50 ms (EEG-camera, EmotiBit-camera)
- **Label validation:** Convergent validity tested via per-participant correlation between within-session "óptimo" rate and PVT change score
- **Teacher label:** Single annotator (per-session teacher); acknowledged as limitation
- **Data governance:** Raw video deleted within 72h of feature extraction (verifiable governance log); audio disabled at device level; pseudonymisation key on encrypted storage
- **Tiered access:** Open (aggregated features + code) / Restricted (raw signals) / Permanently excluded (raw video, audio, identifiers)
- **Statistical analysis plan:** Per-modality validation (sync latency, signal quality, detection performance, sensor responsivity), descriptive characterization of four-month corpus (marginal + joint distributions), construct validity (PVT-teacher label correlation)

## Privacy-by-Design Regime (GDPR Article 9 for minors)

- Raw classroom video deleted within 72h of pose extraction (verifiable governance log with confirmation hashes)
- Camera audio channel disabled at device level (configuration directive documented)
- Pseudonymisation key managed by principal investigator on encrypted storage
- Withdrawal triggers full deletion; deletion event recorded in governance log
- No individual feedback to schools, families, or participants — only aggregate reporting
- Independent audit of privacy pipeline committed before any subsequent compendium article

---

## Seminal References (Multimodal Learning Analytics + Cognitive Sensing)

| Paper | Why It Matters |
|-------|---------------|
| Blikstein & Worsley (2016) "Multimodal Learning Analytics" | Foundational MMLA framework |
| Fredricks et al. (2004) "School engagement: potential of the concept" | Engagement construct definition |
| D'Mello et al. (2012) "Dynamics of affective states during learning" | Affect-engagement dynamics |
| Hutt et al. (2019) "Automated gaze-based mind wandering detection" | Classroom attention sensing |
| Wargocki & Wyon (2007) "Effects of IAQ on office work" | IAQ-cognition evidence base |
| Wargocki et al. (2020) "Relationships between classroom air quality and children's performance" (Building & Environment) | Systematic IAQ-cognition review: reducing CO2 from 2100 to 900 ppm improves performance by 12% |
| Satish et al. (2012) "Is CO2 an indoor pollutant?" | CO2-cognitive performance link |
| Allen et al. (2016) "Associations of cognitive function scores with CO2" | Green office study — building science standard |
| Palacios Temprano et al. (2020) "Indoor environmental quality and learning outcomes: protocol on large-scale sensor deployment" (BMJ Open) | **Direct protocol precedent**: 280 classrooms, 10,000 children, IAQ sensors + cognitive tests. Published protocol with similar study design — cite as comparable approach. |
| Fuentes-Martinez et al. (2023) "Low-cost EEG multi-subject recording platform for assessment of students' attention in secondary school" (Sensors) | **Directly relevant**: EEG classroom deployment protocol for attention assessment in secondary school. 26 citations. |
| Cornide-Reyes et al. (2019) "Introducing Low-Cost Sensors into the Classroom Settings" (Sensors) | MMLA with low-cost sensors in agile classroom practices |
| Prieto et al. (2018) "Multimodal Teaching Analytics: Automated Extraction of Orchestration Graphs from Wearable Sensor Data" (J Comput Assist Learn) | Wearable sensor data for teaching analytics |
| Huertas Celdran et al. (2020) "A Scalable Architecture for Dynamic Deployment of MMLA Applications in Smart Classrooms" (Sensors) | Architecture for smart classroom MMLA deployment |
| Olsen et al. (2021) "EFAR-MMLA: An Evaluation Framework to Assess and Report Generalizability of ML Models in MMLA" (Sensors) | Framework for evaluating MMLA models — validation methodology reference |
| Glasserman-Morales et al. (2023) "Use of wearable devices in the teaching-learning process: a systematic review" (Frontiers in Education) | Systematic review of wearables in education — 13 citations |
| Liu et al. (2022) "Learning analytics based on wearable devices: A systematic literature review from 2011 to 2021" (J Educational Technology) | Comprehensive wearable/education review — 45 citations |
| Nouri (2025) "A scoping review of educational neurotechnology: Methods, applications, opportunities, and challenges" (Review of Education) | Scoping review of neurotechnology in classrooms — recent, methodologically relevant |
| Esterhazy et al. (2025) "Advancing Multimodal Collaboration Analytics: A Scoping Review" (J Learning Analytics) | MMLA scoping review methodology reference |
| Ahuja et al. (2019) "EduSense: practical classroom sensing" | Classroom sensing system precedent |
| Cao et al. (2021) "OpenPose: realtime multi-person 2D pose estimation" | Body-pose estimation pipeline |
| Lugaresi et al. (2019) "MediaPipe" | Alternative pose estimation |
| Lopez-Gordo et al. (2014) "Dry EEG electrodes" | EEG hardware validation |
| Di Flumeri et al. (2019) "Dry EEG in real environments" | EEG field deployment |
| Lau-Zhu et al. (2019) "Mobile EEG in research" | Child/adolescent mobile EEG |
| Dinges & Powell (1985) "Microcomputer analyses of PVT" | Original PVT paper |
| Basner & Dinges (2011) "Maximizing sensitivity of PVT" | PVT sensitivity optimization |
| Basner et al. (2018) "Practice effects in the PVT" | PVT practice effects |
| DiFrancesco et al. (2019) "Network-based responses to PVT during lapses in adolescents" (Scientific Reports) | PVT in adolescent population — brain network correlates |
| González-Fernández et al. (2021) "Effect of physical exercise program based on active breaks on physical fitness and vigilance performance" (Biology) | **PVT + classroom**: active breaks → PVT improvement. 39 citations. Provides PVT-classroom methodology precedent. |
| Ballester et al. (2015) "The relationship between regular sports participation and vigilance in male and female adolescents" (PLoS ONE) | PVT in adolescents — sex differences, 63 citations |
| Barel & Tzischinsky (2022) "The role of sleep patterns from childhood to adolescence in vigilant attention" (IJERPH) | PVT + developmental trajectory — child to adolescent |
| Vanneste et al. (2020) "Towards measuring cognitive load through multimodal physiological data" (Cognition, Technology & Work) | Multimodal EDA+EEG+EOG cognitive load — methodology reference |
| Romine et al. (2020) "Wearable device for measuring students' cognitive load" (Sensors) | EduFit tracker concept — EDA+HR+temp for cognitive load |
| Shen et al. (2025) "Passive sensing for mental health monitoring using ML with wearables" (JMIR) | Scoping review methodology reference; JMIR-venue awareness |
| Martínez-Maldonado et al. (2024) "Lessons learnt from multimodal learning analytics" | Current MMLA deployment review |
| Macenaite (2017) "GDPR and processing of children's data" | GDPR minors legal framework |
| EDPB (2020) "Guidelines on consent under GDPR" | GDPR consent guidance |
| Hoofnagle et al. (2019) "The European Union GDPR: what it is and what it means" (Information & Communications Technology Law) | Comprehensive GDPR introduction — 583 citations, authoritative |
| Campbell et al. (2026) "Toward Youth-Centered Privacy-by-Design in Smart Devices" | Youth privacy-by-design frameworks — systematic review |
| Brauneck et al. (2023) "Federated ML, PETs, and Data Protection Laws" (JMIR) | GDPR technical compliance in research — FL + DP + SMPC |
| Mishra et al. (2020) "MQTT protocol" | Transport layer standard |
| Shi et al. (2016) "Edge computing: vision and challenges" | Edge computing deployment |
| Eysenbach (2004) "Peer Review and Publication of Research Protocols and Proposals" (JMIR) | JMIR protocol review workflow description — the founding editorial |

## Author Team (JRP Protocol Paper 1)

**Primary author:** José Enrique Herrero Albiar (ORCID: [TODO])
- Doctoral candidate, UCLM — Programa Investigación en Humanidades, Artes y Educación

**Co-authors:**
| Author | ORCID | Department | Role |
|--------|-------|------------|------|
| Eloy García-Pérez | `0009-0008-0277-2414` | Dpto. Ingeniería Eléctrica, Electrónica, Automática y Comunicaciones | Ambient IoT, sensor hardware |
| Javier Martínez-López | `0009-0004-1315-8912` | Dpto. Ingeniería Eléctrica, Electrónica, Automática y Comunicaciones | Platform engineering |
| Alejandro L. Borja | `0000-0003-2880-0678` | Dpto. Ingeniería Eléctrica, Electrónica, Automática y Comunicaciones | Hardware architecture |
| Roberto Sánchez-Reolid | `0000-0003-4455-370X` | Dpto. Tecnologías y Sistemas de Información | Signal processing, MMLA methodology |
| Juan Carlos Pastor Vicedo | `0000-0001-5771-6542` | Dpto. Didáctica de la Educación Física, Artística y Música | Corresponding author, educational domain expertise |

---

## Quality Tolerance Thresholds

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| Synchronisation offset | ±5 ms (reported median) | NTP-disciplined MQTT QoS 2 |
| EEG signal quality (PSD bands) | ±0.5 dB | 32-channel semi-dry, classroom environment |
| Teacher label consistency | N/A (single annotator — reported as limitation) | Per-session teacher, acknowledged bias |
| Body-pose detection rate | ±2% of frames | Reolink 4K 180°; occlusion in classroom |
| Ambient sensor reading | ±1% of calibrated range | Factory-calibrated PCB sensors |

---

## Anti-Patterns / What This Paper Is NOT

| This paper is NOT | Don't suggest |
|-------------------|---------------|
| An ML/DL experiment paper | Don't ask for baselines, F1 scores, ablation studies |
| A novel architecture paper | Don't ask for model descriptions, parameter counts, training curves |
| A comparative benchmark | Don't ask for SOTA comparison, LOSO, statistical tests between models |
| A deployment/application paper | Don't ask for inference latency, GPU benchmarking |
| A BSPC/NIPS/ICLR submission | Don't apply BSPC field conventions or CS conference formatting |
| An interventional trial | Don't apply SPIRIT 2025 checklist literally (SPIRIT is for RCTs; this is observational) |
| An EDA-only paper | Don't treat EDA as the primary modality; this is multimodal with 4 equal streams |
