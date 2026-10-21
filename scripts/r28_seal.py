# -*- coding: utf-8 -*-
"""R28 seal: unique recomputation of cross-domain arm outcomes + gate verdicts.

Inputs: results/r28_score.json (exact/guard/flip per row) +
        results/r28_adjudication.json (author verdicts).
Asserts the frozen counts, computes Wilson CIs, and applies PREREG R5 decision rules.

Output: results/r28_seal.json
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))

Z95 = 1.959963984540054


def wilson95(x, n):
    if n <= 0:
        return (0.0, 0.0)
    p = x / n
    z = Z95
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (center - half, center + half)


def main():
    score = json.loads((HERE / "results" / "r28_score.json").read_text(encoding="utf-8"))
    adj = json.loads((HERE / "results" / "r28_adjudication.json").read_text(encoding="utf-8"))

    a = score["arms"]["degenerate_a"]
    b = score["arms"]["uncovered_b"]

    # --- Arm A assertions (frozen) ---
    assert a["n"] == 40, a["n"]
    assert a["n_flips"] == 1, a["n_flips"]
    a_flip_rows = [r for r in a["rows"] if r["flip"]]
    assert len(a_flip_rows) == 1
    assert a_flip_rows[0]["trace_id"] == "r28-a-08"
    a_over_fire = sum(1 for r in a_flip_rows
                      if adj["arm_a_flip_verdicts"].get(r["trace_id"], {}).get("verdict") != "flip_correct")
    assert a_over_fire == 0, a_over_fire

    # --- Arm B assertions (frozen) ---
    assert b["n"] == 40, b["n"]
    assert b["n_flips"] == 0, b["n_flips"]
    b_mc = score["b_miss_candidates"]
    assert len(b_mc) == 22, len(b_mc)
    n_miss = adj["arm_b_n_miss"]
    n_corr_rej = adj["arm_b_n_correct_reject"]
    assert n_miss == 21, n_miss
    assert n_corr_rej == 1, n_corr_rej
    assert n_miss + n_corr_rej == len(b_mc)

    miss_rate = n_miss / b["n"]
    miss_ci = wilson95(n_miss, b["n"])
    miss_ci = (round(miss_ci[0], 4), round(miss_ci[1], 4))  # 4-dp, R26 口径

    # --- PREREG R5 gate verdicts ---
    # P(i) degenerate: strict zero-flip NOT met (1 numeric .0-suffix flip), refined.
    gate_i = {
        "strict_zero_flip_met": (a["n_flips"] == 0),
        "descriptive_direction_met": (a["flip_rate"] < 0.05),
        "verdict": "REFINE",
        "note": "1/40 flip = numeric '.0' suffix (125.0 vs 125) covered by numeric branch; "
                "degenerate space -> ~zero flips except numeric-format variants covered by R",
    }
    # P(ii) uncovered: flip==0 AND miss>0 -> MET.
    gate_ii = {
        "flip_zero_met": (b["n_flips"] == 0),
        "miss_positive_met": (n_miss > 0),
        "verdict": "MET",
        "note": "0 flips, 21/40 miss (English unit variants present but R covers only Chinese units)",
    }

    payload = {
        "arm_a_degenerate": {
            "n": a["n"], "n_exact": a["n_exact"], "n_guard": a["n_guard"],
            "n_flips": a["n_flips"], "flip_rate": a["flip_rate"], "over_fire": a_over_fire,
            "flip_rows": [{"trace_id": r["trace_id"], "predicted": r["predicted"], "gold": r["gold"]}
                          for r in a_flip_rows],
        },
        "arm_b_uncovered": {
            "n": b["n"], "n_exact": b["n_exact"], "n_guard": b["n_guard"],
            "n_flips": b["n_flips"], "flip_rate": b["flip_rate"],
            "n_miss_candidates": len(b_mc), "n_miss": n_miss, "n_correct_reject": n_corr_rej,
            "miss_rate": miss_rate, "miss_wilson95": [miss_ci[0], miss_ci[1]],
        },
        "gates": {"p_i": gate_i, "p_ii": gate_ii},
    }
    (HERE / "results" / "r28_seal.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()