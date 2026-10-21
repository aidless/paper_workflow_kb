"""R22-P1 (read-only): global v32-vs-v33 diff over ALL sealed raw pairs.

Collects (predicted, gold) pairs from every sealed raw evidence file using the
same accessors as the existing analysis scripts, computes v32/v33 outcomes,
and reports the diff set with mechanical characterization of each diff
(single-CJK-substring class or OTHER). Writes results/guard_v33_diff.json.
Touches NO sealed file, NO library module. Exit nonzero only on IO failure
(diff verdict left to human/round logic, never asserted here).
"""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v32 import tolerant_match_v32 as v32  # noqa: E402
from label_match_v31 import norm, _parse_cn_num  # noqa: E402
sys.path.insert(0, str(HERE / "scripts"))
import guard_v33_preexperiment as pre  # noqa: E402 (v33 logic under test)

v33 = pre.tolerant_match_v33

_CJK = re.compile(r"^[\u4e00-\u9fff]$")


def rows_of(doc):
    if isinstance(doc, list):
        return doc
    if isinstance(doc, dict):
        for k in ("rows", "calls", "verdicts"):
            if isinstance(doc.get(k), list):
                return doc[k]
    return []


def pred_of(r):
    for k in ("predicted_label", "predicted", "response", "model_answer"):
        if k in r and r[k] not in (None, ""):
            return str(r[k])
    return None


def gold_of(r):
    for k in ("gold_answer", "gold", "reference"):
        if k in r and r[k] not in (None, ""):
            return str(r[k])
    return None


RAW_FILES = [
    "evidence/d2_60.jsonl",  # jsonl special-cased below
    "evidence/cloud_new60_raw.json",
    "evidence/cloud_math40_raw.json",
    "evidence/cloud_pilot_code_raw.json",
    "evidence/cloud_powrep255_raw.json",
    "evidence/cloud_powrep255_loose_raw.json",
    "evidence/cloud_retest60_raw.json",
    "evidence/cloud_xdomain60_raw.json",
    "evidence/cloud_xdomain60_loose_raw.json",
    "evidence/local_big_raw.json",
    "evidence/local_en_raw.json",
    "evidence/local_new60_raw.json",
    "evidence/local_powrep157_raw.json",
    "evidence/local_powrep157_loose_raw.json",
    "evidence/r18_heteromodel60_raw.json",
    "evidence/r18_heteromodel_gemma60_raw.json",
    "evidence/r18_loose_rep60_raw.json",
    "evidence/qa_pool_big.json",
    "evidence/qa_pool_en.json",
]


def load_pairs():
    pairs = []  # (source, trace_id, predicted, gold)
    seen_files = []
    # d2_60.jsonl
    for line in (HERE / "evidence" / "d2_60.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            p, g = pred_of(r), gold_of(r)
            if p is not None and g is not None:
                pairs.append(("d2_60", r.get("trace_id", "?"), p, g))
    seen_files.append("evidence/d2_60.jsonl")
    for f in RAW_FILES[1:]:
        p = HERE / f
        if not p.exists():
            continue
        seen_files.append(f)
        doc = json.loads(p.read_text(encoding="utf-8"))
        for r in rows_of(doc):
            if not isinstance(r, dict):
                continue
            pr, g = pred_of(r), gold_of(r)
            if pr is not None and g is not None:
                pairs.append((f, str(r.get("trace_id", "?")), pr, g))
    # GOLD-100 grades CSV (responses vs references)
    grows = list(csv.DictReader(open(HERE / "grades_gold100_user.csv", encoding="utf-8-sig")))
    for r in grows:
        pairs.append(("gold100", r["id"].strip(), r["response"], r["reference"]))
    seen_files.append("grades_gold100_user.csv")
    return pairs, seen_files


def classify(a, g):
    a2, g2 = norm(a), norm(g)
    if not a2 or not g2:
        return "OTHER"
    if a2 != g2 and min(len(a2), len(g2)) == 1:
        single = a2 if len(a2) == 1 else g2
        if _CJK.match(single):
            return "single-CJK-substring"
    return "OTHER"


def main():
    pairs, files = load_pairs()
    diffs = []
    n32 = n33 = 0
    for src, tid, a, g in pairs:
        o32 = bool(v32(a, g))
        o33 = bool(v33(a, g))
        n32 += o32
        n33 += o33
        if o32 != o33:
            diffs.append({"source": src, "trace_id": tid, "predicted": a, "gold": g,
                          "v32": o32, "v33": o33, "class": classify(a, g)})
    others = [d for d in diffs if d["class"] != "single-CJK-substring"]
    out = {"n_pairs": len(pairs), "n_files": len(files), "files": sorted(files),
           "n_accept_v32": n32, "n_accept_v33": n33,
           "n_diffs": len(diffs), "n_other_class": len(others), "diffs": diffs,
           "verdict": ("PROMOTE-GO" if not others else "PROMOTE-HOLD")}
    (HERE / "results" / "guard_v33_diff.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"pairs={len(pairs)} files={len(files)} diffs={len(diffs)} "
          f"other={len(others)} verdict={out['verdict']}")
    for d in diffs:
        print(f"  {d['source']} {d['trace_id']} [{d['class']}] {d['predicted']!r} vs {d['gold']!r}")


if __name__ == "__main__":
    main()
