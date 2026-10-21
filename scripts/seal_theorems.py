# -*- coding: utf-8 -*-
"""Seal for the two measurement-error theorems (P5, R31).

Theorem 1 (rule-addition monotonicity): pure disjunct addition R -> R'
  implies Accept(R) ⊆ Accept(R'), Flip(R) ⊆ Flip(R'), Miss(R') ⊆ Miss(R).
  Corroborated by recomputation (not copy): v3.3 -> v3.4 is a pure fallback
  addition (scripts/label_match_v34.py: v33 accept OR token-containment),
  checked on all 400 sealed R26 rows (same alias-set scoring as seal_R26).
  Guard-scope disclosure: v3.1 -> v3.3 added acceptance-*blocking* guards,
  so monotonicity does not apply there by construction; verified instead:
  exactly 8/1700 pairs flip v32-accept -> v33-reject, all single-CJK class.

Theorem 2 (numeric-tolerance over-fire boundary): any wrong numeric
  prediction with |a-g| < 1e-6 or |a-g|/max(|g|,1) < 0.005 is accepted by
  the numeric branch (label_match_v33.py lines 86-91), hence over-fire
  whenever exact rejects. Corroborated: all 5 sealed R29 over-fire rows
  recompute accept=True with relative errors strictly inside (0, 0.005).

Output: results/theorems.json
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))

from label_match_v3 import norm, SUFFIXES, SYNONYMS  # noqa: E402
from label_match_v33 import tolerant_match_v33  # noqa: E402
from label_match_v34 import tolerant_match_v34  # noqa: E402

EV = HERE / "evidence"
RES = HERE / "results"
OUT = RES / "theorems.json"

_CJK = re.compile(r"^[\u4e00-\u9fff]+$")


def parse_first_line(resp):
    lines = [l.strip() for l in str(resp).splitlines() if l.strip()]
    return lines[0] if lines else ""


def main():
    # ---- structural premises (from sealed code) ----
    suffixes_cjk_only = all(bool(_CJK.fullmatch(s)) for s in SUFFIXES)
    assert suffixes_cjk_only, SUFFIXES
    assert SYNONYMS == {"不会": "否", "不是": "否", "会": "是",
                        "yes": "是", "no": "否"}, SYNONYMS

    # ---- behavioral probes (document branch boundaries) ----
    probes = {
        "dot_zero_accept": tolerant_match_v33("125.0", "125"),      # True
        "en_unit_reject": tolerant_match_v33("60 seconds", "60"),   # False
        "en_yes_accept": tolerant_match_v33("yes", "是"),           # True
        "true_uncovered": tolerant_match_v33("True", "是"),         # False
        "div_err_accept": tolerant_match_v33("91.64583333333333", "92"),  # True
    }
    assert probes["dot_zero_accept"] is True
    assert probes["en_unit_reject"] is False
    assert probes["en_yes_accept"] is True
    assert probes["true_uncovered"] is False
    assert probes["div_err_accept"] is True

    # ---- Theorem 1: v33 -> v34 inclusion on all 400 sealed R26 rows ----
    n_rows = 0
    n_incr = 0
    incr_ids = []
    for split in ("trivia", "entity"):
        sample = [json.loads(l) for l in
                  (EV / ("r26_%s_sample.jsonl" % split)).read_text(
                      encoding="utf-8").splitlines() if l.strip()]
        answers = {}
        for l in (RES / ("r26_answers_%s.jsonl" % split)).read_text(
                encoding="utf-8").splitlines():
            if l.strip():
                d = json.loads(l)
                answers[d["id"]] = parse_first_line(d["prediction"])
        assert len(answers) == len(sample) == 200, (split, len(answers))
        for s in sample:
            a = answers[s["id"]]
            g33 = any(tolerant_match_v33(a, al) for al in s["aliases"])
            g34 = any(tolerant_match_v34(a, al) for al in s["aliases"])
            assert (not g33) or g34, ("inclusion violated", s["id"])
            n_rows += 1
            if (not g33) and g34:
                n_incr += 1
                incr_ids.append(s["id"])
    assert n_rows == 400, n_rows
    assert n_incr == 2, (n_incr, incr_ids)  # matches C71 (trivia 2 + entity 0)

    # ---- guard-shrinkage scope check (v3.2 -> v3.3 NOT monotone) ----
    diff = json.loads((RES / "guard_v33_diff.json").read_text(encoding="utf-8"))
    assert diff["n_pairs"] == 1700, diff["n_pairs"]
    assert diff["n_diffs"] == 8, diff["n_diffs"]
    assert all(r.get("v32") is True and r.get("v33") is False
               for r in diff["diffs"]), "all 8 diffs must be accept->reject"
    assert all(r.get("class") == "single-CJK-substring"
               for r in diff["diffs"])

    # ---- Theorem 2: all 5 sealed R29 over-fires inside (0, 0.005) ----
    adj = json.loads((RES / "r29_adjudication.json").read_text(encoding="utf-8"))
    score = json.loads((RES / "r29_score.json").read_text(encoding="utf-8"))
    by_id = {r["trace_id"]: r for r in score["flip_rows"]}
    over_ids = sorted(adj["over_fire"].keys())
    assert len(over_ids) == 5, over_ids
    rel_errs = {}
    for tid in over_ids:
        r = by_id[tid]
        assert r["exact"] is False and r["guard"] is True, tid
        av, gv = float(r["predicted"]), float(r["gold"])
        assert av != gv, tid  # genuinely wrong answers
        rel = abs(av - gv) / max(abs(gv), 1.0)
        assert 0.0 < rel < 0.005, (tid, rel)
        rel_errs[tid] = rel
    assert adj["n_over_fire"] == 5

    payload = {
        "theorem1_monotonicity": {
            "n_rows_checked": n_rows,
            "inclusion_violations": 0,
            "v34_increments": n_incr,
            "increment_ids": sorted(incr_ids),
            "suffixes_cjk_only": suffixes_cjk_only,
            "n_suffixes": len(SUFFIXES),
            "guard_scope": {"n_pairs": diff["n_pairs"],
                              "n_diffs": diff["n_diffs"],
                              "note": "v32->v33 added blocking guards: "
                                      "accept->reject, all single-CJK-substring"},
        },
        "theorem2_numeric_boundary": {
            "n_over_fire_checked": len(over_ids),
            "all_inside_open_interval_0_0005": True,
            "rel_errors": {k: round(v, 6) for k, v in rel_errs.items()},
        },
        "probes": {k: bool(v) for k, v in probes.items()},
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()