# Review Round R1 — R5 可复现 审稿报告

- 日期：2026-09-07 ｜ 论文：Exact versus Tolerant Label Matching… ｜ 审稿角色：R5 可复现
- 独立审稿声明：本报告独立完成，未参考其他角色意见。

## 1. 总体判断

- 一句话评价：算术层全对（正向记录R5-10），缺陷集中在“能否重做”而非“是否算错”。
- Critical 数量：0 ｜ Major：6 ｜ Minor：2 ｜ Nit：2
- 是否建议进入下一轮：是（大修后重审R5）

## 2. 问题清单

| ID | 严重度 | 位置 | 问题 | 期望 | 证据关联 |
|---|---|---|---|---|---|
| R5-01 | Major | Results L232；L239；analyze_gold.py | GOLD-25的25/25按错误参照算出：脚本硬编码“全部guarded皆CORRECT”，但G06=cloud-new-42恰是唯一documented false positive（guard_v31判False，正文L200称incorrect）。盲评“对”应为分歧，真值应为24/25，Wilson CI虚高。 | 修正参照（24/25+重算CI）或剔除分母并披露；同步修脚本断言与正文数字；坚持25/25须给语义依据并撤销guard fix声明。 | gold_key.json（G06→cloud-new-42）；guard_v31.json；grades_gold25_user.csv；gold_agreement.json |
| R5-02 | Major | Methods L101/L104；各collection脚本 | 模型/环境未锁定：ollama标签可变无digest；deepseek无版本/日期；无seed；且自家retest证明temperature 0无字节确定性（1对字符串不同，0.9→0.458漂移）。第三方重采必然不一致，手稿未声明边界。 | 锁定digest/版本/seed；Methods给“可复现边界”声明（flip-set稳、字符串不保字节一致）。 | cloud/local_new60.py；*_raw.json；retest60.json |
| R5-03 | Major | Results L138 | 14/14字节一致范围夸大：名单全早期文件，后期核心（xdomain/powrep/rollups/holm/combined）全不在列；hash硬编码自比对，无云端artifact第三方不可验证。 | 扩展到全部sealed文件+云端sha日志；或收窄主张并披露自报告性质。 | cloud_repro_check.py（CLOUD 14项）；results/约40文件 |
| R5-04 | Major | L249 | “无公开仓库、accept后补”不可接受：942裁决+GOLD+raw是全部可信基础，on request等于把验证推迟到录用后。这是交付物缺失非措辞问题。 | 投稿即给匿名补充材料链接/随投稿上传zip；删“accept后补”。 | submission/仅历史zip |
| R5-05 | Major | Methods L96-100；d2_60.jsonl | pilot层不可再生：包内无deepseek采集脚本；行携source_outcome_source系重标二手行。Holm幸存者之一的数据层无法重做，手稿只字未提。 | 补provenance（版本/日期/提示/解析/置信来源）；丢失则Limitations明示并评估对pilot推断影响。 | d2_60.jsonl首行；scripts/无采集脚本 |
| R5-06 | Major | L232；gold包文件 | “独立盲评”独立性无证据：评分人即作者（user-confirmed）；11/25无题干第三方不可复核。第二验证证明力被高估。 | 披露评分人身份与盲法程序；删“independent”或补独立评分者+一致率；11 stemless收窄解读。 | grades_gold25_user.csv；gold_grading_pack |
| R5-07 | Minor | L224；powrep_judge.json | power-rep judge输入经strip预清洗未披露（judge见“利马”非原文“利马 0.9”）；xdomain同类清洗有披露，形成缺口。第三方按原文重做可能得不同verdict。 | 补一句清洗声明+语义不变论证，或附未清洗对照。 | powrep_judge.json leak_rule |
| R5-08 | Minor | protocol.md；requirements.txt；L249 | 环境锁半成品：requirements留“Fill in…”占位；protocol大片空白。determinism无可验证基线。 | 填实版本/freeze；protocol空白或填或删引用。 | requirements.txt；protocol.md |
| R5-09 | Nit | L131；L259 | analysis_d2.py独置包根与其余scripts/不一致，正文附录路径前缀含混，重做摩擦。 | 统一包根相对路径；说明或移入scripts/。 | 实测路径 |
| R5-10 | Nit | Abstract/Table/results（核验通过） | 核心数字独立重算全吻合：N=942、854/794/60、5个p、Holm step3、Wilson下界；11个文件对齐无缺失。本条为已执行重算记录。 | 无。 | 抽查11个results/evidence文件 |

## 4. 自由评语

- 最强的点：数字层全对，c=0/ECE口径/guard循环等坑均已自我披露。
- 最担心的点：GOLD参照错误 + pilot不可再生，两处动到核心license。
