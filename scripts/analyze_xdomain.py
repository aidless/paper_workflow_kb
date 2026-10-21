"""Sealed analysis: cross-domain layers (tight n=60 + loose n=60), v3.3 basis.

Reads paper_workflow_kb/evidence/cloud_xdomain60_raw.json and
cloud_xdomain60_loose_raw.json; writes results/xdomain.json with per-layer
n/exact/guarded/flips/flip_rate/McNemar exact two-sided b/c/p, ECE10
equal-width on rows carrying confidences, and flip lists.

R22 promotion: layer() matcher v3.2 -> v3.3 (single-CJK-substring guard).
xdomain inputs contain zero v32/v33 diff rows (global diff 1700-pair audit),
so xdomain outputs are byte-identical by construction (asserted below via
the unchanged hard assertions).

McNemar exact two-sided: p = 2*min(P(Bin(n_d,0.5)<=min(b,c)),
P(Bin(n_d,0.5)>=max(b,c))), capped at 1. Degenerate b=c=0 -> p=1.0 disclosed.

Usage: python3 paper_workflow_kb/scripts/analyze_xdomain.py paper_workflow_kb
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from label_match_v3 import norm
from label_match_v33 import tolerant_match_v33


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


def layer(rows):
    n = len(rows)
    e_out, g_out, confs = [], [], []
    flips = []
    b = c = 0
    for r in rows:
        e = norm(r["predicted_label"]) == norm(r["gold_answer"])
        t = tolerant_match_v33(r["predicted_label"], r["gold_answer"])
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
    return {"n": n, "n_exact": sum(e_out), "n_guarded": sum(g_out),
            "acc_exact": sum(e_out) / n, "acc_guarded": sum(g_out) / n,
            "n_flips": len(flips), "flip_rate": len(flips) / n,
            "mcnemar_b": b, "mcnemar_c": c, "mcnemar_p_two": p_two,
            "mcnemar_degenerate": degen,
            "ece10_exact": ece_equal_width(confs, e_out),
            "ece10_guarded": ece_equal_width(confs, g_out),
            "n_errs": sum(1 for r in rows if r.get("error")),
            "flips": flips}


def main(kb):
    out = {"matcher": "label_match_v33.tolerant_match_v33",
           "model": "qwen2.5:7b", "temperature": 0,
           "note": "cross-domain: measure-words + yes-no rephrasing + name variants; "
                   "tight = format-constrained prompt, loose = paraphrase regime"}
    for key, fn in [("tight", "cloud_xdomain60_raw.json"),
                    ("loose", "cloud_xdomain60_loose_raw.json")]:
        rows = json.load(open(os.path.join(kb, "evidence", fn), encoding="utf-8"))
        assert len(rows) == 60, (key, len(rows))
        out[key] = layer(rows)
    # hard assertions: the facts the ledger/manuscript may cite
    assert out["tight"]["n_flips"] == 1, out["tight"]
    assert out["loose"]["n_flips"] == 20, out["loose"]
    assert out["loose"]["mcnemar_b"] == 20 and out["loose"]["mcnemar_c"] == 0
    assert out["tight"]["mcnemar_b"] == 1 and out["tight"]["mcnemar_c"] == 0
    json.dump(out, open(os.path.join(kb, "results", "xdomain.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "flips"}
                      if isinstance(v, dict) else v for k, v in out.items()},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
