# -*- coding: utf-8 -*-
"""R30 BoolQ second-model author adjudication (PREREG_R30_BOOLQ A2, R32).

Frozen semantic rules, applied row by row (identical to the main arm's
scripts/r30_adjudicate_boolq.py), packs written per row:
- flip rows (census): Yes<->True / No<->False => flip_correct, else over_fire.
- reject rows (census since <=60): trailing-period Yes./No. matching gold
  class => miss; bare 1/1.0 => correct_reject (non-answer form); content
  mismatch => correct_reject.

Descriptive only: no Holm entry, no power claim, no paired test. This arm
neither retries nor rewrites the main arm's sealed numbers (C78).

Outputs: r30_flip_pack_boolq_gemma.csv, r30_miss_pack_boolq_gemma.csv,
  results/r30_adjudication_boolq_gemma.json
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def main():
    score = json.loads(
        (HERE / "results" / "r30_score_boolq_gemma.json").read_text(
            encoding="utf-8"))
    sample = {}
    for l in (HERE / "evidence" / "r30_boolq_sample.jsonl").read_text(
            encoding="utf-8").splitlines():
        if l.strip():
            d = json.loads(l)
            sample[d["id"]] = d

    flip_rows, over_fire = [], []
    with open(HERE / "r30_flip_pack_boolq_gemma.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "gold", "predicted", "verdict", "reason"])
        for r in score["flip_rows"]:
            gb = sample[r["id"]]["gold_bool"]
            ok = (r["predicted"] == "Yes" and gb is True) or \
                 (r["predicted"] == "No" and gb is False)
            v = "flip_correct" if ok else "over_fire"
            w.writerow([r["id"], r["gold"], r["predicted"], v,
                        "content match via synonym branch" if ok
                        else "guard accepted wrong content"])
            (flip_rows if ok else over_fire).append(r["id"])
    assert len(flip_rows) + len(over_fire) == score["n_flips"], len(flip_rows)

    miss, correct_reject = [], []
    with open(HERE / "r30_miss_pack_boolq_gemma.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "gold", "predicted", "verdict", "reason"])
        for r in score["reject_rows"]:
            gb = sample[r["id"]]["gold_bool"]
            p = r["predicted"]
            if p in ("Yes.", "No.") and ((p == "Yes.") == (gb is True)):
                v, reason = "miss", "right content, trailing-period variant uncovered"
                miss.append(r["id"])
            elif p in ("1", "1.0"):
                v, reason = "correct_reject", "non-answer numeric form"
                correct_reject.append(r["id"])
            else:
                v, reason = "correct_reject", "wrong content, guard rightly rejects"
                correct_reject.append(r["id"])
            w.writerow([r["id"], r["gold"], p, v, reason])
    assert len(miss) + len(correct_reject) == score["n_rejects"], len(miss)

    payload = {"model": "gemma3:4b", "n_flips": score["n_flips"],
               "n_flip_correct": len(flip_rows),
               "n_over_fire": len(over_fire),
               "n_rejects": score["n_rejects"], "n_miss": len(miss),
               "n_correct_reject": len(correct_reject),
               "n_errors": score["n_errors"], "error_ids": score["error_ids"],
               "miss_ids": sorted(miss)}
    (HERE / "results" / "r30_adjudication_boolq_gemma.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
