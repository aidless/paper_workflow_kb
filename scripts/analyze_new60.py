"""Analyze cloud-new stratum with v3 matchers + merge to N=120.
Single recomputation script for new layer. Outputs results/cloud_new.json + analysis_120.json
"""
import json, sys, math
sys.path.insert(0, "paper_workflow_kb/scripts")
from label_match_v3 import norm, tolerant_match

def exact_match(a, g):
    a2, g2 = norm(a), norm(g)
    return bool(a2 and g2 and a2 == g2)

def ece10(rows, key):
    bins = [[] for _ in range(10)]
    for r in rows:
        c = min(max(r["confidence"], 0.0), 1.0)
        b = min(int(c * 10), 9)
        bins[b].append(1 if r[key] else 0)
    n = len(rows)
    e = 0.0
    for b in bins:
        if b:
            e += len(b) / n * abs(sum(b) / len(b) - (sum(
                min(max(r["confidence"], 0.0), 1.0) for r in rows
                if min(int(min(max(r["confidence"], 0.0), 1.0) * 10), 9) == bins.index(b)) / len(b)))
    return round(e, 4)

def mcnemar_p(b, c):
    # exact two-sided McNemar (binomial, p=0.5, n=b+c)
    from math import comb
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(comb(n, i) for i in range(k + 1)) * (0.5 ** n) * 2
    return min(round(p, 10), 1.0)

rows = json.load(open("paper_workflow_kb/evidence/cloud_new60_raw.json", encoding="utf-8"))
for r in rows:
    r["exact"] = exact_match(r["predicted_label"], r["gold_answer"])
    r["tolerant"] = tolerant_match(r["predicted_label"], r["gold_answer"])
n = len(rows)
n_e = sum(1 for r in rows if r["exact"])
n_t = sum(1 for r in rows if r["tolerant"])
flips = [r for r in rows if r["exact"] != r["tolerant"]]
b = sum(1 for r in rows if (not r["exact"]) and r["tolerant"])
c = sum(1 for r in rows if r["exact"] and (not r["tolerant"]))
out = {"n": n, "n_exact": n_e, "n_tolerant": n_t,
       "acc_exact": round(n_e / n, 4), "acc_tolerant": round(n_t / n, 4),
       "n_flips": len(flips), "flip_rate": round(len(flips) / n, 4),
       "mcnemar_b": b, "mcnemar_c": c, "mcnemar_p_two": mcnemar_p(b, c),
       "discordant_rate": round((b + c) / n, 4),
       "ece10_exact": ece10(rows, "exact"), "ece10_tolerant": ece10(rows, "tolerant"),
       "model": "qwen2.5:7b", "temperature": 0}
json.dump(out, open("paper_workflow_kb/results/cloud_new.json", "w"), indent=2)
json.dump(flips, open("paper_workflow_kb/results/flips_new60.json", "w"),
          ensure_ascii=False, indent=2)
# merge with existing 60 -> 120
old = json.load(open("paper_workflow_kb/results/analysis.json", encoding="utf-8"))
pe = old["pooled_descriptive"]
tot_n = pe["n"] + n
tot_e = pe["n_exact"] + n_e
tot_t = pe["n_tolerant"] + n_t
merged = {"n": tot_n, "n_exact": tot_e, "n_tolerant": tot_t,
          "acc_exact": round(tot_e / tot_n, 4), "acc_tolerant": round(tot_t / tot_n, 4),
          "n_flips": pe["n_flips"] + len(flips),
          "flip_rate": round((pe["n_flips"] + len(flips)) / tot_n, 4)}
merged_full = {"strata": {"d2_60": pe, "cloud_new": out}, "merged_descriptive": merged,
               "N_status": "120/120 (60 prior strata + 60 cloud-new live stratum); inference stratified per stratum",
               "note": "cloud-new is a NEW stratum (fresh questions, qwen2.5:7b live, temp 0), not same-distribution backfill of missing 60; pooled numbers descriptive only"}
json.dump(merged_full, open("paper_workflow_kb/results/analysis_120.json", "w"), indent=2)
print(json.dumps(out, indent=2))
print("MERGED:", json.dumps(merged))
print("WROTE results/cloud_new.json + results/flips_new60.json + results/analysis_120.json")
