# ROUND_R32_CLOSE — 收官（R32 审阅修复＋第二模型臂＋终封）

> 本文件关闭 R32 工作流；R32 内全部数字以各 seal 文件为准，过程细节见
> ROUND_R31.md／ROUND_R32.md 与 STATE_SNAPSHOT.md 的 R32_REVIEWFIX／
> R32_A2_GEMMA／R32_CLOSE 三行。

## 交付（全部 sealed）

- **审阅修复 M1–M7＋minors**（零新实验）：口径统一（78 active＋2 superseded＋
  1 inconclusive＝81 条目）、定理改 instrument lemmas＋shallow 注记、BoolQ
  exact-zero hedge、keywords 入正文、清单摘要全文＋上传文件名指定、分数禁引确认；
  C81 verified。
- **BoolQ 第二模型臂（Amendment A2，C82）**：同 100 冻结行／同中文指令／同
  True→是・False→否 冻结映射，换本地 gemma3:4b（temp0，num_predict 60）重采
  重打分。
  - exact 0/99；guard 45；flip 45（Yes→是 21＋No→否 24），**45/45 内容正确、
    over-fire 0**；
  - guard 拒 54 普查裁决：miss 39（句点变体内容对、无规则覆盖）＋正确拒 15
    （错极性句点形 6＋内容不符短答 8＋非答案 `Unknown.` 1；本臂无裸 `1/1.0`）；
  - flip 率 45/99＝0.4545；miss 率 39/54＝0.7222（Wilson95 [0.5911,0.8238]）；
  - **1 行 boolq-1159 采集超时如实披露**，不进任何分母、不插补（PREREG_R30
    R5 失败路径）；
  - 方向在第二模型族复现，量级低于主臂（45 vs 55）；不入 Holm、不做功效主张、
    无配对检验（b=45/c=0 描述性），**不追认、不改写 C78**。
  - 证据：`results/r30_boolq_gemma_seal.json`（唯一重算
    `scripts/r30_seal_boolq_gemma.py`）；采集／判分／裁决／逐行包见
    `scripts/r30_{collect,score,adjudicate,seal}_boolq_gemma.py` 与
    `r30_{flip,miss}_pack_boolq_gemma.csv`。
- **正文**：BoolQ 小节增 `Second model family (Amendment A2)` 段（数字全部取自
  seal 文件）。
- **终编**：`paper/main.tex` 三遍 XeTeX（xelatex→bibtex→xelatex×2）**零错误、
  零未定义引用**，20 页；新段已渲染进 PDF（pdftotext 已验证）。
- **终封 core**：`submission/submission_tmlr_r31_core.zip` **339 文件 5.5MB、
  0 重复**；匿名 0 命中；`results/r31_core_package_seal.json`。
- **对账**：`results/r31_manifest_reconciliation.md`，manifest 531 vs 包内 338，
  缺口 193 逐类命名（含 `blind-material` 2 与 `audit-scan-report` 5 显式声明
  不给），**未解释 0**。
- **账本**：82 条目校验 **82 PASS / 0 FAIL**（`results/verify_claim_ledger_r32.md`）。

## R32 抓出并修正的两处真实缺陷（非文字级）

1. **包内混入应排除的重型语料**：上一版 core 包仍带 `data_boolq/BoolQ.zip`
   （4.1MB），与 `scripts/seal_r31_core_package.py` 的 `EXCLUDED_HEAVY` 断言
   直接冲突——说明此前的 `results/r31_core_package_seal.json`（325 文件）
   不可能由该断言版本对该包产出，属过期记录。本次剔除并重封，规则与产物一致。
2. **正文引用的一手存证缺失**：`main.tex` 第 110 行标注
   `(evidence/hakim_song_2609.01671.pdf)`，该文件此前不在上传包内。已补齐，
   并把该路径写入 seal 的必需清单断言。

## 诚实边界

- 「方向复现」是**描述性**结论：第二模型族点数更少、单数据集、无配对检验；
  E5–E7 的 harness 进化实验全为 hold（无差异即不放行），未据此做任何模型晋升。
- core 包内 `evidence_manifest.json`、`results/r31_manifest_reconciliation.md`
  与 seal 文件描述包自身，**包内副本按构造落后最终 zip 哈希一代**；以盘上副本
  为准，且每个数字均为重算而非复制（seal 内 `self_reference_note` 已记录）。
- 四扫（number／stats／hallucination／figure-claims）报告为本轮验收门过程产物，
  与历轮一致**不入包**，仅扫描器脚本随包。
- 上传为保护层动作，**未执行**。

## 未竟（移交下一轮）

- R32 主臂（英文母语 yes/no，`PREREG_R32_ENYESNO.md`）**设计已冻结、未采集**：
  正文 Future work 指向该文件；采集后可关闭 R30「exact-zero 是否映射人为产物」
  的诚实缺口。
- 真人偏好数据升级（合成偏好仅为冷启动）；DPO（P2）后模型与 ckpt-136 的
  内容判据重赛仍为 hold。
