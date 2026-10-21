"""Analyze code-domain pilot (n=12) on the guarded basis.

Reads evidence/cloud_pilot_code_raw.json (qwen2.5:7b, temp 0, feasibility probe,
NOT a formal stratum), applies label_match_v32 (== v3.1 on these rows; regression
diff 0/470 in results/guard_v32.json), and writes results/code_pilot.json.

Usage: python3 paper_workflow_kb/scripts/analyze_code_pilot.py paper_workflow_kb
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from label_match_v3 import norm
from label_match_v31 import guarded_tolerant_match as match_v31
from label_match_v32 import tolerant_match_v32 as match_v32


def basis(rows, fn):
    n_exact = n_g = 0
    b_cells, c_cells = [], []
    for r in rows:
        e = norm(r["predicted_label"]) == norm(r["gold_answer"])
        t = fn(r["predicted_label"], r["gold_answer"])
        n_exact += e
        n_g += t
        if (not e) and t:
            b_cells.append(r["trace_id"])
        if e and (not t):
            c_cells.append(r["trace_id"])
    return {"n_exact": n_exact, "n_guarded": n_g,
            "n_b_cells": len(b_cells), "b_cells": b_cells,
            "n_c_cells": len(c_cells), "c_cells": c_cells}


def main(kb):
    rows = json.load(open(os.path.join(kb, "evidence", "cloud_pilot_code_raw.json"),
                          encoding="utf-8"))
    assert len(rows) == 12, len(rows)
    out = {"n": len(rows),
           "note": "feasibility probe only; not a formal stratum; no ledger claim beyond counts",
           "n_errs": sum(1 for r in rows if r.get("error"))}
    out["v31"] = basis(rows, match_v31)
    out["v32"] = basis(rows, match_v32)
    # hard assertions = the pilot facts the theory section may cite:
    # v3.1 exhibits the c-cell edge; v3.2 raw-fallback closes it.
    assert out["v31"]["n_guarded"] == 11, out
    assert out["v31"]["n_c_cells"] == 1 and out["v31"]["c_cells"] == ["code-pilot-04"], out
    assert out["v32"]["n_guarded"] == 12 and out["v32"]["n_c_cells"] == 0, out
    assert out["n_errs"] == 0, out
    json.dump(out, open(os.path.join(kb, "results", "code_pilot.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
