"""Seal extended-stratum rollups (deterministic transform of sealed files).

Extended strata = prior sealed stratum + power-rep arm (disjoint questions,
same protocol family, v3.1/v3.2-equivalent basis). No new model calls.
Prior b/c from: results/analysis.json (pilot, holdout-main),
results/cloud_new.json (raw) + results/guard_v31.json strata.cloud-new (guarded),
results/local_new.json. New b/c from results/powrep.json.

Writes results/powrep_rollups.json. McNemar exact two-sided on summed b/c.

Usage: python3 paper_workflow_kb/scripts/seal_powrep_rollups.py paper_workflow_kb
"""
import json
import math
import os
import sys


def mcnemar_exact_two(b, c):
    n_d = b + c
    if n_d == 0:
        return 1.0, True
    total = 2 ** n_d
    lo = sum(math.comb(n_d, k) for k in range(0, min(b, c) + 1))
    hi = sum(math.comb(n_d, k) for k in range(max(b, c), n_d + 1))
    return min(1.0, 2 * min(lo, hi) / total), False


def main(kb):
    def load(fn):
        return json.load(open(os.path.join(kb, "results", fn), encoding="utf-8"))
    a = load("analysis.json")
    cn = load("cloud_new.json")
    g31 = load("guard_v31.json")
    ln = load("local_new.json")
    pr = load("powrep.json")
    # hard-gate the prior inputs (exact sealed values)
    assert a["subsets"]["pilot"]["mcnemar_b"] == 11
    assert a["subsets"]["pilot"]["mcnemar_c"] == 0
    assert a["subsets"]["holdout-main"]["mcnemar_b"] == 5
    assert a["subsets"]["holdout-main"]["mcnemar_c"] == 0
    assert cn["mcnemar_b"] == 5 and cn["mcnemar_c"] == 0
    assert g31["strata"]["cloud-new"]["mcnemar_b"] == 4
    assert g31["strata"]["cloud-new"]["mcnemar_c"] == 0
    assert ln["mcnemar_b"] == 5 and ln["mcnemar_c"] == 0
    assert pr["pow1_pilot"]["mcnemar_b"] == 0
    assert pr["pow1_holdout"]["mcnemar_b"] == 2
    assert pr["pow2_cloudnew"]["mcnemar_b"] == 1
    assert pr["powL_localnew"]["mcnemar_b"] == 7
    specs = {
        # key: (prior_n, prior_b_raw, prior_b_guarded, new_n, new_b, label)
        "pilot50": (30, 11, 11, 20, 0),
        "holdout108": (30, 5, 5, 78, 2),
        "cloudnew217_raw": (60, 5, 5, 157, 1),
        "cloudnew217_guarded": (60, 4, 4, 157, 1),
        "localnew217": (60, 5, 5, 157, 7),
    }
    out = {"note": "extended strata = prior sealed + power-rep arm; "
                   "post-registration extension, observed significance only",
           "strata": {}}
    for k, (pn, pbr, pbg, nn, nb) in specs.items():
        pb = pbg if k.endswith("guarded") else pbr
        b, c = pb + nb, 0
        p_two, degen = mcnemar_exact_two(b, c)
        out["strata"][k] = {"n": pn + nn, "b": b, "c": c,
                            "mcnemar_p_two": p_two,
                            "mcnemar_degenerate": degen}
    # assertions = the facts the manuscript may cite
    s = out["strata"]
    assert s["pilot50"]["n"] == 50 and s["pilot50"]["b"] == 11
    assert s["holdout108"]["n"] == 108 and s["holdout108"]["b"] == 7
    assert s["cloudnew217_guarded"]["n"] == 217 and s["cloudnew217_guarded"]["b"] == 5
    assert s["localnew217"]["n"] == 217 and s["localnew217"]["b"] == 12
    json.dump(out, open(os.path.join(kb, "results", "powrep_rollups.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
