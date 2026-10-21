# PREREG_R30_BOOLQ — 公开是非问答第二题型（BoolQ dev）

立项：2026-09-11。**本文件落盘先于任何采样与作答；采样种子、样本量、提示、gold 映射、判定规则冻结，事后不得改。**

## R1 目的（判别检验，非 Holm 修复）

在同一个公开数据集内同时检验预测 (ii) 与 (iii)：被 R 覆盖的是非变体
（会／不会／不是／yes／no → 同义分支）应翻转，未被 R 覆盖的是非变体
（True／False／对／错 → 无规则覆盖）应只产生 miss。
本臂为描述性 observed-status，**不进入 Holm family、不做功效主张**（Si 的
「pool fails Holm」是既有封存事实，本臂不触碰它）。

## R2 数据与采样（冻结）

- 来源：SuperGLUE BoolQ 官方包（BoolQ.zip，
  SHA-256 `853fbe7922f70c59629f06a39e8d9ca440c3d740e760fd3b87a5ddf3dcba2436`，
  落盘 `data_boolq/BoolQ.zip`），用 **val.jsonl（dev，3270 行，已标注）**，
  不用无标注 test。（打包注记：初版含官方下载 URL，为 G3 零 URL 标准先改为包内附带＋SHA 锁定；
  R32 按上传体积规则改由 `data_boolq/SHASUMS.txt`＋`data_boolq/BoolQ/val.jsonl`＋冻结样本替代，
  BoolQ.zip 留盘不进上传包；字面 URL 移 ROUND_R31 存档；冻结的种子／样本／映射／规则零改动。）
- 采样：按 gold 类分层 50 True＋50 False，种子 **20260912**（`random.Random(20260912)`，
  类内 shuffle 后各取前 50），n=100。样本封存 `evidence/r30_boolq_sample.jsonl`
 （含 idx／question／passage／gold_bool）。
- Gold 映射（作者冻结，披露）：True→`是`，False→`否`。打分 gold 即中文是／否；
  模型输出的 True／False 按未覆盖变体处理（seal_theorems.py 行为探针已证
  `True`→`是` 被拒）。

## R3 作答协议（冻结）

- 模型 `qwen2:7b`（本地 ollama，与 R26 同模型），temperature 0，num_predict 60。
- 提示（中文指令＋英文原文，变体诱发设计已披露，不约束只答是／否）：
  `阅读以下英文短文并回答问题。用最短答案回答（不要解释）。答完后另起一行写置信度0-1，例如：0.9\n\n短文：{passage}\n\n问题：{question}`
- 解析：首个非空行作答案（同 seal_R26.parse_prediction 口径）。
- 输出 `results/r30_answers_boolq.jsonl`（id＋prediction＋model digest）。

## R4 打分与裁决（冻结）

- 每行跑 exact（norm 后与是／否比对）与 guard v3.3；flip＝exact 拒＋guard 受。
- 翻转行**全部**逐条裁决（作者，语义等价标准；over-fire 计数）。
- Guard 拒行：若 ≤60 行则普查裁决，否则种子 **20260913** 抽 60 行；
  miss＝语义对但被拒（Wilson 95% CI 仅在抽样时报告，普查则报精确率）。

## R5 判定规则（冻结）

- 覆盖输出（会／不会／不是／yes／no） flip、未覆盖输出（True／False／对／错）miss
  的模式成立 ⇒ 理论判别检验通过（记 C78 候选）。
- 若模型几乎全输出是／否原文（翻转≈0）或几乎全输出 True／False（翻转≈0、miss 高），
  照实报告为边界结果（变体未发射或全未覆盖），不改判据、不追采。
- 失败路径：采集错误行如实记录（error 字段），不编造、不删除。

## R6 不做的

- 不动 matcher 版本（v3.3 基准）；不跑 v3.4（R26 已否决）；不入 Holm；
  不做功效／显著性主张；不用 test split（无标注）。

## Amendment A2（R32，第二模型复现；主臂封存后追加，未动主臂任何冻结项）

- 动机：主臂单模型（qwen2:7b），Si 具名局限“单模型”。同 100 冻结行、同冻结映射、
  同中文指令逐字复用，换本地 `gemma3:4b`（temperature 0，num_predict 60；
  R18 短答案格式干净先例）重采重打分。
- 口径：描述性 flip/miss，不入 Holm，不做功效主张，不跑配对检验；
  复现（covered 翻转＋uncovered miss）或不复现（题型×模型依赖）都照实报告，
  不追认、不改写 C78。
- 输出：`results/r30_answers_boolq_gemma.jsonl`（采集）→
  `results/r30_score_boolq_gemma.json`（打分）→ 逐行裁决包 →
  `results/r30_boolq_gemma_seal.json`（C82 候选）。
- 失败路径沿 R5（error 行如实记录）。
