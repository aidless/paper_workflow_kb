# Review Round R1 — R7 伦理 审稿报告

- 日期：2026-09-07 ｜ 论文：Exact versus Tolerant Label Matching… ｜ 审稿角色：R7 伦理
- 独立审稿声明：本报告独立完成，未参考其他角色意见。

## 1. 总体判断

- 一句话评价：Judge偏见披露模范级，Broader Impact诚实；但GOLD-25在唯一安全关键项上人评与guarded裁决矛盾且未披露。
- Critical 数量：0 ｜ Major：1 ｜ Minor：2 ｜ Nit：0
- 是否建议进入下一轮：是（修后再审一轮）

## 2. 问题清单

| ID | 严重度 | 位置 | 问题 | 期望 | 证据关联 |
|---|---|---|---|---|---|
| R7-01 | Major | L232；L239；Abstract L55；Table L151；L261 | GOLD-25掩盖矛盾：G06=cloud-new-42（O vs O2，guard立证单点）作者盲评打“对”，脚本以“all 25 guarded CORRECT”为参照计一致。若参照真是guarded则G06参照为假（guarded下incorrect，表L151 flips=4已剔除）；若参照实为v3则验证的是未guard matcher。两种情形正文均未披露gold含false positive且人评与guarded裁决相反，读者误把25/25当guardrail验证——正是Broader Impact安全主张支点。 | 二选一落字：(a) G06按guarded系记分歧→24/25+重算CI并披露；(b) 明确参照系为v3并加注gold不构成guard验证。Limitations加gold含false positive去向句。 | gold_key.json；grades_gold25_user.csv；analyze_gold.py；gold_agreement.json；L200/L204 |
| R7-02 | Minor | L232；L239；L261 | “independently graded”夸大：评分者即作者（user-confirmed），程序是blinded非independent。与25/25全对结合低估确认偏误。 | 改“blinded author grading”或补独立评分者+一致率；Methods/Limitations写明身份与盲法。 | grades文件备注列 |
| R7-03 | Minor | L249附近；L251-252 | 无COI/资助、无“无人类受试者”、无数据许可显式声明。实质风险低但TMLR要求显式表态而非推断；gold作者自评关系一并显式化。 | 加2-3句显式声明（无资助/无冲突/无受试者/题目自编无许可负担，无则写none）。 | 全文grep无conflict/interest/fund/IRB句 |

## 3. 核验通过（非问题）

- Broader Impact充分：harm如实+配guardrail指局限；无外部受试者；双盲无残留；7B规模无需碳核算；题目自编无许可负担；67=20+9+21+10+7与854=794+60自洽。

## 4. 自由评语

- 最强的点：judge偏见披露（异构/温度/未校准/单rater/失败尝试/两轮留痕/bug修复）是模范级。
- 最担心的点：25/25被误读为guardrail验证，而G06正是guard的立证项。
