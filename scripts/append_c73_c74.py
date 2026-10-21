# -*- coding: utf-8 -*-
"""Append C73/C74 (R28 cross-domain) to CLAIM_LEDGER.md. Idempotent."""
import io

PATH = "CLAIM_LEDGER.md"

C73 = (
    "| C73 | 跨域 Arm A（R28，数学，检验预测 i 退化变体空间）：本地 qwen2:7b 40 道算术题 temp0；"
    "exact 39 / guard 40 / flip 1 / over-fire 0；flip 为 r28-a-08「125.0」vs「125」（numeric .0 尾缀被"
    "数值等价分支覆盖，语义对非 over-fire）；预测 (i) 严格零翻转未达成（1/40=0.025），但描述性方向"
    "（<0.05）成立，正文已精化为「退化变体空间⇒近零翻转，除非数字格式变体被 numeric 覆盖」 | "
    "results/r28_seal.json -> arm_a_degenerate.n / arm_a_degenerate.n_exact / arm_a_degenerate.n_guard / "
    "arm_a_degenerate.n_flips / arm_a_degenerate.flip_rate / arm_a_degenerate.over_fire | "
    "40 / 39 / 40 / 1 / 0.025 / 0 | "
    "scripts/r28_seal.py 唯一重算（assert n=40、flip=1、over-fire=0、flip 行 trace r28-a-08 且裁决 "
    "flip_correct）；采集 scripts/r28_collect.py（题集内嵌冻结于预注册后、作答前）；裁决 scripts/r28_adjudicate.py；纯本地无云依赖 | verified |"
)

C74 = (
    "| C74 | 跨域 Arm B（R28，英文单位，检验预测 ii 覆盖缺失）：本地 qwen2:7b 40 道英文单位/计数题 temp0；"
    "flip 0（R 仅覆盖中文单位不覆盖英文单位），miss 21/40=0.525（Wilson95 [0.375,0.6706]），correct_reject 1"
    "（b-38 骰子点数模型答 6，gold 21）；预测 (ii) 成立：flip=0 且 miss>0（变体存在＋覆盖缺失证据） | "
    "results/r28_seal.json -> arm_b_uncovered.n / arm_b_uncovered.n_exact / arm_b_uncovered.n_guard / "
    "arm_b_uncovered.n_flips / arm_b_uncovered.n_miss / arm_b_uncovered.n_correct_reject / "
    "arm_b_uncovered.miss_rate / arm_b_uncovered.miss_wilson95[0] / arm_b_uncovered.miss_wilson95[1] | "
    "40 / 18 / 18 / 0 / 21 / 1 / 0.525 / 0.375 / 0.6706 | "
    "scripts/r28_seal.py 唯一重算（assert flip=0、miss=21、correct_reject=1、22 candidates）；"
    "裁决逐条作者判定（scripts/r28_adjudicate.py，60 seconds/52 weeks/2000 pounds 等英文单位变体不被 R 覆盖故 guard 全拒为 miss）；诱导设计显式披露 | verified |"
)

with io.open(PATH, encoding="utf-8") as f:
    text = f.read()

added = []
for row in (C73, C74):
    if row not in text:
        added.append(row)

if added:
    if not text.endswith("\n"):
        text += "\n"
    text += "\n".join(added) + "\n"
    with io.open(PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"added {len(added)} rows")
else:
    print("already present")