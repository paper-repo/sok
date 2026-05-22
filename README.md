# Harpo Artifacts 

This repository contains the artifacts for the paper:
**“SoK: A Practical Black-Box Framework for Evaluating Differential Privacy in Cyber-Physical Systems.”**

It provides:
- Harpo evaluation inputs as JSON files (`paper.json`, `weight.json`)
- The scoring implementation (`blackbox.py`) that outputs **Privacy / Utility / Safety** scores in **[0,1]**
- A script to generate the interactive 3D plot (`3Dplot.py`) from the score table
- The score table used for plots (`scores.xlsx`)

> **Anonymity note:** This repository is intended for anonymous review. Please avoid linking it to personal accounts or identifiable information during the review period.

---

## Repository Contents

- `blackbox.py` — computes scores from `paper.json` and `weight.json`
- `paper.json` — example per-paper (edit this for a new paper)
- `weight.json` — fixed weights
- `scores.xlsx` — dataset of reviewed papers’ scores (used for the plots)
- `3Dplot.py` — generates the interactive 3D visualization (HTML) from `scores.xlsx`
- `LICENSE` — MIT license
- `.gitignore`

---

## Quick Start (Compute a Score)

Edit `paper.json` for the paper you want to evaluate, then run:


python blackbox.py paper.json weight.json


---
## Output
The output is a JSON object with three scores in [0,1]:

{
  "Privacy": 0.2,
  "Utility": 0.3,
  "Safety": 0.0
}
## Generate the 3D Plot (Optional)

To generate the interactive 3D plot, use the score table (`scores.xlsx`) and run:


python 3Dplot.py
