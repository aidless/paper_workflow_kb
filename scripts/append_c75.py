# -*- coding: utf-8 -*-
"""Append C75 (R29 power replication) to CLAIM_LEDGER.md. Idempotent."""
import io

PATH = "CLAIM_LEDGER.md"

C75 = (
    "| C75 | local-big 功效复测（R29，160→720）：合并 720 行（local-big 160 + topup 560，"
    "题池 scripts/r29_make_topup.py 生成、div 39 全整除 gold 可复算）；flip 19/720=0.0264，"
    "McNemar b19/c0/p=3.8147e-06 显著；裁决 14 flip_correct（.0 尾随 + 地名市/城/特区变体 + 置信度尾）"
    "＋ 5 over_fire（整除除法模型算错、误差<0.5% 被 numeric 容差误接受，新 over-fire 类）；"
    "n=720 达 n_ceil=720 欠功效消除；McNemar 显著 H1 维持不降级 | "
    "results/r29_power_seal.json -> merged.n / merged.n_flips / merged.flip_rate / "
    "merged.mcnemar_b / merged.mcnemar_c / merged.mcnemar_p_two / merged.n_flip_correct / "
    "merged.n_over_fire | "
    "720 / 19 / 0.0264 / 19 / 0 / 3.8147e-06 / 14 / 5 | "
    "scripts/r29_seal.py 唯一重算（assert n=720、flip=19、c=0、flip_rate=19/720、over_fire 14+5=19）；"
    "采集 scripts/r29_collect.py（qwen2:7b temp0）；裁决 scripts/r29_adjudicate.py；"
    "over-fire 类为 numeric 容差 0.5% 误接受除法算错（新 limitation，入正文） | verified |"
)

with io.open(PATH, encoding="utf-8") as f:
    text = f.read()

if C75 in text:
    print("C75 already present")
else:
    if not text.endswith("\n"):
        text += "\n"
    text += C75 + "\n"
    with io.open(PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("C75 appended")