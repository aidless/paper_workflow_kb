"""Decode GOLD-100 user grades vs sealed guarded outcomes.

Gated on grades_gold100_user.csv (user-filled 你的判定 column with 对/错).
Reports: agreement vs guarded outcomes + Wilson 95% CI (overall, stem/
stemless, flips/nonflips), FP-inventory check on the 7 excluded items
(grader marks 错 where guarded says 对 vindicates the exclusion),
both-wrong negative agreement.

Usage: python3 paper_workflow_kb/scripts/decode_gold100.py paper_workflow_kb
"""
import csv
import json
import math
import os
import sys


def wilson(x, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = x / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round(max(0.0, (c - m) / d), 4), round(min(1.0, (c + m) / d), 4))


def main(kb):
    key = json.load(open(os.path.join(kb, "evidence", "gold100_key.json"),
                         encoding="utf-8"))
    gp = os.path.join(kb, "grades_gold100_user.csv")
    if not os.path.exists(gp):
        raise SystemExit("MISSING grades_gold100_user.csv: user grading pending; "
                         "no decode run (not a failure of the package)")
    rows = list(csv.DictReader(open(gp, encoding="utf-8-sig")))
    assert len(rows) == 100, len(rows)
    agree = stem_a = stem_n = flip_a = flip_n = 0
    fp_vindicated = []
    agree_adj = 0
    adj_diverge = []
    r18_exc = set(json.load(open(os.path.join(kb, 'results', 'r18_adjudication.json'),
                                           encoding='utf-8'))['excluded'])
    het_exc = set(json.load(open(os.path.join(kb, 'results',
        'r18_heteromodel_adjudication.json'), encoding='utf-8'))['excluded'])
    assert r18_exc == {'lr18-54', 'lr18-55'}, r18_exc  # R22: lr18-42 non-flip under v33
    assert het_exc == {'gr18-41', 'gr18-42', 'gr18-45'}, het_exc
    neg_a = neg_n = 0
    for r in rows:
        hid = r["id"].strip()
        v = r["你的判定(对/错)"].strip()
        assert v in ("对", "错"), (hid, v)
        k = key["mapping"][hid]
        g = "对" if k["guarded_outcome"] == 1 else "错"
        hit = int(v == g)
        agree += hit
        if r["question"].strip():
            stem_a += hit
            stem_n += 1
        if k["kind"] in ("flip-confirmed", "flip-excluded"):
            flip_a += hit
            flip_n += 1
        if k["kind"] == "flip-excluded" and v == "错" and g == "对":
            fp_vindicated.append(hid)
        if k["kind"] == "nonflip" and g == "错":
            neg_a += hit
            neg_n += 1
        # adjudicated basis: excluded flips revert to exact (all 7 are b-cell,
        # verified against sealed exclusion lists below); else guarded outcome
        adj = 0 if k["kind"] == "flip-excluded" else k["guarded_outcome"]
        agree_adj += int(("对" if adj == 1 else "错") == v)
        if k["kind"] == "flip-excluded" and adj == 0 and v == "对":
            adj_diverge.append(hid)
    n = len(rows)
    lo, hi = wilson(agree, n)
    out = {"n": n, "agree": agree, "agreement": round(agree / n, 4),
           "wilson95": [lo, hi],
           "stem": {"a": stem_a, "n": stem_n, "wilson95": list(wilson(stem_a, stem_n))},
           "flips": {"a": flip_a, "n": flip_n,
                     "wilson95": list(wilson(flip_a, flip_n))},
           "negatives_bothwrong": {"a": neg_a, "n": neg_n},
           "fp_exclusions_vindicated": fp_vindicated,
           "agree_adjudicated": agree_adj,
           "agreement_adjudicated": round(agree_adj / n, 4),
           "wilson95_adjudicated": list(wilson(agree_adj, n)),
           "adjudicated_divergences": sorted(adj_diverge)}
    json.dump(out, open(os.path.join(kb, "results", "gold100_agreement.json"),
                        "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
