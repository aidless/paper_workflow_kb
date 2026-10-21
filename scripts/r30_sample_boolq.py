# -*- coding: utf-8 -*-
"""R30 BoolQ sampling (PREREG_R30_BOOLQ R2, FROZEN).

Stratified 50 True + 50 False from data_boolq/BoolQ/val.jsonl, seed 20260912.
Output: evidence/r30_boolq_sample.jsonl (id/question/passage/gold_bool/gold).
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SEED = 20260912
OUT = HERE / "evidence" / "r30_boolq_sample.jsonl"


def main():
    rows = [json.loads(l) for l in
            (HERE / "data_boolq" / "BoolQ" / "val.jsonl").read_text(
                encoding="utf-8").splitlines() if l.strip()]
    assert len(rows) == 3270, len(rows)
    trues = [r for r in rows if r["label"] is True]
    falses = [r for r in rows if r["label"] is False]
    assert len(trues) == 2033 and len(falses) == 1237
    rng = random.Random(SEED)
    rng.shuffle(trues)
    rng.shuffle(falses)
    picked = trues[:50] + falses[:50]
    assert len(picked) == 100
    out = [{"id": "boolq-%s" % r["idx"],
            "question": r["question"],
            "passage": r["passage"],
            "gold_bool": r["label"],
            "gold": "是" if r["label"] else "否"} for r in picked]
    assert sum(1 for r in out if r["gold"] == "是") == 50
    OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False)
                             for r in out) + "\n", encoding="utf-8")
    print("sampled=100 true=50 false=50 -> %s" % OUT.relative_to(HERE))


if __name__ == "__main__":
    main()