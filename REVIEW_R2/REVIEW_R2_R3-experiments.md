# Review Round R2 — R3 实验 审稿报告（R15 复核 + NEW 猎取）

- 日期：2026-09-08 ｜ 论文：paper_workflow_kb/paper/main.tex（R15 修改版，264 行）
- 审稿角色：R3 实验充分性与公平性 ｜ 独立审稿声明：本报告独立完成，未与其他角色交流，未修改手稿。
- 输入：ROUND_R15.md（R15 说明）、REVIEW_R1_R3-experiments.md（我方 R1 报告）、CLAIM_LEDGER.md（C01–C48）、results/ 与 evidence/ 一手证据。

## 1. R15 修复复核（我方 R1 领域）

| R1 ID | R15 动作 | 落地？ | 行号/证据 |
|---|---|---|---|
| R3-06 guard in-sample 拟合 | Circularity 披露 + in-sample 标注 + 特异性未测披露 | ✅ 真落地 | L55 "in-sample (one fix…)"；L123 "constructed after seeing the 120-row adjudication…in-sample by construction…no synthetic targeting test was run, so guard specificity…unmeasured"；L208/L239 同述 |
| ECE 不重分箱注释 | 分箱对照句 + 表注 + 未来工作 | ✅ 真落地 | L119 "kept (rather than re-binning sealed strata…)…unified-convention recomputation is future work"；L141 表注 "prior strata equal-frequency bins, live strata equal-width bins, each exact-vs-guarded comparison within one convention"；L245 Limitations 同述 |
| tempscale 0.1692 巧合注 | 注释已加，不改数 | ✅ 真落地且证据对得上 | L206 "on cloud-new both conventions give 0.1692 at T=1, a numerical coincidence"；独立核对：results/guard_v31.json strata.cloud-new.ece10_guarded=0.1692（等宽）== results/tempscale.json strata.cloud-new.ECE_T1=0.1692（等频）——确为同值巧合，无数字错配 |
| GOLD 24/25 + G06 | 五处 24/25 + G06 具名 | ✅ 真落地 | L55/L232/L239；独立核对 results/gold_guarded_agreement.json：agree=24，wilson95=[0.80456,0.9929]→"0.805 to 0.993"✓；stem 13/14、stemless 11/11✓；唯一分歧 G06/cloud-new-42✓；per_item 五层覆盖 pilot 6/cloud-new 5/holdout-main 5/local-new 5/local-big 4✓ |
| R3-02 Holm 进摘要 | 摘要加 Holm 存活限定 | ✅ 真落地 | L54 "Under Holm-Bonferroni…two of the five survive (pilot, cross-domain loose)"；与 results/holm.json（m=17，step3 止于 pool p=0.00390625>0.003333，survivors=[xdomain-loose, pilot]）一致 |
| R3-07 412 不对称出 N | 摘要/表注明 regime-contrast 排除 | ✅ 真落地 | L53 "(plus 412 regime-contrast rows excluded from N)"；L228 "412 of 412 tight, 412 of 412 loose"；与 results/powrep_loose.json 三臂 98+157+157=412 ✓ |
| R3-03 knob 降级 / 改名 | "control knob"→"regime contrast"（R15 称 2 处） | ⚠️ 部分失败（见 R2-R3-01，R1 回归） | "regime contrast" 见 L53/L80/L241；但 "control knob" 残留 L239，"prompt-knob" 残留 L54/L228/L241/L245，"prompt-regime control knob" 残留 L247 |
| R3-05 裁决不对称 | 双 pass 并存 + GOLD 二次覆盖披露 | ✅ 基本落地 | L222 两轮并存；L232 "extension flip rows are included in the 14 stem items, giving them an independent second grading"（GOLD per_item 含 local-new 5 + local-big 4，属实） |
| R3-04 混杂 | 模型/宿主差异披露 | ✅ 文字落地 | L70/L104（不同 generation and capacity）；loose 泄露 L222 披露 |
| R3-09 产物 on-request | R15 选 evidence 回应（无法凭空 mint），L249 维持 | ✅ 诚实回应，非修复 | L249 仍无公开链接——属已披露局限，不新报 |

## 2. 问题清单（只报 R1 未提过的新问题 + 修复失败的 R1 回归）

| ID | 严重度 | 位置 | 问题 | 期望 | 证据链接 | new / R1 回归 |
|---|---|---|---|---|---|---|
| R2-R3-01 | Major | L239（"as the control knob"）、L247（"prompt-regime control knob"）、L54/L228（"prompt-knob effect"）vs R15 改名 | R1 R3-03 修复不完全：license 核心句仍以因果名词 "control knob" 呈现指令格式效应（"replicates it with instruction format as the control knob (tight 1 of 60 ns versus loose 20 of 60…)"），与 R15 降级目标（regime contrast + question-type-dependent 限界）矛盾；"regime contrast"（L53/L80/L241）与 "knob" 全文混用，读者无法判断官方主张是因果开关还是事后 regime 描述。 | 全文统一为 "regime contrast"；L239 license 句改为 "…with instruction format as a regime contrast…"；"prompt-knob effect" 残留处（L54/L228/L241/L245）同步改写或加 "descriptive label, not a causal claim" 限定。 | main.tex L54/L239/L241/L245/L247；ROUND_R15.md §9 | R1 回归（R3-03 修复失败） |
| R2-R3-02 | Major | L54（"Five paired inferences are significant"）、L226（"third and fourth significant paired inferences"）vs L243 + results/holm.json | Rollup 双重检验计入 headline 显著数：extended holdout（7/108）与 extended local-new（12/217）的行与已检分层完全重叠，L243 自定 "deterministic re-views…not new tests" 且 Holm 族（m=17，"rollups excluded"）将其排除在外，但摘要 "five significant" 与 L226 "third and fourth significant inferences" 仍把二者当新增显著推断计数。同一批行在分层检一次、rollup 检一次，两次都报显著，属同一数据双重收割且不受联合误差控制。 | 二选一：(a) 摘要 "five" 改为 "three family tests significant + two rollup re-views nominally significant at per-test alpha, outside the Holm family"（推荐，改动最小）；(b) 将 rollup 纳入 Holm 族重算（注意行重叠违反族独立性，不推荐）。L226 "significant paired inferences" 改为 "nominally significant re-views"。 | main.tex L54/L226/L243；results/holm.json（m/step3/survivors，note "rollups excluded"）；results/powrep_rollups.json（holdout108 p=0.015625；localnew217 p=0.00048828125） | new |
| R2-R3-03 | Major | L239（"pilot-50…now met with 50"）vs L245（"pilot 30 of 50…remain under"）vs L226（"cross-model pool…descriptive only"） | 同一事实正文自相矛盾：L239 称 pilot-50 上限 "now met with 50"（依据 pilot30+PowPilot20 的 50 行 rollup），L245 称 "pilot 30 of 50…remain under"，而 L226 明言该 pilot50 rollup 是 "cross-model pool…descriptive only with no p-value claimed"。一个被论文自己禁止跨模型合并推断的描述性拼盘，不能同时充当功效上限 "已达成" 的依据。 | L239 删除 "pilot-50" 出 met 清单（改为 "pilot-50 met only as a cross-model descriptive rollup, not as powered evidence"），与 L245/L226 口径统一；或在 L245 删对应句。二者只能留其一。 | main.tex L226/L239/L245；results/powrep_rollups.json strata.pilot50（n=50，跨 pilot deepseek-v4-flash + PowPilot qwen2.5:7b）；L78 跨模型仅描述规则 | new |
| R2-R3-04 | Major | L230（"guarded agreement 1.0…identical flip sets (5 and 5)"）vs results/retest60.json + results/guard_v31.json | Retest 混合口径且含已知误接受未披露：retest60.json 只有一套 flip set（n_flip_test=n_flip_retest=5，flip_set_test 含 "氧气的化学符号是？" 即 cloud-new-42/O-vs-O2 类），而 guarded 口径下 cloud-new flips 应为 4（guard_v31.json flips_guarded=4，42 已被拒绝）。L230 把 "guarded agreement 1.0" 与未标注口径的 "(5 and 5)" 并置，读者会误读为 adjudicated 现象 5/5 完美稳定，实则稳定复现的 5 行集合里含 documented false positive。 | 标注口径并披露："raw-basis flip sets identical (5 and 5, including the documented cloud-new-42 false accept); guarded-basis sets identical (4 and 4)"；若 guarded 4/4 未在证据中封存，则补 results/retest60_guarded.json 或退为 "raw-basis 5/5（含已知误接受）"。 | main.tex L200–L204（raw 5 vs guarded 4）；results/retest60.json（flip_set_test/retest 各 5，guarded_mcnemar b=0/c=0）；results/guard_v31.json（flips_guarded=4）；evidence/cloud_judge_new60.json（4/5） | new |
| R2-R3-05 | Minor | L106、L220（"pre-registered in the collection script docstring"） | Docstring 定向说明 ≠ 预注册：script docstring 无时间戳/密封，与论文他处严格区分的 pre-registration（预注册功效池、sealed 结果）不是同一证据等级；"pre-registered" 一词在此处通胀。L220/L245 对该层总体状态诚实标注为 post-registration/observed status，故 functionality 无碍，仅措辞。 | 改为 "direction documented in the collection script docstring before running (not a sealed pre-registration)"。 | main.tex L106/L220/L245 | new |
| R2-R3-06 | Minor | L241（"b=21, c=0 combined on identical questions"） | 跨 prompt 合并 b/c 双计同一批题：tight 与 loose 是同一 60 题在两种 prompt 下的观测，b=21 相加让 60 个问题贡献 120 个 discordant 自由度；虽未配 p 值，但 "combined b=21, c=0" 以 McNemar 记号呈现，易被误读为联合检验量。 | 加 "descriptive sum across prompts (same questions counted twice), no combined test" 或删除该括号。 | main.tex L241；results/xdomain.json（tight b=1 + loose b=20） | new |
| R2-R3-07 | Minor | L224（"at the 0.5% relative-error boundary (999 vs 1000…)"） | 数字措辞不准：999 vs 1000 相对误差为 0.1%，落在 0.5% 容差带内，而非 "at the boundary"。 | 改为 "within the 0.5% relative-error tolerance (999 vs 1000, 0.1% error)"。 | main.tex L115（容差定义 0.5%）、L224；evidence/powrep_judge.json | new |
| R2-R3-08 | Nit | L54（"p=0.0005"、"p=0.016"）vs L226/L224（"p=0.00049"、"p=0.0156"） | 同一 p 值摘要与正文舍入位数不一（localnew217 p=0.00048828125；powL p=0.015625）。 | 统一为正文精度（0.00049；0.0156）。 | main.tex L54/L224/L226；results/powrep_rollups.json、results/powrep.json | new |

## 3. 独立重算记录（证据-first，一手重算）

1. ECE 0.1692 巧合：guard_v31.json → strata.cloud-new.ece10_guarded = 0.1692；tempscale.json → strata.cloud-new.ECE_T1 = 0.1692。两侧独立来源同值，L206 "numerical coincidence" 属实。✅
2. GOLD-25：gold_guarded_agreement.json → agree=24，agreement=0.96，wilson95=[0.80456, 0.9929] → 正文 "24 of 25…0.805 to 0.993" ✅；stem 13/14、stemless 11/11 ✅；唯一分歧 G06/cloud-new-42 ✅；per_item 五层分布 6/5/5/5/4 与 "five flip-carrying strata" ✅。
3. Rollup：powrep_rollups.json → holdout108 p=0.015625（正文 0.0156 ✅）；localnew217 p=0.00048828125（正文 0.00049 ✅，摘要 0.0005 舍入漂移见 R2-R3-08）；cloudnew217_guarded p=0.0625 ✅。
4. Holm：holm.json → m=17，stop step3（pool p=0.00390625 > 0.003333），survivors=[xdomain-loose, pilot] ✅ 与 L243 一致（亦坐实 R2-R3-02 的族外 rollup 问题）。
5. XDomain：xdomain.json → tight 50/51/1 翻转 p=1.0，ECE 0.0533→0.0367 ✅；loose 25/45/20 翻转 p=1.907e-6，ECE 0.4767→0.1433 ✅。
6. Retest：retest60.json → guarded_agreement=1.0，flip 5/5 两轮重合，drift=0.0107 ✅ 数字对得上（口径问题见 R2-R3-04；flip set 含 O2 题，坐实误接受在复现集内）。

## 4. 计数与收敛判定

- R15 修复验证：9/10 落地（guard in-sample ✅、ECE 口径 ✅、0.1692 注 ✅、GOLD ✅、Holm 进摘要 ✅、412 ✅、裁决两轮 ✅、混杂披露 ✅、产物诚实回应 ✅；knob 改名 ⚠️ 部分失败）。
- 本轮：Critical 0 ｜ Major 4（1 R1 回归 + 3 new）｜ Minor 3 ｜ Nit 1。
- 是否收敛：否。R2-R3-01～04 须进 R16（均为措辞层修复，无需新实验；R2-R3-04 若选补封存文件则需一次确定性重算）。R16 只需复核这 4 条 Major 的文字落地 + manifest/number 门重跑。
