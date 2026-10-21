"""Sealed merged computation: 1062-pair descriptive totals (hetero integration).

Sums exact/guarded-adjudicated/flips from sealed per-stratum files only;
asserts the hand-added R18 precedent (809/893/84 at N=1002) plus the hetero
arm (21/29/8) to the new totals. Writes results/merged_1062.json.
No inference; descriptive sums only.

Usage: python3 paper_workflow_kb/scripts/seal_merged_hetero.py
"""
import json
import sys
from pathlib import Path

KB = Path(__file__).resolve().parents[1]


def J(p):
    return json.loads((KB / p).read_text(encoding="utf-8"))


a = J("results/analysis.json")["subsets"]
g31 = J("results/guard_v31.json")["strata"]
cn = J("results/cloud_new.json")
ln = J("results/local_new.json")
le = J("results/local_en.json")
lb = J("results/local_big.json")
mm = J("results/math40.json")
xd = J("results/xdomain.json")
pw = J("results/powrep.json")
r18r = J("results/r18_loose_rep.json")["loose_rep"]
r18a = J("results/r18_adjudication.json")
htr = J("results/r18_heteromodel.json")["heteromodel"]
hta = J("results/r18_heteromodel_adjudication.json")

arms = [
    ("pilot", 30, a["pilot"]["n_exact"], a["pilot"]["n_tolerant"], a["pilot"]["n_flips"]),
    ("holdout-main", 30, a["holdout-main"]["n_exact"], a["holdout-main"]["n_tolerant"],
     a["holdout-main"]["n_flips"]),
    ("cloud-new", 60, cn["n_exact"], g31["cloud-new"]["n_guarded"],
     g31["cloud-new"]["flips_guarded"]),
    ("local-new", 60, ln["n_exact"], ln["n_guarded"], ln["n_flips"]),
    ("local-en", 30, le["n_exact"], le["n_guarded"], le["n_flips"]),
    ("local-big", 160, lb["n_exact"], lb["n_guarded"], lb["n_flips"]),
    ("math", 40, mm["n_exact"], mm["n_guarded"], mm["n_flips"]),
    ("xtight", 60, xd["tight"]["n_exact"], xd["tight"]["n_guarded"], xd["tight"]["n_flips"]),
    ("xloose", 60, xd["loose"]["n_exact"], xd["loose"]["n_guarded"], xd["loose"]["n_flips"]),
    ("powpilot", 20, pw["pow1_pilot"]["n_exact"], pw["pow1_pilot"]["n_guarded"],
     pw["pow1_pilot"]["n_flips"]),
    ("powholdout", 78, pw["pow1_holdout"]["n_exact"], pw["pow1_holdout"]["n_guarded"],
     pw["pow1_holdout"]["n_flips"]),
    ("powcloudnew", 157, pw["pow2_cloudnew"]["n_exact"], pw["pow2_cloudnew"]["n_guarded"],
     pw["pow2_cloudnew"]["n_flips"]),
    ("powlocalnew", 157, pw["powL_localnew"]["n_exact"], pw["powL_localnew"]["n_guarded"],
     pw["powL_localnew"]["n_flips"]),
    ("r18", 60, r18r["n_exact"], r18a["adjudicated_guarded_correct"],
     r18a["adjudicated_flips"]),
    ("hetero-gemma", 60, htr["n_exact"], hta["adjudicated_guarded_correct"],
     hta["adjudicated_flips"]),
]
assert len(arms) == 15
n = sum(x[1] for x in arms)
ne = sum(x[2] for x in arms)
ng = sum(x[3] for x in arms)
nf = sum(x[4] for x in arms)
assert (n, ne, ng, nf) == (1062, 830, 922, 92), (n, ne, ng, nf)
out = {"n": n, "n_exact": ne, "n_guarded_adjudicated": ng, "n_flips": nf,
       "flip_rate": round(nf / n, 4),
       "note": "descriptive sums on the adjudicated basis; no merged inference",
       "arms": [{"stratum": x[0], "n": x[1], "n_exact": x[2],
                 "n_guarded": x[3], "n_flips": x[4]} for x in arms]}
(KB / "results" / "merged_1062.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k != "arms"},
                 ensure_ascii=False, indent=2))
print("WROTE results/merged_1062.json")
