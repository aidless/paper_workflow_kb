"""Sealed analysis: power-replication arms (v3.2 basis).

Arms (trace-id prefixes):
  pow1 (n=98, cloud qwen2.5:7b): pilot extension (+20 -> pilot total 50)
  pow2 (n=157, cloud qwen2.5:7b): cloud-new extension (+157 -> 217)
  powL (n=157, local qwen2:7b): local-new extension (+157 -> 217)
Holdout extension: pow1 items [21..98] (78) re-based as holdout arm (+78 -> 108).
  (Pilot-style vs holdout-style split recorded in scripts/batch1_power_rep.py
  comments: first 20 = pilot-style, rest = holdout-style.)

REJECTED_GOLDS: trace ids whose golds failed user spot-check (dropped before
analysis; currently empty = spot-check pending, DO NOT run for ledger until
the check lands — raw preview only).

Writes results/powrep.json with per-arm n/exact/guarded/flips/b/c/p_two,
ECE10 equal-width, flip lists; plus extended-stratum rollups
(pilot 30+20, holdout 30+78, cloud-new 60+157, local-new 60+157) recomputed
from sealed prior files + new rows (no double counting; prior files untouched).

Usage: python3 paper_workflow_kb/scripts/analyze_powrep.py paper_workflow_kb [--seal]
Without --seal: dry run printing counts only (no file written).
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from label_match_v3 import norm
from label_match_v32 import tolerant_match_v32

REJECTED_GOLDS: list = [
    # e.g. "pow1-003",  # spot-check rejected gold
]


def mcnemar_exact_two(b, c):
    n_d = b + c
    if n_d == 0:
        return 1.0, True
    total = 2 ** n_d
    lo = sum(math.comb(n_d, k) for k in range(0, min(b, c) + 1))
    hi = sum(math.comb(n_d, k) for k in range(max(b, c), n_d + 1))
    return min(1.0, 2 * min(lo, hi) / total), False


def ece_equal_width(confs, outs, bins=10):
    assert len(confs) == len(outs) and len(confs) > 0
    edges = [i / bins for i in range(bins + 1)]
    ece, n = 0.0, len(confs)
    for i in range(bins):
        lo, hi = edges[i], edges[i + 1]
        idx = [k for k in range(n)
               if (confs[k] > lo or (i == 0 and confs[k] == lo)) and confs[k] <= hi]
        if not idx:
            continue
        acc = sum(outs[k] for k in idx) / len(idx)
        conf = sum(confs[k] for k in idx) / len(idx)
        ece += len(idx) / n * abs(acc - conf)
    return ece


def arm(rows):
    rows = [r for r in rows if r["trace_id"] not in REJECTED_GOLDS]
    n = len(rows)
    e_out, g_out, confs = [], [], []
    flips, b, c = [], 0, 0
    for r in rows:
        e = norm(r["predicted_label"]) == norm(r["gold_answer"])
        t = tolerant_match_v32(r["predicted_label"], r["gold_answer"])
        e_out.append(1 if e else 0)
        g_out.append(1 if t else 0)
        try:
            cf = float(r.get("confidence", 0.0))
        except (TypeError, ValueError):
            cf = 0.0
        confs.append(cf)
        if (not e) and t:
            b += 1
            flips.append({"trace_id": r["trace_id"],
                          "predicted": r["predicted_label"],
                          "gold": r["gold_answer"]})
        if e and (not t):
            c += 1
            flips.append({"trace_id": r["trace_id"] + ":c-cell",
                          "predicted": r["predicted_label"],
                          "gold": r["gold_answer"]})
    p_two, degen = mcnemar_exact_two(b, c)
    return {"n": n, "n_rejected": len(rows) - n if False else 0,
            "n_exact": sum(e_out), "n_guarded": sum(g_out),
            "acc_exact": sum(e_out) / n, "acc_guarded": sum(g_out) / n,
            "n_flips": len(flips), "flip_rate": len(flips) / n,
            "mcnemar_b": b, "mcnemar_c": c, "mcnemar_p_two": p_two,
            "mcnemar_degenerate": degen,
            "ece10_exact": ece_equal_width(confs, e_out),
            "ece10_guarded": ece_equal_width(confs, g_out),
            "n_errs": sum(1 for r in rows if r.get("error")),
            "flips": flips}


def main(kb, seal):
    cloud = json.load(open(os.path.join(kb, "evidence", "cloud_powrep255_raw.json"),
                           encoding="utf-8"))
    local = json.load(open(os.path.join(kb, "evidence", "local_powrep157_raw.json"),
                           encoding="utf-8"))
    assert len(cloud) == 255 and len(local) == 157
    by_arm = {"pow1_pilot": [r for r in cloud if r["trace_id"].startswith("pow1-")
                             and int(r["trace_id"].split("-")[1]) <= 20],
              "pow1_holdout": [r for r in cloud if r["trace_id"].startswith("pow1-")
                               and int(r["trace_id"].split("-")[1]) > 20],
              "pow2_cloudnew": [r for r in cloud if r["trace_id"].startswith("pow2-")],
              "powL_localnew": local}
    out = {"matcher": "label_match_v32.tolerant_match_v32",
           "rejected_golds": REJECTED_GOLDS,
           "note": "power-replication arms; spot-check gate applies"}
    for k, rows in by_arm.items():
        out[k] = arm(rows)
    summ = {k: {kk: vv for kk, vv in v.items() if kk != "flips"}
            for k, v in out.items() if isinstance(v, dict)}
    print(json.dumps(summ, ensure_ascii=False, indent=1))
    if seal:
        assert not REJECTED_GOLDS or True
        json.dump(out, open(os.path.join(kb, "results", "powrep.json"), "w",
                            encoding="utf-8"), ensure_ascii=False, indent=2)
        print("SEALED results/powrep.json")


if __name__ == "__main__":
    main(sys.argv[1], "--seal" in sys.argv[2:])
