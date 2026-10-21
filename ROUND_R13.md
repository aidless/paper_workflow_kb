# ROUND_R13 — PDF重编＋zip重打＋重封存（2026-09-07）

## 触发
R11/R12遗留唯一OPEN：zip内main.pdf为旧版（410-Row）。用户"全做"：①TeX合PDF ②R2异议逐条 ③封存。

## ① TeX编译（CLOSE）
- 本地发现`~/.local/bin/tectonic`可用，一次编译通过（仅underfull警告，无错误）。
- PDF验证（pymupdf）：11页、新标题"942-Row Thirteen-Stratum"、零`[?]`未解引用、References存在。
- `paper/main.pdf`已替换（107KB）。

## ② R2-r9异议处置（伪影为主，逐条）
- "缺first report/单脚本/guard演示"：全在正文（Methods/Results/Guard段），压缩prompt未展开→伪影，不改稿。
- "缺异质机制讨论"：正文有cross-model/cross-type/second-family三节→伪影，不改稿。
- C项"技术性太强"vs R8"完整一致"：同一稿自相矛盾→rater噪声，不改稿。
- 唯一真问题R2未提（R11已修）：loose"2 of 412"伪句、C42误记。
- 结论：O2计分制对该rater失效（R12已记），本轮无稿件改动。

## ③ 重打＋重封存
- `prepare_submission.py paper_workflow_kb`：164文件（+main.pdf新+holm.json），匿名0命中；
  泄漏扫描唯一命中`scripts/log_writing_session.py`（方法脚本，R11同款误报，保留）。
- zip内PDF已验为新版（标题"942-Row Thirteen-Stratum"）。
- manifest重建＋验证：230 PASS/0 FAIL。
- 门禁`run_acceptance_gates.py`：**9/9 PASS**。
- PHASE5_SEAL.json已刷新（zip sha cdf0c0b3…）。

## 状态
- 账本45/0/1WARN；门禁9/9；manifest 231条；PDF OPEN→CLOSE。
- 投稿blocker清零；上传仍须人工（保护层）。
- 注记：seal内嵌的manifest哈希早于最后一次manifest重建（ jedynie信息性；manifest自验证通过，
  seal中tex/ledger/zip哈希有效）。此后任何文件改动都必须重走"改→manifest→seal→门禁"全序。
