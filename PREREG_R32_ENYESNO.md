# PREREG_R32_ENYESNO — 英文是非臂（冻结设计，未采集）

立项：R32。**只冻结设计，不采集、不跑数；正文 Future work 指向本文件。**

## R1 动机（接 R30 诚实缺口）

R30 的 exact=0/100 是冻结映射（True→是）与模型英文作答的交互产物（M3 hedge）。
本臂去掉跨语言 confound：同 BoolQ、同模型（qwen2:7b，temp0）、同 100 行规模，
指令与 gold 映射全英文（True→Yes／False→No），检验 exact-zero 是否为映射人为产物、
covered-vs-uncovered 判别是否在母语映射下保持。

## R2 设计（冻结）

- 题集：BoolQ dev（`data_boolq/BoolQ/val.jsonl`），与 R30 样本**不交叠**的新 60 行
  （分层 30 True＋30 False，种子 **20260932**，`random.Random` 类内 shuffle 取前 30）。
- 作答：本地 qwen2:7b，temperature 0，英文短答案指令（`Answer with the shortest
  answer, then confidence on a new line`），num_predict 60。
- Gold 映射：True→`Yes`，False→`No`（母语映射，冻结）。
- 打分：exact（norm）＋ guard v3.3；flip＝exact 拒＋guard 受；裁决口径沿 R30
  （翻转普查＋拒 ≤60 普查；句点变体／数字非答案形规则复用，逐行包落盘）。
- 口径：描述性 observed-status；不入 Holm；不做功效主张；无配对检验。

## R3 判定（冻结）

- 若 exact 率显著高于 R30 的 0（母语映射下模型输出裸 Yes/No），记 exact-zero
  为映射人为产物，R30 hedge 升级为机制结论。
- covered（Yes/No）翻转 vs uncovered（Yes./No.）miss 的判别若保持，R30 判别
  结论加一母语证据点；若不保持，如实记为映射依赖。
- 任何方向都不追认、不改写 R30 封存数。

## R4 不做的

- 不碰 R30 冻结样本；不换模型族（跨模型问题由 P1-2 的 gemma/deepseek 复现覆盖）；
  不做显著性主张。
