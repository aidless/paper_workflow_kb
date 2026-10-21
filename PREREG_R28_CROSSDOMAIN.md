# PREREG_R28_CROSSDOMAIN — 跨域检验 P1 预测 (i) 退化变体空间 / (ii) 覆盖缺失

立项：2026-09-11。**本文件落盘先于任何作答；预期方向、判定规则、arm 定义冻结，事后不得改。**

## 背景与目的

P1（R27）形式化把翻转拆为「答案变体空间 × R 类型覆盖」两独立因子，导出三预测：
(i) 退化变体空间→零翻转（已有 cloud-math 0/40 支撑，本 arm 本地复现 + 独立检验）；
(ii) 覆盖缺失→零翻转（**未被既有数据钉死**——local-en 0/30 记"天然规范"而非覆盖检验）；
(iii) 覆盖变体→正翻转（已有中文 QA 层支撑，本轮不另测）。

R28 用两个非中文-QA arm 分别检验 (i) 与 (ii)，把"matcher 覆盖 + 答案空间"机制从中文短答 QA
迁移到「数学（答案空间退化）」与「英文单位（变体存在但 R 仅覆盖中文单位）」，拆掉 N 的
"窄 QA"与 Si 的"QA-only"扣点。

## R1 matcher 覆盖事实（冻结依据，读 scripts/label_match_v3.py / v31 / v33 代码）

- `SUFFIXES` = 纯中文单位〔年 元 米 小时 公里 秒 约 的〕；无任何英文单位。
- `SYNONYMS` = 中文〔不会/不是→否、会→是〕＋英文 yes/no；`_EN_SYNONYMS_NORM` 仅 3 词
  〔ascorbic acid、shakespear、shakespeare〕。
- substring 分支禁止 gold 为纯数值（`_parse_cn_num(g2) is not None` 时跳过），数值等价分支
  `_parse_cn_num` 只认 `数字(可选小数)(万|亿)?`，**不解析英文单位后缀**。
- ⇒ 英文单位变体（`384400 km` / `384,400 kilometers` / 千分位）既不被 SUFFIXES 剥离、
  也无法进入数值等价（parse 失败），故 tolerant 必拒。

## R2 Arm 定义（冻结）

### Arm A「degenerate」（检验预测 i）— 数学数值
- 40 道简单算术题（加/减/乘/除，答案唯一纯数字），中文题干。
- gold：纯数字字符串（如 `96`、`7`、`-3`）。
- 变体空间退化：答案无合法等价串变体（数字唯一规范形）。
- **预期**：flip ≈ 0。可证伪点：若模型输出带中文"约/的"等 SUFFIXES 前缀（如"约96"）被剥离
  而 tolerant 接受 → flip>0 → 预测 (i) 需精化为「退化变体空间 ⇒ 零翻转当且仅当输出落在规范形」。

### Arm B「uncovered」（检验预测 ii）— 英文单位数值
- 40 道英文事实数值题（地理距离/天文/体育/物理常数，答案含数值＋英文单位），英文题干并
  在题干明确单位词（kilometers / miles / years 等）以诱导英文单位输出。
- gold：纯数字（不带单位）或固定英文单位规范形，每题在采集脚本内嵌固化。
- 变体存在但 R 仅覆盖中文单位：模型预期输出英文单位/千分位/全称-缩略变体。
- **预期**：flip = 0 **且** miss > 0（存在「语义对但 exact 拒且 guard 拒」的变体行）。
  可证伪点：(a) 若出现 flip>0 → R 意外覆盖某英文变体 → 预测 (ii) 被证伪，回改理论；
  (b) 若 miss=0（模型全程规范输出、无变体）→ 无法区分 (i)/(ii)，判题目诱导失败需重设计。

## R3 作答协议
- 模型 `qwen2:7b`（本地 ollama），temperature 0，短答案提示（英文 arm 用英文提示）。
- 输出 `results/r28_answers_{a,b}.jsonl`（question id + prediction 原文 + model digest）。

## R4 打分与裁决
- 每预测跑 exact（对训练固化的 gold）与 guard v3.3；flip = exact 拒 + guard 受。
- Arm A：flip 行（若有）逐条裁决；报 flip 率（描述性）。
- Arm B：翻转行逐条裁决；另对「exact 拒 + guard 拒」行逐条裁决语义等价性（作者，少量标注
  预算）以得 miss 计数（语义对但双拒＝变体存在＋覆盖缺失的证据）。
- 唯一重算：`scripts/r28_score.py` → `results/r28_seal.json`。

## R5 判定规则（冻结）
- **P(i) 成立判据**：Arm A flip = 0（或描述性方向：flip 率显著低于既有中文 QA 层最低正翻转）。
- **P(ii) 成立判据**：Arm B flip = 0 且 miss > 0。miss>0 是"变体存在"的操作化证据。
- Arm B flip>0 → P(ii) 证伪，正文回改预测并如实报；Arm B miss=0 → 诱导失败，重设计题目
  （不算阶段失败，但须在 ROUND 记录诱导失败原因）。

## R6 账本与纸面计划
- 新增 C73（Arm A 数学跨域）、C74（Arm B 英文单位跨域），verified/inconclusive 按判据定。
- 正文 Results 增两 arm 段落（与 P1 三预测对照）；若 (ii) 成立则 Limitations 的"英文天然规范"
  表述改为"覆盖缺失（有变体不覆盖）"，同步 Theory 小节对照句。
- 全套门禁重跑 + manifest 重建。

## R7 不做的
- 不测 (iii)（已有中文层支撑）；不引入云模型；不新增 judge 金集；不重标主表 accuracy/ECE。
- 此轮不切 matcher 版本（guard v3.3 保持基准）。