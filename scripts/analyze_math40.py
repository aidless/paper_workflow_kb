"""Analyze cloud-math stratum (40 fresh MATH questions, cloud qwen2.5:7b) + merge N=410.

Guarded basis (v3.1). ECE mirrors analyze_new60.py (equal-width 10 bins).
Zero flips -> McNemar degenerate (b=c=0, p_two=1.0, disclosed); power ceiling
not computable from zero discordants (disclosed, no assumed effect plugged in).
H1 on math is NOT-SUPPORT (0% <= 5%): boundary condition, G006 needs no adjudication.
Outputs results/math40.json + results/analysis_410.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v31 import norm, guarded_tolerant_match  # noqa: E402


def ece10_binned(rows, key):
    """Copied verbatim from analyze_new60.py (equal-width 10 bins on confidence)."""
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


def exact_match(a, g):
    a2, g2 = norm(a), norm(g)
    return bool(a2 and g2 and a2 == g2)


rows = json.loads((HERE / "evidence" / "cloud_math40_raw.json").read_text(encoding="utf-8"))
for r in rows:
    r["exact"] = exact_match(r["predicted_label"], r["gold_answer"])
    r["guarded"] = guarded_tolerant_match(r["predicted_label"], r["gold_answer"])
n = len(rows)
n_e = sum(1 for r in rows if r["exact"])
n_g = sum(1 for r in rows if r["guarded"])
flips = [r for r in rows if r["exact"] != r["guarded"]]
b = sum(1 for r in rows if (not r["exact"]) and r["guarded"])
cc = sum(1 for r in rows if r["exact"] and (not r["guarded"]))
assert b == 0 and cc == 0 and not flips
out = {"n": n, "n_exact": n_e, "n_guarded": n_g,
       "acc_exact": round(n_e / n, 4), "acc_guarded": round(n_g / n, 4),
       "n_flips": 0, "flip_rate": 0.0, "mcnemar_b": 0, "mcnemar_c": 0,
       "mcnemar_p_two": 1.0, "mcnemar_note": "degenerate: no discordant pairs",
       "ece10_exact": ece10_binned(rows, "exact"), "ece10_guarded": ece10_binned(rows, "guarded"),
       "ece_note": "equal-width 10 bins (sibling of live strata); all 40 rows carry confidences",
       "H1": "NOT-SUPPORT (0.0 <= 0.05): boundary condition, no adjudication per G006",
       "power_note": "ceiling not computable from zero discordants; no assumed effect plugged in",
       "model": "qwen2.5:7b", "temperature": 0, "host": "cloud seetacloud-h3 RTX 3090"}
(HERE / "results" / "math40.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
m180 = json.loads((HERE / "results" / "analysis_180.json").read_text(encoding="utf-8"))
md = m180["merged_descriptive"]
merged = {"n": md["n"] + n, "n_exact": md["n_exact"] + n_e,
          "n_guarded_adjudicated": md["n_guarded_adjudicated"] + n_g,
          "n_flips_guarded_basis": md["n_flips_guarded_basis"] + 0,
          "note": "pooled descriptive only"}
acc_e = round(merged["n_exact"] / merged["n"], 4)
merged["acc_exact"] = acc_e
merged["acc_guarded"] = round(merged["n_guarded_adjudicated"] / merged["n"], 4)
merged["flip_rate_guarded_basis"] = round(merged["n_flips_guarded_basis"] / merged["n"], 4)
assert merged["n"] == 220, merged
(HERE / "results" / "analysis_410.json").write_text(
    json.dumps({"strata": {"prior_180": md, "cloud_math": out},
                "merged_descriptive": merged,
                "N_status": "220 rows in five QA strata + 190 calibration rows (30+30+60+60+40 QA; inference stratified per stratum). Math is a second question family (boundary: H1 not supported)."},
               ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
print("MERGED220-QA + N=410 total")
