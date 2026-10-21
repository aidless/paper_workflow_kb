# PREREG_R26_EXTERNAL — 公开集 guard 外部验证（TriviaQA + EntityQuestions）

立项：2026-09-08。**本文件落盘先于任何数据下载与作答；采样种子与决策规则冻结，事后不得改。**

## R1 研究问题
- Q1：guard v3.3 在公开短答案集上的 miss 率（gold alias 接受但 guard 拒绝）是多少？（外部效度）
- Q2：v3.4 候选（v3.3 + token-containment 回退：gold 任一 alias 的全部 token 出现在预测中，或反之）能否降 miss 且不涨 over-fire？
- 非目标：**不替代 C4 外部 grading**（公开 gold 救 guard，不救我们 106 行裁决的人味）；不作跨集合并推断。

## R2 数据与采样（种子冻结）
- TriviaQA-RC wikipedia dev：洗牌种子 `20260908`，取前 **200** 题（question + alias 集）。
- EntityQuestions test（24 relation 均匀轮抽）：同一种子，取 **200** 题（question + 实体 alias 集）。
- 采样脚本 `scripts/r26_sample.py`，输出 `evidence/r26_trivia_sample.jsonl` /
  `evidence/r26_entity_sample.jsonl`，SHA-256 记入 manifest。
- 欠功效披露：observed-status 外部 pilot（沿 R18 口径），只作描述性报告。

## R3 作答协议
- 模型 `qwen2:7b`（本地 ollama），temperature 0，短答案提示（与 local-new 同模板，见脚本）。
- 输出 `results/r26_answers_trivia.jsonl` / `results/r26_answers_entity.jsonl`（question id +
  prediction 原文 + 模型 digest）。单样本 jitter 不另测（已有 retest60 界）。

## R4 打分与裁决
- 同一预测跑两套：exact-match（对 alias 集任一）与 guard v3.3（对 alias 集逐一，任一接受即接受）。
- 翻转行（exact 拒 + guard 受）**逐条裁决**（作者；语义等价标准同既有层）。
- miss 估计：guard 拒行中抽 **60 行/集**逐条对照 alias 判 miss/真拒，报 miss 率 + Wilson CI（描述性）。
- over-fire：guard 受行中裁决为错的计数（翻转裁决中自然产出）。
- 唯一重算：`scripts/r26_score.py` → `results/r26_external.json`。

## R5 v3.4 决策规则（冻结）
- v3.4 = v3.3 规则 + token-containment 回退（定义见 R1；实现 `scripts/label_match_v34.py`，
  与 v3.3 同输入输出接口）。
- **采用条件（须同时满足）**：(a) 两集合计 miss 下降 ≥5 行；(b) over-fire 增量 ≤2 行。
- 不满足 → 负结果照实报告，**不切版本**（沿"no new guard version is cut"先例），v3.3 保持基准。
- v3.4 只在 R26 密封样本上评价，不反刺既有 1062 行（避免事后挑选）。

## R6 账本与纸面计划
- 新增 C69（TriviaQA 外部 miss/over-fire）、C70（EntityQuestions 同）、C71（v3.4 决策结果，
  采用或负结果）。
- 方法章增"External validation"段（含分布差披露一句）；Limitations 增公开集局限两句。
- 全套门禁重跑 + manifest 重建；投稿包不动（R26 不堵本次投稿，结论先行）。
