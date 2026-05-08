# Round 3 Consistency Referee Report

**Journal:** Biomedical Signal Processing and Control (BSPC)
**Manuscript:** _Efficient Transformer Architectures for Electrodermal Activity-based Arousal Classification_
**Reviewer disposition:** SKEPTIC
**Review date:** 2026-05-08
**Review focus:** Logical and evidentiary coherence (cross-referencing, internal consistency, overclaiming, edge-case coverage, narrative fidelity)

---

## Overall Assessment

This manuscript reports a methodologically careful comparison of eight architectures spanning multiple efficiency paradigms for EDA-based arousal classification. The experimental design (LOSO with 147 participants, grid-search-tuned hyperparameters, five complementary efficiency metrics) is rigorous, and the Pareto-frontier framing is a genuine contribution. However, this Round 3 review identifies **two major inconsistencies** (one of which affects a primary results table), **four moderate concerns** about statistical language, overclaiming, and evidence gaps, and **four minor narrative/formatting issues**. Collectively these do not invalidate the core findings but must be resolved before publication.

---

## Dimension 1: Claims-Evidence Alignment (Weight: 30%)

### MAJOR: Table 3.1 Bold Formatting Contradicts Stated Convention (Score impact: -25)

**Location:** Table 1 (line 409–441), `\label{tab:overall}`

**Finding:** The table caption states _"Bold indicates best performance per metric."_ However, the actual bolding is inconsistent with the numerical values:

| Metric | PatchTST (actual) | Mamba (actual) | Which is **bolded**? | Best value? |
|--------|-------------------|----------------|----------------------|-------------|
| Acc    | **0.873** | 0.868 | Mamba (0.868) | PatchTST 0.873 |
| Prec   | **0.867** | 0.862 | Mamba (0.862) | PatchTST 0.867 |
| Rec    | **0.858** | 0.852 | Mamba (0.852) | PatchTST 0.858 |
| F1     | **0.863** | 0.858 | Mamba (0.858) | PatchTST 0.863 |
| AUC    | **0.915** | 0.913 | **Both** bolded | PatchTST 0.915 |

PatchTST achieves the numerically highest value on **all five** classification metrics. Per the stated convention, PatchTST should be bold on Acc, Prec, Rec, F1, _and_ AUC. Instead, Mamba is bolded on Acc, Prec, Rec, and F1. This creates a direct contradiction between the table caption and the table body—a reader relying on the bolding convention would incorrectly conclude that Mamba is the best-performing model across the first four metrics.

**Risk:** This could mislead readers about which architecture achieves the best predictive performance. The paper's central narrative that "Mamba approaches PatchTST" is factually correct (based on the numbers themselves), but the bold formatting effectively erases PatchTST's performance advantage from visual inspection of the table.

**What would change my mind:** Correct the bolding so PatchTST values are bolded on all five metrics (or revise the caption to explain a different bolding convention, e.g., "bold = best among efficient architectures" — though this would require a clear definition of "efficient").

---

### MODERATE: Abstract "5–6 percentage point" Claim Partially Overstated

**Location:** Abstract (line 58) and repeatedly in text (lines 489, 738, 755)

**Finding:** The abstract states that architectures with global temporal modelling provide a _"consistent 5–6 percentage point improvement over both classical and simple learned baselines."_ Verified against the data:

| Comparison | F1 gap | In "5–6 pp" range? |
|------------|--------|---------------------|
| PatchTST 0.863 vs classical ~0.81 | +5.3 pp | Yes |
| PatchTST 0.863 vs DLinear 0.800 | +6.3 pp | Yes (borderline) |
| Mamba 0.858 vs classical ~0.81 | +4.8 pp | **No** — below 5.0 pp |
| Mamba 0.858 vs DLinear 0.800 | +5.8 pp | Yes |

Mamba is the "key finding" architecture highlighted in the abstract. Its improvement over the classical baseline is 4.8 pp, not 5–6 pp. A 4.8 pp gap rounds to "approximately 5 pp" but "5–6" implies a floor of 5.0.

**What would change my mind:** Either (a) revise to "approximately 5 percentage point improvement" (4.8–6.3 pp range), or (b) restrict the "5–6 pp" language to comparisons involving PatchTST only, with separate language for Mamba (e.g., "4.8 pp").

---

### MODERATE: Interpretability Claims Lack Quantitative Evidence

**Location:** Methods lines 396–400, Results lines 718–731

**Finding:** The Methods section promises a suite of interpretability analyses:
- _"attention weight distributions were extracted and analysed to quantify temporal relevance"_ (line 398)
- _"For Mamba, the discretised state transition matrices were examined"_ (line 397)
- _"Gradient-based saliency maps were computed as S = |∂ŷ/∂X|"_ (line 398)

The Results section provides only qualitative narrative descriptions (lines 722–728):
- _"attention weight distributions concentrate on SCR onset and rising phases"_ — no quantitative support (e.g., mean attention entropy, temporal concentration metrics, examples)
- _"TimesNet's period discovery mechanism identifies dominant periods in the 2–5 second range"_ — no histogram, no per-subject breakdown
- No saliency map figures, no attention heatmaps, no state matrix visualizations appear anywhere in the paper or supplementary materials

The Methods describe quantitative analyses; the Results deliver qualitative summaries. There is a methods-to-results evidence gap.

**What would change my mind:** Either (a) include quantitative metrics (e.g., attention concentration indices, period distribution statistics, saliency-channel contribution fractions) or (b) revise the Methods to frame interpretability as a qualitative discussion rather than a quantified analysis.

---

## Dimension 2: Internal Consistency (Weight: 25%)

### MAJOR: "Five Paradigms" Claim Inconsistent Across Paper

**Location:** Abstract (line 58), Introduction (line 75), figures (lines 161–166, 302–306)

**Finding:** The paper consistently claims _"five paradigms"_ but the classification of architectures into paradigms is inconsistent:

**Abstract claim:** Five paradigms = patch-based attention, sparse attention, frequency-domain modelling, state space models, modernised convolutions.

**Introduction enumeration (line 75):** Lists **seven** distinct paradigm descriptors: "(1) PatchTST (patch-based attention), (2) Informer (sparse attention), (3) Autoformer and TimesNet (frequency/periodicity-based), (4) FEDformer (Fourier attention), (5) Mamba (selective state space model), (6) ModernTCN (modernised convolution), and (7) DLinear (linear decomposition)."

**Figure 3.3 color groups (5 colors):**
- Blue = patch attention (PatchTST) → paradigm 1
- Green = frequency/periodicity (Informer, Autoformer, TimesNet) → paradigm 2
- Orange = Fourier/convolution (FEDformer, ModernTCN) → paradigm 3
- Purple = state space model (Mamba) → paradigm 4
- Red = linear baseline (DLinear) → paradigm 5

**Problems:**
1. Informer (sparse ProbSparse attention, O(L log L)) is grouped under "frequency/periodicity" (green) despite using no frequency analysis — it's a sparsity-based attention mechanism.
2. FEDformer (Fourier-enhanced attention) and ModernTCN (depthwise convolutions) share the orange color despite operating on fundamentally different computational primitives.
3. DLinear is described as a "paradigm" (linear decomposition) in the Introduction list but is clearly positioned as a baseline in the evaluation.
4. The count oscillates between 5 (figures, abstract), 6 (if DLinear is a separate paradigm), and 7 (Introduction list).

**What would change my mind:** Reconcile the paradigm classification across all parts of the paper. If five paradigms is the desired count: (1) patch-based attention (PatchTST), (2) sparse attention (Informer), (3) frequency-domain (Autoformer, TimesNet, FEDformer — all use FFT), (4) state space models (Mamba), (5) modernised convolutions (ModernTCN), with DLinear as a _baseline_ not a paradigm. Update Figure 3.3 captions, color codes, and text accordingly.

---

### MODERATE: Statistical Significance Language Internally Contradictory

**Location:** Lines 716 vs. 748–749

**Finding:** The paper simultaneously asserts and undermines its statistical claims:

- Line 716: _"statistically significant at the conventional α = 0.05 level (p = 0.048)"_ — an inferential claim.
- Lines 748–749: _"The Wilcoxon signed-rank test used for pairwise comparisons assumes independence of paired differences across folds. With leave-one-subject-out cross-validation, training sets for different folds share 146 of 147 subjects, introducing overlap that may inflate the effective sample size. **The reported p-values should be interpreted as descriptive indicators of effect consistency rather than exact inferential statistics.**"_ (emphasis added)

If p-values are _"descriptive indicators"_ rather than _"exact inferential statistics,"_ then the term _"statistically significant at the conventional α = 0.05 level"_ is inappropriate. Statistical significance is, by definition, an inferential claim tied to a null hypothesis test. Using it while acknowledging the test's assumptions are violated creates an internal contradiction.

**What would change my mind:** Either (a) remove all "statistically significant" language and describe the p-values as descriptive effect-consistency indicators throughout, or (b) provide a justification for why the violation of independence is considered minor enough that the test remains approximately valid (e.g., citing Nadeau & Bengio 2003 or a bootstrap-based correction).

---

### MINOR: Training Speed Comparison Uses Two Different Metrics Without Clarification

**Location:** Main text line 553 vs. Supplementary S4 line 127

- Main text: _"approximately 35× faster than PatchTST"_ — refers to per-epoch training time (1.2 s vs 42.8 s = 35.7×).
- Supplementary: _"DLinear converging approximately 100× faster than PatchTST in total wall-clock time"_ — refers to total training-to-convergence (0.6 h vs 60.6 h = 101×).

Both numbers are individually correct (35.7× per epoch, 101× total), but the main text does not explicitly note that these are different metrics. A reader comparing the two passages might perceive an inconsistency.

**What would change my mind:** Add a brief parenthetical in the main text clarifying that 35× refers to per-epoch speed, while the 100× in supplementary materials reflects total convergence time (due to DLinear requiring fewer epochs).

---

## Dimension 3: Overclaiming Detection (Weight: 20%)

### MODERATE: "First" Claim Overreaches Scope

**Location:** Line 73

**Text:** _"Furthermore, the SSM and modernised convolution paradigms have not been benchmarked against Transformer-based methods on physiological classification, leaving practitioners without evidence to guide paradigm selection."_

**Finding:** ECGMamba2024 (already cited in the manuscript, line 71 and line 331) benchmarks Mamba (SSM) against Transformers on ECG classification — explicitly a physiological signal. The paper's qualifier throughout is _"EDA-based arousal classification,"_ but this sentence drops the EDA specificity and claims absence from _"physiological classification"_ writ large. The word "physiological" is in the same sentence.

**What would change my mind:** Revise to: _"have not been benchmarked against Transformer-based methods on **EDA** classification"_ (adding the single word "EDA").

---

### MINOR: "Five complementary efficiency metrics"

**Location:** Abstract (line 58), Methods (lines 384–392)

The Methods section lists **five** metrics: (1) parameter count, (2) FLOPs, (3) inference time, (4) peak memory, (5) training time. This is internally consistent. However, the abstract elevates these to _"primary evaluation dimensions"_ while the rest of the paper predominantly emphasizes predictive accuracy. The efficiency metrics occupy one table and one Pareto figure — appropriate but arguably secondary in practice. This is a framing issue, not a factual error.

---

## Dimension 4: Edge Case Coverage (Weight: 15%)

### ADEQUATE: Most edge cases are covered

The paper addresses:
- Short windows down to 1 second (Figure 3.5)
- Channel ablation (SCR only → SCR + ΔSCR → all three channels) in Table S1
- Per-class F1 breakdown (Table S3)
- Both sliding-window and non-overlapping segmentation strategies
- Training convergence behavior (Table S4)
- The LOSO independence assumption violation (Limitations section)

### MINOR: Missing discussion of EDA decomposition method sensitivity

**Location:** Line 94 mentions alternative decomposition methods (cvxEDA, Ledalab) and acknowledges that _"the choice of decomposition method is known to influence downstream signal characteristics,"_ but no sensitivity analysis is performed. All results are conditioned on CDA decomposition. Given the paper claims to provide "actionable, evidence-based guidance" (line 58), a reader deploying these architectures with a different EDA decomposition pipeline has no evidence about whether architecture rankings would transfer.

This is noted as part of broader generalizability limitations (line 744), so it is partially addressed.

### MINOR: No >40-second window analysis

Figure 3.5 truncates at 40s. The text claims performance plateaus at 15–20s, so longer windows are arguably unnecessary, but a brief mention that >40s windows were not explored (or that they are constrained by the 47s stimulus length) would close this edge case.

---

## Dimension 5: Narrative Fidelity (Weight: 10%)

### The narrative is largely coherent and well-structured

The paper tells a clear story: EDA classification needs efficient architectures → prior work identified PatchTST as best but expensive → we benchmark eight efficient alternatives → Mamba approaches PatchTST at much lower cost → the Pareto frontier guides deployment decisions. This arc is maintained consistently from abstract through conclusion.

### MINOR: Narrative positioning of FEDformer is inconsistent

- In the Introduction (line 72) and Section 2.3.4, FEDformer is described as a frequency-domain architecture with O(L) complexity.
- In Figure 3.1 (pipeline), FEDformer is in the O(L) box alongside Mamba and ModernTCN.
- In Figure 3.3 (arch overview), FEDformer shares orange coloring with ModernTCN under "Fourier/convolution."
- In the narrative ordering (line 483), FEDformer is omitted from the tier description.

FEDformer scores F1=0.836, which is better than ModernTCN (0.827) and almost as good as TST from prior work (0.840). Yet it receives less narrative attention than its performance would warrant. A reader unfamiliar with these architectures might wonder why it's occasionally grouped with convolution-based models.

### MINOR: "Degrade most gracefully" caption overgeneralization

**Location:** Figure 3.5 caption (line 702): _"Mamba and PatchTST (thick lines) degrade most gracefully at short windows."_

At n=5s, Mamba = 0.810, PatchTST = 0.800. At n=1s, both = 0.730. The drop from n=5 to n=1 is Mamba: -0.080, PatchTST: -0.070. PatchTST actually degrades **less** from 5s→1s, but from the plateau, both drop similarly. The "most gracefully" claim is reasonable in aggregate but masks that Mamba outperforms PatchTST at every short window (1–15s). A more precise caption: _"Mamba and PatchTST maintain the highest short-window performance, with Mamba holding a consistent advantage below 15s."_

---

## Cross-Referencing Protocol Results

| Check | Result | Detail |
|-------|--------|--------|
| Abstract ↔ Results numbers | ⚠️ Partial | "5–6 pp" overstates Mamba vs classical (4.8 pp); all other numbers match |
| Introduction ↔ Conclusion contributions | ✅ Match | All 4 contributions map to findings |
| Methods ↔ Results coverage | ⚠️ Gap | Interpretability methods promise quantitative analysis; Results are qualitative |
| Tables ↔ Text numbers | ✅ Match | All verifiable numbers are consistent |
| Tables ↔ Text interpretations | ❌ **ERROR** | Table 1 bolding misrepresents best architecture per stated convention |
| Figures ↔ Captions ↔ Text | ⚠️ Minor | Fig 3.5 caption overgeneralizes; paradigm colors inconsistent with architecture groups |
| Prior work comparison conditions | ✅ Equivalent | Same dataset (147 participants, 4 Hz), same LOSO protocol, explicit accounting for Δ²SCR addition |

---

## Summary of Issues by Severity

### Critical (blocking)
None. No finding invalidates the core experimental results.

### Major (must fix)
1. **Table 3.1 bold formatting error:** PatchTST leads on all 5 metrics; bolding must reflect this per the stated convention.
2. **"Five paradigms" inconsistency:** Count and classification of paradigms differ between abstract (5), introduction (7 descriptors), and figures (5 color groups with misclassified architectures).

### Moderate (should fix)
3. Statistical significance language contradicts acknowledged LOSO independence violation.
4. "First" claim overreaches beyond EDA to all "physiological classification."
5. Interpretability claims lack quantitative evidence to match Methods promises.
6. Abstract "5–6 pp" range overstates Mamba's classical baseline improvement (4.8 pp).

### Minor (consider fixing)
7. Section 3.3 cross-reference for motion artefacts points to latency tiers, not deployment robustness; Section 3.8 is more relevant.
8. Training speed comparison uses two different metrics (per-epoch vs total) without explicit disambiguation.
9. FEDformer narrative positioning is inconsistent (omitted from tier description, grouped with ModernTCN in figure colors despite different mechanisms).
10. Figure 3.5 caption understates Mamba's short-window advantage over PatchTST.

---

## Weighted Composite Score

| Dimension | Weight | Raw Score | Weighted |
|-----------|--------|-----------|----------|
| Claims-Evidence Alignment | 30% | 70 | 21.0 |
| Internal Consistency | 25% | 72 | 18.0 |
| Overclaiming Detection | 20% | 75 | 15.0 |
| Edge Case Coverage | 15% | 78 | 11.7 |
| Narrative Fidelity | 10% | 80 | 8.0 |
| **Aggregate** | | | **73.7** |

The aggregate score falls below the paper's stated 80/100 commit threshold. The two major issues (Table 1 bolding, paradigm count inconsistency) account for the bulk of deductions and are straightforward to fix.

---

## Verdict

**Minor Revision.** The experimental foundations are solid, the LOSO protocol is appropriate, and the Pareto-frontier analysis is a genuine contribution. None of the identified issues undermines the core empirical findings. However, the Table 1 formatting error and paradigm-count inconsistency must be resolved before publication. The four moderate issues should be addressed to strengthen the paper's evidentiary coherence.
