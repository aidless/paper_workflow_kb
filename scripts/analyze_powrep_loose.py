"""Sealed analysis: power-rep LOOSE arms (v3.2 basis).

Arms: pow1L (batch1 loose, n=98 cloud), pow2L (batch2 loose, n=157 cloud),
powLL (batch2 loose, n=157 local). Same arm() engine as analyze_powrep
(imported). Writes results/powrep_loose.json.

Usage: python3 paper_workflow_kb/scripts/analyze_powrep_loose.py paper_workflow_kb [--seal]
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from analyze_powrep import arm


def main(kb, seal):
    cloud = json.load(open(os.path.join(kb, "evidence",
                                        "cloud_powrep255_loose_raw.json"),
                           encoding="utf-8"))
    local = json.load(open(os.path.join(kb, "evidence",
                                        "local_powrep157_loose_raw.json"),
                           encoding="utf-8"))
    assert len(cloud) == 255 and len(local) == 157, (len(cloud), len(local))
    by_arm = {"pow1L": [r for r in cloud if r["trace_id"].startswith("pow1L-")],
              "pow2L": [r for r in cloud if r["trace_id"].startswith("pow2L-")],
              "powLL": local}
    out = {"matcher": "label_match_v32.tolerant_match_v32",
           "golds": "user-approved (全做)",
           "note": "loose-regime rerun of the same power-rep questions"}
    for k, rows in by_arm.items():
        out[k] = arm(rows)
    summ = {k: {kk: vv for kk, vv in v.items() if kk != "flips"}
            for k, v in out.items() if isinstance(v, dict)}
    print(json.dumps(summ, ensure_ascii=False, indent=1))
    if seal:
        json.dump(out, open(os.path.join(kb, "results", "powrep_loose.json"),
                            "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("SEALED results/powrep_loose.json")


if __name__ == "__main__":
    main(sys.argv[1], "--seal" in sys.argv[2:])
