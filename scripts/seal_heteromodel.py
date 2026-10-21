"""Hetero-model adjudication rollup: 11 flips, judge majority rule.

Decision rule (xdomain/R18 precedent): judge rejection on record -> EXCLUDED
(revert to exact outcome); no ERRORs occurred, no ties, no author fill-in.
Excluded gr18-41/42/45 are single-character name fragments (白/子/玄), the
same guard-missed fragment class as lr18-42 (牧/牧之): third/fourth exemplars.
R22 promotion: v3.3 rejects these fragments, so the analysis flip set drops to
the 8 confirmed rows; the judge content rulings (11 rows, 8 correct / 3 reject)
stand unchanged, and adjudicated accuracy is invariant (excluded rows used
exact outcomes in both schemes).

Writes results/r18_heteromodel_adjudication.json.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join("paper_workflow_kb", "scripts"))
from analyze_xdomain import ece_equal_width  # noqa: E402
from label_match_v3 import norm  # noqa: E402


def main(kb):
    raw = json.load(open(os.path.join(kb, "evidence",
                                      "r18_heteromodel_gemma60_raw.json"),
                         encoding="utf-8"))
    jd = json.load(open(os.path.join(kb, "evidence",
                                     "r18_heteromodel_judge.json"),
                        encoding="utf-8"))
    assert len(raw) == 60 and jd["n"] == 11
    verdicts = {r["trace_id"]: r["judge_verdict"] for r in jd["rows"]}
    assert set(verdicts) and all(v in ("correct", "incorrect")
                                 for v in verdicts.values()), verdicts
    excluded = sorted(t for t, v in verdicts.items() if v != "correct")
    confirmed = sorted(t for t, v in verdicts.items() if v == "correct")
    analysis_flips = {f["trace_id"] for f in
                      json.load(open(os.path.join(kb, "results", "r18_heteromodel.json"),
                                     encoding="utf-8"))["heteromodel"]["flips"]}
    # R22: analysis flip set (v3.3) must equal the 8 judge-confirmed rows;
    # the 3 judge-rejected fragments are no longer flips.
    assert analysis_flips == set(confirmed), (analysis_flips, confirmed)
    flips = set(verdicts)
    adj_correct, confs, accs = 0, [], []
    for r in raw:
        tid = r["trace_id"]
        exact_ok = bool(norm(r["predicted_label"]) == norm(r["gold_answer"]))
        ok = exact_ok if tid in excluded else (True if tid in flips else exact_ok)
        adj_correct += ok
        confs.append(float(r.get("confidence", 0.0)))
        accs.append(1.0 if ok else 0.0)
    ece = round(ece_equal_width(confs, accs), 4)
    out = {"n": 60, "raw_flips": len(analysis_flips), "confirmed": confirmed,
           "excluded": excluded, "adjudicated_flips": len(confirmed),
           "adjudicated_guarded_correct": adj_correct,
           "adjudicated_guarded_acc": round(adj_correct / 60, 4),
           "adjudicated_ece_equalwidth": ece}
    json.dump(out, open(os.path.join(kb, "results",
                                     "r18_heteromodel_adjudication.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
