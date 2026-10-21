"""R18 P1-2 analysis: hetero-model (gemma3:4b) layer, v3.2 basis, descriptive only.

Reads evidence/r18_heteromodel_gemma60_raw.json; writes results/r18_heteromodel.json
with n/exact/guarded/flips/flip_rate, b/c (descriptive; no inference under nesting),
ECE10 equal-width canonical + equal-frequency audit, flip lists.
Structural gates: n=60; errors reported, never fabricated.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from analyze_xdomain import layer, ece_equal_width  # noqa: E402
from label_match_v31 import ece_equal_freq  # noqa: E402
from label_match_v3 import norm  # noqa: E402
from label_match_v33 import tolerant_match_v33  # noqa: E402  # R22 promotion


def main(kb):
    rows = json.load(open(os.path.join(kb, "evidence",
                                       "r18_heteromodel_gemma60_raw.json"),
                          encoding="utf-8"))
    assert len(rows) == 60, len(rows)
    res = layer(rows)
    errs = sum(1 for r in rows if r.get("error"))
    c = [float(r.get("confidence", 0.0)) for r in rows]
    e = [int(norm(r["predicted_label"]) == norm(r["gold_answer"])) for r in rows]
    g = [int(tolerant_match_v33(r["predicted_label"], r["gold_answer"]))
         for r in rows]
    res["ece10_ef_exact"] = ece_equal_freq(c, e)
    res["ece10_ef_guarded"] = ece_equal_freq(c, g)
    out = {"matcher": "label_match_v33.tolerant_match_v33",  # R22 promotion
           "model": "gemma3:4b (hetero family + scale vs qwen 7b)",
           "temperature": 0, "n_errs": errs,
           "note": "R18 P1-2 hetero-family validation (PREREG_R18_HETEROMODEL.md "
                   "+ Amendment A1); same 60 xdomain questions, loose prompt "
                   "verbatim; descriptive only",
           "heteromodel": res}
    json.dump(out, open(os.path.join(kb, "results", "r18_heteromodel.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps({k: (v if not isinstance(v, dict) else
                          {kk: vv for kk, vv in v.items() if kk != "flips"})
                      for k, v in out.items()}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main("paper_workflow_kb")
