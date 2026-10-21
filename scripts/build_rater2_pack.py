"""R21-P3: build second-grader blind pack (30 items from GOLD-100).

Pre-specified, mechanical:
- Census of 7 flip-excluded rows (adjudication-critical) + seeded random
  23 of remaining 93 (random.Random(20260909).sample).
- Shuffled with seed 20260909, blind IDs S01..S30.
- Pack CSV contains ONLY: blind id, question, response, reference,
  empty 判定 column, 备注. NO H-id, kind, guarded outcome, or verdict leakage.
- Sealed mapping S-id -> H-id in evidence/rater2_key.json (never with pack).

Usage: python3 scripts/build_rater2_pack.py <kb>; writes
gold100_rater2_pack.csv + evidence/rater2_key.json (key file NOT for delivery).
"""
import csv
import json
import random
import sys

SEED = 20260909


def main(kb):
    key = json.load(open(f"{kb}/evidence/gold100_key.json", encoding="utf-8"))
    rows = list(csv.DictReader(open(f"{kb}/grades_gold100_user.csv", encoding="utf-8-sig")))
    assert len(rows) == 100, len(rows)
    by_id = {r["id"].strip(): r for r in rows}
    exc = [hid for hid, k in key["mapping"].items() if k["kind"] == "flip-excluded"]
    assert len(exc) == 7, exc
    rest = [r["id"].strip() for r in rows if r["id"].strip() not in exc]
    rnd = random.Random(SEED)
    chosen = exc + rnd.sample(rest, 23)
    assert len(set(chosen)) == 30
    rnd.shuffle(chosen)
    pack = []
    mapping = {}
    for i, hid in enumerate(chosen, 1):
        bid = f"S{i:02d}"
        r = by_id[hid]
        pack.append({"id": bid, "question": r["question"], "response": r["response"],
                     "reference": r["reference"], "你的判定(对/错)": "", "备注": ""})
        mapping[bid] = {"h_id": hid, "kind": key["mapping"][hid]["kind"]}
    with open(f"{kb}/gold100_rater2_pack.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "question", "response", "reference",
                                          "你的判定(对/错)", "备注"])
        w.writeheader()
        w.writerows(pack)
    json.dump({"seed": SEED, "n": 30, "mapping": mapping},
              open(f"{kb}/evidence/rater2_key.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    kinds = {}
    for m in mapping.values():
        kinds[m["kind"]] = kinds.get(m["kind"], 0) + 1
    print(f"WROTE gold100_rater2_pack.csv (30) + evidence/rater2_key.json; kinds={kinds}")


if __name__ == "__main__":
    main(sys.argv[1])
