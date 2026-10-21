# -*- coding: utf-8 -*-
"""Build blinded gold-grading pack (GOLD-25).

Design (pre-specified, mechanical):
- Sensitivity items: CENSUS of all 14 flips with stems
  (local-new 5 + cloud-new 5 + local-big 4). No sampling.
- Adjudication-core items: 11 of the 16 pilot/holdout flips
  (seeded sample, NO stems archived -> graded stemless with
  "存疑" escape hatch). Mechanical: random.Random(SEED).sample.
- Total 25, shuffled with seed 20260908, blind IDs G01..G25.
- Pack contains ONLY: blind ID, question stem (14 items; "（题干未存档）"
  for 11), model response, reference answer. NO trace_id, stratum,
  confidence, verdict, or rule-name leakage.
- Mapping sealed in evidence/gold_key.json (never delivered with pack).

Analysis plan (pre-specified): overall agreement + Wilson 95% CI;
stem vs stemless split reported. All 25 guarded outcomes are CORRECT
per evidence, so agreement is measured against unanimous-correct;
"存疑" grades count as non-agreeing-but-uncertain (reported separately,
excluded from denominator in a sensitivity analysis).
"""
import csv
import json
import random

BASE = "."
SEED = 20260908

STRATA = {
    "local-new": ("evidence/local_new60_raw.json", "results/flips_local60.json"),
    "cloud-new": ("evidence/cloud_new60_raw.json", "results/flips_new60.json"),
    "local-big": ("evidence/local_big_raw.json", "results/flips_big.json"),
}

LEAK_WORDS = ["correct", "incorrect", "verdict", "ruling", "同义词",
              "数值容差", "单位后缀", "子串", "否定", "tie-break"]


def load(p):
    with open(f"{BASE}/{p}", encoding="utf-8") as f:
        return json.load(f)


def pred_of(r):
    return r.get("predicted_label", r.get("predicted"))


def gold_of(r):
    return r.get("gold_answer", r.get("gold"))


items = []   # (kind, trace_id, stratum, question, predicted, gold)
key = {}     # blind_id -> provenance (sealed)
controls_plan = {}

for stratum, (raw_p, flip_p) in STRATA.items():
    raw = load(raw_p)
    by_id = {r["trace_id"]: r for r in raw}
    for fl in load(flip_p):
        tid = fl["trace_id"]
        q = fl.get("question") or by_id[tid].get("question", "")
        items.append(("flip-stem", tid, stratum, q, pred_of(fl),
                      fl.get("gold_answer", fl.get("gold"))))

# Adjudication core: 11/16 pilot+holdout flips, seeded sample, stemless
core16 = load("results/flips.json")
assert len(core16) == 16, len(core16)
rng = random.Random(SEED)
for fl in rng.sample(sorted(core16, key=lambda r: r["trace_id"]), 11):
    items.append(("flip-nostem", fl["trace_id"], fl.get("source", "?"),
                  "（题干未存档，仅凭作答与参考答案的常见语义判定；不确定填“存疑”）",
                  fl["predicted"], fl["gold"]))

n_stem = sum(1 for i in items if i[0] == "flip-stem")
n_nostem = sum(1 for i in items if i[0] == "flip-nostem")
assert n_stem == 14, n_stem
assert n_nostem == 11, n_nostem
assert len(items) == 25

rng.shuffle(items)

pack_rows = []
for n, (kind, tid, stratum, q, pred, gold) in enumerate(items, 1):
    bid = f"G{n:02d}"
    pack_rows.append({"id": bid, "question": q,
                      "response": pred, "reference": gold})
    key[bid] = {"kind": kind, "trace_id": tid, "stratum": stratum}

# Leakage scan on deliverables
blob = json.dumps(pack_rows, ensure_ascii=False).lower()
for w in LEAK_WORDS:
    assert w.lower() not in blob, f"LEAK: {w}"
for bid, prov in key.items():
    assert prov["trace_id"] not in blob, f"LEAK trace {prov['trace_id']}"

with open(f"{BASE}/evidence/gold_key.json", "w", encoding="utf-8") as f:
    json.dump({"seed": SEED, "mapping": key,
               "analysis_plan": "overall agreement + Wilson 95% CI; "
               "stem/stemless split; all 25 guarded=TRUE per evidence; "
               "'存疑' reported separately, excluded in sensitivity analysis"},
              f, ensure_ascii=False, indent=2)

with open("gold_grading_pack.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "question", "response",
                                      "reference", "你的判定(对/错)", "备注"])
    w.writeheader()
    for r in pack_rows:
        w.writerow({"id": r["id"], "question": r["question"],
                    "response": r["response"], "reference": r["reference"],
                    "你的判定(对/错)": "", "备注": ""})

lines = [
    "# 金集 Grading 包（GOLD-25，盲化）",
    "",
    "## 填写说明",
    "1. 对每一条，只看【题干】，判断【模型作答】与【参考答案】是否指向同一正确答案。",
    "2. 在 CSV 的“你的判定”列填 **对**（语义一致，作答算正确）或 **错**（语义不一致）。",
    "3. 置信度数字（如作答里夹带的 0.9）是模型输出原文，请忽略它，只判语义。",
    "4. 共 25 条（G01–G25），顺序已打乱；不要查论文手稿或与本任务讨论，每条独立判定。",
    "5. 填完把 CSV 发回，约 30–40 分钟。所有条目的原裁决均已隐去， {} 条含题干、 {} 条无题干（具体是哪些不告诉你）。".format(n_stem, n_nostem),
    "",
    "## 覆盖说明",
    "- 含数字/地名/常识多题型；11 条无题干条目来自早期批次（原始题干未存档），仅凭作答与参考答案的常见语义判定，吃不准就填“存疑”。",
    "- en/math 层零翻转故未纳入（现象缺席本身即证据）；将如实披露金集覆盖边界。",
    "",
    "## 条目（预览，填写请用 CSV）",
    "",
]
for r in pack_rows:
    lines += [f"### {r['id']}",
              f"- 题干：{r['question']}",
              f"- 模型作答：{r['response']}",
              f"- 参考答案：{r['reference']}",
              ""]
with open("gold_grading_pack.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"OK stem={n_stem} nostem={n_nostem} total=25 seed={SEED}")
