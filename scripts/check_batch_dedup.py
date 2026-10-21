"""Batch dedup gate: exact-norm + hint-stripped core comparison vs prior set.

Usage: python3 paper_workflow_kb/scripts/check_batch_dedup.py
Returns exit 0 iff zero collisions (exact-norm and core) and internal dedup OK.
Prior set rebuilt from evidence each run (407 normalized cores at R19).
"""
import glob
import json
import re
import sys

sys.path.insert(0, "paper_workflow_kb/scripts")


def normq(s):
    s = str(s).strip().lower()
    return re.sub(r"[\s，。？?！!、；;：:\"「」『』（）()]+", "", s)


def core(s):
    s = str(s).strip()
    s = re.sub(r"只答.*?[。？?]$|答.*?[。？?]$|[？?]$", "", s)
    return normq(s)


def load_prior():
    qs = {}
    files = (glob.glob("paper_workflow_kb/evidence/*raw.json")
             + ["paper_workflow_kb/evidence/qa_pool_big.json",
                "paper_workflow_kb/evidence/qa_pool_en.json"])
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        rows = d if isinstance(d, list) else d.get("rows", [])
        for r in rows:
            if isinstance(r, dict):
                q = r.get("question", "")
                if q:
                    qs.setdefault(normq(q), (f, q))
                    qs.setdefault("core:" + core(q), (f, q))
    return qs


def check_batch(batch, name):
    from batch1_power_rep import BATCH1  # noqa
    prior = load_prior()
    fails = 0
    seen = set()
    for q, _ in batch:
        if normq(q) in prior:
            print(f"[{name}] EXACT-DUP: {q}");
            fails += 1
        if "core:" + core(q) in prior:
            print(f"[{name}] SEM-DUP: {q}");
            fails += 1
        if core(q) in seen:
            print(f"[{name}] INTERNAL-DUP: {q}");
            fails += 1
        seen.add(core(q))
    print(f"[{name}] n={len(batch)} collisions={fails}")
    return fails


def main():
    from batch1_power_rep import BATCH1
    fails = check_batch(BATCH1, "batch1")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
