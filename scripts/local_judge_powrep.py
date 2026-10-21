"""Heterogeneous judge for the 10 powrep flips (local deepseek-r1:7b, temp 0).

Collection: cloud qwen2.5:7b (pow1/pow2) + local qwen2:7b (powL); judge is a
different family. Reads results/powrep.json flip lists, writes
evidence/powrep_judge.json. Same-line confidence leaks pre-stripped per the
xdomain lesson (rule recorded; raw values kept in the row).

Usage: python3 paper_workflow_kb/scripts/local_judge_powrep.py paper_workflow_kb
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from local_judge_xdomain import judge  # noqa

STRIP = re.compile(r"(?:(?<=\s)|(?<=。)|(?<=\.))0?\.\d+\s*$")
# NOTE (bug caught live, round 24): an earlier version stripped any trailing
# ".0", corrupting "40.0" -> "4". The fixed rule requires a separator
# (space/。/.) before the float, so integer decimals like "40.0"/"618.0"
# survive. powL-074 was judged on the corrupted form (incorrect) and is
# re-judged below on the true form; both records stay on file.


def main(kb):
    pr = json.load(open(os.path.join(kb, "results", "powrep.json"),
                        encoding="utf-8"))
    q = {}
    for fn in ["cloud_powrep255_raw.json", "local_powrep157_raw.json"]:
        for r in json.load(open(os.path.join(kb, "evidence", fn),
                                encoding="utf-8")):
            q[r["trace_id"]] = r["question"]
    flips = []
    for arm in ["pow1_pilot", "pow1_holdout", "pow2_cloudnew", "powL_localnew"]:
        for f in pr[arm]["flips"]:
            tid = f["trace_id"]
            flips.append({"trace_id": tid, "arm": arm,
                          "predicted_raw": f["predicted"],
                          "predicted": STRIP.sub("", f["predicted"]).strip(),
                          "gold": f["gold"], "question": q[tid]})
    assert len(flips) == 10, len(flips)
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
               "leak_rule": "strip trailing same-line confidence float before judging",
               "rows": rows},
              open(os.path.join(kb, "evidence", "powrep_judge.json"), "w",
                   encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE evidence/powrep_judge.json")


if __name__ == "__main__":
    main(sys.argv[1])
