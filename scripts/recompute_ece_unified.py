"""R18 P1-1 (C6): unified equal-width 10-bin ECE recomputation for all strata.

Rebuilds (confs, exact_outs, guarded_outs) from SEALED evidence on the
manuscript basis per stratum, computes equal-width AND equal-frequency ECE,
and asserts reproduction of every already-equal-width manuscript number
(validates the rebuild). Old results files are NOT touched; output is the new
file results/ece_unified.json (equal-width governs the main table;
equal-frequency retained for the appendix).

Also recomputes temperature-scaling and isotonic ECE under equal-width
(same fits: T* from NLL, same PAV/CV; only the binning changes).
"""
import json
import sys
from pathlib import Path

KB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KB / "scripts"))

from analyze_xdomain import ece_equal_width  # noqa: E402
from label_match_v31 import ece_equal_freq, guarded_tolerant_match  # noqa: E402
from label_match_v32 import tolerant_match_v32 as guarded_v32  # noqa: E402
from label_match_v3 import norm  # noqa: E402
from tempscale import fit_T, scale, nll  # noqa: E402
from isotonic import pav, nll_of  # noqa: E402

LOG = []


def check(name, got, want, tol=1e-9):
    ok = abs(got - want) <= tol
    LOG.append(f"[{'OK' if ok else 'MISMATCH'}] {name}: got={got} want={want}")
    if not ok:
        raise SystemExit(f"MISMATCH {name}: got={got} want={want}")


def exact_nn(a, g):
    a2, g2 = norm(a), norm(g)
    return bool(a2 and g2 and a2 == g2)


def load_jsonl(p):
    return [json.loads(l) for l in (KB / p).read_text(encoding="utf-8").splitlines()
            if l.strip()]


def load_json(p):
    return json.loads((KB / p).read_text(encoding="utf-8"))


def conf_rows(rows):
    return [r for r in rows if r.get("confidence") is not None]


def cf(r):
    return float(r.get("confidence", 0.0))


strata = {}
KEEP = {}  # (confs, exact_outs, guarded_outs) for legacy-binner cross-checks

# ---- prior strata (d2_60.jsonl): pilot + holdout-main, v3.1 guarded basis ----
d2 = load_jsonl("evidence/d2_60.jsonl")
for name in ("pilot", "holdout-main"):
    sub = [r for r in d2 if r["source"] == name]
    assert len(sub) == 30, (name, len(sub))
    e = [int(exact_nn(r["predicted_label"], r["gold_answer"])) for r in sub]
    g = [int(guarded_tolerant_match(r["predicted_label"], r["gold_answer"]))
         for r in sub]
    c = [float(r["confidence"]) for r in sub]
    strata[name] = {"n": 30, "n_conf": 30, "acc_exact": sum(e) / 30,
                    "acc_guarded": sum(g) / 30,
                    "ew_exact": round(ece_equal_width(c, e), 4),
                    "ew_guarded": round(ece_equal_width(c, g), 4),
                    "ef_exact": ece_equal_freq(c, e),
                    "ef_guarded": ece_equal_freq(c, g),
                    "basis": "v3.1-guarded; all rows carry confidences"}

# ---- cloud-new (60, v3.1 guarded; adjudicated set == guarded set) ----
cn = load_json("evidence/cloud_new60_raw.json")
assert len(cn) == 60
e = [int(exact_nn(r["predicted_label"], r["gold_answer"])) for r in cn]
g = [int(guarded_tolerant_match(r["predicted_label"], r["gold_answer"]))
     for r in cn]
c = [float(r["confidence"]) for r in cn]
assert sum(e) == 48 and sum(g) == 52
from label_match_v3 import tolerant_match as tolerant_v3  # noqa: E402
t_raw = [int(tolerant_v3(r["predicted_label"], r["gold_answer"])) for r in cn]
assert sum(t_raw) == 53
raw_ew = round(ece_equal_width(c, t_raw), 4)
strata["cloud-new"] = {"n": 60, "n_conf": 60, "acc_exact": 48 / 60,
                       "acc_guarded": 52 / 60,
                       "ew_exact": round(ece_equal_width(c, e), 4),
                       "ew_guarded": round(ece_equal_width(c, g), 4),
                       "ef_exact": ece_equal_freq(c, e),
                       "ef_guarded": ece_equal_freq(c, g),
                       "raw_tolerant_ew": raw_ew,
                       "basis": "v3.1-guarded (== adjudicated 52-set)"}
KEEP["cloud-new"] = (c, e, g)

# ---- local-new (60; ECE on 55 conf rows; guarded basis) ----
ln = load_json("evidence/local_new60_raw.json")
e_all = [int(exact_nn(r["predicted_label"], r["gold_answer"])) for r in ln]
g_all = [int(guarded_tolerant_match(r["predicted_label"], r["gold_answer"]))
         for r in ln]
assert sum(e_all) == 48 and sum(g_all) == 53
sub = conf_rows(ln)
assert len(sub) == 55, len(sub)
e = [int(exact_nn(r["predicted_label"], r["gold_answer"])) for r in sub]
g = [int(guarded_tolerant_match(r["predicted_label"], r["gold_answer"]))
     for r in sub]
c = [float(r["confidence"]) for r in sub]
strata["local-new"] = {"n": 60, "n_conf": 55, "acc_exact": 48 / 60,
                       "acc_guarded": 53 / 60,
                       "ew_exact": round(ece_equal_width(c, e), 4),
                       "ew_guarded": round(ece_equal_width(c, g), 4),
                       "ef_exact": ece_equal_freq(c, e),
                       "ef_guarded": ece_equal_freq(c, g),
                       "basis": "v3.1-guarded; ECE on 55 conf rows"}
KEEP["local-new"] = (c, e, g)

# ---- local-en (30, guarded == exact) ----
le = load_json("evidence/local_en_raw.json")
sub = conf_rows(le)
e = [int(exact_nn(r["predicted_label"], r["gold_answer"])) for r in sub]
g = [int(guarded_tolerant_match(r["predicted_label"], r["gold_answer"]))
     for r in sub]
assert sum(e) == len(sub) == 30 and sum(g) == 30
c = [float(r["confidence"]) for r in sub]
strata["local-en"] = {"n": 30, "n_conf": 30, "acc_exact": 1.0,
                      "acc_guarded": 1.0,
                      "ew_exact": round(ece_equal_width(c, e), 4),
                      "ew_guarded": round(ece_equal_width(c, g), 4),
                      "ef_exact": ece_equal_freq(c, e),
                      "ef_guarded": ece_equal_freq(c, g),
                      "basis": "guarded == exact (0 flips)"}
KEEP["local-en"] = (c, e, g)

# ---- local-big (160; ECE on 156 conf rows) ----
lb = load_json("evidence/local_big_raw.json")
e_all = [int(exact_nn(r["predicted_label"], r["gold_answer"])) for r in lb]
g_all = [int(guarded_tolerant_match(r["predicted_label"], r["gold_answer"]))
         for r in lb]
assert (sum(e_all), sum(g_all)) == (148, 152), (sum(e_all), sum(g_all))
sub = conf_rows(lb)
assert len(sub) == 156, len(sub)
e = [int(exact_nn(r["predicted_label"], r["gold_answer"])) for r in sub]
g = [int(guarded_tolerant_match(r["predicted_label"], r["gold_answer"]))
     for r in sub]
c = [float(r["confidence"]) for r in sub]
strata["local-big"] = {"n": 160, "n_conf": 156, "acc_exact": 148 / 160,
                       "acc_guarded": 152 / 160,
                       "ew_exact": round(ece_equal_width(c, e), 4),
                       "ew_guarded": round(ece_equal_width(c, g), 4),
                       "ef_exact": ece_equal_freq(c, e),
                       "ef_guarded": ece_equal_freq(c, g),
                       "basis": "v3.1-guarded; ECE on 156 conf rows"}
KEEP["local-big"] = (c, e, g)

# ---- math (40, guarded == exact) ----
mm = load_json("evidence/cloud_math40_raw.json")
sub = conf_rows(mm)
assert len(sub) == 40, len(sub)
e = [int(exact_nn(r["predicted_label"], r["gold_answer"])) for r in sub]
g = [int(guarded_tolerant_match(r["predicted_label"], r["gold_answer"]))
     for r in sub]
assert sum(e) == 37 and sum(g) == 37
c = [float(r["confidence"]) for r in sub]
strata["math"] = {"n": 40, "n_conf": 40, "acc_exact": 37 / 40,
                  "acc_guarded": 37 / 40,
                  "ew_exact": round(ece_equal_width(c, e), 4),
                  "ew_guarded": round(ece_equal_width(c, g), 4),
                  "ef_exact": ece_equal_freq(c, e),
                  "ef_guarded": ece_equal_freq(c, g),
                  "basis": "guarded == exact (0 flips)"}
KEEP["math"] = (c, e, g)

# ---- cross-domain tight/loose (v3.1 guarded) ----
xt = load_json("evidence/cloud_xdomain60_raw.json")
xl = load_json("evidence/cloud_xdomain60_loose_raw.json")
for name, rows, ne, ng in (("xtight", xt, 50, 51), ("xloose", xl, 25, 45)):
    assert len(rows) == 60
    e = [int(exact_nn(r["predicted_label"], r["gold_answer"])) for r in rows]
    g = [int(guarded_tolerant_match(r["predicted_label"], r["gold_answer"]))
         for r in rows]
    assert (sum(e), sum(g)) == (ne, ng), (name, sum(e), sum(g))
    c = [cf(r) for r in rows]
    strata[name] = {"n": 60, "n_conf": 60, "acc_exact": ne / 60,
                    "acc_guarded": ng / 60,
                    "ew_exact": round(ece_equal_width(c, e), 4),
                    "ew_guarded": round(ece_equal_width(c, g), 4),
                    "ef_exact": ece_equal_freq(c, e),
                    "ef_guarded": ece_equal_freq(c, g),
                    "basis": "v3.1-guarded"}

# ---- power-replication arms (v3.2 basis; assert == v3.1 row-wise) ----
# cloud_powrep255_raw.json = pow1 (98: first 20 pilot-style, rest holdout-style)
#   + pow2 (157 cloud-new style); local_powrep157_raw.json = powL (157).
p255 = load_json("evidence/cloud_powrep255_raw.json")
pL = load_json("evidence/local_powrep157_raw.json")
pow1 = [r for r in p255 if r["trace_id"].startswith("pow1-")]
pow2 = [r for r in p255 if r["trace_id"].startswith("pow2-")]
assert (len(pow1), len(pow2), len(pL)) == (98, 157, 157), \
    (len(pow1), len(pow2), len(pL))


def pow_arm(rows):
    e = [int(norm(r["predicted_label"]) == norm(r["gold_answer"])) for r in rows]
    g = [int(guarded_v32(r["predicted_label"], r["gold_answer"])) for r in rows]
    g31 = [int(guarded_tolerant_match(r["predicted_label"], r["gold_answer"]))
           for r in rows]
    assert g == g31, "v3.2 differs from v3.1 on powrep rows"
    c = [cf(r) for r in rows]
    return e, g, c


pow_map = {"powpilot": pow1[:20], "powholdout": pow1[20:],
           "powcloudnew": pow2, "powlocalnew": pL}
for name, rows in pow_map.items():
    e, g, c = pow_arm(rows)
    n = len(rows)
    strata[name] = {"n": n, "n_conf": n, "acc_exact": sum(e) / n,
                    "acc_guarded": sum(g) / n,
                    "ew_exact": round(ece_equal_width(c, e), 4),
                    "ew_guarded": round(ece_equal_width(c, g), 4),
                    "ef_exact": ece_equal_freq(c, e),
                    "ef_guarded": ece_equal_freq(c, g),
                    "basis": "v3.2-guarded (== v3.1 row-wise, asserted)"}

# ---- R18 (raw exact EW + adjudicated basis mirror of r18_adjudicate.py) ----
r18raw = load_json("evidence/r18_loose_rep60_raw.json")
assert len(r18raw) == 60
adj = load_json("results/r18_adjudication.json")
flips = {f["trace_id"] for f in load_json("results/r18_loose_rep.json")
         ["loose_rep"]["flips"] if not f["trace_id"].endswith(":c-cell")}
excluded = set(adj["excluded"])
assert len(flips) == 26 and len(excluded) == 2, (len(flips), len(excluded))  # R22 v33
e = [int(norm(r["predicted_label"]) == norm(r["gold_answer"])) for r in r18raw]
ok, c = [], []
for r in r18raw:
    tid = r["trace_id"]
    exact_ok = bool(norm(r["predicted_label"]) == norm(r["gold_answer"]))
    if tid in flips and tid in excluded:
        ok.append(1 if exact_ok else 0)
    elif tid in flips:
        ok.append(1)
    else:
        ok.append(1 if exact_ok else 0)
    c.append(float(r["confidence"]))
assert sum(ok) == adj["adjudicated_guarded_correct"] == 39, sum(ok)
strata["r18"] = {"n": 60, "n_conf": 60, "acc_exact": sum(e) / 60,
                 "acc_guarded": sum(ok) / 60,
                 "ew_exact": round(ece_equal_width(c, e), 4),
                 "ew_guarded": round(ece_equal_width(c, ok), 4),
                 "ef_exact": ece_equal_freq(c, e),
                 "ef_guarded": ece_equal_freq(c, ok),
                 "basis": "adjudicated (24/26 confirmed; 2 excluded revert)"}  # R22 v33

# Canonical convention: analyze_xdomain.ece_equal_width (upper-edge inclusive,
# Guo-style). The analyze_new60 inline copies are legacy; cross-checked below.
def ece_new60_style(confs, outs):
    # Faithful replica of analyze_new60.ece10 INCLUDING its bins.index(b)
    # aliasing quirk (equal-content bins share the first match's mean).
    # Used only to prove outcome-level reproduction of sealed numbers;
    # the quirk is documented and superseded by the canonical convention.
    bins = [[] for _ in range(10)]
    for c, y in zip(confs, outs):
        cc = min(max(c, 0.0), 1.0)
        bins[min(int(cc * 10), 9)].append(1 if y else 0)
    n = len(confs)
    e = 0.0
    for b in bins:
        if b:
            mean_out = sum(b) / len(b)
            mean_cf = sum(min(max(c, 0.0), 1.0) for c in confs
                          if min(int(min(max(c, 0.0), 1.0) * 10), 9)
                          == bins.index(b)) / len(b)
            e += len(b) / n * abs(mean_out - mean_cf)
    return round(e, 4)


# ---- validation A: canonical-binner strata must reproduce manuscript ----
XD_VALIDATE = {
    ("xtight", "ew_exact"): 0.0533, ("xtight", "ew_guarded"): 0.0367,
    ("xloose", "ew_exact"): 0.4767, ("xloose", "ew_guarded"): 0.1433,
    ("powpilot", "ew_exact"): 0.13, ("powpilot", "ew_guarded"): 0.13,
    ("powholdout", "ew_exact"): 0.0261, ("powholdout", "ew_guarded"): 0.0517,
    ("powcloudnew", "ew_exact"): 0.0204, ("powcloudnew", "ew_guarded"): 0.0268,
    ("powlocalnew", "ew_exact"): 0.0349, ("powlocalnew", "ew_guarded"): 0.0668,
    ("r18", "ew_exact"): 0.6425, ("r18", "ew_guarded"): 0.2425,
}
for (s, f), want in XD_VALIDATE.items():
    check(f"{s}.{f}", strata[s][f], want, tol=5e-5)

# ---- validation B: legacy-binner cross-checks (outcome rebuild validation;
# these manuscript numbers are SUPERSEDED by the canonical convention) ----
N6_CROSSCHECK = {
    ("cloud-new", "exact"): 0.1067,
    ("local-new", "exact"): 0.1255, ("local-new", "guarded"): 0.0345,
    ("local-en", "exact"): 0.08, ("local-en", "guarded"): 0.08,
    ("local-big", "exact"): 0.033, ("local-big", "guarded"): 0.0458,
    ("math", "exact"): 0.025, ("math", "guarded"): 0.025,
}
for (s, which), want in N6_CROSSCHECK.items():
    c0, e0, g0 = KEEP[s]
    got = ece_new60_style(c0, e0 if which == "exact" else g0)
    LOG.append(f"[XCHK] {s}.{which} legacy-binner: got={got} sealed={want}")
    if abs(got - want) > 5e-5:
        raise SystemExit(f"XCHK MISMATCH {s}.{which}: got={got} want={want}")

# validation: equal-frequency rebuild must reproduce the old prior numbers
check("pilot.ef_exact", strata["pilot"]["ef_exact"], 0.363)
check("pilot.ef_guarded", strata["pilot"]["ef_guarded"], 0.0037)
check("holdout.ef_exact", strata["holdout-main"]["ef_exact"], 0.3517)
check("holdout.ef_guarded", strata["holdout-main"]["ef_guarded"], 0.205)
check("cloud-new.ef_guarded", strata["cloud-new"]["ef_guarded"], 0.1692)
# (documents that 0.1692 was equal-frequency all along, not a coincidence)

# validation: accuracy counts reproduce the table
EXPECTED_ACC = {
    "pilot": (19 / 30, 30 / 30), "holdout-main": (19 / 30, 24 / 30),
    "cloud-new": (48 / 60, 52 / 60), "local-new": (48 / 60, 53 / 60),
    "local-en": (1.0, 1.0), "local-big": (148 / 160, 152 / 160),
    "math": (37 / 40, 37 / 40), "xtight": (50 / 60, 51 / 60),
    "xloose": (25 / 60, 45 / 60), "powpilot": (16 / 20, 16 / 20),
    "powholdout": (71 / 78, 73 / 78), "powcloudnew": (143 / 157, 144 / 157),
    "powlocalnew": (140 / 157, 147 / 157), "r18": (15 / 60, 39 / 60),
}
for s, (ae, ag) in EXPECTED_ACC.items():
    check(f"{s}.acc_exact", strata[s]["acc_exact"], ae)
    check(f"{s}.acc_guarded", strata[s]["acc_guarded"], ag)

# ---- temperature scaling under equal-width (same NLL fits) ----
sealed_ts = load_json("results/tempscale.json")
ts_ew = {}
for name in ("pilot", "holdout-main", "cloud-new"):
    src = {"pilot": "pilot", "holdout-main": "holdout-main"}.get(name, None)
    if name == "cloud-new":
        rows = cn
    else:
        rows = [r for r in d2 if r["source"] == name]
    confs = [float(r["confidence"]) for r in rows]
    outs = [int(guarded_tolerant_match(r["predicted_label"], r["gold_answer"]))
            for r in rows]
    T_star = sealed_ts["strata"][name]["T_star"]
    nll_1 = round(nll(confs, outs, 1.0), 4)
    nll_s = round(nll(confs, outs, T_star), 4)
    check(f"ts.{name}.NLL_T1", nll_1, sealed_ts["strata"][name]["NLL_T1"])
    check(f"ts.{name}.NLL_Tstar", nll_s, sealed_ts["strata"][name]["NLL_Tstar"])
    e1 = round(ece_equal_width(confs, outs), 4)
    es = round(ece_equal_width([scale(p, T_star) for p in confs], outs), 4)
    ts_ew[name] = {"n": len(rows), "T_star": T_star, "NLL_T1": nll_1,
                   "NLL_Tstar": nll_s, "EW_T1": e1, "EW_Tstar": es,
                   "dEW": round(e1 - es, 4)}

# ---- isotonic under equal-width (same PAV + CV folds) ----
iso_ew = {}
for name in ("pilot", "holdout-main", "cloud-new"):
    if name == "cloud-new":
        rows = cn
    else:
        rows = [r for r in d2 if r["source"] == name]
    sub = sorted([(float(r["confidence"]),
                   int(guarded_tolerant_match(r["predicted_label"],
                                              r["gold_answer"]))) for r in rows],
                 key=lambda r: r[0])
    confs = [c for c, _ in sub]
    ys = [y for _, y in sub]
    n = len(sub)
    fit = pav(ys)
    ece_raw = round(ece_equal_width(confs, ys), 4)
    ece_in = round(ece_equal_width(fit, ys), 4)
    cv_ps, cv_ys = [], []
    for f in range(5):
        te = [i for i in range(n) if i % 5 == f]
        tr = [i for i in range(n) if i % 5 != f]
        tr_xy = sorted([(confs[i], ys[i]) for i in tr], key=lambda r: r[0])
        tr_fit = pav([y for _, y in tr_xy])
        train_map = sorted(set(zip([x for x, _ in tr_xy], tr_fit)))
        for i in te:
            x = confs[i]
            cand = [v for (xx, v) in train_map if xx <= x + 1e-12]
            cv_ps.append(cand[-1] if cand else train_map[0][1])
            cv_ys.append(ys[i])
    ece_cv = round(ece_equal_width(cv_ps, cv_ys), 4)
    nll_c = nll_of(cv_ps, cv_ys)
    sealed_iso = load_json("results/isotonic.json")["strata"][name]
    check(f"iso.{name}.NLL_cv", nll_c, sealed_iso["NLL_isotonic_cv5"])
    iso_ew[name] = {"n": n, "n_blocks": len(set(round(v, 9) for v in fit)),
                    "EW_raw": ece_raw, "EW_insample": ece_in,
                    "dEW_insample": round(ece_raw - ece_in, 4),
                    "EW_cv5": ece_cv, "NLL_raw": nll_of(confs, ys),
                    "NLL_cv5": nll_c}

out = {"convention": "equal-width 10-bin ECE governs the main table; "
                     "equal-frequency retained for the appendix",
       "strata": strata, "tempscale_equalwidth": ts_ew,
       "isotonic_equalwidth": iso_ew,
       "validation_log": LOG}
(KB / "results" / "ece_unified.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("\n".join(LOG))
print("WROTE results/ece_unified.json")
print(json.dumps({s: {k: v[k] for k in ("ew_exact", "ew_guarded")}
                  for s, v in strata.items() if s in
                  ("pilot", "holdout-main", "cloud-new")}, indent=2))
print(json.dumps({"tempscale_ew": ts_ew, "isotonic_ew": iso_ew}, indent=2))
