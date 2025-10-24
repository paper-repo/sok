import json, sys

def load(path):
    with open(path, "r") as f:
        return json.load(f)

def compute_score(ans, wts):
    return sum(wts[k] for k, v in ans.items() if v and k in wts)

def main(answers_file, weights_file):
    answers, weights = load(answers_file), load(weights_file)
    result = {}
    for cat in ["Privacy", "Utility", "Safety"]:
        a = answers.get(cat, {})
        w = weights.get(cat, {})
        result[cat] = round(compute_score(a, w), 3)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 3:
    else:
        main(sys.argv[1], sys.argv[2])
