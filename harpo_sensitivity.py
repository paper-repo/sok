import numpy as np
from scipy.stats import spearmanr

  # ============================================================
  #  WEIGHT SCHEMES
  # ============================================================
PRIVACY_KEYS = ["P1a","P1b","P1c","P2","P3a","P3b","P3c",
                "P4a","P4b","P5","P6"]
UTILITY_KEYS = ["U1a","U1b","U2a","U2b","U3a","U3b",
                  "U4a","U4b","U5a","U5b"]
SAFETY_KEYS  = ["S1a","S1b","S1c","S2a","S2b","S3a","S3b",
                  "S4a","S4b","S5a","S5b","S6a","S6b"]
  
W1 = {
      "privacy": dict(P1a=.10,P1b=.10,P1c=.10,P2=.10,P3a=.05,P3b=.10,
                      P3c=.05,P4a=.05,P4b=.05,P5=.10,P6=.20),
      "utility": {k: .10 for k in UTILITY_KEYS},
      "safety":  dict(S1a=.10,S1b=.10,S1c=.10,S2a=.10,S2b=.05,S3a=.10,
                      S3b=.05,S4a=.10,S4b=.10,S5a=.05,S5b=.05,
                      S6a=.05,S6b=.05),
  }

def perturb(weights, pct=0.25, seed=42):
      rng = np.random.default_rng(seed)
      out = {}
      for dim, w_dim in weights.items():
          keys_list = list(w_dim.keys())
          vals = np.array([w_dim[k] for k in keys_list], dtype=float)
          noise = rng.uniform(1 - pct, 1 + pct, size=len(vals))
          new_vals = vals * noise
          new_vals = new_vals / new_vals.sum()
          out[dim] = {k: float(v) for k, v in zip(keys_list, new_vals)}
      assert set(out.keys()) == {"privacy","utility","safety"}, \
          f"perturb dropped a dimension; got: {set(out.keys())}"
      return out
  
def emphasis(weights, dim_to_boost, factor=1.5):
      out = {}
      for dim, w_dim in weights.items():
          new_w = dict(w_dim)
          if dim == dim_to_boost:
              for k in new_w:
                  new_w[k] = new_w[k] * factor
              s = sum(new_w.values())
              new_w = {k: v / s for k, v in new_w.items()}
          out[dim] = new_w
      assert set(out.keys()) == {"privacy","utility","safety"}, \
          f"emphasis dropped a dimension; got: {set(out.keys())}"
      return out
  
W2 = perturb(W1, pct=0.25, seed=42)
W3 = emphasis(W1, "safety", factor=1.5)
  
  # ============================================================
  #  BOOLEAN-VECTOR HELPERS
  # ============================================================
def P(*keys_true):
      return {k: (1 if k in keys_true else 0) for k in PRIVACY_KEYS}
  
def U(*keys_true):
      return {k: (1 if k in keys_true else 0) for k in UTILITY_KEYS}
  
def S(*keys_true):
      return {k: (1 if k in keys_true else 0) for k in SAFETY_KEYS}
  
ZERO_SAFETY = S()  # all-False safety vector
  
# ============================================================
  #  47 PAPERS (Boolean vectors)
  #  Each entry sums under W1 to the score in Table 3.
  # ============================================================
PAPERS = {
      # ---------- SAFETY = 0 cluster ----------
      "2b":  {"privacy": P("P1a","P1b","P1c","P2","P3b","P5"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a","U5a","U5b"),
              "safety":  ZERO_SAFETY},
      "3b":  {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P5","P6"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a","U5a"),
              "safety":  ZERO_SAFETY},
      "4b":  {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P4a","P4b","P5"),
          "utility": U(*UTILITY_KEYS),
          "safety":  ZERO_SAFETY},
    "16b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P4a","P4b","P5"),
          "utility": U(*UTILITY_KEYS),
          "safety":  ZERO_SAFETY},
      "5b":  {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P5"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b"),
              "safety":  ZERO_SAFETY},
      "7b":  {"privacy": P("P1a","P1b","P1c","P2","P3b","P5"),
              "utility": U("U1a","U1b","U2a","U2b"),
              "safety":  ZERO_SAFETY},
      "9b":  {"privacy": P("P1a","P1b","P1c","P2","P3b","P5"),
              "utility": U("U1a","U1b","U2a","U2b"),
              "safety":  ZERO_SAFETY},
      "10b": {"privacy": P("P1a","P1b","P1c","P3a","P3b"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a"),
              "safety":  ZERO_SAFETY},
      "12b": {"privacy": P("P1a","P1b","P1c","P3a"),
              "utility": U("U1a","U1b"),
              "safety":  ZERO_SAFETY},
      "13b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P5","P6"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a"),
              "safety":  ZERO_SAFETY},
      "14b": {"privacy": P("P1a"),
              "utility": U("U1a","U1b"),
              "safety":  ZERO_SAFETY},
      "17b": {"privacy": P("P1a","P1b","P1c","P2","P3b"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a","U5a"),
              "safety":  ZERO_SAFETY},
      "18b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b"),
              "utility": U("U1a","U1b","U2a","U2b"),
              "safety":  ZERO_SAFETY},
      "19b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P4a","P5"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a","U5a","U5b"),
              "safety":  ZERO_SAFETY},
      "20b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P4a","P5"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a","U5a","U5b"),
              "safety":  ZERO_SAFETY},
      "21b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P5"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a","U5a"),
              "safety":  ZERO_SAFETY},
      "26b": {"privacy": P("P1a","P1b","P1c","P2","P3b"),
              "utility": U("U1a","U1b","U2a","U2b"),
              "safety":  ZERO_SAFETY},
      "31b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P5"),
              "utility": U("U1a","U1b","U2a","U2b"),
              "safety":  ZERO_SAFETY},
      "35b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P5"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a"),
              "safety":  ZERO_SAFETY},
      "38b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P5"),
              "utility": U("U1a","U1b","U2a","U2b"),
              "safety":  ZERO_SAFETY},
      "39b": {"privacy": P("P1a"),
              "utility": U("U1a"),
              "safety":  ZERO_SAFETY},
      "6b":  {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P5"),
              "utility": U("U1a","U1b"),
              "safety":  ZERO_SAFETY},
      "30b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P5"),
              "utility": U("U1a","U1b"),
              "safety":  ZERO_SAFETY},
      "40b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P5"),
              "utility": U("U1a","U1b"),
              "safety":  ZERO_SAFETY},
      "42b": {"privacy": P("P1a","P1b","P1c"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a"),
              "safety":  ZERO_SAFETY},
      "43b": {"privacy": P("P1a","P1b","P1c","P3a","P3c"),
              "utility": U("U1a","U1b","U2a","U2b","U3a"),
              "safety":  ZERO_SAFETY},
      "44b": {"privacy": P("P1a","P1b","P1c","P3a","P3b"),
              "utility": U("U1a","U1b"),
              "safety":  ZERO_SAFETY},
      "overlapping1": {
              "privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P5"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a"),
              "safety":  ZERO_SAFETY},
      "ny": {
              "privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P4a","P4b","P6"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b"),
              "safety":  ZERO_SAFETY},
  
      # ---------- SAFETY > 0 cohort (Boolean reconstruction) ----------
      "11b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P4a","P5"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a"),
              "safety":  S("S1a","S2a","S2b","S3a","S3b","S4a","S4b","S5a")},
      "15b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P5","P6"),
              "utility": U("U1a","U1b","U2a","U2b"),
              "safety":  S("S2a","S2b","S3a","S3b","S4a","S4b")},
      "22b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P5"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b"),
              "safety":  S("S2a","S2b","S3a","S4a","S4b")},
      "23b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P4a","P4b","P5","P6"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a","U5a"),
              "safety":  S("S2a","S2b","S3a","S3b","S4a","S4b")},
     "24b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P4a","P4b","P6"),
          "utility": U("U1a","U1b","U2a","U2b","U3a","U3b"),
          "safety":  S("S1a","S1b","S1c","S2a","S2b","S3a","S3b","S4a","S4b")},
      "25b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P4a","P5"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b"),
              "safety":  S("S2a","S3a","S4a","S4b")},
      "27b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P4a","P4b","P5","P6"),
              "utility": U("U1a","U1b","U2a","U2b"),
              "safety":  S("S1a","S2a","S2b","S3a","S3b","S4a","S4b","S5a","S5b","S6a")},
      "28b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P4a","P4b","P6"),
              "utility": U("U1a","U1b","U2a","U2b","U3a"),
              "safety":  S("S2a","S2b","S3a","S3b","S4a","S4b","S5a","S5b")},
      "29b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P5"),
              "utility": U("U1a","U1b","U2a","U2b"),
              "safety":  S("S2a","S2b","S3a","S3b","S4a","S4b")},
      "33b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b"),
              "utility": U("U1a","U1b","U2a","U2b"),
              "safety":  S("S2a","S2b","S3a")},
       "37b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P4a","P4b","P5"),
          "utility": U("U1a","U1b","U2a","U2b","U3a","U3b"),
          "safety":  S("S2a","S3a","S4a")},
      "45b": {"privacy": P("P1a","P1b","P1c","P3a"),
                "utility": U("U1a","U1b","U2a","U2b"),
                "safety":  S("S2a","S3a")},
       "47b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P5","P6"),
                "utility": U("U1a","U1b","U2a","U2b"),
                "safety":  S("S1a","S2a","S2b","S3a","S3b","S4a","S4b","S5a","S5b","S6a")},
      "48b": {"privacy": P("P1a","P1b","P3a","P3b"),
              "utility": U("U1a","U1b","U2a","U2b"),
              "safety":  S("S2a","S3a","S3b","S4a")},
     "49b": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P4a","P5"),
          "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a","U5a","U5b"),
          "safety":  S("S2a","S2b","S3a","S3b","S4a","S6a")},
      "sibin": {"privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P4a","P4b","P5"),
              "utility": U(*UTILITY_KEYS),
              "safety":  S("S2a","S2b","S3a","S3b","S4a","S4b","S5a","S5b")},
      "psdo": {
              "privacy": P("P1a","P1b","P1c","P2","P3a","P3b","P3c","P4a","P5","P6"),
              "utility": U("U1a","U1b","U2a","U2b","U3a","U3b","U4a","U5a"),
              "safety":  S("S2a","S2b","S3a","S3b","S4a","S4b")},
      "array": {
              "privacy": P("P1a","P1b","P3a"),
              "utility": U("U1a","U1b","U2a","U2b","U5a","U5b"),
              "safety":  S("S2a","S3a","S4a","S4b","S5a")},
}
  
  # ============================================================
  #  SCORE COMPUTATION
  # ============================================================
def score(paper_booleans, weights):
      result = {}
      for dim in ["privacy", "utility", "safety"]:
          if dim not in weights:
              raise KeyError(f"weights missing dim '{dim}'; has: {list(weights.keys())}")
          if dim not in paper_booleans:
              raise KeyError(f"paper_booleans missing dim '{dim}'; has: {list(paper_booleans.keys())}")
          total = sum(weights[dim][k] * paper_booleans[dim][k]
                      for k in paper_booleans[dim])
          result[dim] = round(total, 4)
      return result
  
def all_scores(W):
      return {ref: score(b, W) for ref, b in PAPERS.items()}
  
scores_W1 = all_scores(W1)
scores_W2 = all_scores(W2)
scores_W3 = all_scores(W3)
  
  # ============================================================
  #  SANITY-CHECK: W1 scores match Table 3
  # ============================================================
print("=== W1 (baseline) scores ===")
print(f"{'Paper':<22}{'Privacy':>10}{'Utility':>10}{'Safety':>10}")
print("-" * 52)
for ref in sorted(PAPERS.keys()):
      s = scores_W1[ref]
      print(f"{ref:<22}{s['privacy']:>10.2f}{s['utility']:>10.2f}{s['safety']:>10.2f}")
  
  # ============================================================
  #  SPEARMAN RANK CORRELATIONS
  # ============================================================
print("\n=== Spearman rank correlations (W1 vs W2 perturbed, W1 vs W3 emphasis) ===")
print(f"{'Dimension':<10}{'rho(W1,W2)':>14}{'rho(W1,W3)':>14}")
print("-" * 38)
for dim in ["privacy", "utility", "safety"]:
      refs = list(PAPERS.keys())
      v1 = [scores_W1[r][dim] for r in refs]
      v2 = [scores_W2[r][dim] for r in refs]
      v3 = [scores_W3[r][dim] for r in refs]
      rho12, _ = spearmanr(v1, v2)
      rho13, _ = spearmanr(v1, v3)
      print(f"{dim:<10}{rho12:>14.4f}{rho13:>14.4f}")
  
  # ============================================================
  #  STRUCTURAL ROBUSTNESS COUNT
  # ============================================================
n_zero_safety = sum(1 for r in PAPERS
                      if all(v == 0 for v in PAPERS[r]["safety"].values()))
print(f"\nPapers with Safety = 0 (invariant under any non-negative reweighting): "
        f"{n_zero_safety} / {len(PAPERS)}")