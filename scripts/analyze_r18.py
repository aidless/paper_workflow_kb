"""Sealed analysis: R18 loose-regime replication layer (n=60 fresh), v3.2 basis.

Pre-registered in PREREG_R18_LOOSE_REP.md. Reads
paper_workflow_kb/evidence/r18_loose_rep60_raw.json; writes
results/r18_loose_rep.json with n/exact/guarded/flips/flip_rate,
b/c cells (descriptive; McNemar p retained as arithmetic record only,
NOT cited for inference under the nested-matcher construction), ECE10
equal-width on rows carrying confidences, and flip lists.

Structural gates only (no outcome assertions: the flip count is the
pre-registered unknown): n=60, zero collection errors, all rows carry
a parsed confidence.

Usage: python3 paper_workflow_kb/scripts/analyze_r18.py paper_workflow_kb
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from analyze_xdomain import layer  # noqa: E402  (same v3.2 basis + schema)


def main(kb):
    rows = json.load(open(os.path.join(kb, "evidence", "r18_loose_rep60_raw.json"),
                          encoding="utf-8"))
    assert len(rows) == 60, len(rows)
    out = {"matcher": "label_match_v33.tolerant_match_v33",  # R22 promotion (via layer())
           "model": "qwen2.5:7b", "temperature": 0,
           "note": "R18 pre-registered loose-regime replication: 20 measure-word + "
                   "20 rephrased yes-no + 20 name-variant fresh questions; "
                   "loose prompt identical to xdomain-loose; "
                   "McNemar p is an arithmetic record, not an inference license"}
    res = layer(rows)
    assert res["n_errs"] == 0, res
    out["loose_rep"] = res
    json.dump(out, open(os.path.join(kb, "results", "r18_loose_rep.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "flips"}
                      if isinstance(v, dict) else v for k, v in out.items()},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
