# -*- coding: utf-8 -*-
"""Seal for the hetero second judge (PREREG_R31_HETEROJUDGE R4).

Recomputes from evidence/r18_heteromodel_judge.json (first judge) and
evidence/r18_heteromodel_judge2.json (second judge): row identity, per-row
agreements vs first judge AND vs author sealed conclusion (8 confirmed /
3 excluded gr18-41/42/45), and the >=2/3 systematic-exclusion check.
Descriptive only: reliability evidence, no overturn, no validity claim.

Output: results/r18_heteromodel_judge2_agreement.json
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
EXCLUDED = {"gr18-41", "gr18-42", "gr18-45"}


def main():
    j1 = {r["trace_id"]: r["judge_verdict"] for r in json.loads(
        (HERE / "evidence" / "r18_heteromodel_judge.json").read_text(
            encoding="utf-8"))["rows"]}
    j2 = {r["trace_id"]: r["judge_verdict"] for r in json.loads(
        (HERE / "evidence" / "r18_heteromodel_judge2.json").read_text(
            encoding="utf-8"))["rows"]}
    assert len(j1) == len(j2) == 11, (len(j1), len(j2))
    assert set(j1) == set(j2), set(j1) ^ set(j2)
    assert sum(1 for v in j1.values() if v == "correct") == 8
    assert sum(1 for v in j1.values() if v == "incorrect") == 3

    agree = [t for t in j1 if j1[t] == j2[t]]
    disag = [t for t in j1 if j2[t] != "ERROR" and j1[t] != j2[t]]
    errs = [t for t in j1 if j2[t] == "ERROR"]
    assert len(agree) + len(disag) + len(errs) == 11

    # agreement vs author sealed conclusion (confirmed = not excluded)
    author_ok = {t: (t not in EXCLUDED) for t in j1}
    j2_ok = {t: (j2[t] == "correct") for t in j1 if j2[t] != "ERROR"}
    agree_author = [t for t in j2_ok if j2_ok[t] == author_ok[t]]
    disag_author = [t for t in j2_ok if j2_ok[t] != author_ok[t]]
    # systematic-exclusion check on the 3 excluded rows
    excl_disag = [t for t in EXCLUDED if j2[t] != "incorrect"]
    assert len(excl_disag) < 2, excl_disag  # <2/3: no Limitations trigger

    payload = {
        "n": 11,
        "agree_first_judge": len(agree),
        "n_disagree_first_judge": len(disag),
        "disagree_first_judge": sorted(disag),
        "n_error_rows": len(errs),
        "error_rows": sorted(errs),
        "agree_author": len(agree_author),
        "disagree_author": sorted(disag_author),
        "excluded_disagreements": sorted(excl_disag),
        "limitations_trigger": False,
        "framing": ("reliability across judge families only; "
                    "no overturn of sealed adjudication, no validity claim"),
    }
    (HERE / "results" / "r18_heteromodel_judge2_agreement.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()