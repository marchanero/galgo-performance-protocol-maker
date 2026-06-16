# Humanizer Report — 2026-06-16 (Post-BOSS)

## High-Priority (remove/replace)
| Line | File | Pattern | Verdict |
|------|------|---------|---------|
| results.tex:27 | "MediaPipe Holistic" | "Holistic" | ✅ FALSE POSITIVE — official product name |

**Result: 0 AI vocabulary patterns found.**

## Medium-Priority
**Result: 0 patterns found.**

## Structural Flags (advisory)
| Line | File | Pattern | Note |
|------|------|---------|------|
| discussion.tex:20 | "First,... Second,... Third,... Fourth,..." | Mechanical enumeration | Strengths section — could flow as prose |
| discussion.tex:32 | "First,... Second,..." | Mechanical enumeration | Falsifiability thresholds — acceptable (exactly 2 items) |

## 🚨 Consistency Issue (non-humanizer)

| Line | File | Issue |
|------|------|-------|
| discussion.tex:32 | "$\textrm{óptimo}$-rate" | Still references old **binary scheme** — should reference **BOSS engaged proportion (AET+PET)** |
| discussion.tex:32 | "binary scheme" | References binary labelling — should reference BOSS 5-code |

## Score

| Category | Score |
|----------|-------|
| AI vocabulary density | 0/8,700 words — CLEAN |
| Promotional language | None detected |
| Structural AI patterns | 2 (advisory only) |
| **OVERALL** | **92/100 — Excellent** |
