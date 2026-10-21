# LITERATURE_REVIEW.md（D0：130篇笔记接入）

> 项目：paper_workflow_kb。检索与提炼日期：2026-09-07。
> 源库（只读，不复制正文）：`~/文档/ObsidianKnowledgeBase/01 - Papers/_组织/`
> 单篇笔记 130 = 批量审稿 75 + 论文卡片 51 + arXiv投稿 4（C01–C03 已核验，见 CLAIM_LEDGER）。
> 经验检索：`retrieve_experience.py` ledger 缺失（`.agent-memory/ledger/lessons.md` 不存在），降级为无经验摘要进入 D0（已记录，不阻塞）。
> 诚实声明：本综述仅基于单篇笔记摘录（每张前45行）与源索引提炼；凡笔记区标"待填/待读"者，其贡献一律标 `inconclusive`，不进 novelty 强声明。

## 检索式与日期（可复现）

| # | 检索动作 | 日期 | 结果 |
|---|---|---|---|
| R1 | 源库盘点：`ls 单篇/批量审稿|论文卡片|arXiv投稿` | 2026-09-07 | 75 / 51 / 4 = 130（与 `_单篇索引.md` 130 条一致） |
| R2 | 卡片标题提取（python 读前3000字符取 frontmatter title + H1） | 2026-09-07 | 51 标题全表（见 L06–L56） |
| R3 | 实质卡片精读抽样：Calibration Self-Improvement（90行）、BATCH_R901（46行）、PAPER1_arxiv（36行） | 2026-09-07 | 确认三类性质：实质研究卡 / 审稿日志 / PDF待读 |
| R4 | 权威状态源对照：`_MOC_100papers.md` + `_索引_arXiv_TMLR状态.md` | 2026-09-07 | arXiv 10发表+11在投、TMLR #47–56 审稿中 10 篇、Zenodo 40 publish（沿用论文清单口径，不在本综述重断言） |

L0 scout 说明（按文献综述工作流 L0 必做，本轮为内源 scout）：bleeding-edge/frontier 外源增量扫描尚未跑；
当前池全部为内源笔记（classic/mid-term 为主），新鲜度天然过期——见文末"新鲜度门禁"，
投稿前必须跑 `check_literature_freshness.py` + arXiv 增量扫描。外源 scout 留待选定投稿方向后补跑。

## 文献池（L01..，一句话贡献 + 链接）

### Tier A：实质研究卡（5张，有正文可核验，强相关）

| 编号 | 卡片（单篇笔记） | 一句话贡献 | 源 |
|---|---|---|---|
| L01 | Calibration Self-Improvement | 同一批回答三档 matcher 口径翻转校准结论：exact 63.3%/ECE 0.363 → tolerant 86.7%/0.1297 → 裁决后 100%/0.0037；27/30=1.0 退化使 binning ECE 不可识别 | `单篇/论文卡片/Calibration Self-Improvement.md` → 源 `/data3/Research/01_论文区/论文卡片/Calibration Self-Improvement.md` |
| L02 | SciEvalSuite | 科学 agent 统一可复现 harness（三层 run.json，568 calls，46-entry SHA-256 18/18 重算）；无 matcher 三档翻转，不构成 C07 反例（2026-09-07 已精读源卡片 47 行） | `单篇/论文卡片/SciEvalSuite.md` |
| L03 | Agent Comparison Protocol | 三层统计协议 McNemar/Wilcoxon/Friedman（30 合成任务三层全检出）；无校准内容，不构成 C07 反例（已精读 70 行） | `单篇/论文卡片/Agent Comparison Protocol.md` |
| L04 | Answer Fitting Audit | 答案拟合审计（TARGET 模式扫描，4 脚本验证）；无校准翻转，不构成 C07 反例（已精读 49 行） | `单篇/论文卡片/Answer Fitting Audit.md` |
| L05 | 10Paradigm Agent OS | 10 范式 Agent OS systems artifact（CRM n=300 Δ0.110，p=8.69e-06）；无校准 matcher，不构成 C07 反例（已精读 89 行） | `单篇/论文卡片/10Paradigm Agent OS.md` |

### Tier B：工程基建卡 ext_*（21张，背景相关，非论文主张）

| 编号 | 组 | 成员 | 一句话定位 |
|---|---|---|---|
| L06–L26 | ext 工程系列 | ext_01_rag_knowledge_base / ext_02_agent_workflow / ext_03_multi_model_gateway / ext_04_guardrails_chat / ext_05_vector_db_manager / ext_06_lora_finetune / ext_07_code_review_agent / ext_09_multimodal_doc_understanding / ext_11_dify_workflow / ext_12_prompt_eval_framework / ext_14_mcp_tool_integration / ext_15_agent_security_sandbox / ext_16_kg_rag_fusion / ext_17_llm_observability / ext_18_agent_long_term_memory / ext_19_voice_ai_assistant / ext_20_llm_eval_benchmark / ext_archive_08_smart_customer_service / ext_archive_10_inference_optimization / ext_archive_13_paper_review_agent / README | RAG/工作流/网关/Guardrails/向量库/LoRA/代码评审/多模态/可观测/记忆/评测基准等基建笔记；支撑"可复现执行层"背景，不支撑科学主张；2026-09-07 L06 批次 21 张全部精读源全文（20×39 行 + README 11 行），matcher 类关键词 0 命中，无反例 |

### Tier C：work-mode 探索卡（18 个文件 / 17 条目，pilot 想法，2026-09-07 已精读源全文，仍全部 inconclusive）

| 编号 | 成员 | 一句话定位 |
|---|---|---|
| L27–L41 | work-mode_6a5f555f_Agent_Economics / 6a5f556b_Agent_Unlearning / 6a5f557c_MorphAgent_Textbook / 6a5f5585_Lewis_Signaling_&_GridWorld / 6a5f558e_Agent_Sleep / 6a5f5594_Agent_Mortality / 6a5f55a1_Rituals_Without_Priests / 6a5f55bc_Boredom_&_Intrinsic_Motivation / 6a5f55c3_Agent_Burnout / 6a5f55ca_Friendship_v1+v2 / 6a5f55d1_LieBench / 6a5f55de_Alien_LLM_&_Causal_Fragility / 6a5f55e6_Agent_Soul / 6a5f55ec_Vending_Env / 6a5f55f8_Agent_Addiction / 6a5f5971_Task_Gravity / 6a5eac7d_丢失项目查找报告 | 探索性 pilot（Agent 经济/遗忘/睡眠/倦怠/友谊 v1+v2/谎言基准/因果脆弱性等）；2026-09-07 L27 批次 18 文件源全文已精读（17×65 行 + 丢失项目报告 65 行，word-boundary 关键词 0 命中，LieBench 子串 ECE 系 Deception 误报已复核），0 反例；均为想法记录、笔记区三节待填，不可作为 Related Work 支撑 |

### Tier D：批量审稿日志（75批，R901–R975，方法学背景，非一手文献）

| 编号 | 范围 | 一句话贡献 | 例 |
|---|---|---|---|
| L42–L116 | BATCH_R901 – BATCH_R975（75） | 云端 qwen3:4b 三并行 ten-review 评分日志；累计 783/1000（78.3%）；记录的是"评审活动"而非被评论文的主张，不可转引为科学结论 | R901：tmlr_p7/p11/PAPER12 各 1/10 满分 5.0（`单篇/批量审稿/BATCH_R901.md`） |

### Tier E：arXiv 投稿 PDF（4个，二进制待精读）

| 编号 | 笔记 | 状态 |
|---|---|---|
| L117–L120 | PAPER1_arxiv / PAPER2_arxiv / PAPER4_arxiv / PAPER5_arxiv（`单篇/arXiv投稿/`） | 2026-09-07 已精读 PDF 全文（pdftotext：26/14/20/29 页）：P1 通信效应校准分解（+0.228→+0.207/+0.021，与三档 matcher 正交）/ P2 TTRL bound 理论 / P4 N-灵敏度框架 / P5 记忆架构；四篇 matcher/tolerant/adjudicated 关键词 0 反例，不构成 C07 反例 |

### Tier F：TMLR 在审（10篇，指针，不重复断言）

| 编号 | 内容 |
|---|---|
| L121 | TMLR #47–56 审稿中 10 篇 + ENWI 提交包 + Zenodo 40 publish / 40 draft：权威源为 `/data3/Research/论文清单.md`（2026-08-24版），本综述仅指针，不复制其数字 |

## 方法族归纳表（结构优先，非流水账）

| 方法族 | 机制 | 适用条件 | 已知失败模式 | 代表（本池） | 证据强度 |
|---|---|---|---|---|---|
| 置信度校准测量（matcher 敏感型） | exact/tolerant/逐行裁决三档判定 + binned ECE / smECE / isotonic OOS / MSI | 有 gold、可裁决的 QA/评测集；需报告 matcher 口径 | 标签判定器翻转结论（63.3%→86.7%→100%）；27/30=1.0 退化致 binning ECE 不可识别；跨域差最高 17×（biology 0.1205 vs math 0.479）；自报置信度 OOD 有害 | L01 | verified（L01 摘录 R28：502 manifest / 81 ledger / 外审 8.2/10） |
| 评测协议与审计 | 双 judge（κ0.699）+ human 抽检 + holdout（precision 1.0/recall 0.8276）+ Docker 固化（python:3.12.6-slim，lock 245） | 多模型×多域 census（9模型×600×6域，4999双裁决） | 单轮观测、三臂 N=30 小样本（paired-t 功率仅 0.587，MDE 2.12） | L01–L04 | 部分 verified（功率数来自 L01），其余 inconclusive |
| Agent 横向对比与行为探索 | 对比协议 / LieBench / GridWorld signaling / 友谊 pilot 等 | 探索性 pilot、小 N 行为观测 | 均为想法记录，无功率分析、无复现包 | L03, L27–L41 | inconclusive |
| 基建层（RAG/记忆/可观测/Guardrails） | 知识库/向量库/工作流/网关/沙箱 | 工程执行层 | 不回答科学问题，不可作基线 | L06–L26 | 背景（background） |
| 批量评审活动 | qwen3:4b 云端三并行打分 | 内部质量监控 | 评分者即模型（自偏好风险未校准），不可作"同行共识"引用 | L42–L116 | 背景（评审日志） |

## 评测协议惯例（与 protocol.md 对齐用）

- 校准报告必须同时给出：matcher 口径（exact/tolerant/adjudicated）+ 置信度分布直方图（是否退化）+ ECE 变体（binned/smECE/OOS）+ 跨域分表。仅报单一 binned ECE 者视为口径不完整（L01 教训）。
- 小样本（N≤30）必须报功率或最小可检测效应（L01：N=12 时 paired-t 功率 0.587、MDE 2.12）；N=4 级别 McNemar 功率≈0 不得做强结论。
- 多模型比较优先双裁决 + human 抽检（κ 及正算非零率 0.811/0.224/0.087 见 L01）；单 judge 单轮观测必须 hedge。
- 复现包：Dockerfile + requirements.lock（hash 锁定）+ probe solvable；缺失者降级为 candidate，不进 verified。

## GAP 陈述（4句，逐条可证伪，每条对应 Methods 设计）

1. **G1（matcher 可证伪）**："若固定同一批回答仅切换 matcher（exact→tolerant→adjudicated），校准结论（accuracy±5pp、ECE±0.05）保持不变"——L01 已证伪该不变性（63.3%→86.7%→100%），对应 Methods 设计 M1：任何校准实验必须三档口径同报 + 翻转集逐行裁决（verify_labels 门）。
2. **G2（退化分布可证伪）**："置信度-output 分布退化度（众数占比）与 binned ECE 偏差无关"——L01 反例（27/30=1.0 时 ECE 0.363 vs 0.0037），对应 M2：先报分布退化度，众数占比>80% 时禁用 binned ECE、改用 smECE/OOS。
3. **G3（跨域可证伪）**："同一模型校准误差跨域恒定（max/min<2×）"——L01 反例（17.11×），对应 M3：评测必须分域报告 + 跨域显著性检验，不得只报平均。
4. **G4（空白，可证伪的 inconclusive）**："L02–L05、L27–L41、L117–L120 中至少一篇已给出 matcher 口径无关的校准估计量"——当前未知（全部待精读），对应 M4：逐张精读回填后若仍无，则本论文以"口径无关估计量（smECE/MSI/OOS）对比"为投稿增量；若已有，则改写定位并补基线。

## 基线池清单（D1/D3 对比方法，全部可溯源）

| 基线 | 来源 | 何时用 |
|---|---|---|
| exact-string matcher + binned ECE | L01 三档之 A | 必跑（展示翻转起点） |
| tolerant matcher + binned ECE | L01 三档之 B | 必跑 |
| adjudicated labels + binned ECE | L01 三档之 C | 金标准对照 |
| smECE（语义软标签）+ MSI | L01（0.2349→0.1812，−22.9%） | 口径无关候选基线 |
| isotonic / vector / Dirichlet OOS（0.0375/0.041/0.039） | L01（C66/C68/C82） | OOS 对照组 |
| self-consistency 门控（OOD 相关 −0.20，AUC 0.167→0.995） | L01（C49/C78） | OOD 门控基线 |
| L02–L05 方法 | 待精读回填后补入 | 回填前不得占位引用 |
| Ranked-by-the-Matcher 动机参照（2609.01671：8 协议重排 11/45 逆转，固定预测集 F1 跨 0.16–0.70；机械 matcher 与多人 adjudication 一致 ≤71%，LLM judge 86%） | 外源增量 scout 2026-09-07（Hakim & Song，cs.CR/cs.AI/cs.CL，摘要全文见外源增量 scout 记录表） | Related Work 必引（matcher 依赖性动机支撑）；非可跑基线——知识图谱三元组抽取领域，无 accuracy+ECE 同报，不可作 D1 对照实验 |

## "据我们所知/首次"类候选声明（对应 ledger C07/C08，须附文献条目，当前全部 hedge）

- C07（verified，库内范围限定，2026-09-07 L02+L06+L27 批次回填升级）："在已精读库内范围（L01–L05 实质卡 + L06–L26 工程卡 + L27–L41 探索卡 18 文件 + L117–L120 四投稿 PDF 全文）中，无工作在同一批回答上同时报告三档 matcher 下 accuracy 与 ECE 的翻转幅度"——L02–L05 源卡片全文 + L06–L26 源全文 21 张关键词 0 命中 + L27–L41 源全文 18 文件 word-boundary 关键词 0 命中（LieBench 子串 ECE 系 Deception 误报，已全文复核排除） + 四 PDF 全文关键词扫描（matcher/tolerant/adjudicated 0 反例）支撑；正文仍写 "we are not aware of ..."；库外新工作以后续 arXiv 增量 scout（新鲜度门禁）为准，Phase 5 前必跑。
- C08（inconclusive，原 N2）："据我们所知，退化分布下 binned ECE 不可识别问题尚无标准替代流程"——smECE/MSI 是否已成标准未知，待补外源 scout 后复核。
- N3（verified 范围限定，并入 C05 如何验证）："在本知识库已精读范围内（L01），matcher 翻转与退化失效成立"——限定范围，可进 ledger verified；不得泛化到库外。

## 质量检查

- [x] 每个 GAP 子句可证伪且对应一个 Methods 设计（G1→M1 … G4→M4）
- [x] 基线池只含可溯源方法；待读项明确标 inconclusive，未混入
- [x] 指标/种子数/功率惯例来自 L01 实数（N=12 功率 0.587、MDE 2.12），与 protocol 对齐待 D1 复核
- [x] "首次/最优"声明全部 hedge + 命名升级条件，无强断言
- [x] L02 批次精读回填（2026-09-07）：L02–L05 源卡片全文 + L117–L120 四 PDF 全文（pdftotext 26/14/20/29 页），matcher/tolerant/adjudicated 0 反例；8 张单篇笔记"待填→已精读"（见下节记录）
- [x] L06 批次精读回填（2026-09-07）：L06–L26 工程卡 21 张源全文（20×39 行 + README 11 行），关键词 0 命中，0 反例；21 张单篇笔记"待读→已精读"（见 L06 记录表）
- [x] L27 批次精读回填（2026-09-07）：L27–L41 探索卡 18 文件源全文（18×65 行），word-boundary 关键词（\bECE\b/\bmatcher\b/\btolerant\b/adjudicat）0 命中，0 反例（见 L27 记录表）；计数勘误：前版"15张"实为 18 文件/17 条目（Friendship v1+v2 为两文件），已更正
- [ ] LITERATURE_REVIEW.md 随 evidence_manifest 哈希入账（下一步跑脚本）

## 精读回填记录（L02 批次，2026-09-07，C07 升级依据）

| 笔记 | 精读源 | 反例检查 | 结论 |
|---|---|---|---|
| L02 SciEvalSuite | 源卡片 47 行全文 | matcher/ECE 翻转 0 命中 | 无反例 |
| L03 Agent Comparison Protocol | 源卡片 70 行全文 | 无校准内容 | 无反例 |
| L04 Answer Fitting Audit | 源卡片 49 行全文 | 无校准翻转 | 无反例 |
| L05 10Paradigm Agent OS | 源卡片 89 行全文 | 无校准 matcher | 无反例 |
| L117 PAPER1_arxiv | PDF 26 页全文（103878 字符） | matcher/tolerant/adjudicated 0 命中；100% 仅 2 处非翻转语境 | 无反例 |
| L118 PAPER2_arxiv | PDF 14 页全文（42288 字符） | exact 仅无关语境 2 处；tolerant/adjudicated 0 | 无反例 |
| L119 PAPER4_arxiv | PDF 20 页全文（69931 字符） | 校准案例为通信/时间分解（与三档 matcher 正交） | 无反例 |
| L120 PAPER5_arxiv | PDF 29 页全文（96715 字符） | exact 仅无关语境 1 处 | 无反例 |

方法：源卡片逐行读；PDF 用 pdftotext -layout 全文提取 + 关键词（matcher/exact/tolerant/adjudicat/ECE/c librat/63.3/86.7）计数 + 命中上下文复核。MinerU 服务不可用（fetch failed），降级为 pdftotext（已记录）。
升级语义：verified 限定"已精读库内范围"；库外以后续 arXiv 增量 scout 为准（Phase 5 新鲜度门禁仍有效）。

## 精读回填记录（L06 批次，2026-09-07，Tier B 工程卡 21 张，C07 范围扩展依据）

方法：/data3 源卡片全文读 + 单篇笔记摘录对照 + 关键词（matcher/exact/tolerant/adjudicat/ECE/calibrat/校准/63.3/86.7/smECE/MSI）大小写不敏感计数。21 张源全文（20 张 39 行 + README 11 行）全部 0 命中；工程脚手架卡无实验数字、无校准内容，不构成 C07 反例。单篇笔记 21 张"待读→已精读"，三节（核心观点/方法与证据/关联）已回填，数字仅源文件行数与字符数。

| 笔记 | 源全文 | 反例检查 | 结论 |
|---|---|---|---|
| L06 ext_01_rag_knowledge_base | 源 39 行 758 字符 | 关键词 0 命中 | 无反例 |
| L07 ext_02_agent_workflow | 源 39 行 735 字符 | 关键词 0 命中 | 无反例 |
| L08 ext_03_multi_model_gateway | 源 39 行 762 字符 | 关键词 0 命中 | 无反例 |
| L09 ext_04_guardrails_chat | 源 39 行 726 字符 | 关键词 0 命中 | 无反例 |
| L10 ext_05_vector_db_manager | 源 39 行 740 字符 | 关键词 0 命中 | 无反例 |
| L11 ext_06_lora_finetune | 源 39 行 725 字符 | 关键词 0 命中 | 无反例 |
| L12 ext_07_code_review_agent | 源 39 行 730 字符 | 关键词 0 命中 | 无反例 |
| L13 ext_09_multimodal_doc_understanding | 源 39 行 797 字符 | 关键词 0 命中 | 无反例 |
| L14 ext_11_dify_workflow | 源 39 行 720 字符 | 关键词 0 命中 | 无反例 |
| L15 ext_12_prompt_eval_framework | 源 39 行 764 字符 | 关键词 0 命中 | 无反例 |
| L16 ext_14_mcp_tool_integration | 源 39 行 748 字符 | 关键词 0 命中 | 无反例 |
| L17 ext_15_agent_security_sandbox | 源 39 行 761 字符 | 关键词 0 命中 | 无反例 |
| L18 ext_16_kg_rag_fusion | 源 39 行 717 字符 | 关键词 0 命中 | 无反例 |
| L19 ext_17_llm_observability | 源 39 行 757 字符 | 关键词 0 命中 | 无反例 |
| L20 ext_18_agent_long_term_memory | 源 39 行 774 字符 | 关键词 0 命中 | 无反例 |
| L21 ext_19_voice_ai_assistant | 源 39 行 735 字符 | 关键词 0 命中 | 无反例 |
| L22 ext_20_llm_eval_benchmark | 源 39 行 751 字符 | 关键词 0 命中 | 无反例 |
| L23 ext_archive_08_smart_customer_service | 源 39 行 803 字符 | 关键词 0 命中 | 无反例 |
| L24 ext_archive_10_inference_optimization | 源 39 行 805 字符 | 关键词 0 命中 | 无反例 |
| L25 ext_archive_13_paper_review_agent | 源 39 行 783 字符 | 关键词 0 命中 | 无反例 |
| L26 README（目录说明） | 源 11 行 130 字符 | 关键词 0 命中 | 无反例（非论文） |

升级语义：C07 verified 范围从"L01–L05+L117–L120"扩展为"L01–L05+L06–L26+L117–L120"（累计已精读 29 张）；仍限定库内，库外以 Phase 5 增量 scout 为准。

## 精读回填记录（L27 批次，2026-09-07，Tier C 探索卡 18 文件，C07 范围扩展依据）

方法：源卡片全文读 + word-boundary 关键词（\bECE\b/\bmatcher\b/\btolerant\b/adjudicat\w*，大小写不敏感）计数 + 命中上下文复核。初扫子串匹配在 LieBench 报 ECE×2，复核为 "Deception/deception" 子串误报（word-boundary 0 命中），并全文读该卡确认：仅为欺骗检测基准 pilot 想法记录（68 文件综述 + 三模型 pilot 计划），笔记区三节待填，无 accuracy/ECE 数字，不构成反例。其余 17 文件全部 0 命中。18 文件均为 pilot 想法记录，不可作 Related Work 支撑，Tier C 整体仍 inconclusive。

| 笔记 | 源全文 | 反例检查 | 结论 |
|---|---|---|---|
| L27 work-mode_6a5f555f_Agent_Economics | 源 65 行 1757 字符 | word-boundary 0 命中 | 无反例 |
| L28 work-mode_6a5f556b_Agent_Unlearning | 源 65 行 1346 字符 | word-boundary 0 命中 | 无反例 |
| L29 work-mode_6a5f557c_MorphAgent_Textbook | 源 65 行 1564 字符 | word-boundary 0 命中 | 无反例 |
| L30 work-mode_6a5f5585_Lewis_Signaling_GridWorld | 源 65 行 1624 字符 | word-boundary 0 命中 | 无反例 |
| L31 work-mode_6a5f558e_Agent_Sleep | 源 65 行 1563 字符 | word-boundary 0 命中 | 无反例 |
| L32 work-mode_6a5f5594_Agent_Mortality | 源 65 行 1620 字符 | word-boundary 0 命中 | 无反例 |
| L33 work-mode_6a5f55a1_Rituals_Without_Priests | 源 65 行 1548 字符 | word-boundary 0 命中 | 无反例 |
| L34 work-mode_6a5f55bc_Boredom_Intrinsic_Motivation | 源 65 行 1766 字符 | word-boundary 0 命中 | 无反例 |
| L35 work-mode_6a5f55c3_Agent_Burnout | 源 65 行 1281 字符 | word-boundary 0 命中 | 无反例 |
| L36 work-mode_6a5f55ca_Friendship_v1 | 源 65 行 1669 字符 | word-boundary 0 命中 | 无反例 |
| L37 work-mode_6a5f55ca_Friendship_v2 | 源 65 行 1696 字符 | word-boundary 0 命中 | 无反例 |
| L38 work-mode_6a5f55d1_LieBench | 源 65 行 1606 字符 | 子串 ECE×2 系 Deception 误报，word-boundary 0 命中，全文已复核 | 无反例 |
| L39 work-mode_6a5f55de_Alien_LLM_Causal_Fragility | 源 65 行 1654 字符 | word-boundary 0 命中 | 无反例 |
| L40 work-mode_6a5f55e6_Agent_Soul | 源 65 行 1304 字符 | word-boundary 0 命中 | 无反例 |
| L41a work-mode_6a5f55ec_Vending_Env | 源 65 行 1540 字符 | word-boundary 0 命中 | 无反例 |
| L41b work-mode_6a5f55f8_Agent_Addiction | 源 65 行 1350 字符 | word-boundary 0 命中 | 无反例 |
| L41c work-mode_6a5f5971_Task_Gravity | 源 65 行 1569 字符 | word-boundary 0 命中 | 无反例 |
| L41d work-mode_6a5eac7d_丢失项目查找报告 | 源 65 行 1250 字符 | word-boundary 0 命中 | 无反例（非论文） |

升级语义：C07 verified 范围扩展为"L01–L05+L06–L26+L27–L41（18 文件）+L117–L120"（累计已精读 47）；仍限定库内，库外以 Phase 5 增量 scout 为准。

## 外源增量 scout 记录（2026-09-07，C07 库外复核）

方法：`arxiv_incremental.py --fetch --days 30`（cs.CL/cs.AI/cs.LG/stat.ML，peS2o 54万基座去重）×3 查询：
"calibration ECE" 新增 166 → "exact match evaluation" 新增 162 → "LLM agent evaluation harness" 新增 46，
增量库累计 374 篇。筛查脚本 `scout_c07_screen.py`（matcher 档位词 × 校准词双命中）：matcher 命中 33，
calibration 命中 165，双命中候选 11 篇，摘要逐条全文裁决（`scout_c07_abstracts.py`）。

| 候选 arXiv ID | 标题 | 裁决 |
|---|---|---|
| 2609.01741 | Statute survival certificate（exact/5% tolerance 门，Wilson 界） | 无反例：法定逻辑存活证书，无 accuracy+ECE 三档翻转 |
| 2609.01456 | AutoConcept 图像检索重排（inference-time calibration） | 无反例：检索重排，无 matcher 档位翻转 |
| 2609.01671 | Ranked by the Matcher（8 协议重排 11/45 逆转，F1 跨 0.16–0.70；机械 matcher 与多人 adjudication 一致 ≤71%） | 无反例（C07 要求 accuracy+ECE 同报翻转，本文无 ECE），但列为强相关工作：支持 matcher 依赖性动机，Related Work 必须引用讨论 |
| 2609.03966 | Interface-Induced Trajectory Censoring（0.00 vs 0.96/0.19） | 无反例：服务适配器审查轨迹，非 matcher 档位 |
| 2609.02750 | Bilevel Coordinated Reflection（calibration 为收敛条件） | 无反例：理论收敛，无实验翻转 |
| 2609.02196 | Schrödinger Bridges（Bridge Calibration 系传输校准） | 无反例：生成建模，无关语境 |
| 2609.01783 | SME-BETEL（贝叶斯校准） | 无反例：不涉及 matcher 档位 |
| 2608.23638 | Replicable Conformal Prediction（校准阈值稳定性） | 无反例：一致性预测，无 matcher 档位 |
| 2608.12100 | Confidence Calibration of Deep Learning Systems（标签噪声下校准 thesis） | 无反例（无三档翻转），列为弱相关工作：标签噪声 vs matcher 噪声对照 |
| 2608.10566 | Erasure Count（Adam/QR calibration 系优化器校准） | 无反例：无关语境 |
| 2608.08911 | Acoustic Localization（calibrated uncertainty 系传感器语境） | 无反例：无关语境 |

结论：30 天窗口 374 篇增量中 0 反例。C07 范围扩展为"库内精读 47 + 30 天增量 374 筛查"；
诚实边界：scout 仅覆盖 3 查询×4 分类×30 天，peS2o 基座未做语义筛查，正文仍 hedge；
2609.01671 已入基线池（Related Work 必引行，2026-09-07），投稿前 Phase 5 再跑一次增量。

## 新鲜度门禁（投稿前必跑）

- 本文件 mtime = 2026-09-07；`--max-age-days 30` 下约 2026-10-07 过期，Phase 5 前必须重跑。
- 外源 L0 scout（bleeding-edge/frontier ≥35%、三档 ≥60%）尚未跑：选定投稿方向后按立项日期过滤 arXiv 增量，只审新条目（方法族新成员 / GAP 被抢先 / 基线池补方法），逐条对照 C07/C08 并同步 CLAIM_LEDGER 与 ROUND 记录。

## 2026-09-07 补充增量 scout（校准向 3 查询，44 篇）

- 脚本 `scripts/incr_scout_0907.py`（arXiv API https，2026-08-08→2026-09-07）：3 查询（llm+calibration+confidence / exact-match+QA+tolerance / calibration+ECE+judge），去重后 44 篇，关键词筛查 flip-likely=0、eceproc=0。
- 相邻摘要全文精读 2 篇，均非反例：2608.07827（token-probability 聚合做 math-QA 置信度+Platt/isotonic；无 matcher 档位翻转；列为方法相邻候选引用，引用前须全文核验）→ 支持 isotonic/Platt 对照选择；2608.20511 EDGE（二分类 logistic 回归的校准形式检验；binned ECE"描述性、无零分布、依赖分箱"的批评与 C08 叙述一致，非本设定标准流程；列为方法批评候选引用，引用前须全文核验）。
- 结论：补充 44 篇中 0 反例；C07 范围维持"库内精读 47 + 374 增量筛查 + 本轮 44 篇补充"，正文仍 hedge（scout 查询覆盖有限，peS2o 基座未筛查）。
