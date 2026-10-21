"""R18 adjudication pass 2b: single retry of 4 rows (2 judge ERRORs + 2
suspected judge-noise incorrects whose predictions fully contain gold).

34/46: original predicted strings (no leak present; judge output unparseable).
54/55: leak-stripped strings (same as pass 2 input; testing judge stability).
Writes evidence/r18_judge_pass2b.json; all passes stay on record.

Usage: python3 paper_workflow_kb/scripts/local_judge_r18_pass2b.py paper_workflow_kb
"""
import json
import os
import sys

sys.path.insert(0, os.path.join("paper_workflow_kb", "scripts"))
from local_judge_r18 import judge  # noqa: E402
from local_judge_r18_pass2 import strip_leak  # noqa: E402

RETRY = ["lr18-34", "lr18-46", "lr18-54", "lr18-55"]


def main(kb):
    rows = json.load(open(os.path.join(kb, "evidence", "r18_judge.json"),
                          encoding="utf-8"))
    by_id = {r["trace_id"]: r for r in rows}
    out = []
    for i, tid in enumerate(RETRY, 1):
        r = by_id[tid]
        pred = strip_leak(r["predicted"])
        try:
            v, _ = judge(r["question"], pred, r["gold"])
            err = None
        except Exception as e:
            v, err = "ERROR", str(e)
        out.append({"trace_id": tid, "question": r["question"],
                    "predicted_pass1": r["predicted"], "predicted_pass2b": pred,
                    "gold": r["gold"], "judge_verdict": v, "error": err})
        print(f"{i}/{len(RETRY)} {tid}: {pred!r}: {v}", flush=True)
    json.dump(out, open(os.path.join(kb, "evidence", "r18_judge_pass2b.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE evidence/r18_judge_pass2b.json")


if __name__ == "__main__":
    main(sys.argv[1])
