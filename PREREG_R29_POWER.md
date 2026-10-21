# PREREG_R29_POWER — local-big 功效复测（160 → 720）

立项：2026-09-11。**本文件落盘先于任何新作答；top-up 设计、题型分布、判定规则冻结，事后不得改。**

## R1 目的与口径澄清

- 欠功效层是 **local-big（160 of 720）**，非 pool（pool n=220 ≥ n_ceil=217 已足功效，C26）。
- n_ceil=720 来自 `results/power_big160.json`（exact McNemar，OR=4 占位，p_discordant=0.025，
  alpha=0.05，power=0.8 → 18 discordant → n_total=720）。
- 本复测目标：把 local-big 从 160 扩到 **720**（+560 新行），消除「160/720 欠功效」这一 S 扣点；
  McNemar 取值如实报告（显著与否都照实），不预设方向。

## R2 现有 flip 来源（冻结依据，读 results/local_big.json + evidence/big_adjudication.json）

- local-big 160 行 flip 4/160=0.025，McNemar b=4/c=0/p=0.125 ns。
- 4 翻转**全为整除除法题的 `.0` 尾随小数**（`23.0`/`5.0`/`1740.0`/`1200.0` vs 整数 gold），
  裁决 4/4 correct（`evidence/big_adjudication.json`）。
- 题型分布（`evidence/qa_pool_big.json`）：computed 120（加减乘除）+ hand 40（常识：首都等）。

## R3 top-up 设计（冻结）

- **总量 +560**，匹配原题型比例（computed:hand = 120:40 = 3:1）：
  - computed **420**：算术，按运算符比例 add:sub:mul:div ≈ 105:171:105:39（程序生成，
    gold 由表达式可复算；div 题为**整除**题以保留 `.0` 翻转机制）。
  - hand **140**：国家→首都常识题，gold 从内嵌的首都映射表取（去争议项）。
- 题池生成脚本 `scripts/r29_make_topup.py`，输出 `evidence/r29_topup_560.json`，gold 可复算，
  SHA-256 记入 manifest。
- 合并口径：top-up 560 与既有 local-big 160 **并集**（不替换不重叠），总 n=720。

## R4 作答协议
- 模型 `qwen2:7b`（本地 ollama），temperature 0，短答案提示（同 local-big 模板：
  「只答数字/只答地名」+ 置信度行）。
- 输出 `results/r29_answers_topup.jsonl`（question id + prediction + model digest）。

## R5 打分与判定（冻结）
- 每预测跑 exact（对 gold）与 guard v3.3；flip = exact 拒 + guard 受。
- 翻转行逐条裁决（作者，语义等价标准同既有层）；唯一重算 `scripts/r29_seal.py`
  → `results/r29_power_seal.json`。
- **判定规则**：
  - 总 n 达 720 → 欠功效扣点消除（无论显著与否）。
  - McNemar（合并 720 行）如实报；显著则 H1 表述维持，不显著则 H1 降级并同步下调正文强度。
  - flip 率如实报（预期因 div 题 `.0` 机制维持 ~1%–2.5%，不做高于此的假设）。

## R6 账本与纸面计划
- 新增 C75（local-big top-up 功效复测，720 行 flip/McNemar/功效状态）。
- 正文 Limitations 把「local-big 160 of 720 future work」改为「720 足功效已复测（结果如实）」；
  Future work 段同步更新。
- 全套门禁重跑 + manifest 重建。

## R7 不做的
- 不动 pool（已足功效）；不动 pilot top-up（模型不可用，已批 drop）；不切 matcher 版本；
  不引云模型；不新增 judge 金集。