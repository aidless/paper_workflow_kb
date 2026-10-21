"""R18 P2-2 (M6): temperature-scaling + isotonic disposition at n=157.

Same machinery as tempscale.py / isotonic.py (imported: fit_T, scale, nll,
pav, nll_of), same NLL fits, but on the two n=157 power-replication arms
(PowCloudNew cloud qwen2.5:7b, PowLocalNew local qwen2:7b) under v3.2-guarded
labels (== adjudicated: tight-arm flips judge-confirmed 10/10,
evidence/powrep_judge.json) and the unified equal-width convention
(results/ece_unified.json canonical function).

Question answered: do the mixed/absent ECE repairs persist at 5x the rows?
Degenerate-confidence disclosure applies (few discordants: 1 and 7 flips).

Writes results/tempiso_n157.json. Exit nonzero on violated expectation.
"""
import json
import sys
from pathlib import Path

KB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KB / "scripts"))
from analyze_xdomain import ece_equal_width  # noqa: E402
from label_match_v32 import tolerant_match_v32 as guarded  # noqa: E402
from label_match_v3 import norm  # noqa: E402
from tempscale import fit_T, scale, nll  # noqa: E402
from isotonic import pav, nll_of  # noqa: E402

LOG = []


def check(name, got, want):
    ok = got == want
    LOG.append(f"[{'OK' if ok else 'MISMATCH'}] {name}: got={got} want={want}")
    if not ok:
        raise SystemExit(f"MISMATCH {name}: got={got} want={want}")


def load_json(p):
    return json.loads((KB / p).read_text(encoding="utf-8"))


p255 = load_json("evidence/cloud_powrep255_raw.json")
pL = load_json("evidence/local_powrep157_raw.json")
pow2 = [r for r in p255 if r["trace_id"].startswith("pow2-")]
assert (len(pow2), len(pL)) == (157, 157), (len(pow2), len(pL))

out = {"labels": "v3.2-guarded == adjudicated (tight-arm flips 10/10 "
                 "judge-confirmed)", "arms": {}}
for name, rows in (("powcloudnew", pow2), ("powlocalnew", pL)):
    e = [int(norm(r["predicted_label"]) == norm(r["gold_answer"])) for r in rows]
    g = [int(guarded(r["predicted_label"], r["gold_answer"])) for r in rows]
    c = [float(r.get("confidence", 0.0)) for r in rows]
    n = len(rows)
    b = sum(1 for x, y in zip(e, g) if x == 0 and y == 1)
    # tempscale on guarded labels
    T_star, nll_star = fit_T(c, g)
    nll_1 = round(nll(c, g, 1.0), 4)
    ew_1 = round(ece_equal_width(c, g), 4)
    ew_s = round(ece_equal_width([scale(p, T_star) for p in c], g), 4)
    # isotonic on guarded labels (same PAV + 5-fold CV as isotonic.py)
    sub = sorted(zip(c, g), key=lambda r: r[0])
    cs = [x for x, _ in sub]
    ys = [y for _, y in sub]
    fit = pav(ys)
    ew_raw = round(ece_equal_width(cs, ys), 4)
    ew_in = round(ece_equal_width(fit, ys), 4)
    cv_ps, cv_ys = [], []
    for f in range(5):
        te = [i for i in range(n) if i % 5 == f]
        tr = [i for i in range(n) if i % 5 != f]
        tr_xy = sorted([(cs[i], ys[i]) for i in tr], key=lambda r: r[0])
        tr_fit = pav([y for _, y in tr_xy])
        tmap = sorted(set(zip([x for x, _ in tr_xy], tr_fit)))
        for i in te:
            x = cs[i]
            cand = [v for (xx, v) in tmap if xx <= x + 1e-12]
            cv_ps.append(cand[-1] if cand else tmap[0][1])
            cv_ys.append(ys[i])
    ew_cv = round(ece_equal_width(cv_ps, cv_ys), 4)
    out["arms"][name] = {
        "n": n, "n_exact": sum(e), "n_guarded": sum(g), "b_cell": b,
        "tempscale": {"T_star": T_star, "NLL_T1": nll_1, "NLL_Tstar": nll_star,
                      "EW_T1": ew_1, "EW_Tstar": ew_s,
                      "dEW": round(ew_1 - ew_s, 4)},
        "isotonic": {"n_blocks": len(set(round(v, 9) for v in fit)),
                     "EW_raw": ew_raw, "EW_insample": ew_in, "EW_cv5": ew_cv,
                     "NLL_raw": nll_of(cs, ys), "NLL_cv5": nll_of(cv_ps, cv_ys)}}
    LOG.append(f"[INFO] {name}: n={n} exact={sum(e)} guarded={sum(g)} b={b} "
               f"T*={T_star} ts_dEW={round(ew_1-ew_s,4)} iso_cv={ew_cv}")

check("powcloudnew_guarded", out["arms"]["powcloudnew"]["n_guarded"], 144)
check("powlocalnew_guarded", out["arms"]["powlocalnew"]["n_guarded"], 147)
out["validation_log"] = LOG
(KB / "results" / "tempiso_n157.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("\n".join(LOG))
print("WROTE results/tempiso_n157.json")
