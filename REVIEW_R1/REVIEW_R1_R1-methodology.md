# Review Round R1 — R1 方法论 审稿报告

- 日期：2026-09-07 ｜ 论文：Exact versus Tolerant Label Matching… ｜ 审稿角色：R1 方法论
- 独立审稿声明：本报告独立完成，未参考其他角色意见。

## 1. 总体判断

- 一句话评价：数字诚实但推断骨架错位，H1（比例命题）与 McNemar（方向检验）回答的是不同问题。
- Critical 数量：1 ｜ Major：7 ｜ Minor：1 ｜ Nit：1
- 是否建议进入下一轮：是（存在 Critical，不可投）

## 2. 问题清单

| ID | 严重度 | 位置 | 问题 | 期望 | 证据关联 |
|---|---|---|---|---|---|
| R1-R1-01 | Critical | Sec.1 L63-64; Sec.4 L214/L226; Table L148-161; Abstract L54 | H1是比例命题（翻转率>5%），正式检验却是方向检验（McNemar只看b vs c不对称）。系统性倒挂：pool 9/220（4.09%）p=0.0039显著、PowLocalNew 7/157（4.46%）名义显著，反之5/30（16.7%）p=0.0625不显著。5%阈值无出处。c=0下McNemar显著只取决于b≥6，与H1字面无关。 | 二选一全文统一：(a) H1改写为方向性命题，5%降格为描述性参考并给出处；或(b) 正式检验换单样本比例检验并重算功效。摘要/Discussion计数与所选检验一一对应。 | main.tex L63-64/L75/L214/L226/表；analysis_plan_power_rep.md；全仓无5%出处 |
| R1-R1-02 | Major | Sec.2 L123; Sec.4 L204/L224; Discussion L239 | Guard v3.1见过120行裁决后针对唯一负例（O vs O2）手工构造，“精确复现”是构造性同义反复。两个out-of-sample支撑都是空证据：10个flip无一触发guard；470行零差异回归恰说明零触发。撑不起contribution (iii)。 | 降格为data-dependent patch；或预注册confusable类独立测试集报触发精确率/召回率；或删泛化表述。470行回归须注明触发次数=0。 | main.tex L123/L204；results/guard_v31.json（n_changed=1）；guard_v32.json（n_diff=0）；label_match_v31.py |
| R1-R1-03 | Major | Sec.1 L64; Sec.4 L210/212/216/218/224; Abstract L55 | Adjudication gate自我矛盾：L216是“5%触发式”（math层豁免），实践是“全裁决式”（every discordant row）。按触发式，local-big/tight/powrep四层/臂不应有裁决却被计入67总数。 | 统一gate语义二选一：触发式则低层裁决移出67总数；全裁决式则删L216 trigger豁免论证。67口径重算。 | main.tex L64/L216；Abstract L55 |
| R1-R1-04 | Major | Sec.4 L202/212/218/222/224; Sec.2 L119 | 裁决三重自由度：(1) xdomain见首轮失败后发明strip规则改被裁决对象再判，5/5覆盖首轮；(2) 单rater层与双rater层同动词“confirmed”汇总进67；(3) 置信后缀泄漏（指令缺陷）被计为matcher功绩。Judge无FNR/FPR校准。 | (a) 主数按first-pass报告，stripped重判单列为敏感性分析；(b) 单/双rater分开报告；(c) 泄漏行单列并报告剔除后敏感性。 | xdomain_judge.json（16/21+3错）；pass2.json；xdomain_adjudication.json；L119 |
| R1-R1-05 | Major | Sec.2 L119; Sec.4 L151-152/206/208/210/212 | ECE跨层混用两种估计量（历史equal-frequency vs 新增equal-width），n=30~60近简并时可差数倍。tempscale脚本自述等频却报出与等宽表值相同的0.1692，链条内部已混用。pilot全对层ECE近零是准确率恒等式副产品。 | 统一分箱重算或给双口径敏感性表；删“numbers are unchanged”句；解释tempscale口径矛盾；简并层注明unidentifiable。 | L119；analysis_d2.py L18-23；analyze_new60.py；tempscale.py；tempscale.json |
| R1-R1-06 | Major | Abstract L54; Discussion L239/L243 | 摘要无限定宣称“Five significant”，Holm 17检验后仅存活2个（pool倒在step3阈值0.00333）。“摘要报五个、深处报两个”属选择性呈现。family划分本身事后定义。 | 摘要三选一：降为2层+Holm限定；或预注册family全文只用adjusted计数；或同句披露三层不survive Holm。 | Abstract L54；L243；results/holm.json |
| R1-R1-07 | Major | Sec.2 L131; Sec.4 L214; Limitations L245 | 功效体系循环：OR=4明示placeholder从未更新，n_ceil用观测discordant率反推；pool的217天花板来自local-new观测率，而pool含这60行（27%）——既定线又达线。“唯一预指定powered推断”实为事后达标叙事。 | n_ceil改标post-hoc sensitivity；pool“meeting 217”降格描述性或补事前计算文件；OR给敏感性区间；承认循环性。 | L131/L245；power_update_120.json；power_local60.json；combined_qwen2.json |
| R1-R1-08 | Major | Sec.1 L77-78; Sec.2 L106/L110; Sec.4 L226/L234 | pilot50是跨模型池（pilot30 deepseek + PowPilot20 qwen）却展示McNemar p=0.0010，违反三处“跨模型仅描述性”承诺。标descriptive不治愈（p印出即推断），且Holm以“re-views”将其排除，双重游离。 | 删pilot50的p/b/c仅留描述性翻转率；或改写承诺并纳入Holm family。 | L77-78/L110/L226/L234；powrep_rollups.json（p=0.0009765625） |
| R1-R1-09 | Minor | Sec.2 L115/L121 | 三层matcher边界武断：0.5%容差无依据（999 vs 1000判对）；ablation earliest-firing归因由代码if顺序决定非因果；“exact”基线本身已归一化，修辞夸大鸿沟。容差一动全文p全动，无敏感性分析。 | 给容差依据或敏感性表；ablation注明顺序依赖或改leave-one-out；承认exact已归一化或更名normalized-exact。 | scripts/label_match_v3.py；L115/L121；powrep_judge.json |
| R1-R1-10 | Nit | Title L28 | 标题双计数（942-Row/Thirteen-Stratum）fragile。数字本身验算一致（942=854+…勾稽对，Wilson CI重算吻合）。 | 去计数化；坚持保留则声明scan联动。 | Title L28；表求和942 |

## 4. 自由评语

- 最强的点：自我披露密度罕见，关键弱点作者自己都写进正文。
- 最担心的点：H1检验错位不修，推断骨架不成立；数字可复算性是唯一承重墙。
