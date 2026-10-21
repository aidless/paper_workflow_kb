"""R18 final adjudication rollup: merge 4 judge passes, apply decision rule.

Decision rule (pre-committed here, disclosed in text):
- judge rejection on record (majority of clean reads incorrect) -> EXCLUDED
  from adjudicated guarded set (rows 42, 55).
- judge silence (ERROR x3, no rejection on record) -> author content ruling
  fills (row 46: echo format, same standard as judge-confirmed 47/51).
- 1-1 clean-read tie (row 54) -> author content ruling (contains gold,
  factually accurate), disclosed as tie-break.
- row 42 (牧 vs 牧之): substantive guard FP #2 (G06 class) under v3.2;
  under v3.3 (R22 promotion) the guard itself rejects it, so it drops out of
  the flip set (judge-rejection call retained below as content record only).
- row 55 (海瑞字汝贤): judge 0-3 reject vs author-correct ruling ->
  reported divergence (instrument inconsistency vs 47/51).

Writes results/r18_adjudication.json with per-flip calls + adjudicated
accuracy/ECE recomputed from raw confidences.

Usage: python3 paper_workflow_kb/scripts/r18_adjudicate.py paper_workflow_kb
"""
import json
import os
import re as _re
import sys

sys.path.insert(0, os.path.join("paper_workflow_kb", "scripts"))
from analyze_xdomain import ece_equal_width  # noqa: E402
from label_match_v3 import norm  # noqa: E402
from label_match_v33 import tolerant_match_v33 as guarded_match  # noqa: E402 (R22 promotion)


def verdicts(p1, p2, p2b, p2c):
    d1 = {r["trace_id"]: r["judge_verdict"] for r in p1}
    d2 = {r["trace_id"]: r["judge_verdict"] for r in p2}
    d2b = {r["trace_id"]: r["judge_verdict"] for r in p2b}
    d2c = {r["trace_id"]: r["judge_verdict"] for r in p2c}
    return d1, d2, d2b, d2c


def main(kb):
    ev = os.path.join(kb, "evidence")
    p1 = json.load(open(os.path.join(ev, "r18_judge.json"), encoding="utf-8"))
    p2 = json.load(open(os.path.join(ev, "r18_judge_pass2.json"), encoding="utf-8"))
    p2b = json.load(open(os.path.join(ev, "r18_judge_pass2b.json"), encoding="utf-8"))
    p2c = json.load(open(os.path.join(ev, "r18_judge_pass2c.json"), encoding="utf-8"))
    raw = json.load(open(os.path.join(ev, "r18_loose_rep60_raw.json"), encoding="utf-8"))
    res = json.load(open(os.path.join(kb, "results", "r18_loose_rep.json"),
                         encoding="utf-8"))
    d1, d2, d2b, d2c = verdicts(p1, p2, p2b, p2c)
    flips = {f["trace_id"] for f in res["loose_rep"]["flips"]}
    assert len(flips) == 26, len(flips)  # R22: lr18-42 no longer a flip under v3.3

    _LEAK = _re.compile(r"(0?\.\d+|1\.0+|1(?!\d))")

    calls, excluded = {}, []
    for r in p1:
        tid = r["trace_id"]
        reads = [d1[tid]]
        if tid in d2:
            reads.append(d2[tid])
        if tid in d2b:
            reads.append(d2b[tid])
        if tid in d2c:
            reads.append(d2c[tid])
        clean = [v for v in reads if v in ("correct", "incorrect")]
        n_c = clean.count("correct")
        n_i = clean.count("incorrect")
        leak1 = bool(_LEAK.search(r["predicted"] or ""))
        if (d1[tid] != "correct" and leak1 and d2.get(tid) == "correct"):
            call, note = "confirmed", "leak-artifact resolved (xdomain precedent)"
        elif n_i > n_c:
            call, note = "EXCLUDED", f"judge-rejected ({n_c}c/{n_i}i of {reads})"
            excluded.append(tid)
        elif n_c > n_i:
            call, note = "confirmed", f"judge {n_c}c/{n_i}i"
        else:
            if tid == "lr18-46":
                call, note = "confirmed-author", "judge-ERROR x3; author echo-standard (cf 47/51)"
            elif tid == "lr18-54":
                call, note = "confirmed-author", "clean tie 1-1; author tie-break (contains gold)"
            else:
                call, note = "EXCLUDED", f"tie unresolved {reads}"
                excluded.append(tid)
        calls[tid] = {"reads": reads, "call": call, "note": note}

    # Adjudicated accuracy/ECE: excluded flips revert to exact outcome.
    by_id = {r["trace_id"]: r for r in raw}
    n = len(raw)
    adj_correct, confs, accs = 0, [], []
    for r in raw:
        tid, pred, gold = r["trace_id"], r["predicted_label"], r["gold_answer"]
        exact_ok = norm(pred) == norm(gold)
        g_ok = bool(guarded_match(pred, gold))
        if tid in flips and tid in excluded:
            ok = exact_ok  # adjudicated: guard accept overturned
        elif tid in flips:
            ok = True
        else:
            ok = exact_ok
        adj_correct += ok
        confs.append(float(r["confidence"]))
        accs.append(1.0 if ok else 0.0)
    # equal-width 10-bin ECE (live-stratum convention, same function as layer())
    ece = ece_equal_width(confs, accs)

    # R22: excluded-final scoped to current flip set (lr18-42's judge-rejection
    # call stays in `calls` as content record, but there is no flip to exclude).
    excluded_final = sorted(t for t in excluded if t in flips)
    out = {"n": n, "raw_flips": len(flips), "excluded": excluded_final,
           "adjudicated_flips": len(flips) - len(excluded_final),
           "adjudicated_guarded_correct": adj_correct,
           "adjudicated_guarded_acc": round(adj_correct / n, 4),
           "adjudicated_ece_equalwidth": round(ece, 4),
           "calls": calls}
    json.dump(out, open(os.path.join(kb, "results", "r18_adjudication.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps({k: v for k, v in out.items() if k != "calls"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
