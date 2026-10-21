# Review Round R1 — R2 统计 审稿报告

- 日期：2026-09-07 ｜ 论文：Exact versus Tolerant Label Matching… ｜ 审稿角色：R2 统计
- 独立审稿声明：本报告独立完成，未参考其他角色意见。

## 1. 总体判断

- 一句话评价：p值全部复算一致，但“五个显著”headline在三个Major上越界。
- Critical 数量：0 ｜ Major：3 ｜ Minor：3 ｜ Nit：2
- 是否建议进入下一轮：是（存在 Major，不可按当前headline口径投稿）

## 2. 问题清单

| ID | 严重度 | 位置 | 问题 | 期望 | 证据关联 |
|---|---|---|---|---|---|
| R2-01 | Major | Abstract L53-54 vs Discussion L243 | 17检验未校正报“五个显著”（FWER≈0.58）；Holm仅存活2个（loose、pilot），pool止于step3（p=0.0039>0.00333）。Abstract无Holm限定，越界夸大。 | Abstract改为分层表述（2 survive Holm + 3 stratum-local uncorrected），或把Holm存活数写进Abstract。 | holm.json（survivors/step3/threshold 0.00333）；FWER重算 |
| R2-02 | Major | Table L161 vs L226 | 完全相同证据强度（b=7,c=0,p=0.015625）相反license：extended holdout“newly显著” vs PowLocalNew“nominally…no power conclusion”。 | 统一决策规则（同p同规则），或写出区分arm/rollup的预注册标准并交叉引用。 | powrep.json vs powrep_rollups.json（bitwise identical） |
| R2-03 | Major | Abstract L53-54; L226; L239 | “五个”含两个重叠行集rollup（holdout108含holdout-main 30行；localnew217含local-new 60行），Holm family明确排除rollups。headline把重复检验计成独立发现。 | 去重计数（3独立+2描述性rollup）或标注overlapping row sets。 | holm.json note字段；L226 |
| R2-04 | Minor | Table L155-160; Methods L119 | b=1（p=1.0）与b=c=0（degenerate p=1.0）印成同一“p=1.0”；后缀degenerate/ns行间不一致（PowCloudNew无后缀）。 | 统一标注discordant总数（如n_d=1 vs n_d=0 degenerate），补后缀。 | 重算确认公式一致 |
| R2-05 | Minor | Abstract L54; Methods L131 | n_ceil是观测率+OR=4事后算出，但Abstract写“meeting its required n=217”像事前要求。pool预注册指针本轮未找到可验证命中。 | Abstract改post-hoc/placeholder限定 + 给预注册指针（commit/日期/行）。 | power_*.json（or=4.0）；combined_qwen2.json |
| R2-06 | Nit | Abstract L54 vs L226 | 同一p值（2/4096）Abstract印0.0005、正文印0.00049，舍入口径不一致。 | 全文统一（p=0.00049或4.9e-4），重跑numbers scan。 | powrep_rollups.json（0.00048828125） |
| R2-07 | Minor | Methods L131-132（核验通过） | 双侧选择已核查：c=0下仍用双侧是保守选择（单侧会把三个b=5层翻显著），有c-cell存在性论证。无需修改。 | 保留双侧即可。 | code_pilot.json；重算单侧0.03125 |
| R2-08 | Nit | Abstract/Table/Results（核验通过） | Wilson 25/25得[0.8668,1.0]一致；N=942求和对；854/794/60自洽；表内比例全与n整除一致；loose敏感性19/55 p=3.8e-6吻合。无需修改。 | 无。 | gold_agreement.json；xdomain_sensitivity.json |

## 4. 自由评语

- 最强的点：Holm实际算出并归档，全部p值可逐位复算，算术层诚实。
- 最担心的点：headline计数口径（未校正+重叠行集）与自家Holm口径打架。
