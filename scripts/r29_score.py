# -*- coding: utf-8 -*-
"""R29 scoring + merge: local-big 160 (evidence/local_big_raw.json) + topup 560
(results/r29_answers_topup.jsonl) -> 720 rows. exact/guard/flip per row; merged McNemar.

Output: results/r29_score.json (merged rollup + flip rows for adjudication).
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v3 import norm  # noqa: E402
from label_match_v33 import tolerant_match_v33  # noqa: E402
from stats import exact_mcnemar  # noqa: E402

OUT = HERE / "results" / "r29_score.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def score_rows(rows, source):
    out = []
    for r in rows:
        pred, gold = r.get("predicted_label", ""), r.get("gold_answer", "")
        exact = norm(pred) == norm(gold)
        guard = tolerant_match_v33(pred, gold)
        out.append({
            "trace_id": r.get("trace_id", ""), "source": source,
            "predicted": pred, "gold": gold,
            "by": r.get("by", ""), "expr": r.get("expr", ""),
            "exact": bool(exact), "guard": bool(guard),
            "flip": (not exact) and guard,
            "error": r.get("error"),
        })
    return out


def rollup(rows):
    n = len(rows)
    n_exact = sum(1 for r in rows if r["exact"])
    n_guard = sum(1 for r in rows if r["guard"])
    flips = [r for r in rows if r["flip"]]
    b = len(flips)
    c = sum(1 for r in rows if r["exact"] and (not r["guard"]))
    p, _ = exact_mcnemar(b, c)
    return {
        "n": n, "n_exact": n_exact, "n_guard": n_guard,
        "n_flips": b, "flip_rate": (b / n if n else None),
        "mcnemar_b": b, "mcnemar_c": c, "mcnemar_p_two": p,
        "flip_rows": flips,
    }


def main():
    big = load_json(HERE / "evidence" / "local_big_raw.json")
    top = load_jsonl(HERE / "results" / "r29_answers_topup.jsonl")
    rows = score_rows(big, "local-big") + score_rows(top, "r29-topup")
    assert len(rows) == 720, len(rows)
    merged = rollup(rows)
    payload = {
        "n_total": len(rows),
        "local_big_n": len(big),
        "topup_n": len(top),
        "merged": {k: v for k, v in merged.items() if k != "flip_rows"},
        "flip_rows": merged["flip_rows"],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"merged n={payload['n_total']} flips={payload['merged']['n_flips']} "
          f"flip_rate={payload['merged']['flip_rate']} McNemar p={payload['merged']['mcnemar_p_two']}")
    for f in merged["flip_rows"]:
        print(f"  {f['trace_id']}: pred={f['predicted']!r} gold={f['gold']!r} by={f['by']}")


if __name__ == "__main__":
    main()