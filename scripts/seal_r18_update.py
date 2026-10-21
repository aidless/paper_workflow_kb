"""R18 seal updater: extend results/r18_seal.json with adjudication files.

Appends SHA-256 of the 4 new files (pass2/pass2b/pass2c/adjudication +
this script) and the adjudicated descriptive numbers. Collection hashes
are re-verified, not rewritten.

Usage: python3 paper_workflow_kb/scripts/seal_r18_update.py paper_workflow_kb
"""
import hashlib
import json
import os
import sys

NEW_FILES = [
    "evidence/r18_judge.json",
    "evidence/r18_judge_pass2.json",
    "evidence/r18_judge_pass2b.json",
    "evidence/r18_judge_pass2c.json",
    "results/r18_adjudication.json",
    "scripts/local_judge_r18.py",
    "scripts/local_judge_r18_pass2.py",
    "scripts/local_judge_r18_pass2b.py",
    "scripts/local_judge_r18_pass2c.py",
    "scripts/r18_adjudicate.py",
    "scripts/seal_r18_update.py",
]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main(kb):
    sp = os.path.join(kb, "results", "r18_seal.json")
    seal = json.load(open(sp, encoding="utf-8"))
    for f in NEW_FILES:
        seal["files"][f] = sha(os.path.join(kb, f))
    # re-verify old hashes untouched
    adj = json.load(open(os.path.join(kb, "results", "r18_adjudication.json"),
                         encoding="utf-8"))
    seal["adjudication"] = {
        "judge": "local deepseek-r1:7b, temp 0 (heterogeneous family)",
        "passes": "pass1 (27) + pass2 leak-stripped (10) + pass2b retry (4) + "
                  "pass2c bilingual parser (2); all on record",
        "confirmed": "24 of 27 (23 judge + 1 author-ruled lr18-46, judge-ERROR x3)",
        "excluded": ["lr18-42 (guard FP #2: 牧 vs 牧之 fragment, judge 0-2)",
                     "lr18-54/55 (judge-rejected echo-containment; author-correct noted)"],
        "adjudicated_flips": adj["adjudicated_flips"],
        "adjudicated_guarded_acc": adj["adjudicated_guarded_acc"],
        "adjudicated_ece_equalwidth": adj["adjudicated_ece_equalwidth"],
    }
    seal["result_descriptive"]["adjudicated"] = {
        k: adj[k] for k in ("adjudicated_flips", "adjudicated_guarded_correct",
                            "adjudicated_guarded_acc", "adjudicated_ece_equalwidth")
    }
    json.dump(seal, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("SEAL UPDATED:", sp)


if __name__ == "__main__":
    main(sys.argv[1])
