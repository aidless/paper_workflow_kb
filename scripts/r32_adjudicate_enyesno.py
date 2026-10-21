# -*- coding: utf-8 -*-
"""R32 English yes/no arm author adjudication (PREREG_R32_ENYESNO R2, R3).

Frozen semantic rules from PREREG R2 ("裁决口径沿 R30"), applied row by row,
with per-row packs written:
- flip rows (census): the polarity token at the head of the answer matches the
  gold class => flip_correct, else over_fire.
- reject rows (census): trailing-period Yes./No. with the gold polarity => miss
  (right content, uncovered variant); bare 1/1.0 => correct_reject (non-answer
  numeric form); otherwise content mismatch => correct_reject.

Polarity is read from the RAW answer head with ^(yes|no)\b rather than from
`norm()` output: norm() strips commas, so "Yes, X" would normalise to "yesx" and
a `[.,]`-terminated head check would miss every extended answer. The `\b` is
what keeps "not ..." from being read as polarity "no".

A selftest below asserts the reader on the surface forms this arm actually
produces, including the two negatives that broke the first version.

Descriptive only: no Holm entry, no power claim, no paired test; the R30 sealed
numbers (C78) and the A2 arm (C82) are neither retried nor rewritten.

Outputs: r32_flip_pack_enyesno.csv, r32_miss_pack_enyesno.csv,
  results/r32_adjudication_enyesno.json
"""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v3 import norm  # noqa: E402

POL = re.compile(r"^\s*(yes|no)\b", re.IGNORECASE)


def polarity(pred):
    m = POL.match(str(pred))
    return m.group(1).lower() if m else None


SELFTEST = [
    ("Yes", "yes"), ("No", "no"), ("Yes.", "yes"), ("No.", "no"),
    ("Yes, there is a Las Vegas in New Mexico.", "yes"),
    ("No, you do not need to be on US soil.", "no"),
    ("not sure", None), ("Not necessarily", None), ("Unknown.", None),
]


def selftest():
    bad = [(p, polarity(p), e) for p, e in SELFTEST if polarity(p) != e]
    if bad:
        raise SystemExit("POLARITY SELFTEST FAILED: %s" % bad)
    print("POLARITY SELFTEST: %d cases PASS" % len(SELFTEST))


def main():
    selftest()
    score = json.loads(
        (HERE / "results" / "r32_score_enyesno.json").read_text(
            encoding="utf-8"))
    sample = {}
    for l in (HERE / "evidence" / "r32_enyesno_sample.jsonl").read_text(
            encoding="utf-8").splitlines():
        if l.strip():
            d = json.loads(l)
            sample[d["id"]] = d

    flip_correct, over_fire = [], []
    with open(HERE / "r32_flip_pack_enyesno.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "gold", "predicted", "form", "verdict", "reason"])
        for r in score["flip_rows"]:
            gb = sample[r["id"]]["gold_bool"]
            pol = polarity(r["predicted"])
            ok = (pol == "yes" and gb is True) or (pol == "no" and gb is False)
            v = "flip_correct" if ok else "over_fire"
            w.writerow([r["id"], r["gold"], r["predicted"], r["form"], v,
                        "polarity token matches gold class" if ok
                        else "guard accepted wrong polarity"])
            (flip_correct if ok else over_fire).append(r["id"])
    assert len(flip_correct) + len(over_fire) == score["n_flips"]

    miss, correct_reject = [], []
    reject_lens = []
    with open(HERE / "r32_miss_pack_enyesno.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "gold", "predicted", "form", "len", "verdict",
                    "reason"])
        for r in score["reject_rows"]:
            gb = sample[r["id"]]["gold_bool"]
            p = r["predicted"]
            reject_lens.append(len(p))
            pol = polarity(p)
            if norm(p) in ("yes.", "no.") and \
                    ((pol == "yes") == (gb is True)):
                v, reason = "miss", "right content, trailing-period variant uncovered"
                miss.append(r["id"])
            elif norm(p) in ("1", "1.0"):
                v, reason = "correct_reject", "non-answer numeric form"
                correct_reject.append(r["id"])
            else:
                v, reason = "correct_reject", "wrong content, guard rightly rejects"
                correct_reject.append(r["id"])
            w.writerow([r["id"], r["gold"], p, r["form"], len(p), v, reason])
    assert len(miss) + len(correct_reject) == score["n_rejects"]

    payload = {"model": "qwen2:7b", "n_flips": score["n_flips"],
               "n_flip_correct": len(flip_correct),
               "n_over_fire": len(over_fire),
               "n_rejects": score["n_rejects"], "n_miss": len(miss),
               "n_correct_reject": len(correct_reject),
               "n_errors": score["n_errors"], "error_ids": score["error_ids"],
               "reject_len_max": max(reject_lens) if reject_lens else 0,
               "reject_census": "<= %d chars" % (max(reject_lens) if reject_lens else 0),
               "miss_ids": sorted(miss),
               "over_fire_ids": sorted(over_fire)}
    (HERE / "results" / "r32_adjudication_enyesno.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
