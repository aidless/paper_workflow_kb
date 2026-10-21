"""Seal Holm-Bonferroni multiplicity accounting over the 18 analysis tests.

Family (guarded/adjudicated basis throughout; one comparison per analysis unit):
pilot, holdout-main, cloud-new-guarded, local-new, local-en, local-big, math,
pre-specified pool, xdomain-tight, xdomain-loose, pow1_pilot, pow1_holdout,
pow2_cloudnew, powL_localnew, pow1L, pow2L, powLL, r18-loose-rep (adjudicated
24 b-cells, arithmetic record only -- carries no inferential license under
nesting, same as the other seventeen).
Extended-stratum rollups are deterministic re-views of rows already in the
family and are NOT separate tests (stated in the manuscript).
v1 (17 tests) is preserved as results/holm_v1_17.json; this v2 supersedes it
with R18 added (ledger note R18-HOLM).

Writes results/holm.json with ordered p-values, Holm thresholds at
alpha=0.05, survivors, and the stopping step.

Usage: python3 paper_workflow_kb/scripts/seal_holm.py paper_workflow_kb
"""
import json
import os
import sys


def main(kb):
    def load(fn):
        return json.load(open(os.path.join(kb, "results", fn), encoding="utf-8"))
    a = load("analysis.json")
    v = load("guard_v31.json")
    cn = load("cloud_new.json")
    ln = load("local_new.json")
    en = load("local_en.json")
    big = load("local_big.json")
    math = load("math40.json")
    pool = load("combined_qwen2.json")
    x = load("xdomain.json")
    pr = load("powrep.json")
    lo = load("powrep_loose.json")
    r18 = load("r18_adjudication.json")
    # R18 arithmetic record on the adjudicated basis (b=24, c=0 -> 2/2^24);
    # completeness-only, no inferential license (nested construction).
    r18_p = 2.0 / 2 ** r18["adjudicated_flips"]
    assert r18["adjudicated_flips"] == 24
    assert r18_p == 1.1920928955078125e-07
    tests = {
        "pilot": a["subsets"]["pilot"]["mcnemar_p_two"],
        "holdout-main": a["subsets"]["holdout-main"]["mcnemar_p_two"],
        "cloud-new-guarded": v["strata"]["cloud-new"]["mcnemar_p_two"],
        "local-new": ln["mcnemar_p_two"],
        "local-en": en["mcnemar_p_two"],
        "local-big": big["mcnemar_p_two"],
        "math": math["mcnemar_p_two"],
        "prespecified-pool": pool["mcnemar_p_two"],
        "xdomain-tight": x["tight"]["mcnemar_p_two"],
        "xdomain-loose": x["loose"]["mcnemar_p_two"],
        "pow1_pilot": pr["pow1_pilot"]["mcnemar_p_two"],
        "pow1_holdout": pr["pow1_holdout"]["mcnemar_p_two"],
        "pow2_cloudnew": pr["pow2_cloudnew"]["mcnemar_p_two"],
        "powL_localnew": pr["powL_localnew"]["mcnemar_p_two"],
        "pow1L": lo["pow1L"]["mcnemar_p_two"],
        "pow2L": lo["pow2L"]["mcnemar_p_two"],
        "powLL": lo["powLL"]["mcnemar_p_two"],
        "r18-loose-rep": r18_p,
    }
    # hard-gate inputs (exact sealed values)
    assert tests["pilot"] == 0.0009765624999999999
    assert tests["prespecified-pool"] == 0.00390625
    assert tests["xdomain-loose"] == 1.9073486328125e-06
    assert tests["powL_localnew"] == 0.015625
    assert tests["cloud-new-guarded"] == 0.125
    assert cn["mcnemar_b"] == 5  # raw-basis cross-check, not in family
    m = len(tests)
    assert m == 18
    ordered = sorted(tests.items(), key=lambda kv: kv[1])
    alpha = 0.05
    survivors, stopped_at = [], None
    for k, (name, p) in enumerate(ordered, start=1):
        if p <= alpha / (m + 1 - k):
            survivors.append(name)
        else:
            stopped_at = {"step": k, "name": name, "p": p,
                          "threshold": alpha / (m + 1 - k)}
            break
    out = {"family": "18 analysis comparisons, guarded/adjudicated basis",
           "m": m, "alpha": alpha,
           "ordered": [{"name": n, "p_two": p} for n, p in ordered],
           "holm_survivors": survivors,
           "holm_stop": stopped_at,
           "note": "rollups excluded (re-views, not new comparisons); arithmetic records only, no inferential license under nesting; v1 (17 tests) preserved as results/holm_v1_17.json"}
    assert survivors == ["r18-loose-rep", "xdomain-loose", "pilot"], survivors
    assert stopped_at["name"] == "prespecified-pool"
    json.dump(out, open(os.path.join(kb, "results", "holm.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
