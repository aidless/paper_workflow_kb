# ROUND_R31 — 补强 P5 定理 ＋ P6 公开是非题型（进行中）

> 目标：用户决策（P4 升级回应）：补定理＋补第二题型，且第二题型必须用公开数据集。

## P5 定理（完成，sealed）

- Measurement-error formalization 小节新增 **Theorem 1（规则追加单调性）**：
  纯析取追加 R→R′（无新增接受阻塞 guard）⇒ Accept/Flip 单调不减、Miss 单调不增
  （证明：析取直接得；flip 继承因 e 与 R 无关；miss 由逆否）。
  v3.3→v3.4 恰为此类追加：400/400 R26 行接受包含零违反、增量恰 2。
  适用域外显式排除 guard 追加修订（v3.1→v3.3 加阻塞 guard，8/1700 接受→拒绝
  全单字 CJK 类）——版本史的回归／采用门做法与此一致。
- **Theorem 2（数值容差 over-fire 边界）**：错值相对误差落开区间 (0,0.005)
  ⇒ 数值分支接受，exact 拒时即 over-fire（分支条件直接得）；
  5/5 R29 over-fire 行重算在内（0.0005–0.0043）。
- 两定理均为 sealed 实现的事后陈述（与三预测同口径披露），凭重算印证、
  非凭文字断言；行为探针另文档化分支边界（yes→是接受／True→是拒绝，
  后者直接决定 P6 gold 设计）。
- 账本 C76/C77 verified（77 PASS / 0 FAIL）；门禁 10/10；manifest 461。

## P6 公开是非题型（预注册已冻结，采集中）

- 数据集：SuperGLUE BoolQ 官方包（SHA-256 已记），val dev 3270 行，
  分层 50 True＋50 False（种子 20260912），n=100。
- Gold 映射冻结：True→是／False→否；中文指令＋英文原文提示（变体诱发已披露）。
- 判别设计：覆盖变体（会／不会／不是／yes／no）→翻转 vs
  未覆盖变体（True／False／对／错）→miss，单数据集内区分预测 (ii)/(iii)。
- 描述性 observed-status；不入 Holm；不做功效主张。
- 文件：PREREG_R30_BOOLQ.md（冻结）／scripts/r30_sample_boolq.py／
  scripts/r30_collect_boolq.py（后台采集中，qwen2:7b temp0）。

## 待办（下一轮）

- 采集完成 → 打分（exact/guard v3.3）→ 翻转全裁决＋拒行裁决（≤60 普查／种子抽样）
  → seal → C78 候选 → 正文段落 → 门禁＋manifest → O2 重评是否推进由 N/Si 实际增量定。

## P6 完成（本轮后半）

- 采集 100/100（零错误，digest 单一 `9d468147c0aa91b4`，与 R26 同模型一致）。
- 打分：exact 0（模型从不输出裸是／否）／guard 55／flip 55／reject 45。
- 裁决（作者逐行，包文件落盘）：翻转 55/55 内容正确、over-fire 0；
  拒 45 普查：miss 31（Yes./No. 句点变体内容对）＋正确拒 14（内容错 10＋裸 1/1.0 非答案形 4，规则已披露）。
- Seal：flip 率 0.55；miss 率 31/45＝0.6889（Wilson [0.5434,0.8047]）；
  b＝55/c＝0 描述性（无配对检验，与嵌套规则一致）；判别成立（DISCRIMINATION HOLDS）。
- 正文化：Results 新增 Public yes/no arm (R30, BoolQ) 小节（中文直写风格已统一）。
- 账本 C78 verified（78 PASS / 0 FAIL）；门禁 10/10；manifest 480。
- 诚实边界：exact 0／content 86 皆为描述性；不入 Holm；功效无主张；
  内容正确率 86/100＝55＋31 由封存数组成直接相加，无隐藏推断。

## 复核（用户指令 "你来复核一下"，独立重判）

- **4 个 "1"/"1.0" 行维持 correct_reject**，理由（三条，逐条看过题干）：
  1. 冻结 gold 空间是是／否词形；"1"/"1.0" 不是已确立的肯定变体（不在同义覆盖内，
     也不是模型在他处使用的 Yes/No 词形）。
  2. 退化证据："1.0" 呈置信度形状（预测自带独立 0–1 置信度行，有泄漏先例）；
     boolq-1031 的 "1" 更像复述题干 "1-844" 而非肯定回答。
  3. 保守方向：把含糊非答案计入 miss 会污染 miss 类纯度；维持后 31 个 miss
     全是无歧义的 Yes./No. 内容一致项。
- **抽查**：miss 行 boolq-2401（Yes. 内容对）、boolq-2586（No. 内容对）维持；
  错答行 boolq-763（No vs True，gold 冻结，guard 拒对）维持 correct_reject。
- **翻转侧**：55/55 内容一致零 mismatch（程序化已验），维持。
- 结论：数字零改动（flip 55／over-fire 0／miss 31／正确拒 14／C78 不变），
  本节即复核记录。
