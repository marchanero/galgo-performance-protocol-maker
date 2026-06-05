# Journal Profiles

<!--
These profiles calibrate the domain-referee and methods-referee when reviewing
for a specific journal or conference. Each profile describes the venue's review
culture in plain language — the LLM adapts its priorities accordingly.

Used by: domain-referee.md, methods-referee.md (via /review --peer [venue])
-->

## How This Works

When `/review --peer [venue]` is invoked:

1. **Editor reads the paper** → desk review (reject or send to referees)
2. **Editor selects referees** → draws dispositions and pet peeves from the venue's **Referee pool**
3. **Profile found below** → referees calibrate using the full profile
4. **Profile NOT found** → referees use the venue name + .claude/references/domain-profile.md to adapt
5. **No venue specified** → generic top-tier CS/AI referee behavior

### Referee Pool Field

Each profile includes a **Referee pool** that weights which dispositions the editor draws from. The two referees always get DIFFERENT dispositions. Dispositions: ARCHITECTURE, CREDIBILITY, REPRODUCIBILITY, BASELINE, THEORY, SKEPTIC (see editor.md for definitions).

### Table / Figure Format Convention

**Default (CS/AI):** Results tables use booktabs formatting. No significance stars by default — report exact metrics (F1, AUC, accuracy) with standard deviations across folds. Figures use vector formats (PDF/SVG). Confusion matrices and ROC curves should be publication-quality.

---

## Computer Science / Artificial Intelligence

### IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)
**Focus:** Highest-impact journal in pattern recognition, computer vision, and machine learning
**Bar:** Fundamental contributions with thorough theoretical and empirical validation. Papers should be archival-quality with comprehensive experimental sections. Significance must be broad — not just a minor architectural tweak.
**Domain referee adjusts:** Contribution must matter beyond one specific dataset or domain. Theoretical depth valued alongside empirical results. Extensive literature survey expected. Comparison against broad set of baselines. Method should generalize across domains.
**Methods referee adjusts:** Mathematical rigor expected. Formal definitions, convergence proofs, complexity analysis where applicable. Extensive ablation studies mandatory. Statistical significance tests between methods. Reproducibility: code submission encouraged, hyperparameter sensitivity required.
**Typical concerns:** "Is this a fundamental advance or a dataset-specific tweak?" "Does the contribution generalize beyond the evaluated benchmarks?" "Are the ablation studies thorough enough to isolate what matters?"
**Referee pool:** THEORY (high), CREDIBILITY (high), ARCHITECTURE (high), SKEPTIC (medium), REPRODUCIBILITY (medium), BASELINE (low)

### Journal of Machine Learning Research (JMLR)
**Focus:** All aspects of machine learning — theory, algorithms, applications
**Bar:** Technical depth and novelty. Open access, no page limits. Papers are expected to be comprehensive and thoroughly validated. Strong theoretical analysis valued alongside empirical results.
**Domain referee adjusts:** Contribution must advance the field's understanding, not just beat benchmarks. Literature review must be thorough — JMLR papers are archival. Open-source code and reproducible experiments expected.
**Methods referee adjusts:** Rigorous experimental methodology. Proper train/val/test splits. Statistical significance testing. Hyperparameter sensitivity analysis. Ablation studies that isolate each contribution. Theoretical guarantees where applicable (convergence, generalization bounds, complexity).
**Typical concerns:** "What is the novel insight, beyond the performance improvement?" "Is the experimental methodology rigorous?" "Does the theory match the empirical observations?"
**Referee pool:** THEORY (high), CREDIBILITY (high), REPRODUCIBILITY (high), SKEPTIC (medium), ARCHITECTURE (medium), BASELINE (low)

---

## Top Conferences (Double-Blind Peer Review)

### Neural Information Processing Systems (NeurIPS)
**Focus:** Broadest ML/AI conference — deep learning, optimization, theory, neuroscience, applications
**Bar:** Novelty, technical quality, and significance. Highly competitive (20-25% acceptance). Short format (8-9 pages main text) demands concise, impactful presentation. Rebuttal phase after initial reviews.
**Domain referee adjusts:** Contribution must be clear and compelling within space constraints. "NeurIPS-style" means: clean problem setup, clear motivation, thorough experiments, honest limitations. Visual results (figures, diagrams) highly valued. Wide appeal across ML subfields preferred.
**Methods referee adjusts:** Rigorous experiments in limited space. Well-designed ablation studies despite page constraints. Error bars / confidence intervals on all results. Comparison against strong, recent baselines. Code submission strongly encouraged. Statistical significance when claiming improvement over baselines.
**Typical concerns:** "Is the contribution significant enough for NeurIPS?" "Are the experiments convincing within the page limit?" "Could this be rejected as incremental?"
**Referee pool:** CREDIBILITY (high), ARCHITECTURE (high), REPRODUCIBILITY (high), SKEPTIC (medium), BASELINE (medium), THEORY (medium)

### International Conference on Machine Learning (ICML)
**Focus:** Machine learning — theory, algorithms, applications
**Bar:** Technical depth and rigorous methodology. Slightly more theoretical bent than NeurIPS. Values mathematical formalism alongside empirical validation. Rebuttal phase.
**Domain referee adjusts:** Theoretical contribution or insight valued. Connection to broader ML principles. Comparison against relevant theoretical baselines, not just empirical ones. Implications for the field discussed.
**Methods referee adjusts:** Formal problem statement expected. If claims are theoretical: complete proofs (or proof sketches in main, full in appendix). If empirical: thorough evaluation with properly tuned baselines, ablation studies, sensitivity analysis. Statistical significance testing between methods.
**Typical concerns:** "Is the theoretical contribution sufficient?" "Are the empirical claims properly supported?" "Could this be at a more specialized venue?"
**Referee pool:** THEORY (high), CREDIBILITY (high), ARCHITECTURE (medium), SKEPTIC (medium), REPRODUCIBILITY (medium), BASELINE (low)

### International Conference on Learning Representations (ICLR)
**Focus:** Representation learning, deep learning, optimization for neural networks
**Bar:** Innovation in learning representations or training methodology. OpenReview process — reviews are public, authors can respond. Values novel ideas even if not fully polished — more tolerance for exploratory work than NeurIPS/ICML.
**Domain referee adjusts:** Novelty and insight valued over incremental improvements. Negative results or analyses that advance understanding welcomed. Open discussion culture — constructive engagement expected.
**Methods referee adjusts:** Clear problem motivation. Well-designed experiments that test specific hypotheses about representation learning. Sensitivity to architecture choices and hyperparameters. Comparisons against appropriate representation-learning baselines.
**Typical concerns:** "Does this advance our understanding of representation learning?" "Are the claims about learned representations properly validated?" "Is the insight general, or specific to one architecture?"
**Referee pool:** ARCHITECTURE (high), CREDIBILITY (high), THEORY (medium), SKEPTIC (medium), REPRODUCIBILITY (medium), BASELINE (low)

---

## Affective Computing / Biomedical Engineering

### IEEE Transactions on Affective Computing (TAC)
**Focus:** Emotion recognition, sentiment analysis, affective interaction, physiological sensing for affect
**Bar:** Solid contribution to affective computing with rigorous experimental methodology. Interdisciplinary — psychology/neuroscience grounding expected alongside technical contribution.
**Domain referee adjusts:** Must demonstrate understanding of affective science principles — not just applying ML to emotion data. Ground truth/labeling methodology must be justified. Grounding in psychological theories of emotion (dimensional, categorical, appraisal). Discussion of real-world deployment challenges.
**Methods referee adjusts:** Rigorous subject-independent evaluation (LOSO minimum). Proper handling of imbalanced datasets common in affective computing. Physiological preprocessing must be detailed and replicable. Comparison against domain-specific baselines. Discussion of individual differences and generalization.
**Typical concerns:** "Is the emotion/affect labeling methodology valid?" "Does this generalize across subjects?" "Are you reporting per-class metrics, not just overall accuracy?" "Physiological plausibility of features learned?"
**Referee pool:** CREDIBILITY (high), ARCHITECTURE (high), BASELINE (high), REPRODUCIBILITY (medium), THEORY (low), SKEPTIC (low)

### IEEE Transactions on Biomedical Engineering (TBME)
**Focus:** Biomedical devices, signal processing, physiological modeling, neural engineering
**Bar:** Engineering contribution with demonstrated biomedical relevance. Clinical or physiological validation expected. Methods must be reproducible and applicable to real biomedical problems.
**Domain referee adjusts:** Biomedical context and application must be clear. Physiological interpretation of results expected. Connection to clinical or health applications. Safety and practical deployment considerations.
**Methods referee adjusts:** Signal processing methodology must be clearly described. Comparison against established biomedical signal processing baselines. Proper physiological validation — not just ML metrics. Discussion of signal quality, artifacts, real-world feasibility.
**Typical concerns:** "Is there a clear biomedical application?" "Have you validated on physiologically meaningful ground truth?" "What about artifact robustness?" "Real-time feasibility?"
**Referee pool:** CREDIBILITY (high), REPRODUCIBILITY (high), BASELINE (medium), ARCHITECTURE (medium), THEORY (low), SKEPTIC (low)

### IEEE Journal of Biomedical and Health Informatics (JBHI)
**Focus:** Health informatics, biomedical signal processing, wearable computing, mHealth
**Bar:** Informatics contribution to healthcare. Bridges engineering and clinical domains. Values practical, deployable solutions with demonstrated health impact.
**Domain referee adjusts:** Health/clinical relevance is paramount. Connection to real healthcare workflows or patient outcomes. Practical feasibility — computation, power, deployment constraints. Patient/user-centered design considerations.
**Methods referee adjusts:** Proper clinical/health validation methodology. Comparison against clinically-relevant baselines. Discussion of deployment constraints (computation, memory, power). Robustness to real-world variability (noise, missing data, artifacts). Ethics and privacy considerations.
**Typical concerns:** "How would this deploy in a real healthcare setting?" "What's the clinical significance of the performance improvement?" "Power/memory constraints for wearable deployment?"
**Referee pool:** BASELINE (high), CREDIBILITY (high), REPRODUCIBILITY (high), ARCHITECTURE (medium), THEORY (low), SKEPTIC (low)

---

## Signal Processing / Sensors

### Biomedical Signal Processing and Control (BSPC)
**Focus:** Biomedical signal processing, physiological control systems, medical decision support
**Bar:** Novel signal processing methodology with demonstrated biomedical application. Methods must be tested on real physiological data (not just simulations).
**Domain referee adjusts:** Biomedical signal processing expertise expected. Understanding of physiological signal characteristics and challenges (noise, artifacts, non-stationarity). Connection to medical/clinical applications.
**Methods referee adjusts:** Signal processing methodology must be clearly described and mathematically justified. Preprocessing pipeline details mandatory. Comparison against established signal processing baselines (not just ML models). Robustness to artifacts and signal quality variation.
**Typical concerns:** "Is the signal processing methodology novel or a straightforward application?" "Physiological motivation for the approach?" "Comparison against traditional signal processing methods?"
**Referee pool:** ARCHITECTURE (high), CREDIBILITY (high), REPRODUCIBILITY (medium), SKEPTIC (medium), BASELINE (low), THEORY (low)

**Critical Pet Peeves (BSPC-specific):**
- **Missing classical baselines:** Papers benchmarking DL architectures against only other DL architectures will be flagged. Include handcrafted feature extraction + SVM/RF as reference point. Even retrospective baselines are better than none.
- **"Wearable/mobile/cloud" deployment claims from GPU benchmarks:** BSPC reviewers will reject deployment tier labels based on workstation GPU latency. Use GPU-relative language (low/mid/high-latency GPU) unless benchmarks include actual embedded hardware.
- **Preprocessing without physiological justification:** Every parameter (FIR cutoff, Gaussian sigma, decomposition method) must be linked to EDA signal characteristics or SNS physiology. Cite SPR2012EDA guidelines.

**Constructive Pet Peeves (BSPC reviewers reward):**
- **Thorough preprocessing documentation:** Explicitly justify CDA vs. cvxEDA vs. Ledalab. Mention artifact susceptibility (cite Hossain2022BSPC).
- **Honest limitations:** Distinguish lab validation from clinical deployment. Acknowledge single-dataset constraint, LOSO Wilcoxon independence violation, GPU-relative thresholds.
- **BSPC journal awareness:** Cite 5-8 relevant BSPC papers in introduction. Shows the paper belongs in this venue, not a pure ML journal.
- **Multiple efficiency dimensions:** Parameters, FLOPs, inference time, memory, training time — BSPC values practical deployability.

**Self-Citation Guidelines for BSPC:**
- Keep below ~35% of total cite instances
- Avoid duplicate cites to same paper in same sentence
- Use dataset paper for protocol citations, comparison paper for architecture context
- BSPC papers by the same author group count toward the 5-8 venue-awareness target

### IEEE Sensors Journal
**Focus:** Sensor design, sensor signal processing, sensor systems and applications
**Bar:** Contribution to sensing technology — from hardware to algorithms. Application-oriented with demonstrated sensor-level innovation.
**Domain referee adjusts:** Sensor-system perspective expected. How does the algorithm interact with sensor characteristics? Practical deployment on sensor platforms. Power, latency, hardware constraints discussed.
**Methods referee adjusts:** Sensor signal processing methodology. Noise characterization and handling. Real-time processing constraints. Comparison against sensor-domain baselines. Hardware-in-the-loop validation if applicable.
**Typical concerns:** "What's novel about the sensor-level processing?" "Have you validated on real sensor data?" "Deployment feasibility on resource-constrained sensor platforms?"
**Referee pool:** BASELINE (high), CREDIBILITY (high), REPRODUCIBILITY (medium), ARCHITECTURE (medium), THEORY (low), SKEPTIC (low)

---

## Short Format / Rapid Dissemination

### IEEE Signal Processing Letters (SPL)
**Focus:** Short, high-impact contributions to signal processing theory and applications
**Bar:** One clear technical contribution in 4-5 pages. Novelty must be immediately apparent. Fast review cycle.
**Domain referee adjusts:** Brevity is a feature. One key insight, cleanly presented. No extensive literature review required — position the contribution in 1-2 paragraphs. Experimental validation must be tight and convincing.
**Methods referee adjusts:** Core method must be clearly described in limited space. Key experimental results — not exhaustive ablation. Comparison against strongest baselines. Mathematical clarity valued.
**Typical concerns:** "Can the contribution be communicated in 4 pages?" "Is the single insight significant enough?" "Is the experimental evidence sufficient for a short format?"
**Referee pool:** ARCHITECTURE (high), CREDIBILITY (medium), SKEPTIC (medium), REPRODUCIBILITY (low), BASELINE (low), THEORY (low)

### Conference Short Papers / Workshops
**Focus:** Emerging ideas, preliminary results, position papers
**Bar:** Novelty of idea and clarity of presentation. Preliminary results acceptable — promise matters more than completeness. Good venue for early feedback.
**Domain referee adjusts:** Idea quality and potential valued over completeness. Clear problem statement and motivation expected. Honest about limitations and preliminary nature.
**Methods referee adjusts:** Preliminary results with proper caveats. Methodology description sufficient to understand the approach. Recognition of what remains to be done for a full paper.
**Typical concerns:** "Is the idea promising enough?" "Are the preliminary results convincing about the direction?" "Clear plan for what comes next?"
**Referee pool:** ARCHITECTURE (high), THEORY (medium), CREDIBILITY (medium), SKEPTIC (low), BASELINE (low), REPRODUCIBILITY (low)

---

## Study Protocol / Educational Technology / Multimodal Sensing

### BMJ Open
**Focus:** General medical journal publishing all study types including protocols, with emphasis on methodological rigor and transparency
**Bar:** Protocol must describe a study whose results would have clinical, public health, or health-services relevance. Pre-execution status is accepted — no data required. The "Protocol" article type expects: clear research question, justified study design, detailed methods, statistical analysis plan, ethics and dissemination. Patient and Public Involvement (PPI) statement expected. Protocol registration (ClinicalTrials.gov, OSF, etc.) strongly encouraged.
**Domain referee adjusts:** Contribution must be framed in terms of health/wellbeing outcomes — "cognitive performance in schools" maps to public health/educational health. Literature review should demonstrate the evidence gap the protocol fills. Comparison to similar published protocols (e.g., Palacios Temprano 2020, BMJ Open) strengthens the case. The novelty may be in the conjunctive integration of modalities, the population (minors), the privacy regime, or the deployment context — not necessarily in any single technology.
**Methods referee adjusts:** Study design, population, recruitment, sample size, data collection, outcomes, SAP, ethics, and data governance must each be a clearly delineated subsection. Missing any of these subsections = major revision. SAP must be pre-specified, not deferred. Privacy-by-design claims must be operational (not declarative). BMJ Open reviewers expect protocol registration number. Falsifiability thresholds and acceptance criteria for considering the platform "fit for purpose" are valued.
**Typical concerns:** "Is the study design appropriate for the research question?" "Is the sample size justified?" "Does the SAP match the stated objectives?" "Has the protocol been registered?" "Are ethics and data governance adequately documented?" "Does this fill a genuine evidence gap?"
**Referee pool:** CREDIBILITY (high), REPRODUCIBILITY (high), BASELINE (medium), SKEPTIC (medium), ARCHITECTURE (low), THEORY (low)

### Sensors (MDPI)
**Focus:** Sensor technology, sensor systems, sensor applications — including wearable sensors, ambient sensors, biosensors, and IoT platforms in educational and health contexts
**Bar:** Technical contribution to sensor systems or novel sensor applications. Accepts original research, reviews, and technical notes. No dedicated "protocol" article type — manuscripts should be framed as describing a sensor system design, a validation study, or a methodological contribution. Fast review cycle (typically 4–8 weeks). Open Access (APC ~2400 CHF).
**Domain referee adjusts:** Contribution should center on the sensing platform and its measurement properties — not on educational outcomes per se. The platform architecture, sensor selection, synchronization design, and signal quality validation are the core contribution. Educational context provides application framing but is not the primary evaluative criterion. Comparison to existing sensor platforms for classroom deployment (Fuentes-Martinez 2023, Cornide-Reyes 2019, Huertas Celdran 2020) is expected.
**Methods referee adjusts:** Sensor specifications must be complete (make, model, sampling rate, resolution, configuration). Synchronization protocol must be detailed. Signal quality validation with acceptance criteria expected. Privacy-preserving sensor design (e.g., audio disable, on-device processing, 72h deletion) is a strength. Per-modality validation protocols should report quantitative metrics. Body-pose feature set should be pre-specified.
**Typical concerns:** "What is novel about the sensor system?" "Have the sensor measurement properties been validated?" "Is the synchronization protocol adequate?" "Are sensor specifications complete and reproducible?" "How does this compare to existing classroom sensor platforms?"
**Referee pool:** ARCHITECTURE (high), CREDIBILITY (high), REPRODUCIBILITY (medium), BASELINE (medium), SKEPTIC (low), THEORY (low)

### JMIR Research Protocols (JRP)
**Focus:** Exclusively research protocols and grant proposals in health, medical, and eHealth research. Pre-execution protocols accepted. Also publishes protocols for systematic/scoping reviews.
**Bar:** Protocol must describe a well-designed study with clear objectives, justified methods, and pre-specified analysis plan. No results required — anticipated/expected results accepted. Structured abstract mandatory (Background/Objective/Methods/Results/Conclusions). IRRID line required. Data Availability statement required. Ethics approval must be documented. Peer review focuses on methodology quality and completeness per Eysenbach (2004) editorial.
**Domain referee adjusts:** Contribution is evaluated as a protocol — the question is "would this study produce valid evidence if executed as described?" Not "what did they find?" Literature positioning should establish the evidence gap the study will fill. Digital health / eHealth / mHealth framing expected — the multimodal sensing platform should be positioned as an eHealth or digital health measurement tool. Comparison to published protocols in JMIR family journals is expected.
**Methods referee adjusts:** Study design, setting, population, recruitment, consent (including minor assent if applicable), interventions/procedures, outcomes, data collection, data management, SAP, sample size, ethics, data governance, PPI, and dissemination must each be addressed. Missing any section = desk reject or major revision. SAP must be pre-specified. GDPR/special-category data compliance must be operational. Protocol registration expected. CRediT author statement required.
**Typical concerns:** "Is the methodology sufficiently detailed to replicate?" "Has the protocol been registered?" "Is the SAP pre-specified before data collection?" "Are ethics and data governance adequately addressed?" "Does the protocol follow JRP formatting requirements?" "Are all mandatory sections present?"
**Referee pool:** CREDIBILITY (high), REPRODUCIBILITY (high), SKEPTIC (medium), BASELINE (medium), ARCHITECTURE (low), THEORY (low)

### PLoS ONE
**Focus:** Multidisciplinary open-access journal publishing all scientifically rigorous research regardless of perceived impact or novelty. Study protocols accepted as a specific article type.
**Bar:** Methodology must be sound, ethics must be documented, data must be available (or data availability statement must explain restrictions). PLoS ONE explicitly does not evaluate perceived importance or novelty — only methodological rigor. This makes it suitable for descriptive/observational protocols that may struggle at venues requiring strong novelty claims. Broad multidisciplinary readership. Study Protocol article type has specific formatting requirements: structured abstract, protocol registration number, ethics statement, data availability, completed PLOS questionnaire.
**Domain referee adjusts:** Contribution need not be framed as novel — "this fills a descriptive gap" is sufficient. Thorough literature contextualization and clear methodology are more important than positioning against SOTA. Cross-disciplinary framing (education + engineering + physiology + privacy) is a strength at PLoS ONE's multidisciplinary audience. Replication and data-sharing value are positive factors in editorial assessment.
**Methods referee adjusts:** Rigor is evaluated identically regardless of field. Study design, population, sample size, outcomes, SAP, ethics, and data availability are standard evaluation criteria. Protocol registration is expected. For protocols involving special-category data (GDPR Article 9), data availability restrictions must be clearly documented and justified. The PLOS data policy requires data to be available unless legal/ethical restrictions apply — tiered access model (open aggregated / restricted raw) should be explicitly justified.
**Typical concerns:** "Is the methodology sound?" "Are ethics properly documented?" "Is the data availability statement complete and justified?" "Has the protocol been registered?" "Can the methods be replicated?"
**Referee pool:** CREDIBILITY (high), REPRODUCIBILITY (high), SKEPTIC (medium), BASELINE (low), ARCHITECTURE (low), THEORY (low)

### British Journal of Educational Technology (BJET)
**Focus:** Educational technology research — learning analytics, technology-enhanced learning, digital learning environments, AI in education. Publishes original research, systematic reviews, and theoretical papers.
**Bar:** Strong educational technology contribution with clear implications for practice or policy. Empirical papers preferred — protocol or design papers may need to be framed as methodological contributions or "technology implementation frameworks." High impact factor (5.5) means the bar for acceptance is significantly higher than the other options. Theoretical grounding in educational or learning sciences expected alongside technical contribution. International readership — context should be framed for global relevance.
**Domain referee adjusts:** Contribution must be positioned within educational technology and learning analytics literature. The multimodal sensing platform should be framed as an educational technology innovation, not primarily as a sensor engineering contribution. Theoretical framework for how the modalities relate to cognitive performance/learning must be explicit. Implications for teaching practice, educational policy, or learning design should be discussed. Comparison to published EdTech/MMLA platforms (not sensor-engineering papers) is expected.
**Methods referee adjusts:** Educational research methodology standards apply. Study design, population, setting, and educational context must be thoroughly justified. Privacy and ethics in educational settings are evaluated against educational research standards (BERA, AERA) in addition to GDPR. Learning outcome measures should be validated for the educational context. Design-based research or design-science framing may be more appropriate than clinical protocol framing. Protocol registration is less commonly expected than in biomedical venues.
**Typical concerns:** "What is the educational technology contribution?" "How does this advance learning analytics practice?" "Are the educational implications clear?" "Is the privacy/ethics framework appropriate for educational settings with minors?" "Does this generalize beyond the single-school context?" "What would teachers/practitioners take away from this?"
**Referee pool:** CREDIBILITY (high), ARCHITECTURE (high), SKEPTIC (medium), BASELINE (medium), REPRODUCIBILITY (low), THEORY (low)

---

## Add Your Own Venue

Copy this template and add it above this section:

```markdown
### [Venue Name] ([Abbreviation])
**Focus:** [fields and topics covered]
**Bar:** [what it takes to publish here]
**Domain referee adjusts:** [what matters most to domain reviewers at this venue]
**Methods referee adjusts:** [rigor expectations, preferred methods, required checks]
**Typical concerns:** [common referee questions at this venue]
**Referee pool:** [disposition] (high/medium/low) for each: ARCHITECTURE, CREDIBILITY, REPRODUCIBILITY, BASELINE, THEORY, SKEPTIC
```
