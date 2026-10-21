# ROUND_R14 —— R14新眼审稿问题全修（2026-09-07，用户"所有问题都要修"）

## 审稿输入（R14 fresh-eyes，只读未写）
- 表内加总/N=942/794/854/60、9个McNemar p、Holm幸存集、rollup五层：独立重算零偏离。
- 新问题：W1标题计数过期、W2图-表LN柱不一致、W3中文残留、W4四处minor。

## 修改（8处，均不碰证据）
1. **W1标题**：去计数。`...and Four Significant Inferences` → `...with Adjudication and a Guard Fix`（main.tex L22＋submission/openreview_checklist.md L11）。正文"five stratum-local readings"与Holm"two survive"并存之处不再与标题冲突。
2. **W2图柱**：`\pairbar{5.6}{LN}{0.8}{0.8667}` → `{0.8833}`（=表内53/60 Local-new guarded；0.8667系Cloud-new数，复制串行）。其余12柱R14已验对。
3. **W3中文残留**：删``全做''原文引用，`golds user spot-checked at 10\% with zero objections`独立成句（C40覆盖批准事实；collection脚本docstring未逐字记录该指令，不虚构grounding）。
4. **W4a**：L66占位OR补值`OR=4`（grounding：analysis_plan_power_rep.md＋C18/C26）。
5. **W4b**：L213括号改写`zero flips fall below the adjudication gate's 5\% trigger`。
6. **W4c**：L236 ceiling达成加pilot-50（`50, 108, 217, and 217 rows`）。
7. **W4d**：L108强过程断言弱化为number-scan对账句（grounding：reports/numbers.md）。
8. 账本：无新增声称（标题/图/措辞均为呈现层；OR=4系已有C18/C26值落字），不加条目。

## 验证
- stats exit 0；ledger 45 PASS/0 FAIL/1 WARN；style findings 0；taint clean；hallucination无error。
- number scan（门禁report-only口径）exit 0、stale 0（注：手动加`--fail-on-stale`会exit 1，系该flag严格口径，非门禁口径，无stale行）。
- manifest重建231条 → 门禁 **9/9 PASS**（config_sha256=b3e66a165457…），已record。
- 误操作纠正：首次manifest重建路径写 doubled（paper_workflow_kb/paper_workflow_kb/），已删除并原位重建；门禁随即9/9。

## 残留OPEN
- PDF仍旧版（无TeX）；QUESTION.md文件不存在（grep确认标题仅两处活体，均已改）。
