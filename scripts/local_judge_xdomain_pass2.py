"""Second-pass judge for 5 xdomain items (confidence-leak stripped).

First pass (evidence/xdomain_judge.json): 16 correct / 3 incorrect / 2 ERROR.
The 3 incorrects all carry a same-line confidence leak (e.g. "不是。0.9");
the 2 ERRORs are timeouts. This pass strips a trailing confidence float
(protocol artifact: the analysis parser already takes answer-first-line, so a
same-line leak is parser noise, not model content) and re-judges with the same
judge (local deepseek-r1:7b, temp 0). Both passes are reported; the stripped
pass governs the guarded-basis adjudication, the raw pass stays on record.

Usage: python3 paper_workflow_kb/scripts/local_judge_xdomain_pass2.py paper_workflow_kb
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from local_judge_xdomain import judge

STRIP = re.compile(r"[\s。.]*0?\.\d+\s*$")

RETRY = ["xloose-21", "xloose-25", "xloose-29", "xloose-31", "xloose-33"]


def main(kb):
    first = json.load(open(os.path.join(kb, "evidence", "xdomain_judge.json"),
                           encoding="utf-8"))
    by_id = {r["trace_id"]: r for r in first["rows"]}
    q = {}
    for fn in ["cloud_xdomain60_raw.json", "cloud_xdomain60_loose_raw.json"]:
        for r in json.load(open(os.path.join(kb, "evidence", fn), encoding="utf-8")):
            q[r["trace_id"]] = r["question"]
    rows = []
    for tid in RETRY:
        f = by_id[tid]
        stripped = STRIP.sub("", f["predicted"]).strip()
        try:
            v, _ = judge(q[tid], stripped, f["gold"])
            err = None
        except Exception as e:
            v, err = "ERROR", str(e)
        rows.append({"trace_id": tid, "layer": f["layer"],
                     "predicted_raw": f["predicted"],
                     "predicted_stripped": stripped, "gold": f["gold"],
                     "first_pass": f["judge_verdict"],
                     "second_pass": v, "error": err})
        print(f"{tid}: raw={f['predicted']!r} stripped={stripped!r} "
              f"first={f['judge_verdict']} second={v}", flush=True)
    json.dump({"model": first["model"], "temperature": 0,
               "rule": "strip trailing same-line confidence float, re-judge",
               "rows": rows},
              open(os.path.join(kb, "evidence", "xdomain_judge_pass2.json"), "w",
                   encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE evidence/xdomain_judge_pass2.json")


if __name__ == "__main__":
    main(sys.argv[1])
