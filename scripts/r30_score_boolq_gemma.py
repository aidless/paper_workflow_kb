# -*- coding: utf-8 -*-
"""R30 BoolQ second-model scoring (PREREG_R30_BOOLQ Amendment A2, R32).

Same 100 frozen rows, same frozen Chinese prompt + gold mapping as the main
arm, answered by local gemma3:4b (temperature 0, num_predict 60). Scoring
pipeline is the main arm's: exact (norm vs gold 是/否) + guard v3.3;
flip = exact-reject + guard-accept. Descriptive only.

Reads evidence/r30_boolq_sample.jsonl + results/r30_answers_boolq_gemma.jsonl.
Output: results/r30_score_boolq_gemma.json.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))

from label_match_v3 import norm  # noqa: E402
from label_match_v33 import tolerant_match_v33  # noqa: E402

OUT = HERE / "results" / "r30_score_boolq_gemma.json"


def parse_first_line(resp):
    lines = [l.strip() for l in str(resp).splitlines() if l.strip()]
    return lines[0] if lines else ""


def main():
    sample = [json.loads(l) for l in
              (HERE / "evidence" / "r30_boolq_sample.jsonl").read_text(
                  encoding="utf-8").splitlines() if l.strip()]
    answers = {}
    for l in (HERE / "results" / "r30_answers_boolq_gemma.jsonl").read_text(
            encoding="utf-8").splitlines():
        if l.strip():
            d = json.loads(l)
            answers[d["id"]] = d
    assert len(sample) == 100, len(sample)
    assert len(answers) == 100, len(answers)

    rows, flips, rejects, errors = [], [], [], []
    for s in sample:
        a = answers.get(s["id"])
        # R5 failure path: error rows are recorded as-is, never silently kept
        if a is None or a.get("error") or not a.get("prediction"):
            errors.append(s["id"])
            continue
        pred = parse_first_line(a["prediction"])
        gold = s["gold"]
        exact = norm(pred) == norm(gold)
        guard = tolerant_match_v33(pred, gold)
        row = {"id": s["id"], "gold_bool": s["gold_bool"], "gold": gold,
               "predicted": pred, "exact": exact, "guard": guard}
        rows.append(row)
        if not exact and guard:
            flips.append(row)
        if not guard:
            rejects.append(row)

    payload = {"n": 100, "n_scored": len(rows), "n_errors": len(errors),
               "error_ids": errors,
               "n_exact": sum(1 for r in rows if r["exact"]),
               "n_guard": sum(1 for r in rows if r["guard"]),
               "n_flips": len(flips), "n_rejects": len(rejects),
               "flip_rows": flips, "reject_rows": rejects}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    print("scored=%d exact=%d guard=%d flips=%d rejects=%d errors=%d"
          % (len(rows), payload["n_exact"], payload["n_guard"],
             len(flips), len(rejects), len(errors)))
    for r in flips:
        print("FLIP %s gold=%s pred=%s" % (r["id"], r["gold"], r["predicted"]))


if __name__ == "__main__":
    main()
