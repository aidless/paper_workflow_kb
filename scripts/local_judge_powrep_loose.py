"""Heterogeneous judge for the 7 powrep-loose flips (local deepseek-r1:7b, temp 0).

Same protocol as local_judge_powrep (fixed separator-required STRIP rule).
Reads results/powrep_loose.json, writes evidence/powrep_loose_judge.json.

Usage: python3 paper_workflow_kb/scripts/local_judge_powrep_loose.py paper_workflow_kb
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from local_judge_xdomain import judge
from local_judge_powrep import STRIP


def main(kb):
    pr = json.load(open(os.path.join(kb, "results", "powrep_loose.json"),
                        encoding="utf-8"))
    q = {}
    for fn in ["cloud_powrep255_loose_raw.json", "local_powrep157_loose_raw.json"]:
        for r in json.load(open(os.path.join(kb, "evidence", fn),
                                encoding="utf-8")):
            q[r["trace_id"]] = r["question"]
    flips = []
    for arm in ["pow1L", "pow2L", "powLL"]:
        for f in pr[arm]["flips"]:
            tid = f["trace_id"]
            flips.append({"trace_id": tid, "arm": arm,
                          "predicted_raw": f["predicted"],
                          "predicted": STRIP.sub("", f["predicted"]).strip(),
                          "gold": f["gold"], "question": q[tid]})
    print(f"n_flips={len(flips)}", flush=True)
    rows = []
    for fl in flips:
        try:
            v, _ = judge(fl["question"], fl["predicted"], fl["gold"])
            err = None
        except Exception as e:
            v, err = "ERROR", str(e)
        rows.append({"trace_id": fl["trace_id"], "arm": fl["arm"],
                     "predicted": fl["predicted"], "gold": fl["gold"],
                     "judge_verdict": v, "error": err})
        print(f"{fl['trace_id']}: {fl['predicted']!r} vs {fl['gold']!r} -> {v}",
              flush=True)
    json.dump({"model": "deepseek-r1:7b", "temperature": 0, "n": len(rows),
               "n_correct": sum(1 for r in rows if r["judge_verdict"] == "correct"),
               "n_incorrect": sum(1 for r in rows if r["judge_verdict"] == "incorrect"),
               "leak_rule": "fixed separator-required STRIP (post powL-074 lesson)",
               "rows": rows},
              open(os.path.join(kb, "evidence", "powrep_loose_judge.json"), "w",
                   encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE evidence/powrep_loose_judge.json")


if __name__ == "__main__":
    main(sys.argv[1])
