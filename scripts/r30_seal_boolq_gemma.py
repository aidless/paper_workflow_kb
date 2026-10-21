# -*- coding: utf-8 -*-
"""R30 BoolQ second-model seal (PREREG_R30_BOOLQ A2; R32; C82 candidate).

Unique recomputation of the gemma3:4b arm from raw answers (not from copies),
asserting frozen counts across sample/answers/score/adjudication, then
applying the A2 / R5 descriptive rules.

Descriptive only: no Holm entry, no power claim, no paired test (c=0 by
nesting; b reported descriptively). The one timeout row is disclosed and
kept out of all denominators rather than silently imputed.

Output: results/r30_boolq_gemma_seal.json
"""
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
    for l in (HERE / "results" / "r30_answers_boolq_gemma.jsonl").read_text(
            encoding="utf-8").splitlines():
        if l.strip():
            d = json.loads(l)
            answers[d["id"]] = d
    assert len(answers) == 100

    # recompute exact/guard/flip from scratch
    n_scored = n_exact = n_guard = n_flips = 0
    errors = []
    for s in sample:
        a = answers[s["id"]]
        if a.get("error") or not a.get("prediction"):
            errors.append(s["id"])
            continue
        lines = [l.strip() for l in
                 str(a["prediction"]).splitlines() if l.strip()]
        pred = lines[0] if lines else ""
        e = norm(pred) == norm(s["gold"])
        g = tolerant_match_v33(pred, s["gold"])
        n_scored += 1
        n_exact += e
        n_guard += g
        n_flips += (not e) and g
    assert n_scored == 99, n_scored
    assert errors == ["boolq-1159"], errors
    assert n_exact == 0, n_exact
    assert n_guard == 45, n_guard
    assert n_flips == 45, n_flips

    # cross-check adjudication packs vs recomputed sets
    adj = json.loads((HERE / "results" / "r30_adjudication_boolq_gemma.json")
                     .read_text(encoding="utf-8"))
    assert adj["n_flip_correct"] == 45 and adj["n_over_fire"] == 0
    assert adj["n_rejects"] == 54 and adj["n_miss"] == 39
    assert adj["n_correct_reject"] == 15, adj["n_correct_reject"]
    assert adj["model"] == "gemma3:4b"

    n_rejects = 54
    n_miss = 39
    payload = {
        "model": "gemma3:4b",
        "amendment": "PREREG_R30_BOOLQ Amendment A2 (R32 second-model replication)",
        "n": 100,
        "n_scored": n_scored,
        "n_errors": len(errors),
        "error_ids": errors,
        "error_disclosure": "boolq-1159 timed out at collection; kept out of all "
                            "denominators, not imputed (R5 failure path)",
        "n_exact": n_exact,
        "n_guard": n_guard,
        "n_flips": n_flips,
        "flip_rate_scored": round(n_flips / n_scored, 4),
        "mcnemar_b": n_flips,
        "mcnemar_c": 0,
        "over_fire": 0,
        "n_flip_correct": 45,
        "n_rejects": n_rejects,
        "n_miss": n_miss,
        "n_correct_reject": 15,
        "miss_rate": round(n_miss / n_rejects, 4),
        "miss_wilson95": wilson95(n_miss, n_rejects),
        "gold_mapping": "True->是/False->否 (PREREG_R30_BOOLQ R2, frozen, reused verbatim)",
        "prompt": "frozen Chinese short-answer instruction, reused verbatim from the main arm",
        "comparison_main_arm": {"model": "qwen2:7b", "n_exact": 0, "n_guard": 55,
                                "n_flips": 55, "n_flip_correct": 55,
                                "n_over_fire": 0, "n_miss": 31,
                                "n_correct_reject": 14},
        "verdict": "DIRECTION REPLICATES in a second model family: covered yes/no "
                   "synonym variants flip 45/45 content-correct with zero over-fire "
                   "(45 of 99 scored), uncovered forms miss 39 of 54 rejects. "
                   "Magnitude is lower than the main arm (45 vs 55 flips); "
                   "descriptive observed-status only, no inference.",
        "scope": "no Holm entry, no power claim, no paired test; main-arm sealed "
                 "numbers (C78) neither retried nor rewritten",
    }
    (HERE / "results" / "r30_boolq_gemma_seal.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
