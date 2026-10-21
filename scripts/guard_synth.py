"""R18 P2-1 (C5): guard synthetic precision/recall + CJK-miss quantification.

DESIGN (committed before run; author-labeled ground truth, disclosed):
- Class F (n=12, TRUE REJECT): formula-confusable substring pairs, chemically
  distinct, gold len>=2 (so v3 substring branch fires), both sides short-ASCII.
  Expect v3=True, guarded=False (guard-caused flips). Measures guard RECALL
  on its target class + PRECISION denominator.
- Class A (n=12, TRUE ACCEPT): exact-after-norm (3), suffix-stripped (3),
  synonym (3), CJK full-name containment same-person (3). Expect guarded=True
  everywhere (no guard over-fire). Measures guard SPECIFICITY on accepts.
- Class C (n=8, TRUE REJECT): CJK single-char fragments (4 observed:
  lr18-42, gr18-41/42/45 + 4 author-labeled: 李/李白， 杜/杜甫， 苏/苏轼，
  王/王安石）. R22: expect guarded=False (v33 CJK single-char guard catches
  all 8; was guarded=True miss by construction under v3.1/v3.2). The stated
  limitation is now a measured fix.
- Class R (real data): all 92 confirmed flips reconstructed from sealed
  raws + exclusion lists -> assert guarded-True (92/92); all 7 excluded/
  divergent flips -> assert guarded-True (inventory of known guard-misses:
  G06, lr18-42/54/55, gr18-41/42/45); 3 regression anchors (pilot-03,
  cloud-new-48 accept; cloud-new-42 reject).
- v3.2 vs v3.3 differences asserted to be exactly the 11 single-CJK rows
  (8 synthetic-C + 3 hetero-excluded) on every synthetic + real row.

Writes results/guard_synth.json. Exit nonzero on any violated expectation.
"""
import json
import sys
from pathlib import Path

KB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KB / "scripts"))
from label_match_v3 import tolerant_match as v3  # noqa: E402
from label_match_v31 import guarded_tolerant_match as g31  # noqa: E402 (reference only)
from label_match_v32 import tolerant_match_v32 as g32  # noqa: E402 (reference only)
from label_match_v33 import tolerant_match_v33 as g33  # noqa: E402 (R22 promotion: primary)
from label_match_v3 import norm  # noqa: E402

LOG = []


def check(name, got, want):
    ok = got == want
    LOG.append(f"[{'OK' if ok else 'MISMATCH'}] {name}: got={got} want={want}")
    if not ok:
        raise SystemExit(f"MISMATCH {name}: got={got} want={want}")


def load_json(p):
    return json.loads((KB / p).read_text(encoding="utf-8"))


def load_jsonl(p):
    return [json.loads(l) for l in (KB / p).read_text(encoding="utf-8").splitlines()
            if l.strip()]


# ---------------- synthetic classes (pred, gold, label) ----------------
F = [("O", "O2"), ("H", "H2"), ("C", "CO"), ("N", "N2"), ("O", "O3"),
     ("C", "Ca"), ("P", "Pb"), ("S", "SO2"), ("K", "KCl"), ("C", "Cl"),
     ("N", "Na"), ("F", "Fe")]
A = [("O2", " o2"), ("CO2", "co2"), ("H2O", "h2o"),
     ("5米", "5"), ("3年", "3"), ("10元", "10"),
     ("不会", "否"), ("不是", "否"), ("会", "是"),
     ("东坡居士", "东坡"), ("鲁迅", "鲁迅先生"), ("苏东坡", "东坡")]
C = [("牧", "牧之"), ("白", "太白"), ("子", "子美"), ("玄", "玄德"),
     ("李", "李白"), ("杜", "杜甫"), ("苏", "苏轼"), ("王", "王安石")]

res = {"design": "F=12 true-reject formula; A=12 true-accept; C=8 true-reject CJK",
       "classes": {}}

f_v3 = [int(v3(a, g)) for a, g in F]
f_g = [int(g33(a, g)) for a, g in F]
check("F.v3_all_accept", sum(f_v3), 12)
check("F.guarded_all_block", sum(f_g), 0)
res["classes"]["F"] = {"n": 12, "v3_accept": sum(f_v3),
                       "guarded_accept": sum(f_g),
                       "recall_target_class": "12/12 blocked",
                       "precision": "12/12 (no A-class blocked; see below)"}

a_g = [int(g33(a, g)) for a, g in A]
check("A.guarded_all_accept", sum(a_g), 12)
res["classes"]["A"] = {"n": 12, "guarded_accept": sum(a_g),
                       "specificity_accepts": "12/12 (zero over-fire)"}

c_g = [int(g33(a, g)) for a, g in C]
check("C.guarded_all_caught", sum(c_g), 0)  # R22: v33 catches all 8 single-char fragments
res["classes"]["C"] = {"n": 8, "guarded_accept": sum(c_g),
                       "catch_rate": "8/8 rejected under v33 (R22 patch); "
                                     "was 8/8 missed under v3.1/v3.2 by construction"}

# ---------------- real-data classes ----------------
def rows_of(path, key="rows"):
    return load_json(path)[key]


def ok_rows(rows, *vkeys):
    out = []
    for r in rows:
        for k in vkeys:
            if k in r and str(r[k]).lower() == "correct":
                out.append((r["trace_id"],
                            r.get("predicted", r.get("predicted_stripped", "")),
                            r["gold"]))
                break
    return out


confirmed = []
confirmed += ok_rows(rows_of("evidence/cloud_judge_16.json"), "cloud_verdict")
confirmed += ok_rows(rows_of("evidence/cloud_judge_new60.json"), "cloud_verdict")
confirmed += [(r["trace_id"], r["predicted"], r["gold"])
              for r in rows_of("evidence/local_adjudication.json")]
confirmed += [(r["trace_id"], r["predicted"], r["gold"])
              for r in rows_of("evidence/big_adjudication.json")]
confirmed += ok_rows(rows_of("evidence/xdomain_judge.json"), "judge_verdict")
confirmed += [(r["trace_id"], r["predicted_stripped"], r["gold"])
              for r in rows_of("evidence/xdomain_judge_pass2.json")
              if str(r.get("second_pass", "")).lower() == "correct"]
confirmed += ok_rows(rows_of("evidence/powrep_judge.json"), "judge_verdict")

r18raw = {r["trace_id"]: r for r in
          load_json("evidence/r18_loose_rep60_raw.json")}
hetraw = {r["trace_id"]: r for r in
          load_json("evidence/r18_heteromodel_gemma60_raw.json")}
adj18 = load_json("results/r18_adjudication.json")
adjhet = load_json("results/r18_heteromodel_adjudication.json")
# confirmed = flips minus excluded (no c-cells anywhere: all c=0, asserted)
all18 = {f["trace_id"] for f in
         load_json("results/r18_loose_rep.json")["loose_rep"]["flips"]}
assert all(not t.endswith(":c-cell") for t in all18)
conf18 = sorted(all18 - set(adj18["excluded"]))
for tid in conf18:
    r = r18raw[tid]
    confirmed.append((tid, r["predicted_label"], r["gold_answer"]))
for tid in adjhet["confirmed"]:
    r = hetraw[tid]
    confirmed.append((tid, r["predicted_label"], r["gold_answer"]))

# dedup by trace_id (xdomain pass1/pass2 overlap)
seen, conf_u = set(), []
for t, a, g in confirmed:
    if t not in seen:
        seen.add(t)
        conf_u.append((t, a, g))
confirmed = conf_u
LOG.append(f"[INFO] confirmed flips reconstructed: {len(confirmed)}")
check("confirmed_n", len(confirmed), 92)

conf_g = [int(g33(a, g)) for _, a, g in confirmed]
check("confirmed_guarded_all_accept", sum(conf_g), 92)
res["classes"]["R_confirmed"] = {"n": 92, "guarded_accept": sum(conf_g),
                                 "recall_confirmed": "92/92"}

# excluded/divergent 7: G06 + R18 3 + hetero 3 -> all guarded-True (known misses)
excl = [("cloud-new-42", "O", "O2")]
for tid in adj18["excluded"]:
    r = r18raw[tid]
    excl.append((tid, r["predicted_label"], r["gold_answer"]))
for tid in adjhet["excluded"]:
    r = hetraw[tid]
    excl.append((tid, r["predicted_label"], r["gold_answer"]))
check("excluded_n", len(excl), 6)  # R22: lr18-42 no longer a flip
excl_g = [int(g33(a, g)) for _, a, g in excl]
check("excluded_guarded_accept", sum(excl_g), 2)  # R22: only lr18-54/55 echo accepted
check("excluded_G06_guard_caught", excl_g[0], 0)
res["classes"]["R_excluded"] = {
    "n": 6, "guarded_accept": sum(excl_g),
    "note": "R22 v33: 2 accepted-but-excluded (lr18-54/55 echo rows: judge-majority excluded, author-noted "
            "correct: instrument divergence, see text) + 4 guard-caught (G06 formula FP + gr18-41/42/45 CJK "
            "fragments now rejected by the CJK single-char guard); lr18-42 no longer a flip under v33"}

# regression anchors
d2 = {r["trace_id"]: r for r in load_jsonl("evidence/d2_60.jsonl")}
cnraw = {r["trace_id"]: r for r in load_json("evidence/cloud_new60_raw.json")}
p03 = d2["pilot-03"]
c48 = cnraw["cloud-new-48"]
c42 = cnraw["cloud-new-42"]
check("anchor_pilot03_accept",
      int(g33(p03["predicted_label"], p03["gold_answer"])), 1)
check("anchor_cn48_accept",
      int(g33(c48["predicted_label"], c48["gold_answer"])), 1)
check("anchor_cn42_reject",
      int(g33(c42["predicted_label"], c42["gold_answer"])), 0)

# v3.1 vs v3.2 agreement on every row touched
allpairs = (F + A + C + [(a, g) for _, a, g in confirmed]
            + [(a, g) for _, a, g in excl])
diffs = [(a, g) for a, g in allpairs if bool(g32(a, g)) != bool(g33(a, g))]
LOG.append(f"[INFO] v3.2-vs-v3.3 diffs on {len(allpairs)} rows: {len(diffs)}")
check("v32_v33_diffs", len(diffs), 11)  # R22: 8 synthetic-C + 3 hetero-excluded singles

out = {"labels": "author-labeled synthetic (F/A/C) + sealed judge rows (R)",
       "guard_rule": "v3.1 formula guard + v3.3 CJK single-char substring guard (see label_match_v33.V33_RULE)",
       "results": res,
       "summary": {"formula_recall": "12/12", "formula_precision": "12/12",
                   "accept_specificity": "12/12", "cjk_catch": "8/8 rejected (v33 patch)",
                   "confirmed_recall": "92/92", "excluded_inventory": "2/6 accept + 4 guard-caught",
                   "v32_v33_diffs": f"{len(diffs)}/{len(allpairs)} (all single-CJK class)"},
       "validation_log": LOG}
(KB / "results" / "guard_synth.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("\n".join(LOG))
print("WROTE results/guard_synth.json")
