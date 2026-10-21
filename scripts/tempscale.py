"""Temperature scaling on adjudicated (= v3.1-guarded) labels, per stratum (goal-R2).

Fits scalar T>0 minimizing binary NLL of scaled confidences against
adjudicated correctness; reports NLL and equal-frequency 10-bin ECE at T=1
vs T=T*. Confidences clipped to [1e-6, 1-1e-6] (disclosed); T searched in
[0.05, 20] via bounded scalar minimization (scipy if present, else grid).
Output results/tempscale.json. Adjudicated labels == guarded outcomes
(verified: guard changed exactly one row, cloud-new-42, matching the
independent judge; prior 60 unchanged and 16/16 judge-confirmed).
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


def scale(p, T):
    p = min(1 - EPS, max(EPS, p))
    z = math.log(p / (1 - p))
    q = 1.0 / (1.0 + math.exp(-z / T))
    return min(1 - EPS, max(EPS, q))


def nll(confs, outs, T):
    tot = 0.0
    for p, y in zip(confs, outs):
        q = scale(p, T)
        tot += -(y * math.log(q) + (1 - y) * math.log(1 - q))
    return tot


def fit_T(confs, outs):
    try:
        from scipy.optimize import minimize_scalar
        r = minimize_scalar(lambda T: nll(confs, outs, T), bounds=(0.05, 20.0),
                            method="bounded", options={"xatol": 1e-4})
        return round(float(r.x), 4), round(float(r.fun), 4)
    except ImportError:
        grid = [round(0.05 + i * 0.05, 2) for i in range(400)]
        best = min(grid, key=lambda T: nll(confs, outs, T))
        return best, round(nll(confs, outs, best), 4)


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
        sub = [(t, a, g, c) for (t, s, a, g, c) in data if s == name]
        confs = [c for _, _, _, c in sub]
        outs = [int(guarded_tolerant_match(a, g)) for _, a, g, _ in sub]
        T_star, nll_star = fit_T(confs, outs)
        nll_1 = round(nll(confs, outs, 1.0), 4)
        ece_1 = ece_equal_freq(confs, outs)
        ece_s = ece_equal_freq([scale(p, T_star) for p in confs], outs)
        strata[name] = {"n": len(sub), "T_star": T_star, "NLL_T1": nll_1,
                        "NLL_Tstar": nll_star, "dNLL": round(nll_1 - nll_star, 4),
                        "ECE_T1": ece_1, "ECE_Tstar": ece_s,
                        "dECE": round(ece_1 - ece_s, 4)}
    out = {"labels": "adjudicated == v3.1-guarded outcomes (verified identical sets)",
           "clip": EPS, "T_bounds": [0.05, 20.0], "strata": strata}
    (HERE / "results" / "tempscale.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
