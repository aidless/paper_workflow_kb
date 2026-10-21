# paper_workflow_kb / KB grounding（Obsidian 130 篇已接入）

> paper-writing-agent Phase 0 Intake 产物。知识库是文献侧唯一可信源，正文数字不得脱离本页所列证据快照。

## 知识库位置（源，不复制正文，只快照索引）

- 源库：`~/文档/ObsidianKnowledgeBase/01 - Papers/_组织/`
- 单篇笔记：`单篇/批量审稿/`（75）+ `单篇/论文卡片/`（51）+ `单篇/arXiv投稿/`（4）= 130
- 总索引：`_单篇索引.md`（130 条双链 + 源路径对照）
- 三张源索引：`_索引_批量审稿75批.md`、`_索引_论文卡片53.md`、`_索引_arXiv_TMLR状态.md`
- 总入口：`_MOC_100papers.md`

## 本项目证据快照（已冻结在 evidence/kb/，manifest 哈希对账）

| 快照 | 对应源 | 用途 |
|---|---|---|
| `evidence/kb/_单篇索引.md` | 源 `_单篇索引.md` | 130 条目的存在性证据 |
| `evidence/kb/_MOC_100papers.md` | 源 `_MOC_100papers.md` | 三表入口与分类口径 |
| `evidence/kb/_索引_批量审稿75批.md` | 源同名 | 75 批存在性证据 |
| `evidence/kb/_索引_论文卡片53.md` | 源同名 | 51 卡片存在性证据 |
| `evidence/kb/_索引_arXiv_TMLR状态.md` | 源同名 | arXiv/TMLR 状态权威源 |

## 使用纪律（paper-writing-agent 硬规则映射）

1. Related Work / GAP 引用的每一篇必须点名单篇笔记路径（如 `单篇/论文卡片/X.md`），不得只写"相关研究表明"。
2. 凡写"共 N 篇 / 覆盖 M 批"类数字，必须与 CLAIM_LEDGER 的 KB01–KB03 条目一致（75/51/4/130）。
3. 源库新增笔记后，先同步快照到 `evidence/kb/` 再重跑 manifest `--verify`，否则 Phase 3 视为 stale。
4. 起草顺序：LITERATURE_REVIEW（从单篇笔记提炼 GAP）→ CLAIM_LEDGER → Methods/Results → Discussion → Abstract 最后对齐。
5. 下一步可选：选定 1 个投稿方向后跑 D0 文献综述产出 `LITERATURE_REVIEW.md`，再进入 Phase 1。
