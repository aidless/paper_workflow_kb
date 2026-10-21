# -*- coding: utf-8 -*-
"""R30 BoolQ author adjudication (PREREG_R30_BOOLQ R4; single author).

Frozen semantic rules, applied row by row; packs written per row:
- flip rows (55, census): Yes<->True / No<->False => flip_correct, else over_fire.
- reject rows (45, census since <=60): trailing-period Yes./No. matching gold
  class => miss; content mismatch => correct_reject; bare 1/1.0 =>
  correct_reject (non-answer form, disclosed rule).

Outputs: r30_flip_pack_boolq.csv, r30_miss_pack_boolq.csv,
  results/r30_adjudication_boolq.json
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def main():
    score = json.loads((HERE / "results" / "r30_score_boolq.json").read_text(
        encoding="utf-8"))
    sample = {}
    for l in (HERE / "evidence" / "r30_boolq_sample.jsonl").read_text(
            encoding="utf-8").splitlines():
        if l.strip():
            d = json.loads(l)
            sample[d["id"]] = d

    flip_rows, over_fire = [], []
    with open(HERE / "r30_flip_pack_boolq.csv", "w", newline="",
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
    assert len(flip_rows) + len(over_fire) == 55, len(flip_rows)

    miss, correct_reject = [], []
    with open(HERE / "r30_miss_pack_boolq.csv", "w", newline="",
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
    assert len(miss) + len(correct_reject) == 45, len(miss)

    payload = {"n_flips": 55, "n_flip_correct": len(flip_rows),
               "n_over_fire": len(over_fire),
               "n_rejects": 45, "n_miss": len(miss),
               "n_correct_reject": len(correct_reject),
               "miss_ids": sorted(miss)}
    (HERE / "results" / "r30_adjudication_boolq.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()