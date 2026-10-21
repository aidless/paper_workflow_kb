# ROUND R33 -- R1 修复轮（登记 2026-09-24T18:20:29Z）

上一轮 R32 之后进入 Phase 4.5 对抗审稿的修复期。本轮首条改动见下表；改动由 `apply_candidate.py --go APPLY` 执行并自带逐次备份。

编号说明：本论文目录有 R0..R32 共 33 个轮次文件，排序取数值最大者再 +1（按文件名排会挑到 R9，那样会把新轮次写进三年前的表里）。

| 编号 | 文件 | 改动 | 触发/理由 | 状态 |
|---|---|---|---|---|
| CHG03 | `paper/main.tex`（新增 \section） | Ethics and Broader Impact 插入 224 词 | audit_paper_structure REQUIRED-FAIL=ethics_discussion；候选经必要性/充分性/4 词 stub 反证自证（0 数值字面量 ⇒ 接地检查为真空通过，已注明） | done |

## 追加：伦理小节标题对 venue 闸不可见（登记 2026-09-25T04:19:17Z）

| 编号 | 文件 | 改动 | 触发/理由 | 状态 |
|---|---|---|---|---|
| CHG04 | `paper/main.tex` | `\section{Ethical Considerations}` 这个标题**venue 自己的闸看不见**：check_tmlr_compliance 的 tmlr 头部模式是 `Broader Impact|Ethics`，而 "Ethical" 不含 "Ethics"；我的 audit 用的是 `ethic\w*` 所以判绿 ⇒ 两把尺对同一篇给相反读数。改成 TMLR 自己用的措辞 `\section{Ethics and Broader Impact}`（备份在 arxiv_d0788aa9/backups/，重跑两把尺都绿） | R1 后复测：`check_tmlr_compliance --venue tmlr` 报 `[G7] WARN :: no Broader Impact / Ethics section found`，而 `audit_paper_structure` 报 `REQUIRED-FAIL=-` —— 分歧原因是标题词形 | done |
