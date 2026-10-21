# -*- coding: utf-8 -*-
"""R32 English yes/no arm scoring (PREREG_R32_ENYESNO R2/R3, FROZEN design).

Same pipeline as the R30 arms: exact (norm vs frozen gold) + guard v3.3;
flip = exact-reject AND guard-accept; rejects are the guard-reject rows.

ADDED (and declared as NOT preregistered): a three-way decomposition of the
prediction surface by answer FORM -- bare polarity / trailing-period variant /
extended restatement. This exists because with a NATIVE gold mapping the guard
resolves the period variant through its substring branch ("yes" in "yes."),
whereas with the Chinese mapping it did not ("yes." against gold 是 was a
reject/miss in R30). Without this decomposition the flip/miss counts would be
uninterpretable, because the same surface form lands in a different category
purely because the gold language changed.

Descriptive only: no Holm entry, no power claim, no paired test.

Reads  evidence/r32_enyesno_sample.jsonl + results/r32_answers_enyesno.jsonl
Output: results/r32_score_enyesno.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))

from label_match_v3 import norm  # noqa: E402
from label_match_v33 import tolerant_match_v33  # noqa: E402

OUT = HERE / "results" / "r32_score_enyesno.json"


def parse_first_line(resp):
    lines = [l.strip() for l in str(resp).splitlines() if l.strip()]
    return lines[0] if lines else ""


def form_of(pred):
    n = norm(pred)
    if n in ("yes", "no"):
        return "bare"
    if n in ("yes.", "no."):
        return "period_variant"
    if n.startswith("yes") or n.startswith("no"):
        return "extended"
    return "other"


def main():
    sample = [json.loads(l) for l in
              (HERE / "evidence" / "r32_enyesno_sample.jsonl").read_text(
                  encoding="utf-8").splitlines() if l.strip()]
    answers = {}
    for l in (HERE / "results" / "r32_answers_enyesno.jsonl").read_text(
            encoding="utf-8").splitlines():
        if l.strip():
            d = json.loads(l)
            answers[d["id"]] = d
    assert len(sample) == 60, len(sample)
    assert len(answers) == 60, len(answers)

    rows, flips, rejects, errors = [], [], [], []
    forms = {"bare": 0, "period_variant": 0, "extended": 0, "other": 0}
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
        f = form_of(pred)
        forms[f] += 1
        row = {"id": s["id"], "gold_bool": s["gold_bool"], "gold": gold,
               "predicted": pred, "exact": exact, "guard": guard, "form": f}
        rows.append(row)
        if not exact and guard:
            flips.append(row)
        if not guard:
            rejects.append(row)

    payload = {"n": 60, "n_scored": len(rows), "n_errors": len(errors),
               "error_ids": errors,
               "n_exact": sum(1 for r in rows if r["exact"]),
               "n_guard": sum(1 for r in rows if r["guard"]),
               "n_flips": len(flips), "n_rejects": len(rejects),
               "form_counts": forms,
               "flip_rows": flips, "reject_rows": rejects}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    print("scored=%d exact=%d guard=%d flips=%d rejects=%d errors=%d"
          % (len(rows), payload["n_exact"], payload["n_guard"],
             len(flips), len(rejects), len(errors)))
    print("forms=%s" % json.dumps(forms, ensure_ascii=False))


if __name__ == "__main__":
    main()
