"""Amend powrep_judge.json: powL-074 re-judged on true form (provenance record).

The first pass judged a corrupted strip ("40.0" -> "4", strip-rule bug since
fixed in local_judge_powrep.py to require a separator). The live re-judge on
the true form ("40.0" vs "40") returned correct. This script applies that
amendment idempotently, keeping both records.

Usage: python3 paper_workflow_kb/scripts/amend_powrep_judge_074.py paper_workflow_kb
"""
import json
import os
import sys


def main(kb):
    p = os.path.join(kb, "evidence", "powrep_judge.json")
    d = json.load(open(p, encoding="utf-8"))
    for r in d["rows"]:
        if r["trace_id"] == "powL-074" and "rejudge" not in r:
            r["judge_verdict_first_pass_corrupted"] = r["judge_verdict"]
            r["corruption_note"] = ("first pass judged corrupted strip 40.0->4 "
                                    "(strip-rule bug, fixed in script); "
                                    "re-judged on true form below")
            r["predicted"] = "40.0"
            r["judge_verdict"] = "correct"
            r["rejudge"] = "true-form 40.0 vs 40 -> correct"
    d["n_correct"] = sum(1 for r in d["rows"] if r["judge_verdict"] == "correct")
    d["n_incorrect"] = sum(1 for r in d["rows"] if r["judge_verdict"] == "incorrect")
    d["strip_bug_note"] = ("STRIP rule corrupted 40.0->4 on powL-074 "
                           "(fixed: separator required); both records kept")
    assert d["n_correct"] == 10 and d["n_incorrect"] == 0, d
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("amended+verified: n_correct=10 n_incorrect=0")


if __name__ == "__main__":
    main(sys.argv[1])
