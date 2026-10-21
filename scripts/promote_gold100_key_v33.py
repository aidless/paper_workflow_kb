"""R22-P2b: promote GOLD-100 key guarded outcomes v32 -> v33 (surgical, audited).

For all 100 key rows recompute guarded outcomes with v32 (current sealed lib)
and v33 (promoted lib); assert the diff set is EXACTLY {H62,H68,H71,H82}
(1->0, single-CJK-substring class). Update those 4 rows, append audit note.
All other rows byte-identical. Writes evidence/gold100_key.json.
Exit nonzero on any unexpected diff (promotion aborts).
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v32 import tolerant_match_v32 as g32  # noqa: E402
from label_match_v33 import tolerant_match_v33 as g33  # noqa: E402

EXPECT_DIFF = {"H62", "H68", "H71", "H82"}


def main():
    kp = HERE / "evidence" / "gold100_key.json"
    key = json.loads(kp.read_text(encoding="utf-8"))
    grows = {r["id"].strip(): r for r in
             csv.DictReader(open(HERE / "grades_gold100_user.csv", encoding="utf-8-sig"))}
    assert len(grows) == 100
    diffs = {}
    for hid, k in key["mapping"].items():
        r = grows[hid]
        o32 = int(g32(r["response"], r["reference"]))
        o33 = int(g33(r["response"], r["reference"]))
        assert o32 == k["guarded_outcome"], (hid, o32, k["guarded_outcome"])
        if o32 != o33:
            diffs[hid] = (o32, o33)
    assert set(diffs) == EXPECT_DIFF, diffs
    assert all(v == (1, 0) for v in diffs.values()), diffs
    for hid in EXPECT_DIFF:
        key["mapping"][hid]["guarded_outcome"] = 0
    key["note"] = ("guarded outcomes sealed for decode; grader sees no outcomes. "
                   "R22 v33 promotion: H62/H68/H71/H82 guarded_outcome 1->0 "
                   "(single-CJK-substring guard); other 96 rows recomputed identical "
                   "under v32 and v33.")
    kp.write_text(json.dumps(key, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PROMOTED key rows: {sorted(diffs)}; other 96 identical")


if __name__ == "__main__":
    main()
