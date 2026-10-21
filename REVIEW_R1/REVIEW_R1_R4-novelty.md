# Review Round R1 — R4 新颖性 审稿报告

- 日期：2026-09-07 ｜ 论文：Exact versus Tolerant Label Matching… ｜ 审稿角色：R4 新颖性
- 独立审稿声明：本报告独立完成，未参考其他角色意见。

## 1. 总体判断

- 一句话评价：数字无造假，但“首次”包装与自有先例冲突，攻击点在包装而非诚信。
- Critical 数量：1 ｜ Major：4 ｜ Minor：1 ｜ Nit：0
- 是否建议进入下一轮：是（实质修改后再议）

## 2. 问题清单

| ID | 严重度 | 位置 | 问题 | 期望 | 证据关联 |
|---|---|---|---|---|---|
| R4-01 | Critical | Related work L87-89 | 中央novelty句（无前人same-batch翻转+逐行裁决）与自有先例L01重叠：L01即同批三档翻转（63.3%/0.363→86.7%→裁决后100%/0.0037），正文L89亲自引用。C07 verified仅限库内。“首次”最多是样本扩展。 | 加direct-prior-art对照段写清相对L01的delta（N=30→942、13层、guard、复制臂）；或降级为“we extend … from N=30 to N=942”。 | LITERATURE_REVIEW.md L28/L103；CLAIM_LEDGER C07 |
| R4-02 | Major | Related work L85；main.bib | Related Work仅6条全背景类，零matcher敏感性工作；自家scout裁定必引的2609.01671（matcher重排/多人adjudication≤71%）正文bib零命中。6条对claim novelty过薄。 | bib加入2609.01671+2-3句“为何不构成反例”；处理2608.12100/2608.07827/2608.20511（引或给排除理由）。 | LITERATURE_REVIEW.md L99/L202；main.bib（6条） |
| R4-03 | Major | L87括号；LITERATURE_REVIEW L193-214 | “30天374篇、11双命中零反例”无核查痕迹：三脚本在scripts/不存在，全仓仅自述；包内唯一scout是44篇（与374无关）。不可重跑的筛查不能支撑定量novelty。 | 补三脚本+374清单+11裁决表入manifest；或删定量表述退定性hedge。 | scripts/实测缺失；manifest无条目 |
| R4-04 | Major | contributions (iii) L80/L123-125/L204 | guard单规则补丁（账本自认in-sample by construction）列为六大贡献之一；样本外只有10 flips+470行“没改坏”证据。增量修复包装成范式贡献。 | 改写为post-hoc错误分析口径并把in-sample写进contribution句；或移入Limitations/Appendix。 | CLAIM_LEDGER C19；guard_v31.json |
| R4-05 | Major | contributions (vi) L80 vs L216-228/L243 | (vi)打包多维扩展为正面贡献，但实证大面积null：power四臂+loose三臂全ns；prompt-knob自认未复现；Holm后五剩二（含pool出局）。null堆砌误导。 | 重写(vi)逐臂标成功/失败；novelty收缩到Holm幸存两层。 | powrep.json；powrep_loose.json；L228 |
| R4-06 | Minor | Related work末 L89 | 第二处“to our knowledge”（退化ECE替代流程无共识）账本inconclusive，紧邻主novelty句易被误读为第二个novelty。 | 加“we do not claim novelty…open problem”或移Limitations。 | CLAIM_LEDGER C08 |

## 4. 自由评语

- 最强的点：novelty自我hedge（we are not aware of）、C08 inconclusive、失败复制均有披露；p值与67分解重算吻合。
- 最担心的点：L01重叠 + 遗漏最相关引用，两处都是审稿人一眼可见。
