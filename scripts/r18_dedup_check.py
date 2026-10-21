"""R18 dedup gate: R18_QA vs all prior questions (same caliber as check_batch_dedup).

Usage: python3 paper_workflow_kb/scripts/r18_dedup_check.py   (cwd = workspace root)
Exit 0 iff zero collisions (exact-norm + core) and internal dedup OK.
"""
import sys

sys.path.insert(0, "paper_workflow_kb/scripts")

from check_batch_dedup import load_prior, normq, core  # noqa: E402
from r18_loose_rep60 import R18_QA  # noqa: E402


def main():
    prior = load_prior()
    fails = 0
    seen = set()
    for q, _ in R18_QA:
        if normq(q) in prior:
            print(f"[r18] EXACT-DUP: {q}  <- {prior[normq(q)]}")
            fails += 1
        if "core:" + core(q) in prior:
            print(f"[r18] SEM-DUP: {q}  <- {prior['core:' + core(q)]}")
            fails += 1
        if core(q) in seen:
            print(f"[r18] INTERNAL-DUP: {q}")
            fails += 1
        seen.add(core(q))
    print(f"[r18] n={len(R18_QA)} collisions={fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
