# -*- coding: utf-8 -*-
"""R29 flip adjudication (single author; PREREG_R29 R5).

19 flips -> 14 flip_correct + 5 over_fire.
  flip_correct: guard correctly accepted a semantic-equal variant
    (.0 numeric suffix; city suffix 市/城/特区; trailing confidence digit).
  over_fire:    guard mis-accepted a WRONG numeric answer whose error falls
    within the 0.5% relative tolerance (division errors).

Output: results/r29_adjudication.json
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "results" / "r29_adjudication.json"

FLIP_CORRECT = {
    # local-big .0 suffixes
    "local-big-096": "23.0 vs 23: numeric .0 suffix",
    "local-big-097": "5.0 vs 5: numeric .0 suffix",
    "local-big-103": "1740.0 vs 1740: numeric .0 suffix",
    "local-big-110": "1200.0 vs 1200: numeric .0 suffix",
    # topup div .0 suffixes
    "r29-topup-383": "10.0 vs 10: numeric .0 suffix (680/68)",
    "r29-topup-390": "63.0 vs 63: numeric .0 suffix (5985/95)",
    "r29-topup-411": "80.0 vs 80: numeric .0 suffix (1440/18)",
    # topup hand city variants
    "r29-topup-453": "卢森堡市 = 卢森堡",
    "r29-topup-472": "马普托市 (+conf 0.9) = 马普托",
    "r29-topup-503": "洛美 (+conf 0.9) = 洛美",
    "r29-topup-520": "突尼斯城 = 突尼斯",
    "r29-topup-554": "利马 (+conf 0.9) = 利马",
    "r29-topup-555": "达喀尔 (+conf 0.9) = 达喀尔",
    "r29-topup-558": "华盛顿特区 = 华盛顿",
}

OVER_FIRE = {
    "r29-topup-387": "91.6458... vs 92: division error (8832/96=92), err 0.385% < 0.5% tolerance",
    "r29-topup-399": "64.9677... vs 65: division error (4030/62=65), err 0.05% < 0.5%",
    "r29-topup-403": "77.8211... vs 78: division error (5538/71=78), err 0.229% < 0.5%",
    "r29-topup-406": "75.9090... vs 76: division error (836/11=76), err 0.120% < 0.5%",
    "r29-topup-412": "35.1515... vs 35: division error (2310/66=35), err 0.433% < 0.5%",
}


def main():
    assert len(FLIP_CORRECT) + len(OVER_FIRE) == 19
    payload = {
        "n_flips": 19,
        "n_flip_correct": len(FLIP_CORRECT),
        "n_over_fire": len(OVER_FIRE),
        "flip_correct": FLIP_CORRECT,
        "over_fire": OVER_FIRE,
        "note": "over-fire class = division errors within the 0.5% numeric tolerance "
                "(new guard weakness surfaced by the arithmetic top-up)",
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()