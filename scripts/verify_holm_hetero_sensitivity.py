"""Verify the sealed Holm-family exclusion claim for hetero-gemma (R20-4).

ARITHMETIC COMPLETENESS CHECK ONLY — no inferential license (see paper,
Multiplicity accounting: reverse cells are zero by construction, so any
Holm computation is a definitional tautology reported for completeness).

Claim under test (paper L251): hetero-gemma (fifteenth stratum,
mini-pre-registered descriptive, adjudicated b=8, c=0, arithmetic
p_two = 2/2^8 = 0.0078125) is excluded from the sealed 18-comparison
family, and "its arithmetic b=8 p=0.0078 would not change the survivors
or the stop step".

Procedure:
  1. Load sealed results/holm.json; assert m=18 and the sealed survivors /
     stop step match the paper (C51 values).
  2. Recompute hetero p_two independently as 2/2**8 from the sealed
     adjudicated flip count (results/r18_heteromodel_adjudication.json).
  3. Insert hetero as a 19th comparison, re-sort, re-run Holm step-down at
     alpha=0.05, and assert survivors and stop-step NAME are unchanged.

Writes results/holm_hetero_sensitivity.json. Exit nonzero on any mismatch.
"""

import json
import os
import sys

ALPHA = 0.05


def holm_run(ordered, m, alpha=ALPHA):
    """ordered: list of (name, p) ascending. Returns (survivors, stop)."""
    survivors = []
    for i, (name, p) in enumerate(ordered, start=1):
        thresh = alpha / (m + 1 - i)
        if p <= thresh:
            survivors.append(name)
        else:
            return survivors, {"step": i, "name": name, "p": p,
                               "threshold": thresh}
    return survivors, {"step": m + 1, "name": None, "p": None,
                       "threshold": None}


def main(kb):
    sealed = json.load(open(os.path.join(kb, "results", "holm.json"),
                            encoding="utf-8"))
    assert sealed["m"] == 18, sealed["m"]
    assert abs(sealed["alpha"] - ALPHA) < 1e-12
    base = [(t["name"], float(t["p_two"])) for t in sealed["ordered"]]
    assert len(base) == 18
    assert [n for n, _ in base] == sorted([n for n, _ in base],
                                          key=lambda n: dict(base)[n]), \
        "sealed ordering must be ascending in p"
    surv0, stop0 = holm_run(base, 18)
    assert surv0 == sealed["holm_survivors"], (surv0, sealed["holm_survivors"])
    assert stop0["step"] == sealed["holm_stop"]["step"], stop0
    assert stop0["name"] == sealed["holm_stop"]["name"], stop0
    assert stop0["name"] == "prespecified-pool", stop0
    # C51 pinned values
    assert surv0 == ["r18-loose-rep", "xdomain-loose", "pilot"], surv0
    assert stop0["step"] == 4 and stop0["p"] == 0.00390625, stop0

    # hetero arithmetic p from the sealed adjudicated flip count
    het = json.load(open(os.path.join(
        kb, "results", "r18_heteromodel_adjudication.json"), encoding="utf-8"))
    b = int(het["adjudicated_flips"])
    assert b == 8, b
    p_het = 2.0 / 2 ** b
    assert abs(p_het - 0.0078125) < 1e-12, p_het

    fam19 = sorted(base + [("hetero-gemma", p_het)], key=lambda t: t[1])
    assert [n for n, _ in fam19].index("hetero-gemma") == 4, \
        "hetero must sort 5th (after pool), else the claim setup changed"
    surv1, stop1 = holm_run(fam19, 19)
    assert surv1 == surv0, (surv1, surv0)
    assert stop1["name"] == stop0["name"] == "prespecified-pool", (stop1, stop0)
    assert stop1["step"] == 4, stop1

    out = {
        "sealed_m": 18,
        "extended_m": 19,
        "hetero": {"name": "hetero-gemma", "b": b, "p_two": p_het,
                   "rank19": 5},
        "sealed_survivors": surv0,
        "extended_survivors": surv1,
        "sealed_stop": stop0,
        "extended_stop": stop1,
        "claim_holds": (surv1 == surv0
                        and stop1["name"] == stop0["name"]),
        "license": ("arithmetic completeness only; no inferential license "
                    "under nesting (reverse cells zero by construction)"),
    }
    assert out["claim_holds"]
    json.dump(out, open(os.path.join(
        kb, "results", "holm_hetero_sensitivity.json"), "w",
        encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
