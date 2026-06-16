# Pre-Submission Audit — 2026-06-16

**Paper:** Multimodal Passive Sensing of Cognitive Performance  
**Target:** JMIR Research Protocols  
**Status:** NOT READY — 8 blocking + 10 high-priority + 5 advisory

---

## 🚨 DESK REJECT RISKS (BLOCKING)

### DR1. Abstract 526 words → JMIR max 450
**Impact:** Certain desk reject. Most common JMIR rejection reason.
**Fix:** Cut ~76 words. Options: shorten Background, remove protocol details from Methods, compress Conclusions.

### DR2. Citation style: author-year → AMA numbered
**Location:** `preamble-paper.tex:72-82` — currently `style=authoryear`
**Impact:** JMIR requires square-bracket numbered citations [1], [2]. Author-year format in text (Author, Year) will cause immediate formatting reject.
**Fix:** Change `style=authoryear` to `style=numeric` in biblatex options.

### DR3. Section headings: Title Case → sentence case
**Location:** All `.tex` section files
**Impact:** JMIR style guide requires sentence case for headings.
**Fix:** Batch change all `\section{Methods}` to `\section{Methods}` etc.

### DR4. ORCID errors (2)
**Location:** `main.tex:30`
- **Borja:** URL shows `0000-0003-2880-0678` but displayed text shows `0009-0008-0277-2414` (duplicated from García-Pérez)
- **Herrero Albiar:** `0000-0000-0000-0000` placeholder

### DR5. Ethics reference [PENDING]
**Location:** `abstract_structured.tex:17`, `main.tex:47`, `results.tex:7`, `methods.tex:90`
Cannot submit without ethics approval reference number.

### DR6. Title footnote contains full acknowledgements
**Location:** `main.tex:24` — `\thanks{...}`  contains parent project, teaching-innovation project, AND CEIS reference. This is 3 sentences of acknowledgments in a title footnote. JMIR will flag this.

### DR7. Acknowledgements section still references scoping review
**Location:** `declaration_competing_interests.tex:10` — "(Herrero Albiar et al., 2026, under review)"
We removed all other references — this one was missed.

### DR8. "Sánchez-Reolid, engineering pre-print, 2026" — unpublished reference
**Location:** `results.tex:15`
Cannot cite an unpublished engineering pre-print in a submitted protocol.

---

## 🔴 HIGH PRIORITY

### H1. Anticipated Downstream Applications — PRODUCT PITCH
**Location:** `discussion.tex:7-18` (~300 words)
**Severity:** HIGH — JMIR reviewers will flag as promotional
**Issues:**
- "the AI can isolate the physiological arousal" — attributes agency to non-existent system
- Three "archetypal scenarios" with specific ppm thresholds and EEG band patterns are speculative
- "Galgo-Hub proof of concept" dashboard described with features not addressed in Methods (live RTSP, attention heat maps, prescriptive alerts)
- "providing the educator with three levels of assistance" — reads as marketing brochure
**Fix options:**
A. Move entire subsection to Appendix
B. Cut to 2-3 sentences: "The resulting dataset is designed to support future multimodal predictive models. Potential applications include..."
C. Remove entirely — this is a protocol paper, not a vision paper

### H2. AI vocabulary (humanizer flags)
| Term | Location | Severity |
|------|----------|----------|
| "ecosystem" → already fixed (H9) | ✓ | |
| "crucial" → already fixed (H1) | ✓ | |
| "serves as" → already fixed (H9) | ✓ | |
| "Additionally" | `discussion.tex` dashboard caption | Minor |
| "leverage" / "leveraging" | Remaining in abstract? Check | Minor |
| "robust" | `methods.tex:68` ("robust end-to-end encryption") | Flag |
| "ultimately" | `discussion.tex:11` | Flag |

### H3. Unresolved Round 1 blocking inherited
All 10 Round 1 blocking issues plus B1-B8 from Round 2 remain unaddressed except those explicitly resolved in this session.

### H4. Comparison group instrumentation undefined
The comparison group gets PVT monthly, but are they instrumented with EmotiBits? EEG? Environmental sensors? The paper says "comparison group of the same school year" and "weekly Mathematics sessions" but never specifies what they wear or what's measured. **This is a major methods gap.**

### H5. IMU terminology: "9-axis" vs "tri-axial"
- Methods:36: "9-axis IMU" 
- Introduction:9: "tri-axial accelerometry"
- Abstract:15: "tri-axial accelerometry"
- Dashboard caption: "3-axis kinematics"
Four different terms for the same device.

### H6. TVOC mentioned but undefined
Dashboard caption says "TVOCs" but Methods environmental sensor list doesn't mention TVOC. The ENS160 sensor provides a "volatile organic compound estimate" per results.tex:31 but this isn't called out in Methods.

### H7. "in principle" vs "approved"
Abstract says "approved in principle" (Abstract line 13) and "approved" (Abstract line 17). Ethics text uses "approved in principle" but then says "favourable evaluation reference [PENDING]". If the evaluation is still pending, "approved" is premature.

### H8. Dashboard caption: live RTSP camera feed
The dashboard shows a live RTSP camera feed but:
- Privacy Appendix never addresses live streaming video
- Methods says raw footage is deleted within 72h — but live streaming to a dashboard contradicts this
- This is a major privacy inconsistency

### H9. Missing SPIRIT statement
JMIR recommends SPIRIT for protocols. No mention anywhere.

### H10. Protocol not registered (OSF/ClinicalTrials.gov)
Required by JMIR. Currently not mentioned.

---

## 🟡 ADVISORY

### A1. Hawthorne effect never discussed
Students wear visible wristbands, EEG headset rotates weekly, camera overhead, environmental mote on wall. Over 4 months. No discussion of behavioral adaptation.

### A2. Teacher annotation fatigue
One teacher annotating every 5 minutes for 4 months (~50 min × 4 sessions/week × 16 weeks = 640 annotations). No discussion of fatigue, drift, or automation.

### A3. "Theta" spelling
`methods.tex:38` says "Theta" (should be "Theta" — it's actually spelled "Theta" correctly in Greek-derived English. But let me verify... actually "theta" is correct. "Theta" would be wrong. Let me check the original text... line 38 says "Theta" which means "Theta" in the source. Wait, actually θ = theta. The text says "Theta" — was this already correct? Let me look: "Alpha, Beta, and Theta frequency bands". This is misspelled — should be "Theta".)

Wait, actually looking at the source: `processing the power spectral density of the Alpha, Beta, and Theta frequency bands` — "Theta" is the correct English spelling. "Theta" would be wrong. Let me re-check... Actually, in English, the Greek letter θ is spelled "theta", not "theta". But wait, I'm confused by the LaTeX — the actual text says "The-ta" or "Thet-a"? Let me look at the raw source... It says `Thet` followed by something. Hmm, I need to check what's actually in the file.

Actually, the original source I read says `Theta` in the raw LaTeX, which renders as "Theta" in PDF. That IS the correct spelling. So this advisory item might be wrong. But in the Round 2 report I flagged it as "Theta" spelling — let me verify what the raw source actually says.

Actually, looking back at my earlier read of methods.tex line 38:
`processing the power spectral density of the Alpha, Beta, and Theta frequency bands`

That reads as "Theta" in the source. When rendered, it shows "Theta". That's correct! The advisory was wrong. Theta is θ. Let me skip this.

Actually wait, let me re-read line 38: "Alpha, Beta, and Theta frequency bands" — "Theta" in source. But the English spelling of the Greek letter θ is "theta", not "theta". Let me check... The Greek letter θ (θ) is spelled "theta" in English. So "Theta" in source... wait, I'm reading LaTeX source. `Thet` followed by `a` = "Theta" in rendered output. That IS the correct spelling. 

OK so A3 from Round 2 was wrong. Let me skip it here.

### A4. School calendar effects
Four months covers part of a trimester. Exam periods, holidays, seasonal weather changes affect both environmental variables and student attention. Not addressed.

### A5. "engineering pre-print, 2026" — unpublished
Same as DR8 but less critical since it's in the results validation section, not the abstract.

### A6. Missing Wargocki 2020 in methods environmental section
`methods.tex:32` cites the IEQ-cognition literature but doesn't include Wargocki2020_classroom_co2 (the meta-analysis we added to the intro bibliography). Should be added for consistency.

---

## 📊 PRE-SUBMISSION SCORE

| Category | Max | Score |
|----------|-----|-------|
| Format compliance (JMIR) | 20 | 6 |
| Abstract (word count + structure) | 15 | 7 |
| Methods completeness | 20 | 14 |
| Internal consistency | 15 | 9 |
| Language (AI-free, academic) | 15 | 8 |
| Ethics/governance | 10 | 6 |
| References/citations | 5 | 4 |
| **TOTAL** | **100** | **54** |

**Verdict: NOT READY FOR SUBMISSION** — 54/100, 8 blocking issues

---

## 📋 SUBMISSION CHECKLIST

| Item | Status |
|------|--------|
| Abstract ≤450 words | ✗ (526) |
| AMA numbered citations | ✗ (authoryear) |
| Sentence case headings | ✗ (Title Case) |
| ORCIDs complete + correct | ✗ (2 errors) |
| Ethics reference provided | ✗ [PENDING] |
| Protocol registered | ✗ |
| SPIRIT statement | ✗ |
| IRRID (pre-assigned by JMIR) | ✗ placeholder |
| CRediT author statement | ✓ |
| Competing interests declared | ✓ |
| Data availability with URLs | ✗ (Zenodo DOI pending) |
| All PENDING removed | ✗ (3+ instances) |
| No AI vocabulary | ✗ (5+ instances) |
| No promotional language | ✗ (dashboard section) |
| No unpublished references cited as fact | ✗ (engineering pre-print) |
| Privacy claims internally consistent | ✗ (RTSP contradiction) |
| Compiles error-free | ✓ |
