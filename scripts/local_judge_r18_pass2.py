"""R18 adjudication pass 2: re-judge the 10 non-correct pass-1 rows.

Protocol artifact handling (xdomain precedent): strip ONLY the trailing
confidence float (same-line leak like 是的。0.9); question-echo prefixes
(孟浩然字浩然, 昌龄字少伯) are kept intact -- what the model said is judged.
Both passes stay on record. Genuine content divergences (e.g. 牧 vs 牧之)
are reported as-is, not massaged.

Usage: python3 paper_workflow_kb/scripts/local_judge_r18_pass2.py paper_workflow_kb
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join("paper_workflow_kb", "scripts"))
from local_judge_r18 import judge  # noqa: E402

LEAK = re.compile(r"[。.]?\s*(0?\.\d+|1\.0+|1(?!\d))\s*$")


def strip_leak(s):
    return LEAK.sub("", s)


def main(kb):
    rows = json.load(open(os.path.join(kb, "evidence", "r18_judge.json"),
                          encoding="utf-8"))
    todo = [r for r in rows if r["judge_verdict"] != "correct"]
    print(f"pass2 rows: {len(todo)}")
    out = []
    for i, r in enumerate(todo, 1):
        pred2 = strip_leak(r["predicted"])
        try:
            v, _ = judge(r["question"], pred2, r["gold"])
            err = None
        except Exception as e:
            v, err = "ERROR", str(e)
        out.append({"trace_id": r["trace_id"], "question": r["question"],
                    "predicted_pass1": r["predicted"], "predicted_pass2": pred2,
                    "gold": r["gold"], "judge_verdict": v, "error": err})
        print(f"{i}/{len(todo)} {r['trace_id']}: {r['predicted']!r} -> "
              f"{pred2!r}: {v}", flush=True)
    json.dump(out, open(os.path.join(kb, "evidence", "r18_judge_pass2.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE evidence/r18_judge_pass2.json")


if __name__ == "__main__":
    main(sys.argv[1])
