"""Analyze local-big (n=160) + local-en (n=30) strata, guarded basis + qwen2:7b combined.

Mirrors analyze_local60.py (equal-width 10-bin ECE on conf rows; accuracy/flips
on all rows). Combined pool local-new(60)+local-big(160)=220 same-model rows
pre-specified for the powered McNemar check (n_ceil=217).
Outputs results/local_big.json + results/local_en.json + results/flips_big.json
+ results/flips_en.json + results/combined_qwen2.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v31 import norm, guarded_tolerant_match  # noqa: E402
from stats import exact_mcnemar  # noqa: E402


def exact_match(a, g):
    """Copied from analyze_new60.py."""
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


def analyze(raw_name, out_name, flips_name, model_note):
    rows = json.loads((HERE / "evidence" / raw_name).read_text(encoding="utf-8"))
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
           "ece10_exact": ece10_binned(rows, "exact"),
           "ece10_guarded": ece10_binned(rows, "guarded"),
           "model": "qwen2:7b", "temperature": 0, "note": model_note}
    (HERE / "results" / out_name).write_text(json.dumps(out, ensure_ascii=False, indent=2),
                                             encoding="utf-8")
    (HERE / "results" / flips_name).write_text(json.dumps(flips, ensure_ascii=False, indent=2),
                                               encoding="utf-8")
    return out, flips


big, flips_big = None, None
if (HERE / "evidence" / "local_big_raw.json").exists():
    big, flips_big = analyze("local_big_raw.json", "local_big.json", "flips_big.json",
                             "powered extension batch (120 computed + 40 hand golds)")
    print("BIG:", json.dumps(big, ensure_ascii=False))
else:
    print("SKIP big (raw not ready)")
en, flips_en = analyze("local_en_raw.json", "local_en.json", "flips_en.json",
                       "English cross-type stratum (10 computed + 20 hand golds)")
print("EN:", json.dumps(en, ensure_ascii=False))
# combined same-model pool: local-new 60 + local-big 160 = 220
if big is not None:
    ln = json.loads((HERE / "results" / "local_new.json").read_text(encoding="utf-8"))
    tot_n = ln["n"] + big["n"]
    tot_e = ln["n_exact"] + big["n_exact"]
    tot_g = ln["n_guarded"] + big["n_guarded"]
    tot_f = ln["n_flips"] + big["n_flips"]
    tot_b = ln["mcnemar_b"] + big["mcnemar_b"]
    tot_c = ln["mcnemar_c"] + big["mcnemar_c"]
    p_two, _ = exact_mcnemar(tot_b, tot_c)
    combined = {"n": tot_n, "n_exact": tot_e, "acc_exact": round(tot_e / tot_n, 4),
                "n_guarded": tot_g, "acc_guarded": round(tot_g / tot_n, 4),
                "n_flips": tot_f, "flip_rate": round(tot_f / tot_n, 4),
                "mcnemar_b": tot_b, "mcnemar_c": tot_c, "mcnemar_p_two": p_two,
                "power_note": "n=220 >= n_ceil=217 (OR=4 placeholder); FIRST powered McNemar in this paper",
                "pool": "local-new(60, same 60 questions as cloud-new) + local-big(160, new questions); same model qwen2:7b temp 0; pre-specified"}
    (HERE / "results" / "combined_qwen2.json").write_text(
        json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")
    print("COMBINED220:", json.dumps(combined))
else:
    print("SKIP combined (big not ready)")
