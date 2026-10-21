# ROUND R17 — Phase 5 提交合规封存（post-R3）

基线：R3 收敛（NEW C0/M0；R2 全部 Major 已关）+ 主审 4 处微补丁（L67/L196/L54 pilot 句内标签、L226 删悬空序数）。

## 机器检查（本轮实跑，全绿）
- stats exit 0 · ledger **48/0/1**（WARN=旧 C08）· style 0 findings · taint 0 · hallu 0 cite errors · numbers exit 0（table-vs-prose 0）· tmlr 0 failures（G1/G6/G7 PASS；G4 INFO 允许；G9 WARN 缺 evidence/protocol.md，改前已存）
- 验收门 **9/9 PASS** 已 --record（21:16 后又追加终轮记录）
- 插曲：门禁一度 8/9——manifest 作用域错配（workspace-root 构建致路径前缀漂移，R15/R16 的 252/259 均为 paper-root 作用域）。已纠正：manifest 一律 paper-root 构建（`cd paper_workflow_kb && build .`），核对 260 条；`scripts/rebuild_manifest_scoped.py`（workspace 误构建）已移入 scripts/ 归档，过程记录在此。
- compile_gate：0 编译错误/0 未定义引用（静态误报 #1–#4 同 R15）/0 未定义引用键/0 bib 漏引；TeX 不可用→文档化降级；G2 真编译待用户侧 latexmk。

## G1–G11（TMLR）
- G1 PASS（匿名 tmlr 无选项）· G2 待用户侧编译（降级记录）· G3 机械 0 hits + 人工复扫（模型名为实验装置，R1–R3 无异议）· G4 口径统一（on request + acceptance 链）· G5 zip 0.4MB/168 文件 · G6 机制 present · G7 PASS（78 词 2 关键词）· G8 清单已生成（人工项待上传时勾）· G9 L01 delta 已披露、无新增文本 · G10 同 G3 · G11 门禁 9/9 + manifest 260/0/0。
- 文献新鲜度门 exit 0（age 0 天）。
- 引文门：research-kit verifier 缺席（exit 2 基建错）→ 文档化降级；(E) 类本地已覆盖（hallu 0 cite errors，7 key 全对 bib）。

## 交付物
- `submission/submission_tmlr_n942.zip`（重建，0.4MB，168 文件）· C1–C7 exit 0（C5 曾 FAIL 系先打 zip 后建 manifest 的顺序错，已纠正：打 zip → 建 manifest → 再验）
- `PHASE5_SEAL.json` 已刷新（4  artifact 哈希与 manifest 交叉对账 PASS；manifest 自哈希因 created 时间戳与自排除律移出 seal，原因具名记录）
- 哈希对账：seal 4/4 OK + manifest 260 PASS/0 FAIL。

## 诚实尾巴（用户侧）
1. `latexmk -pdf main.tex` 跑一遍（PDF 仍为旧版；无新宏包）。
2. 上传保持 MANUAL（OpenReview 账号 + G8 人工项确认）。
3. SELF_ASSESSMENT.md 未动（沿用既有版本；双模型重评可选，未做）。
