## 2026-05-08 — BSPC Peer Review: 5 Rounds → ACCEPT (~88/100)

**Operations:**
- BSPC full peer review simulation (R1→R5): 3 referees, 17 review reports generated
- paper/main.tex: 40+ edits — classical SVM baseline, 13 new references (8 BSPC), p-value correction, deployment tier re-labeling, paradigm count fix, LSTM exclusion rationale, seed specification, interpretability qualifiers
- paper/bibliography.bib: corrected `sanchez2020deep` → Deep-SVM IJNS 2020; added 11 new entries (3 BSPC + 5 EDA classical + 3 more BSPC)
- paper/supplementary/main.tex: Table S2 bold + count fix (22→24 raw, 18→13 BH)
- .claude/references/domain-profile.md: full rewrite — author profile (21 pubs from ORCID/Crossref), BSPC calibration, self-citation rules, Overleaf sync conventions
- .claude/references/journal-profiles.md: BSPC expanded with critical/constructive pet peeves + self-citation guidelines
- AGENTS.md: Overleaf sync URL updated to `BSPC-eda-efficient-transformers`
- quality_reports/reviews/2026-05-08_*: 17 review reports across 5 rounds
- quality_reports/reviews/2026-05-08_self_citation_analysis.md: self-citation audit

**Decisions:**
- Classical SVM baseline (F1≈0.81) from Deep-SVM paper anchors DL gains — critical for BSPC
- GPU-relative deployment tiers (Low/Mid/High-latency) instead of wearable/mobile/cloud — avoids hardware overclaiming
- Self-citations reduced from 59%→36% — acceptable for follow-up paper
- DLinear is baseline, not paradigm → "five paradigms and a linear baseline"
- LSTM/BiLSTM excluded with justification — prior work underperforms on 40s EDA windows
- Force push breaks Overleaf sync → use manual clone+copy+normal push

**Results:**
- Starting score: 68/100 (Major Revision, R1)
- Final score: ~88/100 (Accept, R5)
- 41 unique citations, 8 from BSPC
- All 12 R1 issues resolved; all internal contradictions corrected
- Paper now reads as biomedical signal processing contribution, not ML benchmark with EDA

**Commits (this session):**
- `ab55454` BSPC revision: classical SVM baseline, 10 new references, fix p-value + deployment tiers
- `f40e6ab` BSPC R2 re-evaluation: 85/100 Minor Revision → Accept
- `0c6087a` Update agents with BSPC review learnings
- `c8f95a3` Add author profile from ORCID/Crossref
- (plus Overleaf pushes: `b3dc0c0` FINAL)

**Status:**
- Done: Paper ACCEPT ready for BSPC submission. All reviews saved. Agents calibrated.
- Pending: Submit to BSPC. Address any peer review if requested.
- Overleaf: `github.com/marchanero/BSPC-eda-efficient-transformers` (sync: Menu → GitHub → Pull)

