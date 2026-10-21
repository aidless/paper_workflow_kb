"""R21-P3: Cohen's kappa rater1 (user) vs rater2 on the 30-item blind pack.

Gated on grades_rater2_user2.csv (second human fills 你的判定 column with
对/错; "存疑" allowed -> counted as non-agreeing, reported separately).
Compares against grades_gold100_user.csv via sealed evidence/rater2_key.json.
Reports: n, agreement + Wilson 95% CI, Cohen's kappa (unweighted, 对/错 only),
confusion counts. Writes results/rater2_kappa.json.

Usage: python3 scripts/rater2_kappa.py <kb>
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
    gp = os.path.join(kb, "grades_rater2_user2.csv")
    if not os.path.exists(gp):
        raise SystemExit("MISSING grades_rater2_user2.csv: second-human grading "
                         "pending; kappa not run (not a failure of the package)")
    r2 = list(csv.DictReader(open(gp, encoding="utf-8-sig")))
    r1 = {r["id"].strip(): r["你的判定(对/错)"].strip()
          for r in csv.DictReader(open(os.path.join(kb, "grades_gold100_user.csv"),
                                       encoding="utf-8-sig"))}
    key = json.load(open(os.path.join(kb, "evidence", "rater2_key.json"), encoding="utf-8"))
    assert len(r2) == 30, len(r2)
    a = b = c = d = unsure = 0  # a=both对 b=r1对r2错 c=r1错r2对 d=both错
    for r in r2:
        bid = r["id"].strip()
        v2 = r["你的判定(对/错)"].strip()
        hid = key["mapping"][bid]["h_id"]
        v1 = r1[hid]
        assert v1 in ("对", "错"), (hid, v1)
        if v2 == "存疑":
            unsure += 1
            continue
        assert v2 in ("对", "错"), (bid, v2)
        if v1 == "对" and v2 == "对":
            a += 1
        elif v1 == "对" and v2 == "错":
            b += 1
        elif v1 == "错" and v2 == "对":
            c += 1
        else:
            d += 1
    n = a + b + c + d
    agree = a + d
    po = agree / n if n else 0.0
    pe = ((a + b) * (a + c) + (c + d) * (b + d)) / (n * n) if n else 0.0
    kappa = round((po - pe) / (1 - pe), 4) if pe < 1 else 0.0
    out = {"n_graded": n, "n_unsure": unsure, "agree": agree,
           "agreement": round(po, 4), "wilson95": list(wilson(agree, n)),
           "confusion": {"both_correct": a, "r1_only": b, "r2_only": c, "both_wrong": d},
           "expected_agreement": round(pe, 4), "cohens_kappa": kappa}
    json.dump(out, open(os.path.join(kb, "results", "rater2_kappa.json"),
                        "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
