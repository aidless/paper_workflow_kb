# Review Round R3 — R6 写作单项验收报告（R16 版）

- 日期：2026-09-08 ｜ 手稿：paper_workflow_kb/paper/main.tex（R16 版，264 行）｜ 角色：R6-writing（单项验收，未改手稿）
- 输入：REVIEW_R2/REVIEW_R2_R6-writing.md（5 个 Major）、REVIEW_R2/ROUND_R16.md（12 簇日志）、r16_fixes.py（单次脚本，R16 日志称全断言通过；本轮未重跑——脚本为一次性替换，复跑计数必为 0，故以手稿现状 grep/重算为准）
- 方法：全文 grep 行号取证；摘要词数用 R6 同方法（去 `\命令` 后实算）；McNemar 精确双侧 p 值 10 组亲手重算（r3_r6_recalc.py）；Wilson 24/25 亲手重算；括号逐数。凡引数字均有重算，无"未重算"项（CI 与 p 值均为本轮亲算；r16_fixes.py 的通过声明沿用 R16 日志，未独立重跑）。

## 1. R2 五项逐条验收

| R2 ID | R2 期望 | R16 现状（行号证据） | 结论 |
|---|---|---|---|
| R2-R6-01 摘要 433 词 | ≤250 词，四段或瘦身 | ✅ 已修：摘要 L53–55 去命令后实算 **243 词**（本轮亲算，与 R16 脚本打印一致）；Holm 限定句保留但 null 枚举/边界层/c=0 展开已移入正文 | PASS |
| R2-R6-02 knob 残留 | 全文统一 regime contrast，L239/L247 必改 | ✅ 已修：`knob` 大小写 **0 命中**（含 control knob / prompt-knob 全清）；`regime contrast` L54/80/228/239/241/245/247 共 7 处＋`regime-contrast` L53/106/241；L239 "as a regime contrast"、L241 漏网已补 | PASS |
| R2-R6-03 license 句矛盾 | observed vs joint-control 矛盾修辞，与 L243 对齐 | ✅ 已修：L239 重写为 "nominally significant in five counted readings … all five carry observed-significance status, i.e. stratum-local only). Two of the five survive Holm-Bonferroni … (pilot, cross-domain loose)"，与 L243（17 检验、step-3 停、pool 0.0039 > 0.00333 不存活）逐字同口径；括号 **22/22 配平**（R2 时 2 开 1 闭）；附带落地：计数集声明句（PowLocalNew 单臂不计、raw-cloudnew 不计）、"(within the tested families)" 家族限定 | PASS |
| R2-R6-04 newly significant | 删显著性语言或声明推断地位 | ✅ 已修：`newly significant` **0 命中**；L226 为 "nominally significant, observed status"＋"descriptive re-views outside the Holm family rather than new tests"；L239 计数集句与之互锁 | PASS |
| R2-R6-05 pilot caveat 句内 | L67/L196/摘要 pilot 分句句内加 (n=30 of 50) 标签 | ❌ **未修**：L67 "The pilot subset (n=30) clears the descriptive bar and supports H1 inferentially (p=0.0010)."、L196 同样措辞、摘要 L54 "(11 of 30 flips, p=0.0010)" ——三处仍无 n_ceiling=50 句内标签。部分缓解（不算落地）：L239 不再谎称达标（"pilot-50 remains a 30-row stratum plus a 20-row descriptive cross-model extension"）；远端披露 L131（"current 30 … pre-hoc sensitivity is limited"）/ L245 仍在。讽刺的是摘要同句内单臂项反而已标 "without a power conclusion"，pilot 却无 | **FAIL（Major 延续，阻塞）** |

## 2. NEW Critical/Major 扫描（重点：重写摘要 L52–56、license 句 L239）

- 结论：**NEW Critical 0，NEW Major 0**。摘要 headline 数字与正文逐项对齐：pilot 11/30 p=0.0010（L149/L196）、pool 9/220 p=0.0039（L214）、xloose 20/60 p=1.9e-6（L157/L220）、单臂 PowLocalNew 7/157 p=0.0156（L161/L224）、rollup holdout 7/108 p=0.0156＋local-new 12/217 p=0.00049（L226）、Holm 17 检验 2 存活（L243）、c=0、loose 重跑 2/1/4 ns（L228）、67/68、guard in-sample one-fix-zero-regression、gold 24/25 CI 0.805–0.993、retest guarded 1.0、tempscale/isotonic 阴性、854/942（=794+60，L234）。
- 亲手重算：McNemar 精确双侧 10 组（11/0→0.00098≈0.0010；9/0→0.00391≈0.0039；20/0→1.907e-6≈1.9e-6；12/0→0.000488≈0.00049；7/0→0.015625≈0.0156；5/0→0.0625；4/0→0.125；2/0→0.5；1/0,0/0→1.0）**全 match**；Wilson 24/25 = **(0.8046, 0.9929)→0.805/0.993 match**；翻转率 11/30=0.3667、9/220=0.0409、20/60=0.3333、7/157=0.0446、12/217=0.0553、7/108=0.0648 与正文一致。
- R6-07 舍入：✅已修——`0.0005` 0 命中（统一 0.00049，L54/226/243/262）；`0.016` 命中 L156/L218 系 0.0167 翻转率（1/60），不同量，合法。
- 摘要 "Four in-family" vs license "five counted"：集合不同但各自显式定义且 L239 计数集句说明互斥关系（PowLocalNew 单臂不计入 five；two rollups 在 family 外），不计问题，仅备注。

## 3. Minor/Nit（记录，不阻塞）

| ID | 严重度 | 位置 | 问题 |
|---|---|---|---|
| R3-R6-m1 | Minor | L220 vs L226 | 序数松散：L220 称 xloose 为 "the second significant paired inference"，L226 称 ext-holdout/ext-localnew 为 "third and fourth"——pool（p=0.0039，L214 在 xloose 之前）亦显著时序数对不上。R16 前已存在，非 R16 引入；建议删序数或给排序定义 |
| R3-R6-n1 | Nit | L54 | "the rest are stratum-local observed significance"（are＋名词短语）残留；但 "observed-significance status" 已成全文定义术语（L131/239/243），可接受，Nit 保留不阻塞 |
| R2-R6-06/07/08/09/10/11 回归项 | Nit/Minor | — | R2-R6-06（上条 n1）、R2-R6-07（括号，已修 22/22）、R2-R6-08（tolerant/guarded：L196/198 已加"identical to guarded"等价注，版本标定可算落地）、R2-R6-09（家族限定已入 license 句）、R2-R6-10（rollup outside-Holm-family 声明已算区分原则）、R2-R6-11（舍入已修）——均不阻塞 |

## 4. 计数与收敛判定

- Critical：0（新 0）
- Major：**1（遗留 R2-R6-05 延续；新 0）—— 阻塞投稿，未收敛**
- Minor：1（新 R3-R6-m1 序数）—— 不阻塞
- Nit：1（残留 n1）—— 不阻塞
- **是否收敛：否**。4/5 已修（含最危险的 license 句矛盾与摘要数字墙）；唯一阻塞项为单句补丁：L67、L196、摘要 L54 pilot 分句句内加 "(n=30 of required 50; observed, pre-hoc sensitivity limited)" 或等效标签。下一轮只需 R6-writing 单项复核该三处（grep `n_cean\|required 50` 在 L54/L67/L196 命中即放行），无需全员重审。
- 附记：PDF 仍为旧版（R16 日志称本机无 TeX，需用户侧 latexmk -pdf；本轮未编译，仅做括号/文本级核查）。
