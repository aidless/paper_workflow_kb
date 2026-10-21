# -*- coding: utf-8 -*-
"""Fill r26 adjudication CSV verdict column (author draft pass).

verdict semantics (aligned with PREREG_R26_EXTERNAL):
  correct   -> prediction_answer is semantically equivalent to >=1 gold alias
               (flip pack: guard's accept was right / real recall;
                miss pack: guard wrongly rejected -> a miss)
  incorrect -> prediction_answer is NOT equivalent to any gold alias
               (flip pack: guard over-fire;
                miss pack: guard correctly rejected)
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]

V = {
    # ---- flip entity (guard accepted) ----
    "entity-P112-0": "correct", "entity-P131-0": "correct",
    "entity-P17-0": "correct", "entity-P170-0": "correct",
    "entity-P40-0": "correct", "entity-P131-1": "correct",
    "entity-P20-1": "correct", "entity-P106-2": "correct",
    "entity-P17-2": "correct", "entity-P176-2": "correct",
    "entity-P495-2": "correct", "entity-P159-3": "correct",
    "entity-P20-3": "correct", "entity-P276-3": "correct",
    "entity-P495-3": "correct", "entity-P131-4": "correct",
    "entity-P19-4": "correct", "entity-P276-4": "correct",
    "entity-P495-4": "correct", "entity-P69-4": "correct",
    "entity-P159-5": "correct", "entity-P19-5": "correct",
    "entity-P276-5": "incorrect", "entity-P40-5": "correct",
    "entity-P112-6": "correct", "entity-P175-6": "correct",
    "entity-P495-6": "correct", "entity-P127-7": "correct",
    "entity-P131-7": "correct", "entity-P176-7": "correct",
    "entity-P20-7": "correct", "entity-P159-8": "incorrect",
    # ---- miss entity (guard rejected) ----
    "entity-P740-5": "incorrect", "entity-P19-6": "incorrect",
    "entity-P800-4": "incorrect", "entity-P131-8": "incorrect",
    "entity-P136-0": "incorrect", "entity-P36-5": "incorrect",
    "entity-P36-0": "incorrect", "entity-P159-6": "incorrect",
    "entity-P112-2": "incorrect", "entity-P136-4": "incorrect",
    "entity-P69-6": "incorrect", "entity-P276-2": "incorrect",
    "entity-P36-3": "incorrect", "entity-P740-2": "incorrect",
    "entity-P127-4": "incorrect", "entity-P19-2": "incorrect",
    "entity-P112-1": "incorrect", "entity-P127-1": "incorrect",
    "entity-P106-5": "incorrect", "entity-P69-3": "incorrect",
    "entity-P40-4": "incorrect", "entity-P175-4": "incorrect",
    "entity-P131-5": "incorrect", "entity-P740-7": "incorrect",
    "entity-P50-4": "incorrect", "entity-P131-3": "incorrect",
    "entity-P69-2": "incorrect", "entity-P20-4": "incorrect",
    "entity-P20-0": "incorrect", "entity-P136-1": "incorrect",
    "entity-P740-1": "incorrect", "entity-P69-5": "incorrect",
    "entity-P170-7": "incorrect", "entity-P36-2": "incorrect",
    "entity-P276-1": "incorrect", "entity-P800-7": "incorrect",
    "entity-P175-7": "incorrect", "entity-P50-2": "incorrect",
    "entity-P50-1": "incorrect", "entity-P127-5": "incorrect",
    "entity-P276-7": "incorrect", "entity-P176-1": "incorrect",
    "entity-P264-2": "incorrect", "entity-P413-2": "incorrect",
    "entity-P159-1": "incorrect", "entity-P112-3": "incorrect",
    "entity-P800-3": "incorrect", "entity-P170-2": "incorrect",
    "entity-P407-0": "incorrect", "entity-P264-6": "incorrect",
    "entity-P170-6": "incorrect", "entity-P69-7": "incorrect",
    "entity-P495-1": "incorrect", "entity-P276-0": "incorrect",
    "entity-P50-0": "incorrect", "entity-P740-0": "incorrect",
    "entity-P50-3": "incorrect", "entity-P20-2": "incorrect",
    "entity-P176-4": "incorrect", "entity-P40-3": "incorrect",
    # ---- flip trivia (guard accepted) ----
    "trivia-qw_1587": "correct", "trivia-dpql_2929": "correct",
    "trivia-sfq_14501": "correct", "trivia-odql_14997": "correct",
    "trivia-qw_10361": "correct", "trivia-bb_596": "correct",
    "trivia-bb_1372": "correct", "trivia-jp_3910": "correct",
    "trivia-qg_4287": "correct", "trivia-qw_859": "correct",
    "trivia-sfq_14711": "correct", "trivia-sfq_9993": "correct",
    "trivia-qw_12159": "correct", "trivia-odql_8784": "incorrect",
    "trivia-qw_2309": "correct", "trivia-tb_1852": "correct",
    "trivia-bb_4415": "incorrect", "trivia-odql_13192": "correct",
    "trivia-odql_998": "correct", "trivia-sfq_17392": "correct",
    "trivia-qw_14570": "correct", "trivia-qw_10842": "correct",
    "trivia-sfq_10167": "correct", "trivia-qf_1667": "incorrect",
    "trivia-qw_7149": "correct", "trivia-dpql_3969": "correct",
    "trivia-dpql_1865": "correct", "trivia-qw_2792": "correct",
    # ---- miss trivia (guard rejected) ----
    "trivia-sfq_23449": "incorrect", "trivia-qw_12886": "incorrect",
    "trivia-odql_5141": "incorrect", "trivia-qb_5390": "incorrect",
    "trivia-sfq_15917": "incorrect", "trivia-bb_303": "incorrect",
    "trivia-bt_1181": "incorrect", "trivia-qg_4165": "incorrect",
    "trivia-odql_1420": "incorrect", "trivia-dpql_4760": "incorrect",
    "trivia-sfq_6554": "incorrect", "trivia-odql_12669": "incorrect",
    "trivia-qg_577": "incorrect", "trivia-bt_3601": "incorrect",
    "trivia-qb_2363": "incorrect", "trivia-qb_4220": "incorrect",
    "trivia-wh_2109": "incorrect", "trivia-dpql_3635": "incorrect",
    "trivia-odql_13565": "incorrect", "trivia-sfq_221": "incorrect",
    "trivia-sfq_13639": "incorrect", "trivia-qz_3440": "incorrect",
    "trivia-bt_3772": "incorrect", "trivia-sfq_328": "incorrect",
    "trivia-qw_9549": "incorrect", "trivia-qz_1952": "incorrect",
    "trivia-bt_4125": "incorrect", "trivia-qw_8802": "incorrect",
    "trivia-odql_2520": "incorrect", "trivia-sfq_5366": "incorrect",
    "trivia-sfq_8059": "incorrect", "trivia-jp_3064": "incorrect",
    "trivia-qb_6127": "correct", "trivia-sfq_1643": "incorrect",
    "trivia-sfq_3503": "incorrect", "trivia-sfq_6573": "incorrect",
    "trivia-qw_3191": "incorrect", "trivia-bb_6913": "incorrect",
    "trivia-qz_2135": "incorrect", "trivia-sfq_7632": "incorrect",
    "trivia-tc_1333": "incorrect", "trivia-wh_3542": "incorrect",
    "trivia-odql_2213": "incorrect", "trivia-qz_2176": "incorrect",
    "trivia-qw_14413": "incorrect", "trivia-bt_763": "incorrect",
    "trivia-qw_14568": "incorrect", "trivia-tb_1099": "correct",
    "trivia-jp_1823": "incorrect", "trivia-sfq_9261": "incorrect",
    "trivia-dpql_6084": "incorrect", "trivia-odql_904": "incorrect",
    "trivia-qz_2131": "incorrect", "trivia-odql_2768": "incorrect",
    "trivia-qg_581": "incorrect", "trivia-qw_12556": "incorrect",
    "trivia-odql_11103": "incorrect", "trivia-odql_10620": "incorrect",
    "trivia-odql_11908": "incorrect", "trivia-sfq_12896": "incorrect",
}

FILES = [
    "r26_flip_pack_entity.csv",
    "r26_miss_pack_entity.csv",
    "r26_flip_pack_trivia.csv",
    "r26_miss_pack_trivia.csv",
]

report = {}
for fn in FILES:
    p = HERE / fn
    rows = list(csv.reader(p.open("r", newline="", encoding="utf-8")))
    assert rows and rows[0][0] == "id", (fn, rows[0])
    n_correct = n_incorrect = 0
    for r in rows[1:]:
        rid = r[0]
        if not rid:
            continue
        if rid not in V:
            raise KeyError("missing verdict for %s in %s" % (rid, fn))
        r[-1] = V[rid]
        if V[rid] == "correct":
            n_correct += 1
        else:
            n_incorrect += 1
    with p.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    report[fn] = {"rows": len(rows) - 1, "correct": n_correct,
                  "incorrect": n_incorrect}

total_c = sum(x["correct"] for x in report.values())
total_i = sum(x["incorrect"] for x in report.values())
for k, v in report.items():
    print("%-30s rows=%2d correct=%2d incorrect=%2d" %
          (k, v["rows"], v["correct"], v["incorrect"]))
print("TOTAL rows=%d correct=%d incorrect=%d" %
      (total_c + total_i, total_c, total_i))