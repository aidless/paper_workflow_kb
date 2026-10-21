# Review Round R2 — R8 图表 审稿报告（文本级图表核对）

- 日期：2026-09-08 ｜ 手稿：paper_workflow_kb/paper/main.tex（R15 修改版，264 行）
- 审稿角色：R8 图表（R2 轮）｜ 独立审稿声明：本报告独立完成，未与其他角色交流，未修改手稿。
- 方法注记：deepseek-eyes 视觉技能本环境不可用，本轮只做文本级图表核对（tikz 数值字面量 vs 表格 vs 证据 JSON 三向对账），属 documented degradation，不阻塞。
- R15 输入已读：ROUND_R15.md（表注加 ECE 口径句、GOLD 24/25 五处同步）；R1 报告已读（REVIEW_R1_R8-figures.md，全绿：0 Critical / 0 Major / 2 Minor / 2 Nit）。

## 1. 总体判断

- 一句话评价：R15 动过的三处（GOLD 行、ECE 口径注、rollup 行）全部与证据对上，独立重算 6 组数字零错配；无新 Critical/Major。
- 新增 Critical：0 ｜ 新增 Major：0 ｜ R1 回归（persist，未修）：2 Minor + 2 Nit（原样还在，非新问题，不重复升级）。
- 是否收敛（本角色）：是。无阻塞项，无投前必修项。

## 2. 问题清单（本轮新问题：无；下表为 R1 回归确认）

| ID | 严重度 | 位置行号 | 问题 | 期望 | 证据链接 | new / R1 回归 |
|---|---|---|---|---|---|---|
| R2-R8-01 | Minor | Figure 1 L178-188 / caption L192 | 13 个缩写（CN/LN/EN/Big/Math/XDt/XDl/PPi/PHo/PCN/PLN）图注仍无展开映射句，R15 未动图。读者仍须 hunting 正文，图不自明。 | 图注加一句映射（Pilot/Hold/CN/LN/EN/Big/Math/XDt/XDl/PPi/PHo/PCN/PLN）。 | main.tex L176-192 vs Table L149-161 | R1 回归（R8-MIN-01，原样 persist） |
| R2-R8-02 | Minor | Table 1 caption L141 | ECE 分母仍只披露 2 层（local-new 55/60、local-big 156/160）；R15 加的是分箱口径句（equal-frequency vs equal-width），不是全层分母。其余层须拼 body/results。 | 补一行全层分母（或"其余 100% 携带"句）。 | main.tex L141；local_new/big JSON | R1 回归（R8-MIN-02，部分回应：分箱口径已加，分母仍缺） |
| R2-R8-03 | Nit | Table caption L141 + Cloud-new 行 L151 | R15 把 raw 脚注从缺 raw 改为"raw-tier cloud-new: 5 flips, ECE 0.0492, see text"——补了 flips/ECE 但仍缺 raw 准确率 53/60=0.8833；且 0.8833 恰与下行 Local-new guarded 值同数，跨行误读风险仍在（已减弱）。 | 脚注写全"raw 53/60=0.8833, 5 flips, ECE 0.0492; guarded 52/60=0.8667, 4 flips, ECE 0.1692"。 | results/cloud_new.json（tolerant 53/60）；results/guard_v31.json（guarded 52/60） | R1 回归（R8-NIT-01，部分修复，残留 Nit） |
| R2-R8-04 | Nit | Table flips 列 L153-161 | "p=1.0" / "ns" / "degenerate" / "nominally p=…, no power conclusion"混用，仍无声明规则（用法实对：degenerate 仅 b+c=0 处）。R15 未动。 | 统一约定 + caption token 释义。 | 表内 L153-161 | R1 回归（R8-NIT-02，原样 persist） |

注：按任务规则第 3 条，R1 已提过的 Minor/Nit 不重复报为新问题，上表仅作"还在"确认，不计入新问题计数。

## 3. R15 修改点专项核对（必查三项，全绿）

- GOLD 24/25 同步：摘要 L55、方法 L119、结果 L232、讨论 L239、附录 L262 共 5 处一致（24 of 25，CI 0.805–0.993，13/14 stems + 11/11 stemless，唯一分歧 G06/cloud-new-42）。GOLD 是正文叙述项，未进 Table 1（表为十三层 strata，GOLD 非层，进表反而错）——"是否进表"判定：不应进表，现状正确。
- ECE 口径注：caption L141 已加"prior strata equal-frequency bins, live strata equal-width bins, each exact-vs-guarded comparison within one convention"，与方法 L119 口径句一致；表内数字 R15 未改，无需重算口径。
- rollup 行 L226：pilot 11/50（b/c 无 p，描述性）、holdout 7/108 p=0.0156、cloud-new 5/217 guarded p=0.0625（raw 6/217 p=0.031）、local-new 12/217 p=0.00049——与 results/powrep_rollups.json 全对，加和一致性（5+7=12、5+2=7、4+1=5、5+1=6、11+0=11）全对。

## 4. orphan 标签 / 未引用图表检查

- \label 清单：sec:intro（L59）、sec:related（L83）、sec:methods（L92）、sec:results（L134）、tab:stratified（L142）、sec:discussion（L237）、fig:acc（L193）。R15 未增删 label（与 ROUND_R15 "未动图与 label"一致）。
- \ref 清单：tab:stratified 被引 2 次（L138、L192），fig:acc 被引 1 次（L138）。无 orphan 图表，无未引用图表。
- sec:* 五标签零 \ref 引用——与 R1 时一致（ROUND_R15 已记为旧静态解析器噪声，非图表阻塞项，本角色不立项）。

## 5. 重算明细（证据 JSON → tex → 正文引用，R1 方法延续）

脚本：REVIEW_R2/recompute_r8.py（已清理，明细内联如下；python3 运行，全 pass）。

1. GOLD Wilson CI：results/gold_guarded_agreement.json agree=24/25=0.96，json 内 wilson95=[0.804555, 0.992904]；独立重算（标准 Wilson z=1.96）得 [0.804555, 0.992904]，分毫不差；round(.,3)=[0.805, 0.993] 与 tex L55/L232/L237 一致。stem 13/14 + stemless 11/11 = 24/25 与 L232 一致。唯一分歧项 = G06/cloud-new-42（1 项），与 L55/L232 一致。
2. Table L151 Cloud-new guarded 行：guard_v31.json cloud-new（n_guarded=52, acc=0.8667, flips=4, rate=0.0667, p=0.125, ece10_guarded=0.1692）与表行 6 格全对；raw 侧 cloud_new.json（48/60 exact，53/60 tolerant，5 flips，ECE 0.1067/0.0492）与 L200 正文及表 exact 列一致；McNemar(4,0) 独立重算 = 0.125 ✓。
3. Table L157 XDomain-loose 行：xdomain.json loose（25/60=0.4167，45/60=0.75，20 flips=0.3333，p=1.9073486e-06，ECE 0.4767/0.1433）与表行全对；McNemar(20,0)=2/2^20=1.9073e-06 → 表 "p=1.9e-6" ✓。
4. Rollup L226：powrep_rollups.json 五组（pilot50 p=0.0009765625；holdout108 p=0.015625；cloudnew217_raw p=0.03125；cloudnew217_guarded p=0.0625；localnew217 p=0.00048828125）独立 McNemar 重算 5/5 全对；tex 取值（0.0156 / 0.0625 / 0.031 / 0.00049）舍入正确；pilot50 无 p 声称 ✓（R15 已删）。
5. Table L161 PowLocalNew 臂：powrep.json（140/157 vs 147/157，7 flips=0.0446，p=0.015625）与表及 L224 正文一致；与 rollup localnew217 的区分（臂 7/157 p=0.0156 vs 累加 12/217 p=0.00049）无混淆。
6. Figure 1 抽查：tikz 13 对柱（L176-188）与表 guarded/exact 值逐项一致，抽查 PLN（0.8917/0.9363 = 140/157、147/157 ✓）、PCN（0.9108/0.9172 = 143/157、144/157 ✓）、PPi（0.8/0.8 ✓）；caption L192 口径句（pilot 0.6333→1.0、xloose 0.4167→0.75、EN/Math/PPi 零 gap）与表一致；表 n 列加总 30+30+60+60+30+160+40+60+60+20+78+157+157 = 942 ✓。

## 6. 计数与收敛

- 独立重算：6 组（GOLD CI / CN guarded 行 / XD-loose 行 / 5 rollup / PowLocalNew 臂 / 图柱抽查+N 加总），16 个断言全 pass，0 错配。
- 新 Critical：0；新 Major：0；R1 回归 Minor 2 + Nit 2（persist，其中 2 项部分修复残留）。
- 收敛判定：本角色收敛。R15 未引入任何图表类新缺陷；R1 遗留 4 项均为可选修辞（自明性），建议维持 Minor/Nit 不升级，不阻塞投稿。
