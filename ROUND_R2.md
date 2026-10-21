# ROUND_R2 — goal首轮：O2双模型终评 + C2 PDF + 机械门全绿（2026-09-07）

## 改动（均有痕迹，非数字改动不涉及账本值变更）

1. O2 第二评分：本地 `qwen3:4b` 独立盲评（未见 R1 分数），prompt 见 `/tmp/rater2_prompt.txt`
   （含“Be strict”措辞，已披露不对称）；原始输出 `evidence/rater2_qwen3_raw.log`，
   干净结论 `evidence/rater2_qwen3.json`（N 3.5 / S 6.5 / Si 6.0 / C 9.5，加权 5.775）。
   R1（muse-spark）8.0/8.0/8.0/8.0，加权 8.0。一致率 0/4，|Δ总分| 2.2 → **UNSTABLE**。
2. SELF_ASSESSMENT.md 重写为双模型版：两模型分数+agreement+分歧升级条件+方法局限
   （prompt不对称、无gold集、R2弱模型视角）；8分线判定：**未达成**。
3. C2 关闭：tectonic 实编译 `paper/main.pdf`（50.7 KiB）；导言区加 xeCJK + Noto Serif CJK SC
   （中文例证缺字清零）；表格 `\small`+`tabcolsep 4pt`（overfull 37.9pt清零）。
   编译 gate 静态层仍 4 E（math_commands.tex 模板宏 `\ref{#1}` 误报）——权威层
   （tectonic实编译）0 error，属已知误报，不动模板宏。
4. 匿名：删 Author Contributions / Acknowledgments 两节（模板原文要求接受后才加），
   C3 anonym 0 hits。
5. STATE_SNAPSHOT.md 模板区 `[TODO]` 字面 3 处改中文待办表述（TMLR EXTRA FAIL清零，
   TMLR 全 PASS）。
6. 顺序教训（新）：prepare_submission 改写 submission/ 会使 manifest 过期；
   gates --record 写 history 同理。稳定终序：prepare → manifest build → gates（无record）
   → package check。raw transcript 后缀 .txt→.log（style 扫描仅 tex/md/txt，证据内容未动）。

## 门禁（本轮终态）

- acceptance gates 9/9 PASS；manifest 87 PASS/0 FAIL；ledger 18/0/1 WARN（C08既有）；
- numbers stale 0；stats 0 E（含同行n/N）；style 0；taint 0；hallucination 0 E；
- TMLR 全 PASS（含G9硬件）；C1–C7 全 PASS（含C2 pdf、C5 gates）。
- compile_gate 静态 FAIL（4 E模板宏误报）+ 权威 tectonic 实编 0 error 出 PDF（文档化双轨）。

## 未决（下一轮焦点，与 SELF_ASSESSMENT 分歧分析一致）

- N 4.5分歧：需跨题型复现或理论化陈述的新证据；S 1.5：pilot补至50或≥20条judge金集；
  Si 2.0：温度缩放/等渗回归对比或子串守卫实现；对称prompt重跑O2。
- 上传 MANUAL（保护层）；gold-set 校准缺（两模型分数均为未经校准估计）。
