# writing-anti-ai Skill — Full Audit (2026-06-16)

**Paper:** Multimodal Passive Sensing Protocol  
**Tool:** writing-anti-ai v2 (Wikipedia: Signs of AI Writing)

---

## Pattern Scan Results

| Category | Patterns Found |
|----------|:---:|
| Copula avoidance (serves as, stands for, represents) | 0 |
| Undue emphasis (stands as testament, crucial role) | 0 |
| Vague attributions (Experts believe, Studies show) | 0 |
| Superficial -ing analyses | 0 |
| Formulaic challenges (Despite X, faces challenges) | 0 |
| Promotional language (vibrant, breathtaking, unprecedented) | 0 |
| Filler phrases (In order to, Due to the fact that) | 0 |
| Negative parallelisms (not only... but also) | 0 |
| Rule of three (mechanical) | 0 |
| Em-dash overuse | 0 |
| AI vocabulary (delve, underscore, showcase, realm, notably) | 0 |

---

## 5-Dimension Scoring

| Dimension | Score | Commentary |
|-----------|:-----:|------------|
| **Directness** | 9/10 | Direct statements dominate. "The protocol tests four pre-specified hypotheses" — declarative, not hedging. Minor: "in principle" appears once in EEG spotlight section. |
| **Rhythm** | 8/10 | Varied sentence lengths. Introduction mixes long tech-review sentences with short punchy gap statements. Strengths section is enumerated but naturally (4 items). |
| **Trust** | 9/10 | Respects reader intelligence. No throat-clearing. Jumps into the science. Privacy appendix is technically precise without over-explaining. |
| **Authenticity** | 9/10 | Sounds like a research team, not a language model. "To the team's knowledge", "the team commits to report" — first-person academic voice. Specific references (CEIS-738323-C7M2, BOSS codes, sensor model numbers). |
| **Density** | 8/10 | Tight prose. 47 pages for 4 modalities + full pipeline + SAP + fusion + ethics + privacy. Could the data analysis plan be trimmed? Possibly 5% — but protocol papers require this detail. |

| **TOTAL** | **43/50** |
|-----------|:--------:|

---

## Verdict

**43/50 — Excellent (45-50 is "AI patterns removed").** 

The paper scores in the top tier. It doesn't sound AI-generated. The specific details (CEIS-738323-C7M2, AET/PET/OFT-P/OFT-M/OFT-V, EMQX broker, AHT21/ENS160/BMP280/TEMT6000 sensors, Reolink Elite Wi-Fi 4K) are the strongest anti-AI signal — no language model generates that level of hardware specificity.

---

## One Observation (Non-Blocking)

The Discussion section's Strengths paragraph ("First... Second... Third... Fourth...") is the only structurally mechanical passage. It's acceptable — protocol papers often enumerate strengths — but if you want to further humanize it, consider flowing the four strengths as prose without ordinal markers.

```
Current: "First, the simultaneous integration... Second, the 5-minute binary teacher..."
Option:  "The simultaneous integration of four passive modalities under a single NTP-disciplined acquisition pipeline is... The 5-minute binary teacher annotation adds an interpretable ground-truth label..."
```

This is purely stylistic — not required, not an AI marker per se.
