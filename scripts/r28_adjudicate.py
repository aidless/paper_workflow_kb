# -*- coding: utf-8 -*-
"""R28 author adjudication (single author, small annotation budget; PREREG R4).

Verdicts:
  Arm A flip   -> "flip_correct" (guard correctly accepted a semantic-equal variant)
  Arm B miss candidates ->
      "miss"          (numerically/answer correct but guard rejected: variant exists & uncovered)
      "correct_reject"(model answered wrong, guard rejection is correct) -> NOT a miss

Key ruling for Arm A r28-a-08: "125.0" vs "125" — numeric .0 suffix, semantic-equal,
  guard's numeric branch (1e-6) accepts -> a true flip (exact-reject, guard-accept), zero over-fire.
Key ruling for Arm B r28-b-38: "6" vs "21" (die pips sum to 21) — model error, correct reject.

Output: results/r28_adjudication.json
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "results" / "r28_adjudication.json"

# Arm A flip rows (all of them; exactly one expected) -> flip_correct
A_FLIP_VERDICTS = {
    "r28-a-08": {"verdict": "flip_correct",
                 "note": "125.0 vs 125: numeric .0 suffix, semantic-equal, numeric branch accepts"},
}

# Arm B miss candidates (exact-reject & guard-reject), author semantic-equality ruling.
# miss = answer correct but guard rejected (variant present, uncovered by R).
# correct_reject = model answered wrong.
B_MISS_VERDICTS = {
    "r28-b-01": ("miss", "60 seconds = 60"),
    "r28-b-04": ("miss", "computation yields 1440 minutes = 1440"),
    "r28-b-05": ("miss", "86400 seconds = 86400"),
    "r28-b-06": ("miss", "24 hours = 24"),
    "r28-b-09": ("miss", "52 weeks = 52"),
    "r28-b-11": ("miss", "12 inches = 12"),
    "r28-b-12": ("miss", "3 feet = 3"),
    "r28-b-14": ("miss", "16 ounces = 16"),
    "r28-b-15": ("miss", "2000 pounds = 2000"),
    "r28-b-16": ("miss", "100 centimeters = 100"),
    "r28-b-17": ("miss", "1000 meters = 1000"),
    "r28-b-18": ("miss", "1000 grams = 1000"),
    "r28-b-19": ("miss", "1000 milliliters = 1000"),
    "r28-b-20": ("miss", "360 degrees = 360"),
    "r28-b-21": ("miss", "a triangle has 3 sides = 3"),
    "r28-b-24": ("miss", "8 planets = 8"),
    "r28-b-29": ("miss", "8 bits = 8"),
    "r28-b-30": ("miss", "88 keys = 88"),
    "r28-b-31": ("miss", "206 bones = 206"),
    "r28-b-34": ("miss", "100 years = 100"),
    "r28-b-37": ("miss", "1 billion has 9 zeros = 9"),
    "r28-b-38": ("correct_reject", "model said 6, die pips sum to 21: wrong answer"),
}


def main():
    payload = {
        "arm_a_flip_verdicts": A_FLIP_VERDICTS,
        "arm_b_miss_verdicts": {k: {"verdict": v[0], "note": v[1]}
                                for k, v in B_MISS_VERDICTS.items()},
        "arm_b_n_miss": sum(1 for v in B_MISS_VERDICTS.values() if v[0] == "miss"),
        "arm_b_n_correct_reject": sum(1 for v in B_MISS_VERDICTS.values() if v[0] == "correct_reject"),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()