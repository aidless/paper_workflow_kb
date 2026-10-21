# Review Round R1 — R6 写作 审稿报告

- 日期：2026-09-07 ｜ 论文：Exact versus Tolerant Label Matching… ｜ 审稿角色：R6 写作
- 独立审稿声明：本报告独立完成，未参考其他角色意见。

## 1. 总体判断

- 一句话评价：数字逐项重算全过；摘要声明强度超证据许可，无Critical但需摘要+Results实质改写。
- Critical 数量：0 ｜ Major：5 ｜ Minor：4 ｜ Nit：2
- 是否建议进入下一轮：是（改写后再审）

## 2. 问题清单

| ID | 严重度 | 位置 | 问题 | 期望 | 证据关联 |
|---|---|---|---|---|---|
| R6-01 | Major | Abstract L53-54 vs L243 | 摘要“Five significant”无Holm限定；Holm后仅2存活，唯一powered（pool）出局。摘要独立阅读许可强度超证据。 | 加联合控制限定（2 survive Holm over 17 tests）或降标题句。 | holm.json |
| R6-02 | Major | Abstract pilot分句；Intro L67 | pilot n=30<n_ceil=50，声明位（“descriptively and inferentially”）无功效caveat，披露只在远端。 | 声明句内加n/n_ceil与observed标签。 | power_update_120.json（n_ceil=50） |
| R6-03 | Major | Abstract L53-54 | observed-status定语语法仅覆盖两extended，pilot/loose在摘要内无标签；与L239“one+four”自计数对不上。 | 5推断逐一贴status或加总括句“除pool外均为observed”。 | L131/L220/L226 |
| R6-04 | Major | Abstract L55 vs L123 | guard“reproduces exactly”是无hedge强断言；in-sample循环性只在Methods。摘要强度超证据。 | 摘要加in-sample限定。 | guard_v31.json（fit 120行） |
| R6-05 | Major | L226 vs L78/L234/Holm note/Table | rollup双重矛盾：“not new tests”+ pooling仅描述性承诺 vs “newly significant”推断语言；两rollup在Table 1无行，摘要数字无法逐表核对（数值本身复算对：7/108、12/217）。 | 删rollup显著性语言仅留描述性；或增表行并声明推断地位。 | powrep_rollups.json；Table 1 |
| R6-06 | Minor | L224 vs L226 | 同一批7 flips：单臂“no power conclusion”，入rollup转significant observed，区分标准（discordant门槛）未成文。 | 加区分原则句，或rollup同样降描述性。 | powrep.json；rollups |
| R6-07 | Nit | Abstract vs Table vs L224/226 | 同一p值三种写法（0.000488/0.00049/0.0005；0.0156/0.016），无舍入规范。 | 统一舍入规则并逐处对齐。 | rollups.json |
| R6-08 | Minor | 全文 | 术语漂移：guarded/tolerant混用；powered-extension/replication arms/extended strata同指一批行。 | 版本标定+三名择一为主余作别名。 | L196/L204/L214-226 |
| R6-09 | Minor | Abstract L55 | “Every discordant row…(67 confirmed…)” head易误读总数=67；实际68行（67+1 false positive）。 | 改写“67 of 68 confirmed”，分母68落字。 | merged 21行（20+1） |
| R6-10 | Minor | Discussion L239/L241 | “alone”排他因果（配对设计仅支撑同行固定依赖）；“not single-model”基于同家族两模型暗示广义外推。 | “alone”→“holding rows fixed…”；加家族限定。 | 设计无随机化 |
| R6-11 | Nit | Abstract L53-55；L106；caption | 超长句损可核查性：摘要第二句约150词压13层结论；L106约300词压6层。 | 拆句；caption例外移表注。 | 纯可读性 |

## 4. 自由评语

- 最强的点：N/p/CI/retest/guard/67分解逐项重算全过，不利信息均有披露，无编造。
- 最担心的点：摘要headline（five+Holm缺席+observed覆盖不全）是读者第一印象，当前写法许可强度高于证据。
