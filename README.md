# [YOUR-PROJECT-NAME]

[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

> **Authors:** [YOUR-AUTHORS] — [YOUR-INSTITUTION]

[YOUR-DESCRIPTION]

---

## Structure

```
[YOUR-PROJECT]/
├── paper/                        # Manuscript (source of truth)
│   ├── main.tex                  # Primary paper file
│   ├── bibliography.bib          # References
│   ├── sections/ figures/
│   ├── preambles/
│   └── supplementary/
├── data/                         # raw/ and cleaned/
├── scripts/                      # Python (primary), R, Julia
├── explorations/                 # Research sandbox
├── quality_reports/              # Plans, logs, reviews, scores
├── master_supporting_docs/       # Reference papers and data docs
└── .claude/                      # Agents, skills, rules, references
```

---

## Compilation

```bash
cd paper && latexmk main.tex
```

Uses XeLaTeX. Requires TeX Live/MacTeX. `paper/latexmkrc` configures the build.

---

## Built With

This repository uses the Clo-Author framework for agent-assisted academic research and writing.

## License

MIT License.
