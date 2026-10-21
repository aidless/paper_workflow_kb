# Review Round R1 — R8 图表 审稿报告

- 日期：2026-09-07 ｜ 论文：Exact versus Tolerant Label Matching… ｜ 审稿角色：R8 图表
- 独立审稿声明：本报告独立完成，未参考其他角色意见。

## 1. 总体判断

- 一句话评价：13行×图表×证据逐项对上，无一错配；剩余全是自明性问题。
- Critical 数量：0 ｜ Major：0 ｜ Minor：2 ｜ Nit：2
- 是否建议进入下一轮：否（本角色无阻塞项）

## 2. 问题清单

| ID | 严重度 | 位置 | 问题 | 期望 | 证据关联 |
|---|---|---|---|---|---|
| R8-MIN-01 | Minor | Figure 1 L168-194/caption L192 | 13个缩写（CN/LN/PPi/PHo/PCN/PLN/XDt/XDl…）图注图例均不展开，读者须 hunting 正文，图不自明。 | 图注加一句映射（Pilot/Hold/CN/LN/EN/Big/Math/XDt/XDl/PPi/PHo/PCN/PLN）。 | tikz vs table |
| R8-MIN-02 | Minor | Table 1 caption L141 | ECE分母只披露2/13层（55/60、156/160），其余须拼body/results。 | 补一行全层分母（或“其余100%携带”句）。 | local_new/big/json；math40/en |
| R8-NIT-01 | Nit | Table caption L141 + Cloud-new行L151 | raw脚注报flips/ECE缺raw准确率53/60=0.8833，恰与下行Local-new guarded值相同，易跨行误读。 | 脚注写全“raw 53/60=0.8833, 5 flips, ECE 0.0492; guarded 52/60=0.8667, 4 flips, ECE 0.1692”。 | cloud_new.json；guard_v31.json |
| R8-NIT-02 | Nit | Table flips列L153-161 | “p=1.0”/“ns”/“degenerate”混用无声明规则（用法实对：degenerate仅b+c=0处）。 | 统一约定+caption token释义。 | 表内5行 |

## 3. 核验通过（非问题）

- Table 1全部13行（n/Acc/ECE/flips/p）与sealed results逐项吻合，N=942；13对tikz柱与表guarded值全对；LN 53/60=0.8833、cloud guarded 52/60=0.8667、rollups 11/50·7/108·5/217·12/217全对；摘要/正文/表/注数字一致。

## 4. 自由评语

- 最强的点：表图证三方零错配是本轮唯一全绿角色。
- 最担心的点：缩写不展开是读者体验问题，非证据问题。
