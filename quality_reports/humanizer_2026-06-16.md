# Humanizer Agent — 2026-06-16

## AI Writing Pattern Scan

### 🔴 Major (should be fixed)

| # | Pattern | Location | Text |
|---|---------|----------|------|
| 1 | **"serves as"** | methods.tex:90 | "which serves as input to an XGBoost classifier" → "fed to an XGBoost classifier" |
| 2 | **"not merely declarative"** | discussion.tex:20 | Negative parallelism — classic AI pattern. "operationally enforceable, not merely declarative" → "operationally enforceable" (cut "not merely") |
| 3 | **"First... Second... Third... Fourth..."** | discussion.tex:20 | Mechanical enumeration. AI loves this. Rephrase as flowing prose |
| 4 | **"additionally"** | methods.tex:112 | Weak transition → "also" or restructure |
| 5 | **"wide range of"** | methods.tex:36 | AI filler → "on many spectral and event-related features" | 
| 6 | **"comprehensive"** | Not found ✓ |

### 🟡 Minor (style, not blocking)

| # | Pattern | Location | Notes |
|---|---------|----------|-------|
| 7 | **"in principle"** (×2) | intro.tex:3, methods.tex:112 | Weak hedge. Keep one, remove the other |
| 8 | **"to the team's knowledge"** | discussion.tex:20 | Acceptable academic hedge, but overused in this paper |
| 9 | **"it is appealing"** | intro.tex:3 | Slightly promotional. "Passive multimodal sensing is continuous, ecologically valid..." (cut "appealing because it is") |
| 10 | **"on a wide range of spectral and event-related features"** | methods.tex:36 | Already flagged as "wide range of" |

### 🟢 Clean (no AI patterns)

| Section | Status |
|---------|--------|
| Data Analysis Plan | ✅ Technical, precise, no fluff |
| Privacy Appendix | ✅ Operational language, no AI |
| SAP (descriptive characterisation) | ✅ Direct, metric-focused |
| Limitations | ✅ Honest, specific, no hedging |
| Sample size | ✅ Numerical, concrete |
| Fusion architecture | ✅ New version is specific (XGBoost + 1DCNN + TCN → LR), not shopping list |

---

## Recommendations

### Must-fix (5 edits):
1. methods.tex:90 — "serves as" → "fed to"
2. discussion.tex:20 — remove "not merely declarative"
3. discussion.tex:20 — de-enumerate "First...Second...Third...Fourth"
4. methods.tex:112 — "additionally" → "also"
5. methods.tex:36 — remove "wide range of"

### Should-fix (3 edits):
6. intro.tex:3 — remove "appealing because it is" → "Passive multimodal sensing is continuous, ecologically valid..."
7. intro.tex:3 — remove one "in principle"
8. methods.tex:90 — "serves as" already covered

### Score

| Category | Score |
|----------|-------|
| AI vocabulary density | LOW (3 instances across 8,700 words) |
| Promotional language | NONE (dashboard section already cleaned) |
| Mechanical enumeration | MODERATE (2 occurrences) |
| Weak hedging | LOW (2 "in principle") |
| **OVERALL** | **78/100 — Acceptable for submission** |
