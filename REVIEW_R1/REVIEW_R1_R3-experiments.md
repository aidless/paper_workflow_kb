# Review Round R1 — R3 实验 审稿报告

- 日期：2026-09-07 ｜ 论文：Exact versus Tolerant Label Matching… ｜ 审稿角色：R3 实验充分性与公平性
- 独立审稿声明：本报告独立完成，未参考其他角色意见。

## 1. 总体判断

- 一句话评价：层内配对设计守住，数字全对；但公平对照（口径/混杂/裁决对称性）有七处Major。
- Critical 数量：0 ｜ Major：8 ｜ Minor：1 ｜ Nit：0
- 是否建议进入下一轮：是（大修后重审）

## 2. 问题清单

| ID | 严重度 | 位置 | 问题 | 期望 | 证据关联 |
|---|---|---|---|---|---|
| R3-01 | Major | Methods L119；Table L141-166 | ECE双口径不可比：prior等频 vs live等宽，n小且置信简并时可差数倍；“不重写哈希”冻结混用，但跨层归纳（两种修复fail、guard repair）横跨口径。 | 同一口径重算全部strata，或分列标注且跨层结论降级描述性。 | local_new.json ece_note；analysis_d2.py系 |
| R3-02 | Major | Abstract L53-55；L214；L243 | pool按单层alpha宣称显著，但自家Holm下止于step3不存活；Holm限定只在Discussion。选择性报告。 | 摘要/表格显著性带Holm状态，或pool降级名义显著。 | holm.json（step3 stop） |
| R3-03 | Major | Results L220-228；Discussion L241 | prompt-knob内部矛盾：cross-domain上1 vs 20（头号机制发现），power-rep同题复现tight(0/2/1/7) vs loose(2/1/4)全ns。“question-type-dependent”事后命名，调节变量无预指定操作化。 | 预指定调节变量+新题型确认性复现；否则knob降级事后观察、移出核心贡献。 | xdomain.json；powrep_loose.json |
| R3-04 | Major | Methods L101-110；L218-224 | 三混杂：模型（2.5:7b vs 2:7b）+宿主（云vs本地）+题型同步变；loose把置信float写进答案同行，flip与格式违规不可分。 | 宿主×模型析因对照或标confounded；loose补“去leak重采”对照。 | xdomain.json flips（“不是。0.9”）；L222 |
| R3-05 | Major | Methods L119-120；L202/212/222 | 裁决不对称：extension全单rater（失败qwen3:4b丢弃）；xdomain首轮16/21后剥离strip再判拼21/21，属按结果改输入；judge同族无校准，c=0下只可能确认tolerant。 | extension补第二独立rater+一致率；或降级探索性；second pass按预注册重采重判。 | local/big_adjudication.json（single-rater）；L245 |
| R3-06 | Major | L121-125；L239/241 | guard in-sample拟合；470行零差异是“无触发故无差异”空检验；10个flip无一属guard针对的短ASCII类，假阳类fresh零检验机会。“one fix, zero regressions”不可外推。 | 构造同类保留探针集fresh预注册测试真阳/假阳；或降级为记录性规则移出核心贡献。 | guard_v31.json（changed=1）；guard_v32.json（diff=0） |
| R3-07 | Major | Abstract L53；L228；Table注L141 | 412 loose行不对称出N：同255题tight 412行进N，loose 412行排除。headline N/flip率成tight条件统计，恰是knob复现失败的一半被移出分母。 | N改双数并列（TIGHT-942+412 contrast）或统一N=1354；摘要/表注明示条件值。 | powrep.json（412）；powrep_loose.json（412） |
| R3-08 | Minor | Abstract/Table/Results（核验通过） | 数字一致性独立重算通过：N=942、60 flips、854、五p值、rollup加总（5+2=7、5+7=12、4+1=5）全对；raw/guarded双口径有交代。建议表内raw/guarded双行并列。 | 维持现状。 | Table L149-161；evidence |
| R3-09 | Major | L249；L131；L138 | 产物不足TMLR门槛：“on request无公开链接”；重算脚本分散无一键入口；结合双ECE口径第三方无法统一复算；模型/宿主版本无pin。 | 匿名仓库/快照链接；一键重算脚本统一口径输出全表。 | submission/仅历史zip |

## 4. 自由评语

- 最强的点：分层披露诚实，ns不隐藏，自曝Holm失败与单rater局限。
- 最担心的点：c=0 + 双口径 + Holm出局三叠加，标题级因果解读缺公平对照。
