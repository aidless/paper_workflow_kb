# Review Round R2 — R2 统计审稿报告

- 日期：2026-09-08 ｜ 手稿：paper_workflow_kb/paper/main.tex（R15 修改版，264 行）
- 审稿角色：R2 统计 ｜ 独立审稿声明：本报告独立完成，未与其他角色交流，未修改手稿。
- 输入：ROUND_R15.md（R15 改动说明）、REVIEW_R1_R2-statistics.md（上一轮本角色报告）、CLAIM_LEDGER.md、results/*.json。

## 1. R15 修项复核（R1 本角色项是否真落地）

| R15 修项 | 核对位置 | 结论 |
|---|---|---|
| #3 摘要 Holm 限定 2/5 存活 | main.tex L54："Under Holm-Bonferroni over all seventeen paired tests, two of the five survive (pilot, cross-domain loose); the other three are stratum-local observed significance." | 落地 ✓（R1 R2-01 关闭） |
| #3 Holm 程序细节 | L243：family=17（13 strata + pool + 3 loose arms），survivors=(xloose, pilot)，step3 pool p=0.0039 > threshold 0.00333；results/holm.json 逐位一致 | 落地 ✓ |
| #4 n_ceil 标 post-hoc | L131："With observed discordant rates (post-hoc: each ceiling is computed from the same stratum's observed rate, so these are sensitivity checks rather than pre-data power justifications…)" | 落地 ✓（方法段） |
| #4 pool 降级 | L131（"only the pool composition was pre-specified…stratum-local observed significance"）、L214（"Only the pool composition was pre-specified; under joint error control this reading is stratum-local observed significance"）、L243 | 落地 ✓（R1 R2-05 方法/结果侧关闭；摘要侧残留见 R2-R2-02） |
| #5 pilot50 去 p | L226："descriptive only with no p-value claimed; the pilot inference rests on the 30-row stratum, p=0.0010" | 落地 ✓ |
| #5 rollup 重叠披露 | L226："the rollup rows overlap strata already tested, so rollups are descriptive re-views rather than new tests"；L220 跨域 5/60 重叠灵敏度；L243 family 明确排除 rollups | 落地 ✓（R1 R2-03 关闭） |
| #5 R2-02 license 调平 | L224（arm）与 L226（holdout rollup）同为 "significant at alpha=0.05 as a single-arm observation with observed status … no power conclusion"，b=7/c=0/p=0.015625 两边一致 | 落地 ✓（R1 R2-02 关闭） |
| #2 24/25 Wilson CI | L55、L232、L239 均为 "24 of 25 … Wilson 95% CI 0.805 to 0.993"；与 results/gold_guarded_agreement.json [0.8045552759497747, 0.9929039496133009] 舍入一致 | 落地 ✓（见 §2 独立重算） |

## 2. 独立重算结论（stdlib only：math.comb + Wilson 公式手写，无第三方统计库）

- McNemar 精确双侧公式：p = 2·Σ_{k=0}^{min(b,c)} C(b+c,k) / 2^{b+c}（cap 1；b+c=0 报 1.0）。重算 9 格 b=12/7/9/11/20/5/4/2/1（c 全 0）：
  12→0.00048828125 ✓｜7→0.015625 ✓｜9→0.00390625 ✓｜11→0.0009765625 ✓｜
  20→1.9073486328125e-06 ✓｜5→0.0625 ✓｜4→0.125 ✓｜2→0.5 ✓｜1→1.0 ✓。
  全部与 powrep.json / powrep_rollups.json / combined_qwen2.json / holm.json **逐位一致**。
- Wilson 95%（z=1.96）：24/25 → [0.8045552759497747, 0.9929039496133009]，
  与 gold_guarded_agreement.json **逐位一致**；round(.,3)=[0.805, 0.993]，手稿三处印刷 ✓。
- Holm step3：threshold = 0.05/(17−3+1) = 0.0033333333333333335 ✓；pool p=0.00390625 > threshold，止步 ✓；survivors=[xdomain-loose, pilot] ✓。
- 求和：N = 30+30+60+60+30+160+40+60+60+20+78+157+157 = 942 ✓；
  flips = 11+5+4+5+0+4+0+1+20+0+2+1+7 = 60，60/942 = 0.0637 ✓（L234）；
  adjudication 20+9+21+10+7 = 67 of 68 ✓（L55/L80）。
- **重算结论：≥2 个 p 值 + Wilson CI 全部复算通过，无数字伪造；R15 未引入数字错误。**

## 3. 问题清单（只报 R1 未提过的新 Critical/Major；R1 项仅修复失败才回归）

| ID | 严重度 | 位置 | 问题 | 期望 | 证据链接 | new / R1 回归 |
|---|---|---|---|---|---|---|
| R2-R2-01 | Major | L224 vs L54 / L239 / L243 | "five" 计数成员规则未声明，排除了同等显著的第六个读数。L224 许可 PowLocalNew 单臂（b=7, c=0, p=0.0156）为 "significant at alpha=0.05 as a single-arm observation with observed status"——与被计入 "five" 的 holdout rollup（L226，同为 b=7/c=0/p=0.0156，逐位相同证据强度）显著性地位完全相同，却被排除在 "five" 之外且无解释。另 L226 括号内 raw-basis cloudnew217 p=0.031 是第七个名义显著（非声明基底）。于是 "five" 既非全部未校正显著读数，也非 Holm 存活集（2 个），其成员规则全文未写；L239 "significant in five stratum-local readings（…列举五者）" 呈穷举式表述，与 L224 矛盾。 | 加一句话声明计数集（例如 "the five = pilot, pool, xloose + 2 rollups; the four power-rep single arms are reported separately and not counted toward the five"），或把计数修正为六并注明两处 p=0.0156 证据强度相同；同时声明 raw-basis p=0.031 不计入的原因（非声明基底）。 | paper/main.tex L224, L226, L54, L239；results/powrep.json（powL_localnew p_two=0.015625）；results/powrep_rollups.json（holdout108 p_two=0.015625） | new（R1 R2-02 只要求统一 license，未涉及 headline 计数的穷举性；R2-03 是重叠 double-count，本项是镜像的 exclusion under-count） |
| R2-R2-02 | Minor | L54（摘要）vs L131（方法） | R1 R2-05 要求摘要 n_ceil 加 post-hoc 限定；R15 只落在方法 L131 与局限 L245，摘要 L54 仍为裸 "meeting its required n=217"，结果 L214 "(n=220, meeting n_ceil=217)" 同样无 post-hoc 限定词。 | 摘要/结果两处 meeting 后加 "(post-hoc sensitivity ceiling, see Methods)" 或等效 5 词限定。 | paper/main.tex L54, L214 vs L131 | R1 回归（R2-05 部分修复失败） |
| R2-R2-03 | Nit | L54 / L243（p=0.0005）vs L226（p=0.00049） | R1 R2-06 舍入口径不一致仍存在：同一量（2/4096=0.00048828125）摘要与 Multiplicity 段印 0.0005，rollup 段印 0.00049。 | 全文统一为一版（建议 0.00049 或 4.9e-4），重跑 numbers scan。 | paper/main.tex L54, L226, L243；results/powrep_rollups.json（0.00048828125） | R1 回归（R2-06 未修） |

## 4. 狩猎空区声明（查过、无新问题）

- FWER 新话术：Holm family 构成（13+1+3=17，rollups 排除）与 holm.json 一致；"observed / stratum-local observed significance" 全文用法一致且均有 Multiplicity accounting 交叉引用；未发现新的未校正显著话术。
- CI 与显著性一致性：唯一 CI 声称（24/25 Wilson）下限 0.805，与高一致率声称同向；无从 CI 反推显著性的声称；stem 13/14 子 CI 未印刷，无矛盾。
- n/N 一致性：N=942 十三层直加 ✓；67/68 分解（20+9+21+10+7）✓；854−794=60 ✓；412 regime-contrast（tight 在 N 内 98+157+157=412，loose 被排除 98+157+157=412）与 L53/L228/L241 一致 ✓。

## 5. 收敛判定

- 新 Critical：0 ｜ 新 Major：1（R2-R2-01）｜ Minor/Nit 回归：2（均为 R1 旧项修复失败，无新 Minor/Nit）。
- **是否收敛：否。** R2-R2-01 为投前必修（headline 计数规则一句话修复），修后本角色可收敛；R2-R2-02/03 建议同轮顺手修复。无阻塞投稿项（全部数字逐位可复算，无伪造）。
