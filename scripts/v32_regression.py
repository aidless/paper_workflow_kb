"""v3.2 regression: unit tests + full response-row regression v3.1 vs v3.2.

Unit tests (assertions):
  U1 ('//','//') -> v3.1 False, v3.2 True (c-cell edge fixed)
  U2 ('','') -> both False (empty-answer guard intact)
  U3 ('','x') / ('x','') -> both False
  U4 ('//','/') -> v3.2 False (both norm empty, raw differs -> reject)
  U5 v3.1 checklist preserved under v3.2: cloud-new-42 False, pilot-03 True,
     cloud-new-48 True (row data loaded from evidence, not hardcoded outcomes
     except trace identity)

Regression: all response rows with predicted_label (60+60+60+40+60+160+30=470):
  d2_60.jsonl, cloud_new60_raw, cloud_retest60_raw, cloud_math40_raw,
  local_new60_raw, local_big_raw, local_en_raw.
  Expected diff set: rows where both raw non-blank but both norm empty.
  Exit nonzero unless diff == expected class exactly.
  Output: results/guard_v32.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v31 import guarded_tolerant_match as v31, norm  # noqa: E402
from label_match_v32 import tolerant_match_v32 as v32  # noqa: E402

EV = HERE / "evidence"


def both_norm_empty(a, g) -> bool:
    return (bool(str(a).strip()) and bool(str(g).strip())
            and not norm(a) and not norm(g))


def main() -> None:
    # ---- unit tests ----
    assert v31("//", "//") is False, "U1a: v3.1 must still reject //-//"
    assert v32("//", "//") is True, "U1b: v3.2 must accept //-// via raw-fallback"
    assert v31("", "") is False and v32("", "") is False, "U2"
    assert v31("", "x") is False and v32("", "x") is False, "U3a"
    assert v31("x", "") is False and v32("x", "") is False, "U3b"
    assert v32("//", "/") is False, "U4: raw differs -> reject"
    assert v31("//", "/") is False, "U4b: v3.1 rejects too"

    files = ["d2_60.jsonl", "cloud_new60_raw.json", "cloud_retest60_raw.json",
             "cloud_math40_raw.json", "local_new60_raw.json",
             "local_big_raw.json", "local_en_raw.json"]
    rows = []
    for f in files:
        p = EV / f
        if f.endswith(".jsonl"):
            rows += [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines()
                     if l.strip()]
        else:
            rows += json.loads(p.read_text(encoding="utf-8"))
    assert len(rows) == 470, f"expected 470 response rows, got {len(rows)}"

    by_id = {}
    for r in rows:
        a, g = str(r.get("predicted_label", "")), str(r.get("gold_answer", ""))
        by_id[r["trace_id"]] = (r.get("source"), a, g)
    # U5: v3.1 checklist rows exist and keep outcomes under v3.2
    assert v32(*by_id["cloud-new-42"][1:]) is False, "U5a cloud-new-42 stays rejected"
    assert v32(*by_id["pilot-03"][1:]) is True, "U5b pilot-03 stays accepted"
    assert v32(*by_id["cloud-new-48"][1:]) is True, "U5c cloud-new-48 stays accepted"

    diff, unexpected = [], []
    for tid, (src, a, g) in by_id.items():
        o31, o32 = bool(v31(a, g)), bool(v32(a, g))
        if o31 != o32:
            rec = {"trace_id": tid, "source": src, "predicted": a, "gold": g,
                   "v3.1": o31, "v3.2": o32}
            diff.append(rec)
            if not both_norm_empty(a, g):
                unexpected.append(rec)
    out = {"matcher": "label_match_v32.tolerant_match_v32 (v3.1 + empty-guard raw-fallback)",
           "n_rows": len(rows), "n_diff_vs_v31": len(diff), "diff": diff,
           "n_unexpected": len(unexpected), "unexpected": unexpected}
    (HERE / "results" / "guard_v32.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2)[:2000])
    assert not unexpected, f"{len(unexpected)} diffs outside expected class: {unexpected}"
    print(f"V32 REGRESSION OK: n=470 diff={len(diff)} all in both-norm-empty class")


if __name__ == "__main__":
    main()
