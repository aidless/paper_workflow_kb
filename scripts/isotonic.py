"""Isotonic regression comparison on adjudicated (= v3.1-guarded) labels (goal-R3).

Per stratum: sort rows by confidence (stable sort; tie order disclosed as
arbitrary-but-deterministic), fit Pool-Adjacent-Violators isotonic regression
(count-weighted block means), report in-sample NLL/ECE plus 5-fold CV ECE/NLL
(folds = sorted-order round-robin; held-out prediction = fitted value at the
largest train confidence <= x, else the smallest train value; clipped to
[1e-6, 1-1e-6] for NLL). In-sample isotonic ECE is optimistic by construction;
the CV column is the honest one. No sklearn dependency (hand-rolled PAV).
Output results/isotonic.json.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v31 import guarded_tolerant_match, ece_equal_freq  # noqa: E402

EPS = 1e-6


def pav(y):
    """Count-weighted PAV; y sorted by x. Returns fitted values, same order."""
    blocks = [[float(v), 1] for v in y]
    i = 0
    while i < len(blocks) - 1:
        m1 = blocks[i][0] / blocks[i][1]
        m2 = blocks[i + 1][0] / blocks[i + 1][1]
        if m1 > m2 + 1e-12:
            blocks[i][0] += blocks[i + 1][0]
            blocks[i][1] += blocks[i + 1][1]
            del blocks[i + 1]
            if i > 0:
                i -= 1
        else:
            i += 1
    out = []
    for s, c in blocks:
        out += [s / c] * c
    return out


def clip(p):
    return min(1 - EPS, max(EPS, p))


def nll_of(ps, ys):
    tot = 0.0
    for p, y in zip(ps, ys):
        q = clip(p)
        tot += -(y * math.log(q) + (1 - y) * math.log(1 - q))
    return round(tot, 4)


def main() -> None:
    rows60 = [json.loads(l) for l in
              (HERE / "evidence" / "d2_60.jsonl").read_text(encoding="utf-8").splitlines()
              if l.strip()]
    rowsnew = json.loads((HERE / "evidence" / "cloud_new60_raw.json").read_text(encoding="utf-8"))
    data = ([(r["trace_id"], r["source"], str(r.get("predicted_label", "")),
              str(r.get("gold_answer", "")), float(r.get("confidence", 0.0)))
             for r in rows60]
            + [(r["trace_id"], r["source"], str(r.get("predicted_label", "")),
                str(r.get("gold_answer", "")), float(r.get("confidence", 0.0)))
               for r in rowsnew])

    strata = {}
    for name in ("pilot", "holdout-main", "cloud-new"):
        sub = sorted([(c, int(guarded_tolerant_match(a, g)))
                      for (t, s, a, g, c) in data if s == name],
                     key=lambda r: r[0])  # stable sort by confidence
        confs = [c for c, _ in sub]
        ys = [y for _, y in sub]
        n = len(sub)
        fit = pav(ys)
        ece_raw = ece_equal_freq(confs, ys)
        ece_in = ece_equal_freq(fit, ys)
        # 5-fold CV over sorted order (round-robin spreads confidence levels)
        cv_ps, cv_ys = [], []
        for f in range(5):
            te = [i for i in range(n) if i % 5 == f]
            tr = [i for i in range(n) if i % 5 != f]
            tr_xy = sorted([(confs[i], ys[i]) for i in tr], key=lambda r: r[0])
            tr_fit = pav([y for _, y in tr_xy])
            train_map = sorted(set(zip([x for x, _ in tr_xy], tr_fit)))
            for i in te:
                x = confs[i]
                cand = [v for (xx, v) in train_map if xx <= x + 1e-12]
                cv_ps.append(cand[-1] if cand else train_map[0][1])
                cv_ys.append(ys[i])
        strata[name] = {"n": n, "n_blocks": len(set(round(v, 9) for v in fit)),
                        "ECE_raw": ece_raw, "ECE_isotonic_insample": ece_in,
                        "dECE_insample": round(ece_raw - ece_in, 4),
                        "ECE_isotonic_cv5": ece_equal_freq(cv_ps, cv_ys),
                        "NLL_raw": nll_of(confs, ys), "NLL_isotonic_cv5": nll_of(cv_ps, cv_ys)}
    out = {"labels": "adjudicated == v3.1-guarded outcomes",
           "method": "hand-rolled count-weighted PAV on stable-conf-sorted rows; "
                     "5-fold CV round-robin; clip 1e-6; in-sample ECE optimistic by construction",
           "strata": strata}
    (HERE / "results" / "isotonic.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
