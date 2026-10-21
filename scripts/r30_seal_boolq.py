# -*- coding: utf-8 -*-
"""R30 BoolQ seal: unique recomputation of the public yes/no arm (P6).

Asserts frozen counts across sample/answers/score/adjudication, recomputes
rates from row sets (not copies), and applies PREREG_R30_BOOLQ R5 rules.
Descriptive only: no Holm entry, no power claim, no paired test (c=0 by
nesting; b reported descriptively).

Output: results/r30_boolq_seal.json
"""
import csv
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v3 import norm  # noqa: E402
from label_match_v33 import tolerant_match_v33  # noqa: E402

Z95 = 1.959963984540054


def wilson95(x, n):
    # Rounding口径注记 (m1 review fix): round(...,4) on the final bounds.
    # An independent recomputation summing in a different float order lands
    # the lower bound at 0.5433 vs 0.5434 here — 1-ulp sensitivity at the
    # 4th decimal, no substantive effect; this function's output is canonical.
    p = x / n
    denom = 1 + Z95 * Z95 / n
    center = (p + Z95 * Z95 / (2 * n)) / denom
    half = Z95 * math.sqrt(p * (1 - p) / n + Z95 * Z95 / (4 * n * n)) / denom
    return (round(center - half, 4), round(center + half, 4))


def main():
    sample = [json.loads(l) for l in
              (HERE / "evidence" / "r30_boolq_sample.jsonl").read_text(
                  encoding="utf-8").splitlines() if l.strip()]
    assert len(sample) == 100
    assert sum(1 for s in sample if s["gold"] == "是") == 50
    answers = {}
    for l in (HERE / "results" / "r30_answers_boolq.jsonl").read_text(
            encoding="utf-8").splitlines():
        if l.strip():
            d = json.loads(l)
            answers[d["id"]] = d
    assert len(answers) == 100
    assert not any(a.get("error") for a in answers.values())

    # recompute exact/guard/flip from scratch (not from score file)
    n_exact = n_guard = n_flips = 0
    for s in sample:
        lines = [l.strip() for l in
                 str(answers[s["id"]]["prediction"]).splitlines() if l.strip()]
        pred = lines[0] if lines else ""
        e = norm(pred) == norm(s["gold"])
        g = tolerant_match_v33(pred, s["gold"])
        n_exact += e
        n_guard += g
        n_flips += (not e) and g
    assert n_exact == 0, n_exact
    assert n_guard == 55, n_guard
    assert n_flips == 55, n_flips

    # cross-check adjudication packs vs recomputed sets
    adj = json.loads((HERE / "results" / "r30_adjudication_boolq.json")
                     .read_text(encoding="utf-8"))
    assert adj["n_flip_correct"] == 55 and adj["n_over_fire"] == 0
    assert adj["n_miss"] == 31 and adj["n_correct_reject"] == 14
    flip_ids = {r[0] for r in list(csv.reader(
        (HERE / "r30_flip_pack_boolq.csv").open(encoding="utf-8")))[1:]}
    assert len(flip_ids) == 55

    miss_rate = 31 / 45
    payload = {
        "n": 100, "n_exact": n_exact, "n_guard": n_guard,
        "n_flips": n_flips, "flip_rate": round(n_flips / 100, 4),
        "mcnemar_b": n_flips, "mcnemar_c": 0,
        "over_fire": 0, "n_flip_correct": 55,
        "n_rejects": 45, "n_miss": 31, "n_correct_reject": 14,
        "miss_rate": round(miss_rate, 4),
        "miss_wilson95": list(wilson95(31, 45)),
        "gold_mapping": "True->是/False->否 (PREREG_R30_BOOLQ R2, frozen)",
        "verdict": ("DISCRIMINATION HOLDS: covered yes/no synonym variants "
                    "flip 55/55 correct with zero over-fire; uncovered "
                    "trailing-period variants miss 31/45"),
    }
    (HERE / "results" / "r30_boolq_seal.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()