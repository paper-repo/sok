import json, sys
import json
import sys

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def compute_score(pap, wts):
    return sum(wts[k] for k, v in pap.items() if v and k in wts)

def main(paper_file, weights_file):
    paper, weights = load(paper_file), load(weights_file)
    result = {}
    for cat in ["Privacy", "Utility", "Safety"]:
        p = paper.get(cat, {})
        w = weights.get(cat, {})
        result[cat] = round(compute_score(p, w), 3)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python blackbox.py paper.json weight.json")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
