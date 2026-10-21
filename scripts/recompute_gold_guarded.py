# -*- coding: utf-8 -*-
"""GOLD-25 agreement against GUARDED outcomes (ROUND R15 fix for R5-01/R7-01).

Root cause: the pre-registered decode (scripts/analyze_gold.py) assumes
"all 25 guarded outcomes are CORRECT per evidence". That assumption fails on
exactly one item: G06 (trace cloud-new-42, "O" vs "O2"), which
scripts/build_gold_pack.py drew from the RAW flip file
(results/flips_new60.json, 5 raw flips incl. cloud-new-42) while the guarded
verdict (results/guard_v31.json, single changed row) rejects it. The blinded
grader marked G06 对 (semantically accepted), which DISAGREES with the guarded
verdict (incorrect). True agreement vs guarded = 24/25, not 25/25.

Derivation (all from sealed evidence, no hand values):
- guarded_incorrect(trace_id) <=> trace_id == guard_v31.changed_single_trace_id
- user grades read from grades_gold25_user.csv (assert all 25 present, valid)
- agreement <=> (grade == 对) == guarded_correct
Outputs results/gold_guarded_agreement.json. Fails loudly on any deviation.
"""
import csv
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def wilson(x, n, z=1.96):
    assert n > 0
    p = x / n
    den = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - m) / den, (c + m) / den


def main():
    key = json.loads((HERE / "evidence" / "gold_key.json").read_text(encoding="utf-8"))
    guard = json.loads((HERE / "results" / "guard_v31.json").read_text(encoding="utf-8"))
    mapping = key["mapping"]
    bad_tid = guard["changed_single_trace_id"]
    assert guard["n_changed_vs_v3"] == 1, guard["n_changed_vs_v3"]

    grades = {}
    with open(HERE / "grades_gold25_user.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            grades[r["id"]] = (r.get("你的判定(对/错)", "") or "").strip()
    assert set(grades) == set(mapping), "grade/key id mismatch"
    assert all(g in ("对", "错", "存疑") for g in grades.values()), grades

    per_item, agree = [], 0
    stem_a = stem_n = nostem_a = nostem_n = 0
    for bid, meta in sorted(mapping.items()):
        guarded_correct = meta["trace_id"] != bad_tid
        g = grades[bid]
        match = (g == "对") == guarded_correct if g in ("对", "错") else None
        if match is True:
            agree += 1
        per_item.append({"id": bid, "trace_id": meta["trace_id"],
                         "stratum": meta.get("stratum"), "kind": meta["kind"],
                         "guarded_correct": guarded_correct,
                         "user_grade": g, "agree_vs_guarded": match})
        if meta["kind"] == "flip-stem":
            stem_n += 1
            stem_a += match is True
        else:
            nostem_n += 1
            nostem_a += match is True

    n = len(mapping)
    assert n == 25, n
    n_incorrect_guarded = sum(1 for p in per_item if not p["guarded_correct"])
    assert n_incorrect_guarded == 1, per_item
    assert per_item and [p["id"] for p in per_item if not p["guarded_correct"]] == ["G06"]
    assert agree == 24, agree
    assert (stem_a, stem_n) == (13, 14), (stem_a, stem_n)
    assert (nostem_a, nostem_n) == (11, 11), (nostem_a, nostem_n)

    lo, hi = wilson(agree, n)
    slo, shi = wilson(stem_a, stem_n)
    tlo, thi = wilson(nostem_a, nostem_n)
    out = {
        "reference": "guarded (v3.1) outcomes; disagreeing item G06/cloud-new-42",
        "diverges_from_preregistered_decode": "analyze_gold.py assumed all-25 guarded-correct; false exactly on G06",
        "n": n, "agree": agree, "agreement": agree / n,
        "wilson95": [lo, hi],
        "stem": {"a": stem_a, "n": stem_n, "agreement": stem_a / stem_n,
                 "wilson95": [slo, shi]},
        "stemless": {"a": nostem_a, "n": nostem_n, "agreement": 1.0,
                     "wilson95": [tlo, thi]},
        "per_item": per_item,
    }
    (HERE / "results" / "gold_guarded_agreement.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"agree={agree}/{n} wilson=[{lo:.4f},{hi:.4f}] "
          f"stem={stem_a}/{stem_n} [{slo:.4f},{shi:.4f}] "
          f"stemless={nostem_a}/{nostem_n} [{tlo:.4f},{thi:.4f}]")


if __name__ == "__main__":
    sys.exit(main())
