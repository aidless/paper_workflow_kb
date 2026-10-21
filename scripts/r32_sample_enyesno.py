# -*- coding: utf-8 -*-
"""R32 English yes/no arm sampling (PREREG_R32_ENYESNO R2, FROZEN).

New stratified 30 True + 30 False from data_boolq/BoolQ/val.jsonl, seed
20260932, `random.Random` class-internal shuffle, first 30 per class, and
DISJOINT from the R30 100-row sample (R2 requires "与 R30 样本不交叠").

Disjointness is enforced as a filter, not as a hope: R30 took
`trues[:50] + falses[:50]` under seed 20260912, so a fresh shuffle under
20260932 can land on the same rows. Rows already in R30 are skipped, and the
disjointness is asserted before anything is written.

Output: evidence/r32_enyesno_sample.jsonl
(id/question/passage/gold_bool/gold) with gold "Yes"/"No" (native mapping).
"""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SEED = 20260932
N_PER_CLASS = 30
OUT = HERE / "evidence" / "r32_enyesno_sample.jsonl"
R30_SAMPLE = HERE / "evidence" / "r30_boolq_sample.jsonl"


def main():
    rows = [json.loads(l) for l in
            (HERE / "data_boolq" / "BoolQ" / "val.jsonl").read_text(
                encoding="utf-8").splitlines() if l.strip()]
    assert len(rows) == 3270, len(rows)
    trues = [r for r in rows if r["label"] is True]
    falses = [r for r in rows if r["label"] is False]
    assert len(trues) == 2033 and len(falses) == 1237

    r30_ids = set()
    if R30_SAMPLE.exists():
        for l in R30_SAMPLE.read_text(encoding="utf-8").splitlines():
            if l.strip():
                r30_ids.add(json.loads(l)["id"])
    print("R30 rows excluded from the candidate pool: %d" % len(r30_ids))

    rng = random.Random(SEED)
    rng.shuffle(trues)
    rng.shuffle(falses)

    picked = []
    for pool in (trues, falses):
        take = [r for r in pool
                if ("boolq-%s" % r["idx"]) not in r30_ids][:N_PER_CLASS]
        assert len(take) == N_PER_CLASS, len(take)
        picked += take
    assert len(picked) == 60, len(picked)

    out = [{"id": "boolq-%s" % r["idx"], "question": r["question"],
            "passage": r["passage"], "gold_bool": r["label"],
            "gold": "Yes" if r["label"] else "No"} for r in picked]

    # frozen invariants
    ids = [r["id"] for r in out]
    assert len(set(ids)) == 60, "duplicate id"
    overlap = sorted(set(ids) & r30_ids)
    assert not overlap, "overlap with R30 sample: %s" % overlap
    assert sum(1 for r in out if r["gold"] == "Yes") == 30
    assert sum(1 for r in out if r["gold"] == "No") == 30
    assert set(r["gold"] for r in out) == {"Yes", "No"}

    OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False)
                             for r in out) + "\n", encoding="utf-8")
    print("sampled=60 true=30 false=30 overlap_with_R30=0 seed=%d -> %s"
          % (SEED, OUT.relative_to(HERE)))


if __name__ == "__main__":
    main()
