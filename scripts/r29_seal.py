# -*- coding: utf-8 -*-
"""R29 seal: unique recomputation of merged 720-row power replication + gate verdicts.

Inputs: results/r29_score.json (merged exact/guard/flip + McNemar) +
        results/r29_adjudication.json (19 flip verdicts).
Asserts frozen counts; applies PREREG_R29 R5 rules.

Output: results/r29_power_seal.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))


def main():
    score = json.loads((HERE / "results" / "r29_score.json").read_text(encoding="utf-8"))
    adj = json.loads((HERE / "results" / "r29_adjudication.json").read_text(encoding="utf-8"))

    m = score["merged"]
    # frozen assertions
    assert score["n_total"] == 720, score["n_total"]
    assert score["local_big_n"] == 160 and score["topup_n"] == 560
    assert m["n_flips"] == 19, m["n_flips"]
    assert m["mcnemar_c"] == 0, m["mcnemar_c"]
    assert abs(m["flip_rate"] - 19 / 720) < 1e-9
    assert len(score["flip_rows"]) == 19
    assert adj["n_flips"] == 19
    assert adj["n_flip_correct"] + adj["n_over_fire"] == 19

    n_over_fire = adj["n_over_fire"]
    n_flip_correct = adj["n_flip_correct"]
    p = m["mcnemar_p_two"]

    # --- PREREG R29 R5 gate ---
    # n=720 met -> underpower gap closed (regardless of significance)
    gate_power = {
        "n_met": (score["n_total"] == 720),
        "n_ceil": 720,
        "verdict": "MET",
        "note": "local-big 160 -> 720, the '160 of 720 placeholder OR=4' gap is closed",
    }
    # McNemar: p significant -> H1 maintained (not downgraded)
    gate_mcnemar = {
        "p_two": p,
        "significant": (p < 0.05),
        "verdict": "SIGNIFICANT" if p < 0.05 else "NOT_SIGNIFICANT",
        "note": "b=19, c=0 (exact McNemar); H1 maintained (not downgraded)" if p < 0.05
                else "H1 downgraded per PREREG failure path",
    }
    # over-fire: new limitation class disclosed
    gate_overfire = {
        "n_over_fire": n_over_fire,
        "n_flip_correct": n_flip_correct,
        "over_fire_rate_in_flips": n_over_fire / 19,
        "note": "5 division-error over-fires within 0.5% numeric tolerance (new class)",
    }

    payload = {
        "merged": {
            "n": score["n_total"], "n_flips": m["n_flips"], "flip_rate": m["flip_rate"],
            "mcnemar_b": m["mcnemar_b"], "mcnemar_c": m["mcnemar_c"],
            "mcnemar_p_two": p, "n_flip_correct": n_flip_correct, "n_over_fire": n_over_fire,
        },
        "gates": {"power": gate_power, "mcnemar": gate_mcnemar, "over_fire": gate_overfire},
    }
    (HERE / "results" / "r29_power_seal.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()