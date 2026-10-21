# PREREG_R31_HETEROJUDGE — hetero 第二独立 judge（回应 Si「单 rater 描述性」）

立项：2026-09-11。**本文件落盘先于任何第二 judge 调用；行集、模型、提示、解析、
一致率口径冻结，事后不得改。**

## R1 目的（可靠性证据，非推翻依据）

hetero 层 8/60 确认翻转由单 rater（qwen2.5:7b，与被测 gemma3:4b 异家族）裁决，
为两轮 O2 的 Si 具名扣分项（"descriptive-only / single-rater"）。
本轮换**第三家族** deepseek-r1:7b（与 gemma、qwen 均异家族）独立重判同一 11 个
raw flip 行，报告跨 judge 家族一致率。单轮模型重判**不推翻**封存裁决
（作者保留排除依据；此处与 κ 的 reliability-not-validity 口径一致，只谈可靠性）。

## R2 行集与模型（冻结）

- 行集：`evidence/r18_heteromodel_judge.json` 的 11 行（8 correct＋3 incorrect；
  该文件即一裁时的 11 raw flip 全集，`results/r18_heteromodel.json` 的 flips 字段
  只存 8 确认行）。**Amendment A1（运行前修正，judge 零成功调用，分析未发生）**：
  初版误写 flips 字段含 11 行，首跑 assert 8 失败；改从一裁文件取全集，
  行身份（trace_id／question／predicted／gold）与一裁逐字同一来源，不断言新增行。
- Judge：本地 `deepseek-r1:7b`，temperature 0。**Think 允许**（与一裁的短答案格式不同，
  已披露：裁决是推理任务；R18 Amendment A1 的 think 纪录是采集端先例，不适用于 judge 端；
  解析时先剥 `<think>…</think>` 块再判单字）。
- 提示与一裁**逐字相同**（local_judge_heteromodel.py judge() 内 prompt 原样），
  num_predict 500（容纳 think＋单字 verdict），timeout 600。

## R3 解析与输出（冻结）

- 解析顺序与一裁一致（先找 INCORRECT 再找 CORRECT，因前者含后者子串）；
  剥 think 块后无命中记 ERROR。
- ERROR 行最多重试 3 次（沿 lr18-46 先例：三次尝试含一次换表述重试），
  仍 ERROR 则如实记录，不删除、不编造。
- 输出 `evidence/r18_heteromodel_judge2.json`（model／temperature／n／rows，
  每行 trace_id／question／predicted／gold／judge_verdict／error）。

## R4 一致率与判定（冻结）

- 报告：与一裁 verdict 的逐行一致率（11 行），以及与作者封存结论
  （8 confirmed／3 excluded）的逐行一致率；分歧行逐条列出原文。
- 判定：一致率描述性报告，不设采用门（无版本切换、无数字推翻）；
  若第二 judge 与作者在已排除行上系统性分歧（≥2/3），如实记入 Limitations
  作 instrument 不一致证据（lr18-54/55 先例口径），不改封存数。

## R5 不做的

- 不重采 hetero 答案；不改 gold；不碰 Holm；不做显著性主张；
  不把单轮模型一致率表述为效度（validity）。
