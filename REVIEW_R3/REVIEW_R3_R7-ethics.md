# Review Round R3 — R7 伦理轻量验收报告（R16 E/L 簇）

- 日期：2026-09-08 ｜ 论文：Exact versus Tolerant Label Matching…（264 行，R16 版）
- 审稿角色：R7 伦理（只验收披露簇 E/L，不做全稿重审；独立工作，未修改手稿）
- 输入：`paper_workflow_kb/paper/main.tex`（R16）、`paper_workflow_kb/REVIEW_R2/ROUND_R16.md`（改动日志）、`paper_workflow_kb/REVIEW_R2/REVIEW_R2_R7-ethics.md`（R2 遗留问题）、`paper_workflow_kb/results/gold_guarded_agreement.json`、`paper_workflow_kb/grades_gold25_user.csv`
- 独立审稿声明：本报告独立完成。

## 1. R2 遗留问题验收（逐项，证据优先）

| R2 ID | R16 落地情况（行号） | 判定 |
|---|---|---|
| R2-R7-01（Major）：三处 independent 原样保留＋新增 independent second grading，评分者=作者全文零披露 | **落地 PASS**。(1) L119 方法段现为 "was graded blindly item by item by the author without access to guarded outcomes"（R2 的 "graded independently item by item" 已改）；(2) L232 结果段现为 "blinded item-by-item grading agrees 24 of 25"＋"giving them a blinded second grading beyond the in-session single rater"（两处 "independent" 已改 "blinded"）；(3) 新增披露句 L232 末 "Blinding note: the single blinded grader is the author, grading item-by-item without access to guarded outcomes; the 11 of 11 stemless grades are therefore author grades with no external check, reported as-is."＋摘要 L55 "grader: the author, blinded to outcomes"。全文 grep `independent(ly)` 仅剩 3 处合法（L85 "independently supports"/"independent motivation" 指引文、L245 "no independent calibration-improvement claim" 指校准主张），**零残留 independent 指代评分者**。披露句与证据一致：JSON 25 项 `user_grade` 全为"对"（同一人），G06 `guarded_correct:false` vs `user_grade:对` → L232 "the blinded grader accepted the response while guarded says incorrect" 逐字吻合 | **CLOSED** |
| R2-R7-02（Minor）：COI/资助/受试者声明缺席 | **落地 PASS**。L249 新增显式一句："Conflicts, funding, human subjects: no conflicts to declare, no external funding, no human participants (the only human grading is the author's own blinded grading disclosed in Results)." 全文 grep `conflict\|funding\|human particip` 在 L249 命中；三要素（冲突/资助/受试者）一次覆盖，且括号内评分者身份句与 L119/L232 互锁 | **CLOSED** |

## 2. 数字亲手重算（本轮实算，非声明未重算）

- 脚本 `r3_r7_wilson_check.py`（assert 强制）：JSON `per_item` 逐项重数 agree=**24/25**（唯一分歧 G06：`guarded_correct:false`＋`user_grade:对`＋`agree_vs_guarded:false`）；stem 13/14、stemless 11/11 与正文 L119/L232 一致；25 项 `user_grade` 全为"对"（单人评分者反证成立）。
- Wilson 95% CI（z=1.96）亲手重算得 [0.8045552759497747, 0.9929039496133009]，与文件值精确一致（差 <1e-12）；正文 L55/L119/L232/L239 "0.805 to 0.993" 为正确舍入。**无 claim-data 矛盾。**

## 3. NEW 问题扫描（伦理域内，R16 新增文本）

- R16 在伦理域的新增文本（L55 摘要 grader 句、L232 blinded 改写＋Blinding note、L249 COI 句、L253 BI G06 句）逐一核对，均诚实无拔高；stemless "no external check, reported as-is" 属主动限权，好。
- **NEW Critical：0；NEW Major：0。**
- Minor（记录，不阻塞）：R3-R7-m01 — L232 "a blinded second grading beyond the in-session single rater" 中 "second grading" 仍可被速读误作"第二评分者"；虽同句 Blinding note 已明示 single grader 为作者，仍建议收紧为 "a second blinded pass by the same rater"（一词级措辞，非披露缺失）。
- Nit（记录，不阻塞）：无（L249 括号句与 L232 互锁，无需再改）。

## 4. 计数与收敛判定

- Critical：0 ｜ Major：0 ｜ Minor：1（NEW 措辞建议 R3-R7-m01，非阻塞） ｜ Nit：0
- R2 遗留：R2-R7-01 CLOSED、R2-R7-02 CLOSED（遗留清零）
- 是否收敛：**收敛**——伦理域无阻塞项；R3-R7-m01 可由作者自行决定是否采纳，无需 R4 伦理再审。
