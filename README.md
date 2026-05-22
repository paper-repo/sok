# Harpo Artifacts
  
  This repository contains the artifacts for the paper:
  **“SoK: A Practical Black-Box Framework for Evaluating Differential Privacy in Cyber-Physical Systems.”**
  
  Harpo is a quantitative scoring framework that evaluates how thoroughly differential-privacy
  research in cyber-physical systems (CPS) reports along three dimensions —
  **Privacy**, **Utility** and **Safety** — across a corpus of 47 primary research papers.
  
  This artifact lets you:
  
  - **Score a single paper** using a Boolean checklist (`paper.json`) and fixed weights (`weight.json`).
  - **Visualize the full corpus** as a static 2D bubble plot or an interactive 3D plot.
  - **Reproduce the sensitivity analysis** that shows the ranking is essentially invariant to weight choice (Spearman ρ ≥ 0.999).
  
  > **Anonymity note.** This repository is intended for anonymous peer review. Please avoid
  > linking it to personal accounts or identifiable information during the review period.
  
  --------------------------------------------------------------------------------------------------------------------
  ## Repository Contents
  
  | File | Purpose |
  |---|---|
  | `blackbox.py` | Scores one paper from `paper.json` + `weight.json` |
  | `2d.py` | Generates the 2D bubble plot (Privacy × Utility, Safety as size + color) |
  | `3d.py` | Generates the interactive 3D plot (HTML) in the Privacy–Utility–Safety space |
  | `sensitivity.py` | Reproduces the sensitivity analysis (W1 / W2 / W3 + Spearman ρ) |
  | `paper.json` | Per-paper Boolean checklist (edit this for a new paper) |
  | `weight.json` | Fixed per-criterion weights used across all papers |
  | `scores.xlsx` | Score table for the 47-paper corpus (used by `2d.py` and `3d.py`) |
  | `LICENSE` | MIT license |
  | `.gitignore` | Standard Python ignores |
  
  --------------------------------------------------------------------------------------------------------------------
  
  ## Requirements
  
  - Python 3.9 or later
  - Install dependencies:

  ```bash
  pip install pandas numpy scipy plotly openpyxl
  
  (openpyxl is needed for pandas to read scores.xlsx; plotly is used by both plot scripts.)
  
  --------------------------------------------------------------------------------------------------------------------
  1. Score a single paper — blackbox.py
  
  What it does
  
  Reads the Boolean checklist in paper.json and the fixed weights in weight.json, and prints
  three normalized scores in [0, 1] — one for Privacy, Utility and Safety.
  
  How to run
  
  python3 blackbox.py paper.json weight.json
  
  Example output
  
  {
    "Privacy": 0.80,
    "Utility": 1.00,
    "Safety": 0.60
  }

  How to score a new paper
  
  1. Open paper.json.
  2. For each of the 11 Privacy + 10 Utility + 13 Safety sub-criteria, set the value to true
  if the paper satisfies that criterion, false otherwise.
  3. Save and re-run blackbox.py.
  
  The criterion codes (P1a, P1b, …, S6b) and their meanings are defined in Table 1 of the paper.
  
  --------------------------------------------------------------------------------------------------------------------
  2. Generate the 2D bubble plot — 2d.py
  
  What it does
  
  Reads scores.xlsx and produces a 2D scatter plot of the 47-paper corpus in the Privacy–Utility
  plane. The third dimension (Safety) is encoded redundantly as both marker size and marker
  color (viridis colormap).
  
  How to run
  
  python3 2d.py
  
  Output

  Opens an interactive Plotly figure in the browser. Hovering shows the paper reference and its
  Privacy / Utility / Safety scores.
  
  What the figure shows
  
  - Most points are small and dark → those papers have a Safety score near zero.
  - A small subset of large yellow bubbles → papers that reach a non-trivial Safety score.
  - Papers with identical (P, U, S) scores are plotted as a single marker with a combined
  reference label (e.g. 13, 22).
  
  --------------------------------------------------------------------------------------------------------------------
  3. Generate the 3D interactive plot — 3d.py
  
  What it does

  Reads scores.xlsx and produces an HTML file with an interactive 3D scatter in the
  Privacy–Utility–Safety space.
  
  How to run

  python 3d.py
  
  Output
  
  Writes 3d.html in the current directory. Open it in any modern browser. You can:
  - Rotate the view (drag).
  - Zoom (scroll).
  - Hover a point to see the paper's reference number and its three scores.
  
  This is the figure embedded in the project webpage.
  
  --------------------------------------------------------------------------------------------------------------------
  4. Reproduce the sensitivity analysis — sensitivity.py
  
  What it does
  
  Verifies that the Harpo ranking is not sensitive to the specific weight choice. It evaluates the
  corpus under three weight schemes:
  
  - W1 — baseline weights from weight.json.
  - W2 — each sub-weight multiplied by an independent uniform factor in [0.75, 1.25] and renormalized (±25% perturbation).
  - W3 — all Safety sub-weights scaled by 1.5× and renormalized (Safety emphasis).
  
  It then computes the Spearman rank correlation ρ between the W1 baseline ranking and each
  alternative, separately for Privacy, Utility and Safety.
  
  How to run

  python3 sensitivity.py
  
  Example output
  
  === W1 (baseline) scores ===
  Paper                    Privacy   Utility    Safety
  ----------------------------------------------------
  1                           0.90      0.70      0.00
  2                           0.35      0.40      0.20
  4                           0.80      1.00      0.60
  …
  
  === Spearman rank correlations ===
  Dimension     rho(W1,W2)    rho(W1,W3)
  --------------------------------------------------------------------------------------------------------------------
  privacy           0.9998        1.0000
  utility           0.9994        1.0000
  safety            0.9998        1.0000
  
  Papers with Safety = 0 (invariant under any non-negative reweighting): 29 / 47
  
  How to interpret it
  
  - ρ ≥ 0.999 in every dimension means the ranking is essentially invariant to weight choice
  within the studied perturbation envelope.
  - 29 / 47 papers receive Safety = 0 because none of the 13 Safety sub-criteria is satisfied.
  Since zero × any non-negative weight is zero, those papers stay tied at the bottom of the
  Safety ranking under any reweighting — this is a structural property of the data, not the
  weights.
  
  --------------------------------------------------------------------------------------------------------------------
  File Formats

  paper.json
  
  A JSON object with three top-level keys (Privacy, Utility, Safety). Each key maps a
  sub-criterion code to a Boolean. A snippet:
  
  {
   "Privacy": {
    "P1a: Privacy Mechanism, Mention of Mechanism": false,
    "P1b: Privacy Mechanism, Mechanism Description": false,
    "P1c: Privacy Mechanism, Evidence or Implementation": false,
      "...": "..."
    }
  }

  weight.json
  
  Same shape as paper.json but values are floats in [0, 1]. Weights sum to 1.0 within each
  dimension. Do not edit unless you want to test a custom weighting.
  
  scores.xlsx
  
  A spreadsheet with four columns: Paper, Privacy, Utility, Safety. One row per
  distinct (Privacy, Utility, Safety) coordinate; papers with identical scores are grouped onto
  a single row with a combined label (e.g. 13, 22).
  
  --------------------------------------------------------------------------------------------------------------------
  Reproducing the Paper Results
  
  To reproduce the per-paper scores reported in Table 4 of the paper:
  
  python3 blackbox.py paper.json weight.json
  
  To reproduce the visualizations in the paper:

  python3 2d.py   # → opens the 2D bubble plot
  python3 3d.py   # → writes 3d.html
  
  To reproduce the sensitivity analysis :
  
  python3 sensitivity.py
  
  All four commands run in seconds on a standard laptop and require no GPU.
  
  --------------------------------------------------------------------------------------------------------------------
  License
  
  MIT License. See LICENSE for details.
