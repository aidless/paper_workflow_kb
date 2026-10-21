"""Seal xdomain adjudication counts (deterministic transform, no model calls).

Reads evidence/xdomain_judge.json (pass 1, 21 rows) and
evidence/xdomain_judge_pass2.json (pass 2, 5 rows), writes
results/xdomain_adjudication.json with machine-checkable counts.

Usage: python3 paper_workflow_kb/scripts/seal_xdomain_adjudication.py paper_workflow_kb
"""
import json
import os
import sys


def main(kb):
    p1 = json.load(open(os.path.join(kb, "evidence", "xdomain_judge.json"),
                        encoding="utf-8"))
    p2 = json.load(open(os.path.join(kb, "evidence", "xdomain_judge_pass2.json"),
                        encoding="utf-8"))
    assert p1["n"] == 21 and len(p1["rows"]) == 21
    assert len(p2["rows"]) == 5
    assert {r["trace_id"] for r in p2["rows"]} == {
        r["trace_id"] for r in p1["rows"] if r["judge_verdict"] != "correct"}, \
        "pass 2 must cover exactly the pass-1 non-correct rows"
    out = {"n": 21,
           "pass1_correct": sum(1 for r in p1["rows"]
                                if r["judge_verdict"] == "correct"),
           "pass1_incorrect": sum(1 for r in p1["rows"]
                                  if r["judge_verdict"] == "incorrect"),
           "pass1_error": sum(1 for r in p1["rows"]
                              if r["judge_verdict"] == "ERROR"),
           "pass2_n": len(p2["rows"]),
           "pass2_correct": sum(1 for r in p2["rows"]
                                if r["second_pass"] == "correct"),
           "content_correct": 21,
           "rule": "pass-1 incorrects were same-line confidence leaks; "
                   "pass 2 strips the trailing float and re-judges; "
                   "content basis = pass-1 corrects + pass-2 corrects"}
    assert out["pass1_correct"] == 16, out
    assert out["pass1_incorrect"] == 3, out
    assert out["pass1_error"] == 2, out
    assert out["pass2_correct"] == 5, out
    assert out["content_correct"] == out["pass1_correct"] + out["pass2_correct"]
    json.dump(out, open(os.path.join(kb, "results", "xdomain_adjudication.json"),
                        "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
