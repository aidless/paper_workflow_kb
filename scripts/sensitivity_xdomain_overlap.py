"""Sensitivity: xdomain minus 5 items overlapping pre-xdomain rows.

5/60 xdomain questions share a core stem with pre-existing rows (unit conversions
一公里等于多少米 / 一年有多少个月, capitals 中国/日本/法国首都; different
format hints). This script drops those 5 trace ids per layer and recomputes the
v3.2-basis McNemar exact two-sided + counts. Writes
results/xdomain_sensitivity.json.

Usage: python3 paper_workflow_kb/scripts/sensitivity_xdomain_overlap.py paper_workflow_kb
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from label_match_v3 import norm
from label_match_v32 import tolerant_match_v32

DROP = {"09", "16", "53", "54", "55"}


def mcnemar_exact_two(b, c):
    n_d = b + c
    if n_d == 0:
        return 1.0
    total = 2 ** n_d
    lo = sum(math.comb(n_d, k) for k in range(0, min(b, c) + 1))
    hi = sum(math.comb(n_d, k) for k in range(max(b, c), n_d + 1))
    return min(1.0, 2 * min(lo, hi) / total)


def main(kb):
    out = {"dropped_trace_suffixes": sorted(DROP),
           "reason": "core-stem overlap with pre-xdomain rows",
           "overlapping": {
               "09": "一公里等于多少米", "16": "一年有多少个月",
               "53": "中国的首都是哪里", "54": "日本的首都是哪里",
               "55": "法国的首都是哪里"}}
    for key, fn in [("tight", "cloud_xdomain60_raw.json"),
                    ("loose", "cloud_xdomain60_loose_raw.json")]:
        rows = [r for r in json.load(
            open(os.path.join(kb, "evidence", fn), encoding="utf-8"))
            if r["trace_id"].split("-")[1] not in DROP]
        assert len(rows) == 55, (key, len(rows))
        b = c = ng = 0
        for r in rows:
            e = norm(r["predicted_label"]) == norm(r["gold_answer"])
            t = tolerant_match_v32(r["predicted_label"], r["gold_answer"])
            ng += t
            b += ((not e) and t)
            c += (e and (not t))
        out[key] = {"n": 55, "n_guarded": ng, "n_flips": b + c,
                    "mcnemar_b": b, "mcnemar_c": c,
                    "mcnemar_p_two": mcnemar_exact_two(b, c)}
    assert out["tight"]["mcnemar_b"] == 1 and out["tight"]["mcnemar_c"] == 0
    assert out["loose"]["mcnemar_b"] == 19 and out["loose"]["mcnemar_c"] == 0
    json.dump(out, open(os.path.join(kb, "results", "xdomain_sensitivity.json"),
                        "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
