# -*- coding: utf-8 -*-
"""Decode GOLD-25 user grades (pre-registered analysis, runs AFTER grades arrive).

Usage: python3 scripts/analyze_gold.py <grades_csv>
  grades_csv: copy of gold_grading_pack.csv with '你的判定(对/错)' filled
              with 对 / 错 / 存疑.

Pre-specified (from build_gold_pack.py docstring + analysis_plan in key):
- Reference: all 25 guarded outcomes are CORRECT per evidence, so a user
  grade of 对 counts as agreement, 错 as disagreement.
- Primary: overall agreement proportion + Wilson 95% CI.
- Split: stem (flip-stem, n=14) vs stemless (flip-nostem, n=11) reported.
- '存疑' grades: reported separately; sensitivity analysis excludes them
  from the denominator. Empty grades: hard FAIL (pack incomplete).

Outputs: results/gold_agreement.json (evidence) + stdout summary.
"""
import csv
import json
import math
import sys


def wilson(x, n, z=1.96):
    assert n > 0
    p = x / n
    den = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - m) / den, (c + m) / den


def main():
    gpath = sys.argv[1]
    key = json.load(open("evidence/gold_key.json", encoding="utf-8"))
    mapping = key["mapping"]
    rows = list(csv.DictReader(open(gpath, encoding="utf-8-sig")))
    assert len(rows) == 25, len(rows)
    assert {r["id"] for r in rows} == set(mapping), "id mismatch vs sealed key"

    agree = disagree = unsure = 0
    stem_a = stem_n = nostem_a = nostem_n = 0
    per_item = []
    for r in rows:
        bid = r["id"]
        g = (r.get("你的判定(对/错)", "") or "").strip()
        assert g in ("对", "错", "存疑"), f"{bid}: incomplete/invalid grade {g!r}"
        kind = mapping[bid]["kind"]
        if g == "对":
            agree += 1
            ok = True
        elif g == "错":
            disagree += 1
            ok = False
        else:
            unsure += 1
            ok = None
        if kind == "flip-stem":
            stem_n += 1
            if ok is True:
                stem_a += 1
        else:
            nostem_n += 1
            if ok is True:
                nostem_a += 1
        per_item.append({"id": bid, "kind": kind,
                         "stratum": mapping[bid]["stratum"],
                         "grade": g, "agree": ok})

    n_total = agree + disagree  # primary denominator excludes 存疑 per plan
    lo, hi = wilson(agree, n_total)
    # sensitivity: 存疑 excluded from denominator entirely
    n_sens = agree + disagree
    slo, shi = wilson(agree, n_sens)
    s_lo, s_hi = wilson(stem_a, stem_n) if stem_n else (0.0, 0.0)
    t_lo, t_hi = wilson(nostem_a, nostem_n) if nostem_n else (0.0, 0.0)

    out = {
        "n": 25,
        "agree": agree,
        "disagree": disagree,
        "unsure": unsure,
        "agreement": agree / n_total,
        "wilson95": [lo, hi],
        "sensitivity_excl_unsure": {"n": n_sens, "agreement": agree / n_sens,
                                    "wilson95": [slo, shi]},
        "stem": {"a": stem_a, "n": stem_n,
                 "agreement": stem_a / stem_n, "wilson95": [s_lo, s_hi]},
        "stemless": {"a": nostem_a, "n": nostem_n,
                     "agreement": nostem_a / nostem_n,
                     "wilson95": [t_lo, t_hi]},
        "per_item": per_item,
    }
    json.dump(out, open("results/gold_agreement.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"GOLD agree={agree}/25 disagree={disagree} unsure={unsure}")
    print(f"primary agreement={agree}/{n_total}={agree/n_total:.3f} "
          f"Wilson95=[{lo:.3f},{hi:.3f}]")
    print(f"stem={stem_a}/{stem_n} stemless={nostem_a}/{nostem_n}")
    print("WROTE results/gold_agreement.json")


if __name__ == "__main__":
    main()
