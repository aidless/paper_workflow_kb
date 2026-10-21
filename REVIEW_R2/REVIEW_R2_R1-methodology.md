# Review Round R2 — R1 方法论 复核报告（R15修改版）

- 日期：2026-09-08 ｜ 手稿：paper_workflow_kb/paper/main.tex（R15版，264行）
- 审稿角色：R1 方法论（R2轮，独立审稿，未与其他角色交流，未修改手稿）
- 输入：ROUND_R15.md（10项修复清单）、REVIEW_R1_R1-methodology.md（R1报告）、CLAIM_LEDGER.md、results/ 与 evidence/ 一手证据
- 总体判断：R15把R1的Critical与全部Major修到可接受水平，无新Critical/Major；残留2处R1措辞回归（均为Minor）+ 1个新Minor + 1个新Nit。方法论层面可收敛（pending Minor/Nit可选修）。

## 1. R15修复项逐条复核结论

| R1原问题 | R15对应修项 | 结论 | 行号证据 |
|---|---|---|---|
| R1-01 Critical：H1比例命题 vs McNemar方向检验错位，5%无出处 | #1 H1方向化+5%降描述性bar | 已修好 | main.tex L63-64（H1改配对非对称命题+McNemar；5%为G006描述性bar+程序gate非H1部分）；用法一致：L67/L196显著层"supports H1 inferentially"，L68-69/L200/L202/L210/L212/L218 ns层仅"clears/misses descriptive bar"；L75池双读数并列 |
| R1-02 Major：guard循环+knob因果 | #9 guard降级 | 已修好（核心），knob隐喻残留见R2-R1-01 | L123"in-sample by construction"+"no synthetic targeting test"；L239"in-sample (one fix, zero regressions)"；out-of-sample支撑限定于新题臂+470行回归 |
| R1-03 Major：adjudication gate触发式 vs 全裁决式矛盾 | 未在10项中具名，属附带修 | 已修好（核心），L216触发措辞残留见R2-R1-02 | L64统一为全裁决语义（each flip must be adjudicated）；实践全覆盖；67/68总数本轮重算吻合（见§3） |
| R1-04 Major：裁决三重自由度 | 未具名（R1-R8去重附带） | 已修好 | L222双pass全在案（16/3/2+5/5→content 21/21）+泄漏归因证据；L55/L80单/双rater分解（20/21 vs 9/9 vs 21/21 vs 10/10 vs 7/7）；lead-number用content-basis属编辑选择，first-pass数同句可审计 |
| R1-05 Major：ECE双口径混用 | #6 口径注释 | 已修好 | L119分箱披露+sealed哈希不动理由+统一重算列future work；L206 tempscale等频vs等宽+cloud-new T=1同值0.1692系巧合注；表注L141每层内单一口径 |
| R1-06 Major：摘要五显著无Holm限定 | #3 | 已修好 | L54"two of the five survive (pilot, cross-domain loose); the other three are stratum-local"；与results/holm.json一致（见§3）；L243程序止步step3（pool p=0.0039>阈值0.00333） |
| R1-07 Major：功效循环 | #4 | 已修好 | L131"post-hoc…sensitivity checks rather than pre-data power justifications"+placeholder OR=4；池降级"Only the pool composition was pre-specified…stratum-local observed significance"；L245 ceilings"met by construction…not pre-registered power conclusions" |
| R1-08 Major：pilot50跨模型p值 | #5 | 已修好 | L226"descriptive only with no p-value claimed; the pilot inference rests on the 30-row stratum"；L78/L234跨模型仅描述性；rollup重叠披露同段 |
| R1-09 Minor / R1-10 Nit | 不在R15范围 | 未动（out-of-scope，原样保留） | L224已披露999/1000系0.5%容差接受（诚实但无敏感性表）；标题计数未动。不计入回归 |
| #7 RW（hakim2026+L01 delta） | #7 | 已修好 | L85 hakim2026ranked动机引用+域外声明；paper/main.bib L43条目在；hallucination门已过；L89 L01三档delta（63.3/0.363→100/0.0037同一pilot+四点delta） |
| GOLD 24/25 + 67/68 | #2 | 已修好 | L55/L80/L232五处一致；与results/gold_guarded_agreement.json一致（见§3重算）；G06分歧具名披露 |

## 2. 问题清单（仅R1未提过的新问题 + R1修复失败项）

| ID | 严重度 | 位置 | 问题 | 期望 | 证据链接 | 类型 |
|---|---|---|---|---|---|---|
| R2-R1-01 | Minor | L239"as the control knob"、L247"control knob"（对比L241已 hedge"regime contrast…rather than a universal knob"） | R15修项#9自述"control knob→regime contrast（2处）"，但因果隐喻"knob"在摘要L54"prompt-knob"、讨论L239/L247残留无hedge；与本稿C42证据（复制题上knob不复现）直接冲突，读者可误读为通用因果开关 | 全文统一为"regime contrast"，或在L239/L247同句加"question-type-dependent, not universal"限定 | main.tex L239/L247 vs L241/L245/L228；results/powrep_loose.json（tight b3 vs loose b3、本地tight b7 vs loose b4）；ROUND_R15.md L22 | R1回归（R1-02子项修补不全） |
| R2-R1-02 | Minor | L216"No adjudication is required (zero flips fall below the adjudication gate's 5% trigger)" | 全稿已统一全裁决语义（L64 each flip must be adjudicated），此处残留"5% trigger"触发式措辞，把G006描述性bar与adjudication gate混为一谈；零翻转层按任一语义均无需裁决，故无数字后果，纯术语污染 | 改为"No adjudication is required (zero flips, nothing to adjudicate)"，删"5% trigger" | main.tex L216 vs L64；ROUND_R15.md修项#1 | R1回归（R1-03子项残留） |
| R2-R1-03 | Minor | L220"second significant"、L226"third and fourth significant" vs L54/L239"five significant" | 序数链只数到第四（pilot隐含第一+xloose第二+两扩展第三/四），显著池（p=0.0039）被排除在序数链外，与"five paired inferences are significant"自相矛盾；任一计数口径下序数与总数不能同时成立 | 删序数词（改"also significant"），或把池编入给"fifth"并说明口径 | main.tex L54/L214/L220/L226/L239；results/holm.json（ordered 17项） | new |
| R2-R1-04 | Nit | L54"p=0.0005" vs L226"p=0.00049"（同一localnew217） | 同一数字两种舍入并存 | 统一为0.00049（与results/powrep_rollups.json字段0.00048828125的常规舍入一致） | main.tex L54/L226；results/powrep_rollups.json→strata.localnew217.mcnemar_p_two | new |

## 3. 独立重算（Python3一手重算，非复述账本）

- Wilson 95% CI（24/25，z=1.96）：重算 **[0.80456, 0.99290]**；正文L55/L232"0.805 to 0.993"为正确舍入；证据results/gold_guarded_agreement.json→wilson95 [0.8045552759497747, 0.9929039496133009]一致。**一致**。
- McNemar精确双侧：b=9/c=0→2×0.5⁹=**0.00390625**（L214/L243 pool p=0.0039；results/combined_qwen2.json→mcnemar_p_two一致）；b=20→**1.9073486328125e-06**（L157/L220 p=1.9e-6；results/holm.json ordered[0]一致）；b=7→0.015625（L226 holdout108）；b=12→0.00048828125（L226 localnew217）。**全一致**。
- 67/68分解重算：20+9+21+10+7=**67**；分母21+9+21+10+7=**68**（=16/16+4/5先验双层20/21；local-new 5/5+local-big 4/4扩展9/9；xdomain 21/21；powrep 10/10；loose-regime 7/7）。L55/L80组成数字与evidence/cloud_judge_16.json、cloud_judge_new60.json、local_adjudication.json、big_adjudication.json、xdomain_adjudication.json→content_correct=21、powrep_judge.json、powrep_loose_judge.json各自n_correct一致。**一致**。
- 翻转总数：11+5+4+5+0+4+0+1+20+0+2+1+7=**60**=854−794（L234 merged 60 flips, 0.0637）。**一致**。
- Holm：holm.json→m=17、survivors=[xdomain-loose, pilot]、stop step3 pool p=0.00390625>阈值0.0033333333333333335；L243转述准确。**一致**。

## 4. 收敛判定

- 本轮新Critical：**0** ｜ 新Major：**0** ｜ 新Minor：1 ｜ 新Nit：1 ｜ R1回归Minor：2 ｜ R1修复失败Critical/Major：0。
- 方法论维度**收敛**（无阻塞项；R2-R1-01/02/03/04均为投前可选小修，建议与R2微调轮合并处理，不值得单独开轮）。
