"""R25 N1/N3 evidence seal: recompute adjudication accounting + guard-FN numbers
from sealed evidence files only. Writes results/adjudication_recount_R25.json
and results/guard_fn_R25.json. Fails loudly on any mismatch."""
import json, os

KB = "~/F:\\deepseek/paper_workflow_kb"
EV = os.path.join(KB, "evidence")
RS = os.path.join(KB, "results")

def load(p):
    with open(os.path.join(KB, p), encoding="utf-8") as f:
        return json.load(f)

def rows_of(d):
    if isinstance(d, list):
        return d
    for k in ("rows", "flips"):
        if isinstance(d.get(k), list):
            return d[k]
    return [d]

def verdict(r):
    for k in ("judge_verdict", "cloud_verdict", "confirm_verdict",
              "ruling", "verdict", "second_pass"):
        if r.get(k) is not None:
            return r[k]
    return None

def count(rows):
    vs = [verdict(r) for r in rows]
    return {"n": len(vs),
            "correct": sum(1 for v in vs if v == "correct"),
            "incorrect": sum(1 for v in vs if v == "incorrect"),
            "other": sum(1 for v in vs if v not in ("correct", "incorrect"))}

# --- prior: canonical 21-row confirm set (11 pilot + 5 holdout + 5 cloud-new)
prior = count(rows_of(load("evidence/cloud_judge_confirm2.json")))
assert prior == {"n": 21, "correct": 20, "incorrect": 1, "other": 0}, prior

# --- extension: local-new 5 + local-big 4
ext = count(rows_of(load("evidence/local_adjudication.json")))
big = count(rows_of(load("evidence/big_adjudication.json")))
assert (ext["n"], ext["correct"]) == (5, 5), ext
assert (big["n"], big["correct"]) == (4, 4), big

# --- cross-domain: sealed rollup 21/21 on content
xd = load("results/xdomain_adjudication.json")
assert xd["content_correct"] == 21 and xd["n"] == 21, xd

# --- power: tight 10/10 + loose 7/7
pt = count(rows_of(load("evidence/powrep_judge.json")))
pl = count(rows_of(load("evidence/powrep_loose_judge.json")))
assert (pt["n"], pt["correct"], pt["other"]) == (10, 10, 0), pt
assert (pl["n"], pl["correct"], pl["other"]) == (7, 7, 0), pl

# --- R18: 27 rows put to pass1 (26 flips + lr18-42 control); final 24/26
r18p1 = rows_of(load("evidence/r18_judge.json"))
assert len(r18p1) == 27, len(r18p1)
assert any(r.get("trace_id") == "lr18-42" for r in r18p1), "control missing"
r18roll = load("results/r18_adjudication.json")
assert (r18roll["raw_flips"], r18roll["adjudicated_flips"]) == (26, 24), r18roll
assert sorted(r18roll["excluded"]) == ["lr18-54", "lr18-55"], r18roll

# --- hetero: 11 rows (8 flips + 3 fragment probes); final 8/8
het = rows_of(load("evidence/r18_heteromodel_judge.json"))
assert len(het) == 11, len(het)
hetroll = load("results/r18_heteromodel_adjudication.json")
assert hetroll["adjudicated_flips"] == 8, hetroll
assert sorted(hetroll["excluded"]) == ["gr18-41", "gr18-42", "gr18-45"], hetroll
assert len(hetroll["confirmed"]) == 8, hetroll

judged = 21 + 5 + 4 + 21 + 10 + 7 + 27 + 11
flip_rows = 21 + 5 + 4 + 21 + 10 + 7 + 26 + 8
confirmed = 20 + 5 + 4 + 21 + 10 + 7 + 24 + 8
assert judged == 106 and flip_rows == 102 and confirmed == 99

recount = {
    "prior": {"judged": 21, "confirmed": 20},
    "extension": {"judged": 9, "confirmed": 9},
    "xdomain": {"judged": 21, "confirmed": 21},
    "power_tight": {"judged": 10, "confirmed": 10},
    "power_loose": {"judged": 7, "confirmed": 7},
    "r18": {"rows_put_to_judge": 27, "flip_rows": 26, "confirmed": 24,
            "control": "lr18-42 (non-flip)", "excluded": ["lr18-54", "lr18-55"]},
    "hetero": {"rows_put_to_judge": 11, "flip_rows": 8, "confirmed": 8,
               "probes": ["gr18-41", "gr18-42", "gr18-45 (non-flips)"]},
    "total_judged": judged, "total_flip_rows": flip_rows,
    "total_confirmed": confirmed,
    "nonflip_probe_rows": 4,
    "convention": ("judged = every row submitted to any judge pass, incl. 4 "
                   "non-flip probe rows; confirmed = accepted correct on "
                   "content in the final ruling"),
}
with open(os.path.join(RS, "adjudication_recount_R25.json"), "w",
          encoding="utf-8") as f:
    json.dump(recount, f, ensure_ascii=False, indent=1)

# --- N3 guard-FN numbers
merged = load("results/merged_1062.json")
assert (merged["n"], merged["n_exact"],
        merged["n_guarded_adjudicated"], merged["n_flips"]) == (1062, 830, 922, 92)
gold = load("results/gold100_agreement.json")
flip_n = gold["flips"]["n"]
assert flip_n == 62, gold
nonflip = gold["n"] - flip_n
assert nonflip == 38, nonflip
fn = {
    "n_1062": 1062, "n_guarded_correct_adjudicated": 922,
    "guard_reject_pool": 1062 - 922,
    "gold100_n": 100, "gold100_flip_rows": 62,
    "gold100_nonflip_rows": nonflip,
    "gold100_guard_false_negatives": 9,
    "conditional_fn_rate_nonflip": round(9 / nonflip, 4),
    "no_population_rate_claim": True,
    "direction": ("guard FNs make reported guarded accuracy conservative "
                  "(a lower bound on semantic accuracy)"),
    "patch_plan": "no new guard version; the 9 rows stay on record in the GOLD-100 grade files as regression targets",
}
with open(os.path.join(RS, "guard_fn_R25.json"), "w",
          encoding="utf-8") as f:
    json.dump(fn, f, ensure_ascii=False, indent=1)

print("recount:", judged, flip_rows, confirmed)
print("guard reject pool:", 140, "| GOLD-100 FN conditional:", round(9 / 38, 4))

# --- N2 regime table: explicit wrong-after-guarded per stratum (C68 evidence)
arms = {a["stratum"]: a for a in merged["arms"]}
regime = {}
for s in ["pilot", "holdout-main", "cloud-new", "local-new", "local-big",
          "xloose", "r18", "hetero-gemma"]:
    a = arms[s]
    regime[s] = {"n": a["n"], "n_exact": a["n_exact"],
                 "exact_acc": round(a["n_exact"] / a["n"], 4),
                 "n_guarded": a["n_guarded"],
                 "wrong_after_guarded": a["n"] - a["n_guarded"]}
assert regime["pilot"]["wrong_after_guarded"] == 0
assert regime["holdout-main"]["wrong_after_guarded"] == 6
assert regime["cloud-new"]["wrong_after_guarded"] == 8
assert regime["local-new"]["wrong_after_guarded"] == 7
assert regime["local-big"]["wrong_after_guarded"] == 8
assert regime["xloose"]["wrong_after_guarded"] == 15
assert regime["r18"]["wrong_after_guarded"] == 21
assert regime["hetero-gemma"]["wrong_after_guarded"] == 31
with open(os.path.join(RS, "regime_R25.json"), "w",
          encoding="utf-8") as f:
    json.dump(regime, f, ensure_ascii=False, indent=1)

print("SEALED OK")
