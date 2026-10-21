# Review Round R3 — R2 统计轻量验收报告（计数簇）

- 日期：2026-09-08 ｜ 手稿：paper_workflow_kb/paper/main.tex（R16 版，264 行）
- 改动日志：paper_workflow_kb/REVIEW_R2/ROUND_R16.md（A–L 簇，数字零触碰）
- 审稿角色：R2 统计（R3 轻量验收，只验收计数簇，不做全稿重审）
- 输入：REVIEW_R2_R2-statistics.md（R2 遗留 R2-R2-01 Major / R2-R2-02 Minor / R2-R2-03 Nit）
- 独立审稿声明：本报告独立完成，未与其他角色交流，未修改手稿。
- 重算脚本：paper_workflow_kb/scripts/r3_stats_recompute.py（stdlib only：math.comb + Wilson 手写 + JSON 直读；本次凡引 p/CI 数字全部亲手重算，无“未重算”项）

## 1. R2 遗留三项验收

| ID | 原严重度 | R16 对应簇 | 核对位置（行号） | 结论 |
|---|---|---|---|---|
| R2-R2-01 | Major | A（license 句重写 + 计数集声明句） | L239 license 段；L54 摘要；L226 结果段；L224/L161 | **消解 ✓（Major 关闭）**，见 §2 细节与残留 Minor R3-R2-m02 |
| R2-R2-02 | Minor | C（L75+L214 meeting→post-hoc） | L54“composition pre-specified, ceiling post-hoc”；L75“post-hoc n_ceil=217, composition pre-specified”；L214“(n=220; post-hoc n_ceil=217, composition pre-specified)”；方法 L131 post-hoc 定义保留 | **消解 ✓（关闭）**：摘要/结果两处 meeting 均已加 post-hoc 限定 |
| R2-R2-03 | Nit | L（p 统一 0.00049） | L54“p=0.00049”；L226“p=0.00049”；L243“extended local-new (p=0.00049)”；全文 grep `0\.0005` 零命中 | **消解 ✓（关闭）**：2/4096=0.00048828125 全文统一印 0.00049，无 0.0005 残留 |

## 2. R2-R2-01 消解细节：five 计数集声明与自洽性

R16 在 L239 落地的计数集声明句（原文）：

> “the paired direction is nominally significant in five counted readings: pilot, pre-specified pool, cross-domain loose, extended holdout, and extended local-new … The counted set is these five by construction: the PowLocalNew single arm (b=7, c=0, p=0.0156, same strength as extended holdout) is a nominal single-arm observation without a power conclusion and is not counted, and the raw-basis cloud-new reading (6 of 217, p=0.031) is off the guarded basis and is not counted.”

验收判定：

1. **成员规则已声明 ✓**：R2 时“全文未写”的缺陷已修复——L239 以穷举名单 + “by construction” + 逐项点名两个排除项的方式声明了计数集，L239 的“five counted”不再是 R2 时 L239 旧文案的穷举式表述，与 L224（PowLocalNew 单臂显著）不再矛盾。
2. **三处表述算术一致 ✓**：
   - 摘要 L54：4 个 in-family 名义显著（pilot / pool / xloose / PowLocalNew 单臂）+ 2 个 deterministic rollups（holdout / local-new）= 6 个名义显著读数；
   - 结果 L226：两个 rollup 为“third and fourth nominally significant readings”，与 L220 xloose“second significant paired inference”衔接（见残留 m01）；
   - license L239：6 − PowLocalNew 单臂（点名排除）= five counted ✓；raw-basis cloud-new（p=0.031）属第七个“某口径下名义显著”读数，以“off the guarded basis”点名排除 ✓；
   - L214“like the other four”（pool + 其余四者 = 五）与 five counted 自洽 ✓。
3. **raw-cloudnew 排除理由自洽 ✓**：guarded-basis 规则——全部五个 counted 读数均为 guarded 口径（pilot/pool/xloose 与 guarded 一致或即 guarded；两 rollup 取 guarded：holdout108 b=7、localnew217 b=12，见 rollups JSON），raw 6/217 p=0.031 非 guarded 口径故不计入，判据统一、无反例。
4. **PowLocalNew 排除理由基本可用、措辞有残留不对称（→ Minor R3-R2-m02，不阻塞）**：声明句给出的显式理由是“nominal single-arm observation without a power conclusion”，但被计入的 extended holdout 在 L226 同样表述为“a single-arm observation with observed status and no power conclusion”——该措辞本身不能区分“计入/不计入”，真正的构造性区分是“rollup（先验层 + power-rep 臂的确定性重看，非新检验；L243 明确排除于 Holm family）vs 单臂（四个 observed arms 之一，另行报告）”。L239 的“by construction + 点名排除”已使成员关系无歧义，Major 的核心（规则未声明/与 L224 矛盾）已消除；剩余只是理由措辞的区分度问题，降级为 Minor，不阻塞。
5. **p=0.0156 双胞胎披露 ✓**：L239 明确承认 PowLocalNew 与 extended holdout“same strength”，R2 指出的“同等显著、证据强度逐位相同却一计一不计且无解释”已正面回应（powrep.json powL_localnew p_two=0.015625 vs rollups holdout108 p_two=0.015625，本次直读 JSON 确认逐位相同）。

## 3. 独立重算结论（本次亲手重算，公式与 R2 同口径）

McNemar 精确双侧 p = 2·Σ_{k=0}^{min(b,c)} C(b+c,k)/2^{b+c}（c 全 0 退化为 2/2^b；b=0 报 1.0）：

| b | 重算 p | 手稿印刷 | 位置 | 结论 |
|---|---|---|---|---|
| 11 | 0.0009765625 | 0.0010 | L54/L196/L226(pilot50)/holm.json | ✓ |
| 9 | 0.00390625 | 0.0039 | L54/L214/L239/combined_qwen2.json | ✓ |
| 20 | 1.9073486328125e-06 | 1.9e-6 | L54/L157/L220/holm.json | ✓ |
| 19 | 3.814697265625e-06 | 3.8e-6 | L220 灵敏度分析 | ✓ |
| 12 | 0.00048828125 | 0.00049 | L54/L226/L243/rollups localnew217 | ✓ |
| 7 | 0.015625 | 0.0156 | L54/L161/L224(PowLocalNew)/L226(holdout108)/holm.json | ✓（双胞胎逐位一致） |
| 6 | 0.03125 | 0.031 | L226 raw cloudnew217_raw | ✓ |
| 5 | 0.0625 | 0.0625 | L226 guarded cloudnew217_guarded | ✓ |
| 4 | 0.125 | 0.125 | L204/L212 | ✓ |
| 2/1/0 | 0.5/1.0/1.0 | 同值 | L224/L228/L210 等 | ✓ |

- Wilson 95%（z=1.96）24/25 → [0.8045552759497747, 0.9929039496133009]，与 gold_guarded_agreement.json **逐位一致**；round(.,3)=[0.805, 0.993]，手稿 L55/L232/L239 三处印刷 ✓。
- Holm step3：threshold=0.05/(17−3+1)=0.0033333333333333335；pool p=0.00390625 > threshold，止步 ✓；survivors=[xdomain-loose, pilot] ✓，与 holm.json（含 powL_localnew p=0.015625 列第 4 位、rollups 被排除在 family 外之注记）一致；L243 转述 ✓。
- 求和：N=30+30+60+60+30+160+40+60+60+20+78+157+157=942 ✓；flips=11+5+4+5+0+4+0+1+20+0+2+1+7=60，60/942=0.0637 ✓（L234）。
- **重算结论：R16 数字零触碰声明可信——全部 headline p/CI 与 R2 时逐位一致，无数字伪造、无新数字错误。**

## 4. 问题清单（NEW Critical/Major 扫描 + Minor/Nit 记录）

| ID | 严重度 | 位置 | 问题 | 期望 | new / 旧项 |
|---|---|---|---|---|---|
| — | — | — | **NEW Critical：0；NEW Major：0**（计数簇内未发现新编造、新穷举矛盾、新口径错标） | — | — |
| R3-R2-m01 | Minor（不阻塞；遗留措辞，前存非 R16 引入） | L220 vs L214/L224/L226 | 序数词链条跳过 pool 与 PowLocalNew 单臂：L220 xloose 自称“second significant paired inference”，L226 rollups 自称“third and fourth”，但按未校正显著排序 pool（L214，p=0.0039，先于 xloose 出现）与 PowLocalNew 臂（L224，p=0.0156）亦显著，序数“second/third/fourth”至多只在“pilot→xloose→两 rollup”子链成立。R16 未动这些序数（数字零触碰可信），R2 亦未 flag，故判前存 + 非阻塞。 | 将 L220 改为“second stratum-level paired inference besides the pool”或删序数词；L226 改为“two additional nominally significant rollup readings”。可选修，不入验收门。 | 前存（R15 即有），非 NEW |
| R3-R2-m02 | Minor（不阻塞；R2-R2-01 残留） | L239 | 见 §2.4：PowLocalNew 排除理由措辞（“without a power conclusion”）不能区分同样无 power 结论的 extended holdout；真实区分是 rollup-vs-single-arm 构造。成员已点名、无歧义，故仅措辞级。 | 补半句：“…is not counted because the counted set comprises the three in-family inferential readings plus the two deterministic rollups; the four single arms are reported separately (L224)”。可选修，不入验收门。 | R2-R2-01 残留降级 |

说明：R3-R2-m01 的判定依据——ROUND_R16.md A–L 簇无一触碰 L220/L226 序数词，且 R2 报告狩猎空区未提序数问题；按“只报 NEW”纪律只能记 Minor 不阻塞。若父 agent 要求零 Minor，可一句话顺手修。

## 5. 收敛判定

- 计数 C（新 Critical）：0 ｜ M（新 Major）：0 ｜ m（Minor，非阻塞）：2（m01 前存序数、m02 残留措辞）｜ n（Nit）：0。
- R2 遗留：R2-R2-01 Major **关闭**（消解，残留 m02 不阻塞）｜ R2-R2-02 Minor **关闭** ｜ R2-R2-03 Nit **关闭**。
- **是否收敛：是（本角色计数簇收敛）。** A/C/L 簇达到了 R2 要求的“一句话修复”目标：计数集已声明、双胞胎已承认并点名排除、raw 口径排除有统一判据、三处表述算术一致、全部数字亲手重算通过。两个 Minor 均为可选措辞 polish，不构成投前必修。
- 验收门建议：本角色放行 R16计数簇；m01/m02 可与下一轮措辞修改同修，无需单独成轮。
