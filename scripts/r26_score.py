"""R26 scoring (PREREG_R26_EXTERNAL R4, canonical recount).

For each answered row: exact vs guard-v3.3 vs guard-v3.4 against the gold
alias set (any-alias accept). Answer = first non-empty line of prediction
(local-new convention); confidence parsed from a trailing 0-1 float when
present (record only, no ECE here).

Outputs:
  results/r26_external.json      -- descriptive counts (exact/guarded/flips)
  r26_flip_pack_<split>.csv      -- flip rows for author adjudication
  r26_miss_pack_<split>.csv      -- guard-reject sample (60/split, seed+1) for
                                    author miss grading
Adjudicated verdicts land via a follow-up seal script (user-graded CSVs).
"""
import csv
import json
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


def score_split(split):
    sample = [json.loads(l) for l in
              (EV / ("r26_%s_sample.jsonl" % split)).read_text().splitlines()
              if l.strip()]
    answers = {}
    for l in (RES / ("r26_answers_%s.jsonl" % split)).read_text().splitlines():
        if l.strip():
            d = json.loads(l)
            answers[d["id"]] = d["prediction"]
    assert len(answers) == len(sample), (len(answers), len(sample))
    rows, flips, rejects = [], [], []
    for s in sample:
        pred_raw = answers[s["id"]]
        answer, conf = parse_prediction(pred_raw)
        na = norm(answer)
        exact = any(na == norm(a) for a in s["aliases"])
        g33 = any(tolerant_match_v33(answer, a) for a in s["aliases"])
        g34 = any(tolerant_match_v34(answer, a) for a in s["aliases"])
        row = {"id": s["id"], "question": s["question"],
               "aliases": s["aliases"], "prediction": pred_raw,
               "answer": answer, "confidence": conf,
               "exact": exact, "guard33": g33, "guard34": g34}
        rows.append(row)
        if not exact and g33:
            flips.append(row)
        if not g33:
            rejects.append(row)
    rng = random.Random(MISS_SEED)
    rng.shuffle(rejects)
    miss_sample = rejects[:MISS_N]
    for pack_rows, name in ((flips, "flip"), (miss_sample, "miss")):
        with (HERE / ("r26_%s_pack_%s.csv" % (name, split))).open(
                "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "question", "prediction_answer", "aliases",
                        "verdict"])
            for r in pack_rows:
                w.writerow([r["id"], r["question"], r["answer"],
                            " | ".join(r["aliases"]), ""])
    return {
        "n": len(rows),
        "n_exact": sum(r["exact"] for r in rows),
        "n_guard33": sum(r["guard33"] for r in rows),
        "n_guard34": sum(r["guard34"] for r in rows),
        "n_flips33": len(flips),
        "n_rejects33": len(rejects),
        "n_miss_sample": len(miss_sample),
    }


def main():
    RES.mkdir(exist_ok=True)
    out = {"rule33": "label_match_v33.tolerant_match_v33",
           "rule34": "label_match_v34.tolerant_match_v34 (candidate)",
           "splits": {}}
    for split in ("entity", "trivia"):
        try:
            out["splits"][split] = score_split(split)
            print(split, out["splits"][split], flush=True)
        except FileNotFoundError as e:
            print("skip %s: %s" % (split, e), flush=True)
    (RES / "r26_external.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1))
    print("wrote results/r26_external.json", flush=True)


if __name__ == "__main__":
    main()
