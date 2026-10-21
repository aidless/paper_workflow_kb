"""Matcher component ablation on d2_60 16 flips: which v3 rule fires per flip.
Deterministic, local. Output: paper_workflow_kb/results/ablation.json
"""
import json, sys
sys.path.insert(0, "paper_workflow_kb/scripts")
from label_match_v3 import norm, SUFFIXES, SYNONYMS, _parse_cn_num
import re
_CN_RE = re.compile(r"[\u4e00-\u9fff]+")

def component(a, g):
    a2, g2 = norm(a), norm(g)
    if a2 == g2:
        return "exact"
    a3, g3 = a2, g2
    for suf in SUFFIXES:
        a3 = a3.replace(suf, "")
        g3 = g3.replace(suf, "")
    if a3 == g3:
        return "unit_suffix"
    if SYNONYMS.get(a3) == g3:
        return "synonym"
    if g3 in ("否", "是"):
        for p in ("不是", "不会"):
            if a3.startswith(p) and g3 == "否":
                return "neg_prefix"
        for p in ("是", "会"):
            if a3.startswith(p) and g3 == "是":
                return "pos_prefix"
    if len(g3) >= 2 and _parse_cn_num(g3) is None and (g3 in a3 or a3 in g3):
        return "substring"
    av, gv = _parse_cn_num(a3), _parse_cn_num(g3)
    if av is not None and gv is not None:
        if abs(av - gv) < 1e-6:
            return "numeric_exact"
        if abs(av - gv) / max(abs(gv), 1.0) < 0.005:
            return "numeric_tolerance"
    return "unexplained"

flips = json.load(open("paper_workflow_kb/results/flips.json", encoding="utf-8"))
from collections import Counter
c = Counter()
rows = []
for r in flips:
    k = component(r["predicted"], r["gold"])
    c[k] += 1
    rows.append({"trace_id": r["trace_id"], "source": r["source"],
                 "predicted": r["predicted"], "gold": r["gold"], "component": k})
out = {"n_flips": len(flips), "by_component": dict(c), "rows": rows}
# Canonical top-level count keys (fixed order = ledger C13 convention 7/4/3/1/1);
# makes the file byte-reproducible by this script (cloud-recompute verified).
for k in ("synonym", "numeric_tolerance", "unit_suffix", "substring", "neg_prefix",
          "numeric_exact", "pos_prefix", "exact", "unexplained"):
    if k in c:
        out[f"n_{k}"] = c[k]
json.dump(out, open("paper_workflow_kb/results/ablation.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print(json.dumps(out["by_component"], ensure_ascii=False))
print("WROTE results/ablation.json")
