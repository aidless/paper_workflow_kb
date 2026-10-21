# -*- coding: utf-8 -*-
"""R28 scoring: exact vs guard v3.3 per answered row; flip flags; arm rollups.

exact  = norm(pred) == norm(gold)   (vendored normalizer + normalized equality)
guard  = tolerant_match_v33(pred, gold)
flip   = (not exact) and guard       (exact-reject, guard-accept)
miss_candidate (arm B) = (not exact) and (not guard)  -> adjudicate for semantic equality

Output: results/r28_score.json  (per-arm rollup + per-row flags + arm-B miss candidates)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v3 import norm  # noqa: E402
from label_match_v33 import tolerant_match_v33  # noqa: E402

OUT = HERE / "results" / "r28_score.json"


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
        flip = (not exact) and guard
        out.append({
            "trace_id": r["trace_id"], "source": source,
            "question": r["question"], "predicted": pred, "gold": gold,
            "exact": bool(exact), "guard": bool(guard), "flip": bool(flip),
            "error": r.get("error"),
        })
    return out


def rollup(rows):
    n = len(rows)
    n_err = sum(1 for r in rows if r.get("error"))
    n_exact = sum(1 for r in rows if r["exact"])
    n_guard = sum(1 for r in rows if r["guard"])
    n_flip = sum(1 for r in rows if r["flip"])
    return {
        "n": n, "n_error": n_err, "n_exact": n_exact, "n_guard": n_guard,
        "n_flips": n_flip, "flip_rate": (n_flip / n if n else None),
    }


def main():
    a = score_rows(load_jsonl(HERE / "results" / "r28_answers_a.jsonl"), "r28-a")
    b = score_rows(load_jsonl(HERE / "results" / "r28_answers_b.jsonl"), "r28-b")
    b_miss_candidates = [r for r in b if (not r["exact"]) and (not r["guard"])]
    payload = {
        "arms": {
            "degenerate_a": {"rows": a, **rollup(a)},
            "uncovered_b": {"rows": b, **rollup(b)},
        },
        "b_miss_candidates": b_miss_candidates,
        "n_miss_candidates_b": len(b_miss_candidates),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"a: {rollup(a)}")
    print(f"b: {rollup(b)}")
    print(f"b miss candidates (exact-reject & guard-reject): {len(b_miss_candidates)}")
    for c in b_miss_candidates:
        print(f"  {c['trace_id']}: pred={c['predicted']!r} gold={c['gold']!r}")


if __name__ == "__main__":
    main()