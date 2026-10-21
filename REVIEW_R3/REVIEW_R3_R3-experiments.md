# Review Round R3 — R3 实验轻量验收报告（R16 措辞簇验收）

- 日期：2026-09-08 ｜ 论文：paper_workflow_kb/paper/main.tex（R16 版实测 263 行；改动日志 ROUND_R16.md 缺失，见 §5 备注）
- 审稿角色：R3 实验充分性与公平性（R3-experiments）｜ 只验收措辞簇，不做全稿重审
- 输入：REVIEW_R2_R3-experiments.md（4 个 Major：R2-R3-01～04）、main.tex 全文、一手证据（results/retest60.json、results/guard_v31.json、results/powrep_rollups.json、results/powrep.json、results/holm.json）
- 独立审稿声明：本报告独立完成，未与其他角色交流，未修改手稿。

## 1. R2 四项 Major 验收结论（逐条：修好 / 未修好 + 行号 + 重算）

| R2 ID | 结论 | 行号/证据 |
|---|---|---|
| R2-R3-01 knob 残留（"control knob"/"prompt-knob" 6 处） | ✅ 修好 | 全文正则 `[Kk]nob` 零命中（亲手 grep，0 行）。旧 L239 license 句现为 L239 "with instruction format as a regime contrast…"；"regime contrast" 见 L53/L80/L239/L241，无混用。 |
| R2-R3-02 rollup 计入 five 却被排除 Holm 族 | ✅ 修好（实质） | 摘要旧 "Five paired inferences are significant" 已删除。现 L54："Four in-family readings are nominally significant… Two deterministic rollups are nominally significant outside the test family (holdout 7 of 108, p=0.0156; local-new 12 of 217, p=0.00049)"；L226："rollups are descriptive re-views outside the Holm family rather than new tests" + "the rollup rows overlap strata already tested"；L243："extended-stratum rollups are deterministic re-views of rows already tested, not new tests"，Holm 族 m=17（results/holm.json note "rollups excluded"，亲手核对）。行重叠双重收割的披露已补上。计数口径说明：摘要 "four in-family" = pilot/pool/xdomain-loose/PowLocalNew 四者确为 Holm 族内成员（holm.json ordered 含 prespecified-pool 与 powL_localnew，亲手核对 17 条）；Discussion L239 的 "five counted" 为另一套 by-construction 计数并明示排除项（PowLocalNew 单臂、raw-basis cloud-new），两套口径各自披露充分（残留序数小瑕见 Minor R3-R3-01）。 |
| R2-R3-03 pilot-50 上限矛盾（L239 "now met with 50" vs L245/L226） | ✅ 修好 | 旧 "now met with 50" 已删除。现 L239："holdout-108, cloud-new-217, and local-new-217 are now met with 108, 217, and 217 rows (pilot-50 remains a 30-row stratum plus a 20-row descriptive cross-model extension, cf. Extended strata)"；L245："pilot 30 of 50…remain under…"；L226 pilot50 rollup "descriptive only with no p-value claimed; the pilot inference rests on the 30-row stratum"。三处口径统一。 |
| R2-R3-04 retest 混合口径含误接受未披露 | ✅ 修好（取 R2 选项一：标注口径+披露） | 现 L230："identical raw-basis flip sets (5 and 5, including the documented O2 mis-accept; guarded basis 4 and 4)"。未封存 retest60_guarded.json，但 R2 允许"标注口径并披露"路径，已满足（"raw-basis" 明示 + 误接受明示 + guarded 4/4 明示）。数字亲手重算见 §3。 |

## 2. 问题清单（NEW 猎取 + 回归）

| ID | 严重度 | 位置 | 问题 | 期望 | new / 回归 |
|---|---|---|---|---|---|
| R3-R3-01 | Minor | L226 "These are the third and fourth nominally significant readings" | 序数悬空：按 Discussion 五计数（pilot/pool/xdomain-loose/ext-holdout/ext-localnew）二者应为第四/第五；按正文出现顺序亦非第三/第四。无推断后果，同句的 observed-status + 族外披露正确。 | 改为 "These are two further nominally significant re-views" 或按 Discussion 口径写 "fourth and fifth"。 | new（Minor，不阻塞） |
| — | 备注 | L106/L220、L241、L224、L54/L226 | R2 的 Minor/Nit（R2-R3-05 docstring 预注册通胀、R2-R3-06 b=21 合并、R2-R3-07 0.5% boundary、R2-R3-08 p 舍入）本轮顺带复核：L106/L220 已加 "(not a sealed pre-registration)"；L241 已加 "combined as a descriptive sum on identical questions, no test"；L224 已改为 "well within the 0.5% relative-error tolerance (999 vs 1000…)"；L54/L226 统一为 0.00049/0.0156（"0.0005"/"0.016" 零残留）。全部 ✅，无回归。 | — | R2 minor 复核通过 |

- NEW Critical：0。NEW Major：0。

## 3. 独立重算记录（证据-first，一手重算；McNemar 精确双侧公式亲手实现复算）

1. Retest：retest60.json → flip_set_test == flip_set_retest（各 5 行，含 "氧气的化学符号是？"即 O2 题），guarded_agreement=1.0，exact_string_agreement=0.9833，drift=0.0107，guarded_mcnemar b=0/c=0。L230 "raw-basis 5 and 5（含 O2 误接受）" ✅。
2. Guarded 基准：guard_v31.json strata.cloud-new.flips_guarded=4（v3→v3.1 唯一改动 cloud-new-42 "O" vs "O2"）。L230 "guarded basis 4 and 4" = raw 5/5 减去该已知误接受，算术可导 ✅（派生值，非封存文件，已在 L230 按口径披露）。
3. Rollup：powrep_rollups.json → holdout108 b=7 p=0.015625（正文 0.0156 ✅）；localnew217 b=12 p=0.00048828125（正文 0.00049 ✅）；pilot50 b=11 p=0.0009765625；cloudnew217_guarded b=5 p=0.0625（L226 ✅）；raw 6/217 p=0.03125（L226/L239 ✅）。亲手 McNemar 复算 b=7/12/11/9/20/5/6/2/1/4（c=0）全部命中 ✅。
4. Holm：holm.json → m=17（亲手数 ordered 17 条），stop step3（pool p=0.00390625 > 0.003333），survivors=[xdomain-loose, pilot]，note "rollups excluded"。L54/L243 ✅。PowLocalNew（powL_localnew, b=7, p=0.015625）确为族内第 4 个 per-test 显著，摘要 "four in-family" 有据 ✅；powrep.json powL_localnew n=157/n_flips=7 ✅。
5. Knob：全文 `[Kk]nob` 零命中 ✅；"five significant"/"Five paired"/"0.0005"（p 值语境）零残留 ✅。

## 4. 计数与收敛判定

- R2 四项 Major：4/4 修好（R2-R3-01 ✅、R2-R3-02 ✅、R2-R3-03 ✅、R2-R3-04 ✅）。
- 本轮：Critical 0 ｜ Major 0 ｜ Minor 1（R3-R3-01，不阻塞）｜ Nit 0。
- 是否收敛：是（R3 措辞簇范围）。Minor R3-R3-01 建议顺手改，不设为 R4 门禁条件。

## 5. 过程备注

- paper_workflow_kb/paper/ROUND_R16.md 缺失（paper_workflow_kb/ 下最新 ROUND 日志为 ROUND_R15.md；paper/ 目录内无 ROUND 文件）。本验收以 main.tex 落地文字为准，不以日志为准；建议补写 ROUND_R16.md 记录 R16 改动与 manifest 重跑，但属流程项，不影响本验收结论。
