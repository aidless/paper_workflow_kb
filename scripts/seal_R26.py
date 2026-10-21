# -*- coding: utf-8 -*-
"""R26 seal — the unique recount producing final C69/C70/C71 numbers.

Reads the author-adjudicated verdict CSVs (r26_{flip,miss}_pack_{entity,trivia}.csv)
and recomputes, from the sealed sample + answers:
  * exact / guard-v3.3 / guard-v3.4 acceptance over the full 200-row splits
  * miss rate (guard rejects sampled-with-wrong-verdict=correct) + Wilson 95% CI
  * over-fire (guard-accept flips adjudicated = incorrect)
  * the v3.4 increment (v3.3 reject + v3.4 accept) and its miss-drop /
    over-fire-increase decomposition, then applies the frozen adoption bar.

Pre-reg invariants (PREREG_R26_EXTERNAL R4/R5) enforced by assert:
  A1  flip CSV id set == scored flip (exact-reject + v3.3-accept) id set
  A2  miss CSV id set == seeded 60-row guard-reject sample id set
  A3  every v3.4-increment row is inside the miss sample (so its verdict exists)
  A4  r26_external.json counts match this recount exactly.
"""
import csv
import json
import math
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v31 import norm  # noqa: E402
from label_match_v33 import tolerant_match_v33  # noqa: E402
from label_match_v34 import tolerant_match_v34  # noqa: E402

EV = HERE / "evidence"
RES = HERE / "results"
MISS_SEED = 20260909
MISS_N = 60
CONF_RE = re.compile(r"^\s*(0(\.\d+)?|1(\.0+)?|0?\.\d+)\s*$")
Z95 = 1.959963984540054  # z* for a two-sided 95% interval


def parse_prediction(resp):
    lines = [l.strip() for l in str(resp).splitlines() if l.strip()]
    answer = lines[0] if lines else ""
    conf = None
    for l in lines[1:]:
        if CONF_RE.match(l):
            try:
                conf = min(max(float(l), 0.0), 1.0)
            except ValueError:
                pass
    return answer, conf


def wilson95(x, n):
    if n <= 0:
        return (0.0, 0.0)
    p = x / n
    z = Z95
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def load_verdicts():
    V = {}
    files = [
        "r26_flip_pack_entity.csv", "r26_miss_pack_entity.csv",
        "r26_flip_pack_trivia.csv", "r26_miss_pack_trivia.csv",
    ]
    for fn in files:
        rdr = csv.reader((HERE / fn).open("r", newline="", encoding="utf-8"))
        header = next(rdr)
        assert header[0] == "id" and header[-1] == "verdict", (fn, header)
        for r in rdr:
            if not r or not r[0]:
                continue
            V[r[0]] = r[-1]
    return V


def score_split(split, V):
    sample = [json.loads(l) for l in
              (EV / ("r26_%s_sample.jsonl" % split)).read_text(
                  encoding="utf-8").splitlines() if l.strip()]
    answers = {}
    for l in (RES / ("r26_answers_%s.jsonl" % split)).read_text(
            encoding="utf-8").splitlines():
        if l.strip():
            d = json.loads(l)
            answers[d["id"]] = d["prediction"]
    assert len(answers) == len(sample), (split, len(answers), len(sample))

    rows, flips, rejects = [], [], []
    for s in sample:
        answer, conf = parse_prediction(answers[s["id"]])
        exact = any(norm(answer) == norm(a) for a in s["aliases"])
        g33 = any(tolerant_match_v33(answer, a) for a in s["aliases"])
        g34 = any(tolerant_match_v34(answer, a) for a in s["aliases"])
        row = {"id": s["id"], "exact": exact, "guard33": g33, "guard34": g34}
        rows.append(row)
        if not exact and g33:
            flips.append(row)
        if not g33:
            rejects.append(row)

    rng = random.Random(MISS_SEED)
    rng.shuffle(rejects)
    miss_sample = rejects[:MISS_N]

    flip_ids = [r["id"] for r in flips]
    miss_ids = [r["id"] for r in miss_sample]
    incr = [r for r in rows if not r["guard33"] and r["guard34"]]
    incr_ids = [r["id"] for r in incr]

    # ---- cross-check vs adjudicated CSV id sets ----
    csv_flip = [r[0] for r in csv.reader(
        (HERE / ("r26_flip_pack_%s.csv" % split)).open(
            "r", newline="", encoding="utf-8"))][1:]
    csv_flip = [i for i in csv_flip if i]
    csv_miss = [r[0] for r in csv.reader(
        (HERE / ("r26_miss_pack_%s.csv" % split)).open(
            "r", newline="", encoding="utf-8"))][1:]
    csv_miss = [i for i in csv_miss if i]

    assert set(csv_flip) == set(flip_ids), \
        (split, "flip id mismatch", len(csv_flip), len(flip_ids),
         set(csv_flip) ^ set(flip_ids))
    assert set(csv_miss) == set(miss_ids), \
        (split, "miss id mismatch", len(csv_miss), len(miss_ids),
         set(csv_miss) ^ set(miss_ids))
    assert len(csv_miss) == MISS_N, (split, len(csv_miss))
    # every v3.4-increment row must be inside the miss sample to have a verdict
    assert set(incr_ids) <= set(miss_ids), \
        (split, "v3.4 increment row outside miss sample",
         set(incr_ids) - set(miss_ids))

    # ---- adjudicated counts ----
    miss = sum(1 for r in miss_sample if V[r["id"]] == "correct")
    over_fire = sum(1 for r in flips if V[r["id"]] == "incorrect")
    incr_miss_drop = sum(1 for r in incr if V[r["id"]] == "correct")
    incr_overfire = sum(1 for r in incr if V[r["id"]] == "incorrect")

    lo, hi = wilson95(miss, MISS_N)
    return {
        "n": len(rows),
        "n_exact": sum(r["exact"] for r in rows),
        "n_guard33": sum(r["guard33"] for r in rows),
        "n_guard34": sum(r["guard34"] for r in rows),
        "n_flips33": len(flips),
        "n_rejects33": len(rejects),
        "n_miss_sample": MISS_N,
        "miss": miss,
        "miss_rate": miss / MISS_N,
        "miss_wilson95": [round(lo, 4), round(hi, 4)],
        "over_fire": over_fire,
        "v34_increment": len(incr),
        "v34_miss_drop": incr_miss_drop,
        "v34_overfire_increase": incr_overfire,
    }


def main():
    V = load_verdicts()
    external = json.loads((RES / "r26_external.json").read_text(encoding="utf-8"))
    out = {
        "rule33": "label_match_v33.tolerant_match_v33",
        "rule34": "label_match_v34.tolerant_match_v34 (candidate)",
        "adoption_bar": {"miss_drop_required": 5,
                         "overfire_increase_allowed": 2},
        "wilson_z95": Z95,
        "splits": {},
    }
    for split in ("entity", "trivia"):
        res = score_split(split, V)
        out["splits"][split] = res
        # A4: recount must match the earlier descriptive result file exactly
        exp = external["splits"][split]
        for k in ("n", "n_exact", "n_guard33", "n_guard34",
                  "n_flips33", "n_rejects33", "n_miss_sample"):
            assert res[k] == exp[k], (split, k, res[k], exp[k])
        # v3.4 recount gap must equal the miss-drop + over-fire-increase sum
        assert res["n_guard34"] - res["n_guard33"] == res["v34_increment"], split

    miss_drop = out["splits"]["entity"]["v34_miss_drop"] + \
        out["splits"]["trivia"]["v34_miss_drop"]
    overfire_increase = out["splits"]["entity"]["v34_overfire_increase"] + \
        out["splits"]["trivia"]["v34_overfire_increase"]
    adopt = miss_drop >= 5 and overfire_increase <= 2
    out["combined"] = {
        "miss_drop": miss_drop,
        "overfire_increase": overfire_increase,
        "adopt_v34": adopt,
        "verdict": ("adopt" if adopt else
                    "negative: miss drop %d < 5, v3.4 not cut, "
                    "v3.3 remains baseline" % miss_drop),
        "total_over_fire": out["splits"]["entity"]["over_fire"] +
                            out["splits"]["trivia"]["over_fire"],
    }
    (RES / "r26_seal.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1))
    for split in ("entity", "trivia"):
        r = out["splits"][split]
        print("%-8s n=%d exact=%d g33=%d g34=%d flips=%d reject=%d "
              "miss=%d/%d wilson=%s overfire=%d v34incr=%d "
              "(drop=%d overfire=%d)" %
              (split, r["n"], r["n_exact"], r["n_guard33"], r["n_guard34"],
               r["n_flips33"], r["n_rejects33"], r["miss"], r["n_miss_sample"],
               r["miss_wilson95"], r["over_fire"], r["v34_increment"],
               r["v34_miss_drop"], r["v34_overfire_increase"]), flush=True)
    print("combined: miss_drop=%d overfire_increase=%d adopt=%s verdict=%s "
          "total_over_fire=%d" %
          (miss_drop, overfire_increase, adopt, out["combined"]["verdict"],
           out["combined"]["total_over_fire"]), flush=True)
    print("wrote results/r26_seal.json", flush=True)


if __name__ == "__main__":
    main()