#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D2 canonical analysis: exact vs tolerant (v3) on d2_60. Unique recompute script (FM-15/16).

Reads: evidence/d2_60.jsonl (+ scripts/label_match_v3.py vendored v3+R3).
Writes: results/exact.json, results/tolerant.json, results/flips.json, results/analysis.json.
Pairing: McNemar pairs = same row two matchers (valid within subset); pooled across
pilot+holdout is descriptive/stratified only (different models/questions) — N=120 still pending.
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "scripts"))
import label_match_v3 as lm
from stats import exact_mcnemar

def ece_equal_freq(confs, outs, bins=10):
    pairs = sorted(zip(confs, outs))
    n = len(pairs)
    if n == 0:
        return 0.0
    size = max(1, n // bins)
    tot = 0.0
    for i in range(0, n, size):
        b = pairs[i:i + size]
        c = sum(p[0] for p in b) / len(b)
        a = sum(p[1] for p in b) / len(b)
        tot += abs(a - c) * len(b) / n
    return round(tot, 4)

rows = [json.loads(l) for l in (HERE / "evidence" / "d2_60.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
for r in rows:
    a, g = str(r.get("predicted_label", "")), str(r.get("gold_answer", ""))
    r["exact"] = bool(lm.norm(a) == lm.norm(g))
    r["tolerant"] = bool(lm.tolerant_match(a, g))

def subset(name, rs):
    n = len(rs)
    ne = sum(1 for r in rs if r["exact"])
    nt = sum(1 for r in rs if r["tolerant"])
    flips = [r for r in rs if r["exact"] != r["tolerant"]]
    b = sum(1 for r in rs if (not r["exact"]) and r["tolerant"])
    c = sum(1 for r in rs if r["exact"] and (not r["tolerant"]))
    p_two, p_one = exact_mcnemar(b, c)
    ce = [float(r["confidence"]) for r in rs if r.get("confidence") is not None]
    ee = [1 if r["exact"] else 0 for r in rs if r.get("confidence") is not None]
    et = [1 if r["tolerant"] else 0 for r in rs if r.get("confidence") is not None]
    return {"n": n, "n_exact": ne, "n_tolerant": nt,
            "acc_exact": round(ne / n, 4), "acc_tolerant": round(nt / n, 4),
            "flip_rate": round(len(flips) / n, 4), "n_flips": len(flips),
            "mcnemar_b": b, "mcnemar_c": c, "mcnemar_p_two": p_two,
            "discordant_rate": round((b + c) / n, 4),
            "ece10_exact": ece_equal_freq(ce, ee), "ece10_tolerant": ece_equal_freq(ce, et)}

pilot = [r for r in rows if r["source"] == "pilot"]
hold = [r for r in rows if r["source"] == "holdout-main"]
sp, sh = subset("pilot", pilot), subset("holdout-main", hold)
sall = subset("pooled-descriptive", rows)

# FM-15 assert: pooled counts equal sum of subsets
assert sall["n"] == sp["n"] + sh["n"]
assert sall["n_flips"] == sp["n_flips"] + sh["n_flips"]
assert sall["mcnemar_b"] + sall["mcnemar_c"] == (sp["mcnemar_b"] + sp["mcnemar_c"] + sh["mcnemar_b"] + sh["mcnemar_c"])

res = HERE / "results"
res.mkdir(exist_ok=True)
(res / "exact.json").write_text(json.dumps({"pilot": {k: sp[k] for k in ("n", "n_exact", "acc_exact", "ece10_exact")},
    "holdout-main": {k: sh[k] for k in ("n", "n_exact", "acc_exact", "ece10_exact")},
    "note": "exact = norm-equality; N=120 pending, this is 60-link snapshot"}, ensure_ascii=False, indent=2), encoding="utf-8")
(res / "tolerant.json").write_text(json.dumps({"matcher": "label_match_v3 vendored (v3+R3)",
    "pilot": {k: sp[k] for k in ("n", "n_tolerant", "acc_tolerant", "ece10_tolerant")},
    "holdout-main": {k: sh[k] for k in ("n", "n_tolerant", "acc_tolerant", "ece10_tolerant")}}, ensure_ascii=False, indent=2), encoding="utf-8")
flips = [{"trace_id": r["trace_id"], "source": r["source"], "predicted": r["predicted_label"],
          "gold": r["gold_answer"], "exact": r["exact"], "tolerant": r["tolerant"],
          "source_outcome": r.get("source_outcome"), "adjudication": "pending-except-pilot-src-v2"} for r in rows if r["exact"] != r["tolerant"]]
(res / "flips.json").write_text(json.dumps(flips, ensure_ascii=False, indent=2), encoding="utf-8")
analysis = {"subsets": {"pilot": sp, "holdout-main": sh}, "pooled_descriptive": sall,
    "H1": "flip_rate>5% per subset (paired exact-vs-tolerant, same rows)",
    "H1_result": {k: ("SUPPORT" if v["flip_rate"] > 0.05 else "NOT-SUPPORT") for k, v in (("pilot", sp), ("holdout-main", sh))},
    "power_note": "N=120 registered still pending (60/120). Observed discordant rates feed power update; do not claim N=120 done.",
    "N_status": "60/120 snapshot; pre-registration N=120 NOT yet fulfilled"}
(res / "analysis.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(analysis, ensure_ascii=False, indent=2))
