"""R18 P1-3 (C4): GOLD-100 expert-grading package (build; grades pending human).

Composition (n=100, seeded RNG seed=100, asserts below):
- 7 excluded/divergent flips (census: G06, lr18-42/54/55, hr18-41/42/45).
- 55 confirmed flips, stratified: pilot 6, holdout 3, cloud-new 2, local-new 3,
  local-big 2, xtight 1, xloose 11, powrep-tight 5 (holdout-arm 2 + cloud-arm 1
  + local-arm 2), R18 14, hetero 5, loose-regime 3.
- 38 non-flips (exact==guarded), stratified across 13 strata, preferring
  both-wrong rows where available (tests grader agreement on negatives).

Blinding: global shuffle (seed 100), no outcomes in the sheet; stems included
where archived (d2 prior rows are stemless, disclosed like GOLD-25).
Key sealed at build: evidence/gold100_key.json (guarded outcomes for decode).
Sheet: gold100_grading_pack.csv (same columns as GOLD-25).
Grader: the human user. Decode: scripts/decode_gold100.py (gated on
grades_gold100_user.csv; agreement vs guarded + Wilson + FP-inventory check).

Writes: gold100_grading_pack.csv, GOLD100_README.md,
evidence/gold100_key.json. Exit nonzero on any violated expectation.
"""
import csv
import json
import random
import sys
from pathlib import Path

KB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KB / "scripts"))
from label_match_v31 import guarded_tolerant_match as g31  # noqa: E402
from label_match_v32 import tolerant_match_v32 as g32  # noqa: E402
# R22 FROZEN: this script is the v3.2-era historical record of how the sealed
# GOLD-100 selection was built (incl. the 7-excluded census with lr18-42).
# Under v3.3 lr18-42 is no longer a flip, so a from-scratch rebuild is
# intentionally unsupported (excl_n would be 6, not 7). Guarded-outcome
# promotion lives in scripts/promote_gold100_key_v33.py (surgical, audited);
# evidence/gold100_key.json is the sealed artifact. DO NOT re-run this build.
from label_match_v3 import norm  # noqa: E402

SEED = 100
rng = random.Random(SEED)
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


def rows_of(path):
    return load_json(path)["rows"]


def ok_rows(rows, *vkeys):
    out = []
    for r in rows:
        for k in vkeys:
            if k in r and str(r[k]).lower() == "correct":
                out.append(r)
                break
    return out


# ---- confirmed-flip pools (trace_id -> (pred, gold, stem, stratum)) ----
def reg(rows, stratum, out):
    for r in rows:
        out[r["trace_id"]] = (r.get("predicted", r.get("predicted_stripped", "")),
                              r["gold"], "", stratum)


pool = {}
reg(ok_rows(rows_of("evidence/cloud_judge_16.json"), "cloud_verdict"),
    "prior", pool)
reg(ok_rows(rows_of("evidence/cloud_judge_new60.json"), "cloud_verdict"),
    "cloud-new", pool)
for r in rows_of("evidence/local_adjudication.json"):
    pool[r["trace_id"]] = (r["predicted"], r["gold"], "", "local-new")
for r in rows_of("evidence/big_adjudication.json"):
    pool[r["trace_id"]] = (r["predicted"], r["gold"], "", "local-big")
reg(ok_rows(rows_of("evidence/xdomain_judge.json"), "judge_verdict"),
    "xdomain", pool)
for r in rows_of("evidence/xdomain_judge_pass2.json"):
    if str(r.get("second_pass", "")).lower() == "correct":
        pool[r["trace_id"]] = (r["predicted_stripped"], r["gold"], "",
                               "xdomain")
reg(ok_rows(rows_of("evidence/powrep_judge.json"), "judge_verdict"),
    "powrep", pool)
reg(ok_rows(rows_of("evidence/powrep_loose_judge.json"), "judge_verdict"),
    "powrep-loose", pool)

r18raw = {r["trace_id"]: r for r in load_json("evidence/r18_loose_rep60_raw.json")}
hetraw = {r["trace_id"]: r for r in
          load_json("evidence/r18_heteromodel_gemma60_raw.json")}
adj18 = load_json("results/r18_adjudication.json")
adjhet = load_json("results/r18_heteromodel_adjudication.json")
all18 = {f["trace_id"] for f in
         load_json("results/r18_loose_rep.json")["loose_rep"]["flips"]}
for tid in sorted(all18 - set(adj18["excluded"])):
    r = r18raw[tid]
    pool[tid] = (r["predicted_label"], r["gold_answer"], r.get("question", ""),
                 "r18")
for tid in adjhet["confirmed"]:
    r = hetraw[tid]
    pool[tid] = (r["predicted_label"], r["gold_answer"], r.get("question", ""),
                 "hetero")

# attach stems where archived (raws carry question except d2)
stem_by_tid = {}
for rp, gfn in (("evidence/cloud_new60_raw.json", g31),
                ("evidence/local_new60_raw.json", g31),
                ("evidence/local_big_raw.json", g31),
                ("evidence/cloud_xdomain60_raw.json", g31),
                ("evidence/cloud_xdomain60_loose_raw.json", g31),
                ("evidence/cloud_powrep255_raw.json", g32),
                ("evidence/local_powrep157_raw.json", g32),
                ("evidence/cloud_powrep255_loose_raw.json", g32),
                ("evidence/local_powrep157_loose_raw.json", g32)):
    for r in load_json(rp):
        if r.get("question"):
            stem_by_tid[r["trace_id"]] = r["question"]
for tid in pool:
    if tid in stem_by_tid:
        a, g, _, s = pool[tid]
        pool[tid] = (a, g, stem_by_tid[tid], s)

# split confirmed pool by stratum source prefix
prior = sorted(t for t in pool if t.startswith("pilot-")
               or t.startswith("holdout-"))
check("prior_pool_n", len(prior), 16)
cn = sorted(t for t in pool if t.startswith("cloud-new-"))
check("cn_pool_n", len(cn), 4)
ln = sorted(t for t in pool if t.startswith("local-new-"))
check("ln_pool_n", len(ln), 5)
lb = sorted(t for t in pool if t.startswith("local-big-"))
check("lb_pool_n", len(lb), 4)
xt = sorted(t for t in pool if t.startswith("xdomain-"))
xl = sorted(t for t in pool if t.startswith("xloose-"))
check("xdomain_pool_n", len(xt) + len(xl), 21)
p1h = sorted(t for t in pool if t.startswith("pow1-"))
p2 = sorted(t for t in pool if t.startswith("pow2-"))
pL = sorted(t for t in pool if t.startswith("powL-"))
check("powrep_pool_n", len(p1h) + len(p2) + len(pL), 10)
pl = sorted(t for t in pool if "L-" in t and t not in pL)
check("powrep_loose_pool_n", len(pl), 7)
r18c = sorted(t for t in pool if t.startswith("lr18-"))
check("r18_pool_n", len(r18c), 24)
hetc = sorted(t for t in pool if t.startswith("gr18-"))
check("het_pool_n", len(hetc), 8)
check("confirmed_pool_n", len(pool), 99)  # 92 main-regime + 7 loose-regime (judged 106, confirmed 99)

pilot_p = [t for t in prior if t.startswith("pilot-")]
hold_p = [t for t in prior if t.startswith("holdout-")]


def take(ids, k, tag):
    check(f"take_{tag}_pool", len(ids) >= k, True)
    return rng.sample(sorted(ids), k)


confirmed_sel = (take(pilot_p, 6, "pilot") + take(hold_p, 3, "holdout")
                 + take(cn, 2, "cn") + take(ln, 3, "ln") + take(lb, 2, "lb")
                 + take(xt, 1, "xt") + take(xl, 11, "xl") + take(p1h, 2, "p1h")
                 + take(p2, 1, "p2") + take(pL, 2, "pL") + take(r18c, 14, "r18")
                 + take(hetc, 5, "het") + take(pl, 3, "plo"))
check("confirmed_sel_n", len(confirmed_sel), 55)

# ---- excluded 7 (census) ----
excl = [("cloud-new-42", "O", "O2", "cloud-new")]
for tid in adj18["excluded"]:
    r = r18raw[tid]
    excl.append((tid, r["predicted_label"], r["gold_answer"], "r18"))
for tid in adjhet["excluded"]:
    r = hetraw[tid]
    excl.append((tid, r["predicted_label"], r["gold_answer"], "hetero"))
check("excl_n", len(excl), 7)

# ---- non-flip pools: exact==guarded per stratum basis ----
nonflip_spec = [
    # (raw_path, guard_fn, stratum, quota)
    ("evidence/cloud_new60_raw.json", g31, "cloud-new", 4),
    ("evidence/local_new60_raw.json", g31, "local-new", 4),
    ("evidence/local_big_raw.json", g31, "local-big", 4),
    ("evidence/local_en_raw.json", g31, "local-en", 3),
    ("evidence/cloud_math40_raw.json", g31, "math", 3),
    ("evidence/cloud_xdomain60_raw.json", g31, "xtight", 3),
    ("evidence/cloud_xdomain60_loose_raw.json", g31, "xloose", 2),
    ("evidence/cloud_powrep255_raw.json", g32, "powrep", 4),
    ("evidence/local_powrep157_raw.json", g32, "powrep", 0),
    ("evidence/r18_loose_rep60_raw.json", g32, "r18", 2),
    ("evidence/r18_heteromodel_gemma60_raw.json", g32, "hetero", 2),
    ("evidence/cloud_powrep255_loose_raw.json", g32, "powrep-loose", 1),
]


def exact_nn(a, g):
    a2, g2 = norm(a), norm(g)
    return bool(a2 and g2 and a2 == g2)


d2 = load_jsonl("evidence/d2_60.jsonl")
d2p = [r for r in d2 if r["source"] == "pilot"]
d2h = [r for r in d2 if r["source"] == "holdout-main"]
nonflip_sel = []
for rows, tag, q in ((d2p, "pilot", 3), (d2h, "holdout-main", 3)):
    nf = [(r["trace_id"], str(r.get("predicted_label", "")),
           str(r.get("gold_answer", "")), "", tag)
          for r in rows
          if int(exact_nn(r["predicted_label"], r["gold_answer"]))
          == int(g31(r["predicted_label"], r["gold_answer"]))]
    wrong = [x for x in nf if not exact_nn(x[1], x[2])]
    right = [x for x in nf if exact_nn(x[1], x[2])]
    nw = min(2, len(wrong), q) if wrong else 0
    sel = rng.sample(wrong, nw) if nw else []
    sel += rng.sample(right, q - len(sel))
    check(f"nonflip_{tag}_n", len(sel), q)
    nonflip_sel += sel

for rp, gfn, tag, q in nonflip_spec:
    if q == 0:
        continue
    rows = load_json(rp)
    if "powrep255" in rp and "loose" not in rp:
        rows = [r for r in rows if r["trace_id"].startswith(("pow1-", "pow2-"))]
    nf = [(r["trace_id"], str(r.get("predicted_label", "")),
           str(r.get("gold_answer", "")), str(r.get("question", "")), tag)
          for r in rows
          if int(exact_nn(r["predicted_label"], r["gold_answer"]))
          == int(gfn(r["predicted_label"], r["gold_answer"]))]
    wrong = [x for x in nf if not exact_nn(x[1], x[2])]
    right = [x for x in nf if exact_nn(x[1], x[2])]
    nw = min(2, len(wrong), q) if wrong else 0
    sel = rng.sample(wrong, nw) if nw else []
    sel += rng.sample(right, q - len(sel))
    check(f"nonflip_{tag}_{rp.split('/')[-1][:12]}_n", len(sel), q)
    nonflip_sel += sel
check("nonflip_sel_n", len(nonflip_sel), 38)

# ---- assemble, shuffle, write ----
items = []
for t in confirmed_sel:
    a, g, stem, s = pool[t]
    items.append({"kind": "flip-confirmed", "trace_id": t, "pred": a,
                  "gold": g, "stem": stem, "stratum": s})
for t, a, g, s in excl:
    items.append({"kind": "flip-excluded", "trace_id": t, "pred": a,
                  "gold": g, "stem": stem_by_tid.get(t, ""), "stratum": s})
for t, a, g, stem, s in nonflip_sel:
    items.append({"kind": "nonflip", "trace_id": t, "pred": a, "gold": g,
                  "stem": stem, "stratum": s})
check("items_n", len(items), 100)
rng.shuffle(items)

stem_n = sum(1 for it in items if it["stem"])
key = {"seed": SEED,
       "mapping": {},
       "counts": {"n_items": 100, "n_stem": stem_n,
                    "n_confirmed": 55, "n_excluded": 7, "n_nonflip": 38},
       "note": "guarded outcomes sealed for decode; grader sees no outcomes"}
with open(KB / "gold100_grading_pack.csv", "w", encoding="utf-8-sig",
          newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "question", "response", "reference", "你的判定(对/错)",
                "备注"])
    for i, it in enumerate(items, 1):
        hid = f"H{i:02d}"
        gfn = g32 if it["stratum"] in ("powrep", "powrep-loose", "r18",
                                       "hetero") else g31
        gout = int(gfn(it["pred"], it["gold"]))
        key["mapping"][hid] = {"kind": it["kind"], "trace_id": it["trace_id"],
                               "stratum": it["stratum"],
                               "guarded_outcome": gout}
        w.writerow([hid, it["stem"], it["pred"], it["gold"], "", ""])
(KB / "evidence" / "gold100_key.json").write_text(
    json.dumps(key, ensure_ascii=False, indent=2), encoding="utf-8")

LOG.append(f"[INFO] stem items: {stem_n}/100; "
           f"kinds: confirmed=55 excluded=7 nonflip=38")

readme = """# GOLD-100 专家标注包（真人 grading，盲评）

## 做什么
逐行判断 response 是否表达了 reference 的正确答案（语义等价，非字符串相等），
在 `你的判定(对/错)` 列填 对 或 错。可在"备注"列留理由（可选）。

## 规则
- 不要查本论文任何结果文件/账本（盲评；trace_id 已隐去，顺序已打乱）。
- 题干为空的行只看 response/reference 两列判定（与 GOLD-25 stemless 同类）。
- 完成后另存为 `grades_gold100_user.csv`（同目录），通知 agent 解码。

## 构成（供解码后核对， grading 时无需关心）
100 项＝7 个已知分歧翻转＋55 个已确认翻转（分层抽样）＋38 个非翻转行
（含两判皆错行，测负例一致性）。key 封存于 evidence/gold100_key.json。
预计 30-40 分钟。
"""
(KB / "GOLD100_README.md").write_text(readme, encoding="utf-8")
print("\n".join(LOG))
print("WROTE gold100_grading_pack.csv GOLD100_README.md evidence/gold100_key.json")
