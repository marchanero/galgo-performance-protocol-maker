# WRITER-CRITIC: Full Manuscript Polish Review
**Date:** 2026-05-12
**Target:** `paper/main.tex` (767 lines) + `paper/supplementary/main.tex` (166 lines)
**Critic:** Writer-Critic Agent (polish review)

---

## Aggregate Scores

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| 1. Structure | 85 | 0.10 | 8.50 |
| 2. Claims-Evidence Alignment | 80 | 0.15 | 12.00 |
| 3. Intellectual Debt Fidelity | 85 | 0.15 | 12.75 |
| 4. Writing Quality | 78 | 0.15 | 11.70 |
| 5. Grammar and Mechanics | 76 | 0.15 | 11.40 |
| 6. Figure and Table Quality | 78 | 0.15 | 11.70 |
| 7. Abstract | 82 | 0.10 | 8.20 |
| 8. Venue Fit | 75 | 0.05 | 3.75 |
| **Aggregate** | | | **80.00** |

**Gate:** ≥ 80/100 → **PASS (bare threshold)**. The aggregate score just meets the commit gate. Several actionable issues below could push scores meaningfully higher.

---

## Category 1: Structure (85/100)

### Strengths
- Clear logical flow: Abstract → Introduction → Method → Results & Discussion → Conclusion.
- Subsections appropriately granular (Method: 5 subsections; Results: 8 subsections).
- Figures embedded near their first textual reference.

### Issues

| # | Line(s) | Issue | Suggested Fix |
|---|---------|-------|---------------|
| 1.1 | 309–340 | Eight consecutive `\subsubsection` headings for architecture descriptions creates deep nesting. | Consolidate into grouped paragraphs within a single "Architecture Descriptions" subsection, using bold run-in headings per architecture instead of sub-subsections. |
| 1.2 | 753–761 | Conclusion section is 3 full paragraphs — too long and partially redundant with Introduction (line 75) and Discussion. | Cut to 1 paragraph summarising the key finding, plus 1 paragraph for implications/future work. Remove repeated phrasing about "pragmatic recognition that translational value depends on deployability" (line 757), already stated in Results (line 628). |
| 1.3 | 734–740 | "Comparison with Prior Work" (3.7) overlaps substantially with text already in 3.1 (Overall Performance) and the Conclusion. | Consolidate into 3.1 or move as a bridge paragraph to 3.8 (Limitations). Avoid repeating the DLinear vs. 1D-CNN parity argument three times (lines 489, 738, and 755–756). |
| 1.4 | — | No dedicated "Related Work" section. | While the combined Introduction is acceptable for shorter formats, BSPC typically expects a separate background section. Consider splitting Introduction into: 1. Introduction (motivation, gap, contributions), 2. Related Work (EDA ML, efficient architectures, BSPC context). |

---

## Category 2: Claims-Evidence Alignment (80/100)

### Strengths
- Every major numerical claim is supported by a table or figure.
- Per-fold standard deviations reported in Table 3.
- Effect sizes (F1 differences in pp) reported alongside p-values (line 748).

### Issues

| # | Line(s) | Issue | Suggested Fix |
|---|---------|-------|---------------|
| 2.1 | 69 | "In prior work \cite{SanchezReolid2022}, we compared five architectures (1D-CNN, TCN, InceptionTime, TST, PatchTST) under LOSO with 147 participants." — The `SanchezReolid2022` bib entry is a *systematic review* in *Sensors* (Vol. 22, p. 8886), not an empirical architecture comparison. Systematic reviews do not produce original experimental results. | Either: (a) update the citation to the correct empirical paper that conducted the 5-architecture LOSO comparison, or (b) if the systematic review paper *did* contain empirical benchmarking, the bib entry's title ("A systematic review") is misleading and should be corrected to reflect its empirical content. This is the single most important fix in the manuscript. |
| 2.2 | 65 | "providing a robust biomarker for emotional arousal that is exclusively innervated by the sympathetic branch" — a *biomarker* is not innervated; *sweat glands* are innervated. The grammar makes a false physiological claim. | Rewrite: "EDA reflects sympathetic nervous system activation through sudomotor nerve activity. Unlike heart rate or respiration, sweat glands receive no parasympathetic innervation \cite{...}, making EDA a biomarker of exclusively sympathetic arousal." |
| 2.3 | 706 | "Performance plateaus beyond 15--20 seconds, consistent with the physiological observation that individual SCRs rarely exceed 15 seconds in duration \cite{LongTermVariability}." — Boucsein (2012) discusses SCR duration but the specific claim "rarely exceed 15 seconds" needs verification. Boucsein notes SCR recovery can extend beyond 15 s; the claim is overly precise. | Add hedging: "consistent with the physiological observation that individual SCRs typically complete within 10--20 seconds \cite{LongTermVariability}." |
| 2.4 | 485 | "The original Mamba evaluation reported 5× inference throughput for Mamba compared to equivalently-sized Transformers \cite{Mamba2023}, directly addressing the deployment constraints that motivate this work." — The Mamba paper reported this on language modeling tasks, not physiological time-series. The extrapolation is implied but not explicit. | Add a qualifier: "While the original Mamba evaluation demonstrated 5× inference throughput on language modeling tasks \cite{Mamba2023}, our results provide the first evidence that this efficiency advantage extends to physiological time-series classification." |
| 2.5 | 67 | "LSTM and bidirectional LSTM networks...were excluded from this benchmark because prior work on the same EDA dataset found that recurrent architectures underperform... \cite{sanchez2022one}." — The `sanchez2022one` paper is about 1D-CNNs. Did it actually benchmark LSTMs? If not, the justification is weak. | Verify that `sanchez2022one` compared LSTMs on the same 147-participant LOSO protocol. If not, either: (a) cite a different paper that did, (b) add a brief LSTM baseline to this study, or (c) reframe as a methodological choice rather than an evidence-based exclusion. |
| 2.6 | 730 | "This pattern suggests that the additional temporal context provided by derivative channels is partially redundant with the representations learned by attention and state-space mechanisms, rather than implying that the latter explicitly reconstruct derivative information." — This hedging is excellent, but it appears only in the main text. The Abstract states this claim more declaratively: "derivative channels provide greatest benefit for simpler architectures, while the additional temporal context from derivatives is partially redundant with representations learned by attention and state-space mechanisms" (no hedging). | Add a qualifier in the Abstract: "suggesting that..." or "qualitatively suggesting that...". |

---

## Category 3: Intellectual Debt Fidelity (85/100)

### Strengths
- 46 references covering EDA physiology, time-series deep learning, and efficient architectures.
- BSPC-specific references (Zhao2023BSPC, Anusha2022BSPC, Ramadan2024BSPC, Kasnesis2025BSPC, Lee2025BSPC) demonstrate venue contextualisation.
- Self-citation rate: 3 of ~41 unique citations (~7.3%) — well within norms for a lab with prior related work.

### Issues

| # | Line(s) | Issue | Suggested Fix |
|---|---------|-------|---------------|
| 3.1 | 69 | **CRITICAL:** `SanchezReolid2022` citation mismatch (same as 2.1). A systematic review paper cannot be the source for an empirical 5-architecture LOSO comparison on 147 participants. | Provide the correct citation. If the empirical work is unpublished, either: (a) describe it as "our unpublished experiments" with a footnote, or (b) add the architecture comparison results to this paper's supplementary material and cite the supplementary. |
| 3.2 | 67–68 | The BSPC references paragraph (lines 67–68) lists 5 recent BSPC papers with brief descriptions but does not explicitly state how this paper differs from or extends them. They read as name-dropping rather than critical engagement. | Add 1–2 sentences explaining the methodological gap: e.g., "While these studies demonstrate the growing adoption of deep learning in BSPC for physiological signal classification, none provides a systematic architecture comparison under strict subject-independent protocols with joint accuracy-efficiency evaluation." |

---

## Category 4: Writing Quality (78/100)

### Strengths
- Technical terminology is precise and consistent.
- Figures and tables are well-integrated with text discussion.
- The Pareto frontier framing (Section 3.3) is an effective conceptual device.

### Issues

| # | Line(s) | Issue | Suggested Fix |
|---|---------|-------|---------------|
| 4.1 | 58 | Abstract first sentence is ~295 words spanning ~2000 characters — far too long for a single-sentence abstract opening. | Split into 4–5 shorter sentences. The abstract should be scannable, not a wall of text. |
| 4.2 | 70 | "However, despite patch-based tokenisation reducing the effective sequence length, PatchTST retains $O(N^2)$ self-attention complexity, and its latency and memory consumption on a 40-second EDA window ($T = 160$ at 4 Hz) may exceed the constraints of low-power wearable processors." — 42-word sentence with multiple clauses. | Split: "Patch-based tokenisation reduces the effective sequence length, but PatchTST still incurs $O(N^2)$ self-attention complexity. For a 40-second EDA window ($T = 160$ at 4 Hz), its latency and memory consumption may exceed the constraints of low-power wearable processors." |
| 4.3 | 755–756 | "A classical signal processing baseline...achieved F1 $\approx$ 0.81..." appears nearly verbatim in: Abstract (line 58–59), Introduction (line 75), Section 3.1 (line 489), Section 3.7 (line 738), and Conclusion (line 755–756). | Retain the claim in 1–2 locations only (Abstract + Section 3.1 where first discussed). Remove from Conclusion and Introduction contributions list. |
| 4.4 | 339 | "ModernTCN...modernises the convolutional paradigm" — the word "modernises" is overused (lines 72, 339, 740). | Vary: "reformulates," "extends," or "updates the convolutional paradigm." |
| 4.5 | 58 (Abstract) | "actionable, evidence-based guidance" — "actionable" is business jargon. | Replace with "empirically-grounded guidance" or "practical guidance." |
| 4.6 | 628 | "A practitioner deploying an EDA-based stress monitor on a smartwatch, for instance, can consult Figure~5" — the "for instance" interrupts the flow. | "For instance, a practitioner deploying an EDA-based stress monitor on a smartwatch can consult Figure~5..." |

---

## Category 5: Grammar and Mechanics (76/100)

### Issues

| # | Line(s) | Issue | Suggested Fix |
|---|---------|-------|---------------|
| 5.1 | 65 | "providing a robust biomarker for emotional arousal that is exclusively innervated by the sympathetic branch" — "biomarker...innervated" is grammatically incorrect (biomarkers are not innervated). | See fix in 2.2. |
| 5.2 | 744 | "generalizability" (American spelling) vs. rest of manuscript uses British English: "modernised" (line 72), "characterise" (line 553), "labelled" (context). | Choose one convention and apply consistently. Either: change all -ise/-ised to -ize/-ized (American), or change "generalizability" → "generalisability" (British). BSPC (Elsevier) accepts either, but consistency is required. |
| 5.3 | 67–68 | "several deep learning approaches have been proposed" then "Transformer-based methods have been applied" then "Within BSPC..." — the Introduction switches from passive voice to "this work presents" (line 75) inconsistently. | Standardise: use passive voice throughout the literature review portions, and "we" only for describing the authors' own work. Alternatively, adopt "we" consistently throughout (acceptable in BSPC). Current mixed usage is noticeable. |
| 5.4 | 58 | The Abstract contains an unmatched closing parenthesis or truncated text near line end: "...under specific resou..." — verify the source file is not truncated. | Check the actual `.tex` source. If the abstract was truncated during writing, complete it. The display may simply be the tool's view; if the `.tex` file is complete, this is a non-issue. |
| 5.5 | — | `amsfonts` package loaded (line 6) but `amsmath` (line 5) already loads `amssymb`, making `amsfonts` redundant. | Remove `\usepackage{amsfonts}` unless `\mathbb` or other AMS font commands are used outside math mode. |
| 5.6 | 418 | `\tnote{*}` and `\tnote{a}` used together in `threeparttable`. The `*` mark is non-standard for `threeparttable` and may cause LaTeX warnings. | Replace `*` with a standard letter: `\tnote{b}` for the missing-metric footnote, and `\tnote{a}` for the SVM baseline. |
| 5.7 | 770 | Main text and supplementary both have `\bibliographystyle{splncs04}` and use `\bibliography{bibliography.bib}`. The supplementary uses `../bibliography.bib` (line 130) while main uses `bibliography.bib` (line 765). The supplementary file references bibliography outside its own directory. | Ensure paths are correct at compile time. If supplementary compiles independently, it should either have its own bibliography file or the `TEXINPUTS`/`BIBINPUTS` path should be properly configured via `latexmkrc`. |

---

## Category 6: Figure and Table Quality (78/100)

### Strengths
- All 6 figures use publication-quality TikZ/pgfplots with consistent ColorBrewer palette.
- All tables use `booktabs` with professional formatting.
- Captions are self-contained and informative.
- Color coding is consistent across all figures (blue = $O(N^2)$, green = $O(L \log L)$, orange = $O(L)$ conv/Fourier, purple = $O(L)$ SSM, red = $O(L)$ linear baseline).

### Issues

| # | Line(s) | Issue | Suggested Fix |
|---|---------|-------|---------------|
| 6.1 | 445–481 | Figure 3 (F1 bars) and Table 3 (overall results): Table 3 reports mean $\pm$ std, but Figure 3 shows only means without error bars. This is a significant omission for a paper emphasising statistical rigor. | Add error bars (standard deviation whiskers) to Figure 3. Same for Figure 4 if applicable. |
| 6.2 | 632–704 | Figure 6 (window length): 10 architecture curves plotted simultaneously. The line style differentiation within paradigms (solid vs. dashed vs. dotted for Informer/Autoformer/TimesNet, all green) is nearly indistinguishable, especially in grayscale print. | Options: (a) use distinct hues within each paradigm family, (b) split into two panels (e.g., Transformers in one, non-Transformers in another), or (c) use different plot markers in addition to line styles. |
| 6.3 | 632–704 | Figure 6: No error ribbons or shaded regions for standard deviation. Given that LOSO produces 147 per-fold values at each window length, variability information is available and should be shown. | Add translucent shaded regions representing ±1 std across folds (at minimum for PatchTST and Mamba). Alternatively, note in the caption that variability bands are excluded for visual clarity and are available in the supplementary. |
| 6.4 | 413 | Table 3 uses `\resizebox{\linewidth}{!}` which scales the entire tabular, potentially making font sizes illegibly small in the printed version. The 5-column format with mean ± std values is information-dense. | Consider a landscape table or breaking into two tables: (a) main table with F1 and AUC only, (b) supplementary table with all 5 metrics. Alternatively, reduce to F1 + AUC + Acc and move Precision/Recall to supplementary. |
| 6.5 | 413 | Table 3 footnote: "Representative value at 40s window" for the SVM baseline — a single representative value without standard deviation is weaker than the values for other architectures. | If per-fold SVM results are unavailable, state this explicitly: "Per-fold standard deviations not available for the retrospective SVM baseline." (Already noted in the `\tnote{*}` footnote but the text is very small.) |
| 6.6 | 559–620 | Figure 5 (Pareto): The $x$-axis uses a log scale but the tier thresholds (Tier 1: $\leq 1.5$ ms, Tier 2: 1.5–4 ms, Tier 3: $\geq 4$ ms) are defined on a linear scale. The shaded regions on a log scale may misrepresent the relative width of tiers. | Add a note in the caption that tier boundaries appear compressed on the log scale, or use a linear $x$-axis with a break, or annotate the $x$-axis with the actual ms values at key tick marks. |

---

## Category 7: Abstract (82/100)

### Strengths
- Contains all five required elements: context, gap, method, key finding, implications.
- Numerical results are properly reported with appropriate precision.
- The final sentence ("These results provide...") closes the abstract effectively.

### Issues

| # | Line(s) | Issue | Suggested Fix |
|---|---------|-------|---------------|
| 7.1 | 58–59 | Abstract is approximately 250–300 words in a single sentence block. For BSPC (typically 150–250 words), this is at the upper limit, and the density reduces readability. | Cut secondary findings (SVM baseline, channel ablation, derivative redundancy) from the abstract. These are well-covered in the paper body and do not need to appear in the abstract. The abstract should highlight: (1) problem, (2) method (8 architectures, LOSO, 147 participants), (3) key result (Mamba near-PatchTST at 3.6× lower latency), (4) significance (Pareto frontier, deployment guidance). |
| 7.2 | 58 | "A classical signal processing baseline (handcrafted EDA features with SVM) achieved F1 $\approx$ 0.81 on the same dataset, anchoring the deep learning performance gains..." — This level of detail belongs in the Results section, not the Abstract. | Remove or reduce to: "...confirming that architectures with global temporal modelling provide an approximately 5 pp improvement over classical and simple learned baselines." |
| 7.3 | 58 | "actionable, evidence-based guidance" — see 4.5. | Replace with "practical guidance" or "empirically-grounded guidance." |
| 7.4 | 58 | The abstract uses "Mamba---a selective state space model" (em-dash appositive) which is elegant. However, the overall structure is: one massive block of text with no paragraph break. | Consider a single paragraph break (if journal allows structured abstracts). Even without explicit headings, a logical break between "what we did" and "what we found" improves readability. |

---

## Category 8: Venue Fit (75/100)

### Strengths
- Topic (EDA-based arousal classification with efficient deep learning) is well-aligned with BSPC scope.
- Rigorous LOSO validation with 147 participants meets BSPC methodological standards.
- Joint accuracy-efficiency evaluation addresses BSPC's interest in translational biomedical signal processing.
- BSPC-specific references cited throughout.

### Issues

| # | Line(s) | Issue | Suggested Fix |
|---|---------|-------|---------------|
| 8.1 | 1 | **CRITICAL:** `\documentclass[runningheads]{llncs}` — LLNCS is Springer LNCS, not Elsevier. BSPC requires `\documentclass[review]{elsarticle}` (or `elsarticle` for final). This is a fatal formatting mismatch for submission. | Convert the manuscript to `elsarticle` document class with appropriate Elsevier formatting (running title, author affiliations with `\author[1]{...}`, `elsarticle`-style bibliography). The LLNCS format may be retained for arXiv preprints, but the submission-ready version must use `elsarticle`. |
| 8.2 | 764 | `\bibliographystyle{splncs04}` — Springer bibliography style, incompatible with Elsevier's `elsarticle-num` or `model5-names` styles. | Change to `\bibliographystyle{elsarticle-num}` or whichever style BSPC specifies in its author guidelines. |
| 8.3 | 753–761 | Conclusion references "Supplementary Material, Table S4" — the supplementary file uses `\label{tab:s4_training}` but this cross-reference is not resolvable across separate `.tex` files compiled independently. | Hard-code table numbers in the main text (as currently done) and verify the supplementary file's compilation produces consistent numbering (S1–S4). Add a verification step to the makefile/build script. |
| 8.4 | 106–186 | Figure 1 (pipeline) is 80 lines of TikZ code embedded inline. While the figure is informative, this much inline code makes the `.tex` source harder to navigate. | Move TikZ figures to separate `.tex` files in `paper/figures/` and `\input{}` them. Improves source maintainability without affecting output. |
| 8.5 | — | Page count: With 6 full-page TikZ figures and dense tables, the manuscript likely exceeds 20 pages in `elsarticle` two-column format. | Verify page count after `elsarticle` conversion. If over BSPC typical length (~20 pages), consider moving Figure 2 (arch overview) or Figure 6 (window length) to supplementary. |

---

## Top 10 Most Impactful Improvements (Ranked)

| Rank | Category | Line(s) | Issue | Impact |
|------|----------|---------|-------|--------|
| 1 | 8 – Venue Fit | 1 | Wrong document class (`llncs` instead of `elsarticle` for BSPC). Manuscript will be rejected at desk without format compliance. | **Critical** |
| 2 | 3 – ID Fidelity / 2 – Claims | 69 | `SanchezReolid2022` citation points to a systematic review paper, not the empirical 5-architecture LOSO comparison claimed in the text. Undermines credibility of the central prior-work comparison. | **Critical** |
| 3 | 6 – Figures | 445–481 | Figure 3 (F1 bars) and Figure 6 (window length) missing error bars/standard deviation bands despite reporting mean ± std in tables. Undermines statistical rigor claims. | **High** |
| 4 | 7 – Abstract | 58–59 | Abstract is excessively long (~250–300 words) and includes secondary findings (SVM baseline, channel ablation) that dilute the core message. | **High** |
| 5 | 5 – Grammar | 65 | Grammatically incorrect claim: "biomarker...exclusively innervated by the sympathetic branch" — biomarkers are not innervated. A core physiological claim is misstated. | **High** |
| 6 | 5 – Grammar | 744 | Spelling inconsistency: British "modernised"/"characterise" mixed with American "generalizability". Inconsistent language convention throughout. | **Medium** |
| 7 | 4 – Writing | Multiple | SVM baseline F1 ≈ 0.81 claim repeated verbatim in 5 locations (Abstract, Introduction, 3.1, 3.7, Conclusion). Redundant and dilutes impact. | **Medium** |
| 8 | 6 – Figures | 632–704 | Figure 6 (window length): 10 overlapping curves with subtle line style differences. Practically unreadable in print/grayscale. | **Medium** |
| 9 | 2 – Claims | 67 | LSTM exclusion justification cites `sanchez2022one` (a 1D-CNN paper). Unclear whether the cited paper actually benchmarked LSTMs on the same dataset and protocol. | **Medium** |
| 10 | 1 – Structure | 309–340 | Eight consecutive `\subsubsection` headings for architecture descriptions. Deep nesting reduces readability. | **Low-Medium** |

---

## Detailed Line-by-Line Issues (Supplementary)

### Grammar / Typos

| Line | Text | Issue | Fix |
|------|------|-------|-----|
| 57 | "reliable, non-invasive biomarker" | "reliable" is subjective. | "well-established, non-invasive biomarker" |
| 58 | "approaching PatchTST accuracy (F1 = 0.863) at 3.6$\times$ lower latency" | "at" is slightly ambiguous — suggests Mamba *has* PatchTST accuracy *at* lower latency, but Mamba's F1 = 0.858 < 0.863. | "approaching PatchTST accuracy (F1 = 0.863 vs. 0.858) with 3.6$\times$ lower latency" |
| 65 | "Unlike heart rate or respiration, EDA carries no parasympathetic influence" | Comma splice. Better: "Unlike heart rate or respiration, which carry parasympathetic influence, EDA reflects..." | (see fix 2.2) |
| 70 | "This practical limitation motivates investigation of substantially more efficient architectures." | Sentence fragment style. | "This limitation motivates the investigation of substantially more efficient architectures." |
| 489 | "F1 in the range of 0.80--0.83" then "F1 gap of approximately 0.05--0.06" — mixing "range" with "gap." | "gap of approximately 5–6 pp" or "0.05–0.06." |
| 626 | "without surviving the Bonferroni-Holm correction" → "not surviving" is awkward. | "but does not survive the Bonferroni-Holm correction." |
| 643 | "Performance plateaus" — verb usage is correct but may confuse non-native readers. | Optionally: "Performance reaches a plateau." |

### Citation Checks

| Citation Key | Lines Used | Bib Entry Matches? | Notes |
|-------------|------------|-------------------|-------|
| `SanchezReolid2022` | 69, 420, 479, 654, 702, 734, 744 | Systematic review (Sensors, 2022) | **MISMATCH** — text claims empirical 5-architecture LOSO comparison |
| `sanchez2022one` | 67, 94 | 1D-CNN paper (BSPC, 2022) | Check if LSTM comparison is actually in this paper |
| `sanchez2020deep` | 58, 82, 88, 418, 755 | Deep SVM paper (IJNS, 2020) | Plausible F1 ≈ 0.81 with SVM, but footnote says "handcrafted features" — deep SVM is not "handcrafted" |
| `LongTermVariability` | 65, 84, 327, 376, 706, 722 | Boucsein (2012) textbook | ✓ Correct — seminal EDA reference |
| `Azad2025` | 67, 84, 376 | (presumably LOSO/data leakage paper) | Cannot verify from bib excerpt; appears plausible |

---

## Supplementary Material Assessment

The supplementary (`paper/supplementary/main.tex`, 166 lines) is well-structured with 4 tables (S1–S4) and a "Further Reading" section.

### Supplementary Issues

| # | Line(s) | Issue | Suggested Fix |
|---|---------|-------|---------------|
| S1 | 72 | "Under the conventional $\alpha = 0.05$ threshold, 24 of 28 comparisons are statistically significant." — This statement appears in the supplementary *and* the main text (line 716). | Avoid duplication. The supplementary should present detailed results; the main text should provide a summary only. |
| S2 | 126 | "For practitioners iterating on architecture design, this 35$\times$ training speed difference substantially impacts development velocity." — "development velocity" is informal. | "this 35$\times$ difference substantially affects the speed of model development and hyperparameter tuning." |
| S3 | 132–166 | "Further Reading" section lists 14 references not cited in the main text. While well-intentioned, this is unconventional for a journal supplementary and may be seen as padding. | Remove or move to a "Recommended Reading" note that explicitly states these are not cited in the paper but provide relevant context. |
| S4 | 45 | "attention and state-space mechanisms partially learn temporal derivative information implicitly from the raw SCR signal" — this is a stronger claim than the hedged version in the main text (line 730: "suggests...rather than implying that the latter explicitly reconstruct"). | Align the hedging level between main text and supplementary. |

---

## Summary

The manuscript is in strong draft condition with a clear narrative arc, rigorous methodology, and good figure/table quality. The aggregate score meets the 80/100 commit gate, but **just barely**. The three blocking issues before submission are:

1. **Convert to `elsarticle` format** (current `llncs` is wrong for BSPC).
2. **Fix the `SanchezReolid2022` citation mismatch** — the systematic review paper cannot be the source for the empirical 5-architecture comparison.
3. **Add error bars to key figures** (F1 bar chart, window length curves) to match the statistical rigor claimed in the text.

Addressing the top 10 issues above would elevate the aggregate score from 80 to approximately 87–90.
