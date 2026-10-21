# -*- coding: utf-8 -*-
"""Derive machine-checkable GOLD-25 pack meta (counts only, no verdicts).

Reads gold_grading_pack.csv (25 rows) + evidence/gold_key.json mapping kinds,
asserts design 14 stem + 11 stemless, writes results/gold_pack_meta.json.
No response/reference text or mapping is echoed to stdout.
"""
import csv
import json

rows = list(csv.DictReader(open("gold_grading_pack.csv", encoding="utf-8-sig")))
key = json.load(open("evidence/gold_key.json", encoding="utf-8"))
mapping = key["mapping"]
assert len(rows) == 25, len(rows)
assert {r["id"] for r in rows} == set(mapping)
kinds = [mapping[r["id"]]["kind"] for r in rows]
n_stem = sum(1 for k in kinds if k == "flip-stem")
n_nostem = sum(1 for k in kinds if k == "flip-nostem")
assert n_stem == 14, n_stem
assert n_nostem == 11, n_nostem
out = {"n": 25, "n_stem": n_stem, "n_nostem": n_nostem,
       "seed": key["seed"]}
json.dump(out, open("results/gold_pack_meta.json", "w", encoding="utf-8"),
          indent=2)
print(json.dumps(out))
print("WROTE results/gold_pack_meta.json")
