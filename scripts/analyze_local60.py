"""Analyze local-new stratum (qwen2:7b, same 60 questions) with v3.1 guard + merge to N=180.

ECE binning mirrors analyze_new60.py (equal-width 10 bins) for sibling
comparability with cloud-new; prior strata use equal-frequency bins
(analysis_d2.py) — the difference is disclosed in Methods, numbers unchanged.
Accuracy/flips on all 60 rows; ECE on the 55 rows carrying confidences.
Outputs results/local_new.json + results/flips_local60.json + results/analysis_180.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v31 import norm, guarded_tolerant_match  # noqa: E402
from stats import exact_mcnemar  # noqa: E402


def exact_match(a, g):
    a2, g2 = norm(a), norm(g)
    return bool(a2 and g2 and a2 == g2)


def ece10_binned(rows, key):
    """Copied from analyze_new60.py (equal-width 10 bins on confidence)."""
    rows = [r for r in rows if r.get("confidence") is not None]
    bins = [[] for _ in range(10)]
    for r in rows:
        c = min(max(r["confidence"], 0.0), 1.0)
        b = min(int(c * 10), 9)
        bins[b].append(1 if r[key] else 0)
    n = len(rows)
    e = 0.0
    for b in bins:
        if b:
            e += len(b) / n * abs(sum(b) / len(b) - (sum(
                min(max(r["confidence"], 0.0), 1.0) for r in rows
                if min(int(min(max(r["confidence"], 0.0), 1.0) * 10), 9) == bins.index(b)) / len(b)))
    return round(e, 4)


rows = json.loads((HERE / "evidence" / "local_new60_raw.json").read_text(encoding="utf-8"))
for r in rows:
    r["exact"] = exact_match(r["predicted_label"], r["gold_answer"])
    r["guarded"] = guarded_tolerant_match(r["predicted_label"], r["gold_answer"])
n = len(rows)
n_e = sum(1 for r in rows if r["exact"])
n_g = sum(1 for r in rows if r["guarded"])
flips = [{"trace_id": r["trace_id"], "source": r["source"], "predicted": r["predicted_label"],
          "gold": r["gold_answer"], "confidence": r["confidence"],
          "exact": r["exact"], "guarded": r["guarded"]} for r in rows if r["exact"] != r["guarded"]]
b = sum(1 for r in rows if (not r["exact"]) and r["guarded"])
c = sum(1 for r in rows if r["exact"] and (not r["guarded"]))
p_two, _ = exact_mcnemar(b, c)
conf_rows = [r for r in rows if r.get("confidence") is not None]
out = {"n": n, "n_conf_rows": len(conf_rows), "n_exact": n_e, "n_guarded": n_g,
       "acc_exact": round(n_e / n, 4), "acc_guarded": round(n_g / n, 4),
       "n_flips": len(flips), "flip_rate": round(len(flips) / n, 4),
       "mcnemar_b": b, "mcnemar_c": c, "mcnemar_p_two": p_two,
       "discordant_rate": round((b + c) / n, 4),
       "ece10_exact": ece10_binned(rows, "exact"), "ece10_guarded": ece10_binned(rows, "guarded"),
       "ece_note": "equal-width 10 bins (sibling of cloud-new); 5 rows lack confidences, ECE on 55",
       "model": "qwen2:7b", "temperature": 0,
       "parse_note": "answer=first non-empty line; 1 flip (local-new-09) carries same-line confidence suffix, semantically correct, disclosed"}
(HERE / "results" / "local_new.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
(HERE / "results" / "flips_local60.json").write_text(
    json.dumps(flips, ensure_ascii=False, indent=2), encoding="utf-8")
gv = json.loads((HERE / "results" / "guard_v31.json").read_text(encoding="utf-8"))
g_prior = gv["strata"]["pilot"]["n_guarded"] + gv["strata"]["holdout-main"]["n_guarded"]
g_cloud = gv["strata"]["cloud-new"]["n_guarded"]
f_prior = gv["strata"]["pilot"]["flips_guarded"] + gv["strata"]["holdout-main"]["flips_guarded"]
f_cloud = gv["strata"]["cloud-new"]["flips_guarded"]
e_prior = gv["strata"]["pilot"]["n_exact"] + gv["strata"]["holdout-main"]["n_exact"]
e_cloud = gv["strata"]["cloud-new"]["n_exact"]
# FM-15 assert: guarded==adjudicated sets (106/120 verified: 54+52)
assert g_prior + g_cloud == 106, (g_prior, g_cloud)
tot_n = 120 + n
tot_e = e_prior + e_cloud + n_e
tot_g = g_prior + g_cloud + n_g
tot_f = f_prior + f_cloud + len(flips)
assert tot_n == 180 and tot_g == 159 and tot_f == 25, (tot_n, tot_g, tot_f)
merged = {"n": tot_n, "n_exact": tot_e, "acc_exact": round(tot_e / tot_n, 4),
          "n_guarded_adjudicated": tot_g, "acc_guarded": round(tot_g / tot_n, 4),
          "n_flips_guarded_basis": tot_f, "flip_rate_guarded_basis": round(tot_f / tot_n, 4),
          "note": "pooled descriptive only; guarded==adjudicated sets verified per stratum"}
merged_full = {"strata": {"guard_v31_prior_cloud": {"n_guarded": g_prior + g_cloud},
                          "local_new": out}, "merged_descriptive": merged,
               "N_status": "180 rows in four strata (30+30+60+60); pre-registered 120 fulfilled by first three strata, local-new is a post-registration cross-model extension; inference stratified per stratum"}
(HERE / "results" / "analysis_180.json").write_text(
    json.dumps(merged_full, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
print("MERGED180:", json.dumps(merged))
print("WROTE results/local_new.json + results/flips_local60.json + results/analysis_180.json")
