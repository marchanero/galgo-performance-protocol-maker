# Paper: A Comparative Study of Emerging Architectures for EDA-based Arousal Classification

**Venue:** Biomedical Signal Processing and Control (BSPC)
**Status:** Accepted (92/100, 5 rounds of peer review)
**Authors:** Roberto Sánchez-Reolid, Daniel Sánchez-Reolid, Francisco Javier Celdrán, Antonio Fernández-Caballero
**Institution:** Universidad de Castilla-La Mancha (UCLM) — I3A / TSI

---

## Compilation

```bash
latexmk main.tex
```

- **Engine:** XeLaTeX (configured in `latexmkrc`)
- **Class:** `elsarticle` (Elsevier)
- **Bib:** `bibliography.bib` (70 entries)

Clean auxiliary files: `latexmk -c`

---

## Manuscript Structure

The paper is a single-file LaTeX document (`main.tex`, 863 lines). All sections, figures (TikZ), and tables are inline.

| Section | Content |
|---|---|
| Introduction | EDA, arousal classification, efficiency gap |
| Related Work | EDA-based affect recognition, efficient architectures |
| Methods | 8 architectures, 5 paradigms, LOSO protocol |
| Results | F1, AUC, parameter count, FLOPs, inference time, memory, training time |
| Discussion | Pareto frontier, channel ablation, classical baseline comparison |
| Limitations | Single dataset, lab conditions, generalisability |

Supplementary material in `supplementary.tex`.

---

## Resources

- **Overleaf sync:** [github.com/marchanero/BSPC-eda-efficient-transformers](https://github.com/marchanero/BSPC-eda-efficient-transformers)
- **Reference paper (prior work):** `../master_supporting_docs/supporting_papers/reference_paper.tex`
- **Figures:** All TikZ, ColorBrewer colorblind-safe palette
- **Agent framework:** `../.claude/` — 23 agents used for development and peer review simulation
