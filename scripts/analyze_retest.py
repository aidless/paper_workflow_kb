# -*- coding: utf-8 -*-
"""Test-retest stability: cloud-new (test) vs cloud-retest (retest), same 60 Qs.

Pairs by question string. Single recomputation script. Outputs
results/retest60.json:
- exact-label string agreement + exact-correct McNemar (test vs retest)
- guarded-label (tolerant_match) agreement + guarded-flip set stability
- confidence mean absolute drift
"""
import json
import sys
sys.path.insert(0, "paper_workflow_kb/scripts")
from label_match_v3 import norm, tolerant_match


def exact_match(a, g):
    a2, g2 = norm(a), norm(g)
    return bool(a2 and g2 and a2 == g2)


def mcnemar_p(b, c):
    # exact two-sided McNemar (binomial, p=0.5, n=b+c); duplicated from
    # analyze_new60 to avoid executing that module's top-level pipeline
    from math import comb
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(comb(n, i) for i in range(k + 1)) * (0.5 ** n) * 2
    return min(round(p, 10), 1.0)


def main():
    test = json.load(open("paper_workflow_kb/evidence/cloud_new60_raw.json",
                           encoding="utf-8"))
    retest = json.load(open("paper_workflow_kb/evidence/cloud_retest60_raw.json",
                            encoding="utf-8"))
    rq = {r["question"]: r for r in retest}
    assert len(test) == 60 and len(retest) == 60
    missing = [t["question"] for t in test if t["question"] not in rq]
    assert not missing, missing

    pairs = [(t, rq[t["question"]]) for t in test]
    for t, r in pairs:
        t["exact"] = exact_match(t["predicted_label"], t["gold_answer"])
        r["exact"] = exact_match(r["predicted_label"], r["gold_answer"])
        t["guarded"] = tolerant_match(t["predicted_label"], t["gold_answer"])
        r["guarded"] = tolerant_match(r["predicted_label"], r["gold_answer"])

    n = len(pairs)
    str_agree = sum(1 for t, r in pairs
                    if norm(t["predicted_label"]) == norm(r["predicted_label"]))
    b = sum(1 for t, r in pairs if t["exact"] and not r["exact"])
    c = sum(1 for t, r in pairs if (not t["exact"]) and r["exact"])
    gb = sum(1 for t, r in pairs if t["guarded"] and not r["guarded"])
    gc = sum(1 for t, r in pairs if (not t["guarded"]) and r["guarded"])
    g_agree = sum(1 for t, r in pairs if t["guarded"] == r["guarded"])
    t_flip = {t["question"] for t, r in pairs if t["exact"] != t["guarded"]}
    r_flip = {t["question"] for t, r in pairs if r["exact"] != r["guarded"]}
    conf_drift = sum(abs(t["confidence"] - rq[t["question"]]["confidence"])
                     for t, r in pairs) / n
    differing = [{"question": t["question"],
                  "test_pred": t["predicted_label"],
                  "retest_pred": r["predicted_label"],
                  "test_conf": t["confidence"],
                  "retest_conf": r["confidence"],
                  "test_exact": t["exact"], "retest_exact": r["exact"],
                  "test_guarded": t["guarded"],
                  "retest_guarded": r["guarded"]}
                 for t, r in pairs
                 if norm(t["predicted_label"]) != norm(r["predicted_label"])]

    out = {
        "n": n, "model": "qwen2.5:7b", "temperature": 0,
        "exact_string_agreement": round(str_agree / n, 4),
        "exact_correct_test": sum(1 for t, r in pairs if t["exact"]),
        "exact_correct_retest": sum(1 for t, r in pairs if r["exact"]),
        "mcnemar_b": b, "mcnemar_c": c, "mcnemar_p_two": mcnemar_p(b, c),
        "guarded_agreement": round(g_agree / n, 4),
        "guarded_mcnemar_b": gb, "guarded_mcnemar_c": gc,
        "guarded_mcnemar_p_two": mcnemar_p(gb, gc),
        "flip_set_test": sorted(t_flip), "flip_set_retest": sorted(r_flip),
        "n_flip_test": len(t_flip), "n_flip_retest": len(r_flip),
        "flip_set_overlap": len(t_flip & r_flip),
        "confidence_mean_abs_drift": round(conf_drift, 4),
        "n_differing_strings": len(differing),
        "differing": differing,
    }
    json.dump(out, open("paper_workflow_kb/results/retest60.json", "w",
                         encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print("WROTE results/retest60.json")


if __name__ == "__main__":
    main()
