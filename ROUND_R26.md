# ROUND R26 — 公开集 guard 外部验证（TriviaQA + EntityQuestions，预注册 PREREG_R26_EXTERNAL）

- 范围：预注册外部验证（R26）+ R6 纸面收尾。**不堵本次投稿**（pre-reg：投稿包不动、结论先行）。
- 冻结语义：采样种子 20260908、miss/over-fire 计数口径、v3.4 采用门（miss 降≥5 且 over-fire 增≤2）在 PREREG_R26_EXTERNAL.md 落盘先于任何下载/作答，事后未改。

## R0–R3 采样与作答
- TriviaQA-RC wikipedia dev 洗牌取 200 题、EntityQuestions test 24 relation 轮抽 200 题（`scripts/r26_sample.py` / `r26_sample_trivia.py`）；数据源：UW 官方链接 404 → 作者 HuggingFace 镜像 `mandarjoski/trivia_qa`（数据同一、抽样规则不变，已披露）。
- 作答 `qwen2:7b`（本地 ollama temp 0，local-family）→ `results/r26_answers_trivia.jsonl` / `r26_answers_entity.jsonl`。

## R4 打分与裁决
- 同一预测两套：exact-match 与 guard v3.3（gold alias 集任一接受）。
- 翻转行（exact 拒 + guard 受）逐条裁决 = over-fire 计数；guard 拒行抽 60/集逐条判 miss = miss 率 + Wilson CI。
- 裁决落在 `r26_flip_pack_{entity,trivia}.csv` / `r26_miss_pack_{entity,trivia}.csv`；复审一轮裁决 `R26_ADJUDICATION_REVIEW.md`（单处纠错：trivia Vanessa atalanta 题干词 echo 由 correct 改 incorrect，over-fire 4→5）。

## R5 seal（唯一重算 `scripts/seal_R26.py` → `results/r26_seal.json`，4 条 assert 全过）
- entity：n=200，exact 25，guard33 57；翻转 32 中 2 over-fire；miss 0/60=0.0，Wilson95 [0.0,0.0602]。
- trivia：n=200，exact 95，guard33 123；翻转 28 中 3 over-fire；miss 2/60=0.0333，Wilson95 [0.0092,0.1136]。
- v3.4 候选：合 miss 降 2（entity 0 + trivia 2）、over-fire 增量 0、总 over-fire 5；miss 降 2<5 → **不切版，v3.3 保持基准（负结果照实）**。

## R6 纸面收尾（本文件之后完成）
- 账本新增 C69（TriviaQA）/ C70（EntityQuestions）/ C71（v3.4 决策，负结果），状态 verified。首次门禁发现 C69/C70 值列取整（0.0333 vs 0.033333… 超 TOL 2e-5）与 Wilson 列表未索引导致 2 FAIL → 改 `miss_wilson95[0]/[1]` 索引 + miss_rate 五位小数，重跑全绿。
- `paper/main.tex`：Methods 增 `\subsection{External validation (R26, descriptive)}`（含分布差披露句 + sealed 描述性结果）；Discussion Limitations 增公开集局限两句（描述性欠功效 + 公开集分布差 + 3 行 EntityQuestions 属性标注噪声 + 单作者裁决）。
- 写稿溯源：`log_writing_session.py` 追加 R26-external-validation（main.tex sha256 62a7e2af…）。

## 门禁验证
- manifest 重建 409 条目 → gates 10/10 PASS（record 进 gates_history.jsonl）。
- compile 门 PASS：0 错误、0 undefined ref/cite、2 overfull + 5 orphan-sec-label（与 R25 一致，非阻塞）。
- tmlr 扫描：G1/G4/G6/G7/G9 PASS；G3 残留 2 命中均为 `7b@local` 模型署名（`qwen2:7b@local` judge 标识，位于 CLAIM_LEDGER.md:83 过程文档，非投稿正文）；投稿包内 anonym_check 0 命中；过程文档不进入 submission zip，不做非 R6 范围改动。
- 投稿包未重建（`submission/submission_tmlr_r25.zip` 保持，pre-reg R6 "投稿包不动"）。

## 结论
- v3.4 负结果：token-containment 回退在公开集上 miss 降 2，未达采用门，沿"no new guard version is cut"先例不切版。
- R26 为描述性外部效度补充，不改主结论（1062 行 fifteen-strata 描述研究），投稿结论先行。