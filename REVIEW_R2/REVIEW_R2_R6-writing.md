# Review Round R2 — R6 写作审稿报告（R15 修改版复核）

- 日期：2026-09-08 ｜ 手稿：paper_workflow_kb/paper/main.tex（R15 版，265 行）｜ 角色：R6 写作（独立审稿，未与其他角色交流，未修改手稿）
- 输入：ROUND_R15.md（R15 改动清单）、REVIEW_R1_R6-writing.md（R1 报告，R6-01~R6-11）、CLAIM_LEDGER.md（C09--C48）
- 方法：全文逐行 grep 复核（关键词行号均为证据）；摘要词数用正则去命令后实算；括号配对逐字符核对 L239

## 1. R1 逐条复核（修复是否真落地）

| R1 ID | R15 声称 | 复核结论 |
|---|---|---|
| R6-01 摘要 Holm 限定 | 加联合控制限定 | ✅ 落地（L54 第二句 two survive / other three stratum-local） |
| R6-02 pilot 功效 caveat 声明句内 | 功效诚实化 | ❌ 回归：L67、L196、摘要 L54 pilot 分句仍无 n=30/50 内联 caveat，仅远端 Methods L131 / Limitations L245 有 |
| R6-03 observed 全覆盖五推断 | 总括句 | ✅ 落地（L54 第二句覆盖余下三层；首句悬垂修饰语见新 Nit R2-R6-06） |
| R6-04 guard in-sample | 2 处 | ✅ 落地（L55、L239 均有 in-sample） |
| R6-05 rollup 矛盾 | 删 p 值/调平 | ❌ 回归：L226 保留 "newly significant"＋"third and fourth significant paired inferences"，同时自称 "rather than new tests"（见 R2-R6-04） |
| R6-06 单臂 vs rollup 区分标准 | 措辞调平 | ⚠️ 部分：L224/L226 均挂 observed 标签，但何时单臂可升级为 "significant paired inference" 的判定标准仍未成文 |
| R6-07 舍入统一 | — | ❌ 回归：0.0005（L54）/ 0.00049（L226）/ 0.00048828125（账本 C44）；0.016（L54）/ 0.0156（L161/224/226） |
| R6-08 术语 tolerant/guarded | 版本标定 | ⚠️ 部分：L196/198 用 "tolerant-correct"、L200 标注 (raw) 可辩护，但与表注 "guarded (v3.1) basis"（L141）并存，全文未给版本标定句 |
| R6-09 67-of-68 | 2 处 | ✅ 落地（L55、L80 "67 of the 68 judged rows"） |
| R6-10 alone＋家族限定 | alone 删 | ✅/❌ 各半：alone 全文 0 命中（已删）；但 "not single-model"（L239）仍无同家族限定（仅 Methods L104 提 same family，license 句无） |
| R6-11 长句可核查性 | — | ❌ 未动：摘要仍 433 词（见新 Major R2-R6-01），L106 仍为 ~300 词巨句 |
| 附录指针 gold_guarded＋C09--C48（R15-10） | 新增 | ✅ 落地（L262 尾部含 results/gold_guarded_agreement.json (24 of 25) 与 CLAIM_LEDGER.md (C09--C48 verified)） |
| H1 拆分 / BI 加 G06 句 / three-matcher 定义 | — | ✅ 均落地：L64（H1＋两非推断公约分离）、L253（G06 残余风险句）、L53（exact / tolerant / guarded v3.1 三档定义） |
| 中英残留 / raw-guarded 基线指代 / 时态 | — | ✅ 通过：CJK 命中均为有意示例（L61/115/198/218/222）＋导言 xeCJK 设置；"Every discordant row was adjudicated (67 of 68…)" 自洽（第 68 行已裁决为 incorrect，非漏裁） |

## 2. 问题清单（只报 R1 未提过的新 Critical/Major＋修复失败回归；Minor/Nit 标明不阻塞）

| ID | 严重度 | 位置 | 问题 | 期望 | 证据链接 | new / R1 回归 |
|---|---|---|---|---|---|---|
| R2-R6-01 | Major | L52--56（摘要全文） | 摘要 433 词（去命令后实算，13 句），数字墙仍在：一句内压 13 层结论＋Holm＋裁决＋gold＋guard＋tempscale，远超 150--250 词常规；R15 未动摘要长度 | 拆分为背景/方法/结果/限定四段、目标 ≤250 词；或至少把 Holm 限定句与 null 层枚举移入正文，摘要只留 headline＋限定 | main.tex L52-56；ROUND_R15.md 第 16 项（功效诚实化未含摘要瘦身） | new（R6-11 仅点长句，本次首次量化 433 词并升级严重度） |
| R2-R6-02 | Major | L239、L247 vs L80、L241 | "control knob" 强因果措辞残留并与新术语打架：R15 声称 knob→regime contrast（2 处：L80、L241 尾部已落地），但 license 句 L239 仍为 "as the control knob"，L247 仍为 "prompt-regime control knob"，L228/L241/L245 仍用 "prompt-knob"；同一概念两套术语，且最强因果词恰留在 license 句 | 全文统一为 regime contrast（或给 knob 下操作定义）；L239/L247 必须改，与 L228 的不复现结论（"not a universal instruction switch"）一致 | main.tex L80/L228/L239/L241/L245/L247；ROUND_R15.md 第 9 项 | new（R15 改写引入的新不一致） |
| R2-R6-03 | Major | L239 license 句 | license 句自相矛盾："significant in five stratum-local readings (…; all five observed-significance under joint error control); two of the five survive Holm" —— observed-significance 与 under joint error control 矛盾修辞；按字面读者会误读为五层在联合控制下成立，而实际仅两层存活 | 改写为 "significant in five stratum-local readings; under joint error control only two survive (…), the other three are stratum-local observed significance only"（与 L243 Multiplicity 口径逐字对齐） | main.tex L239 vs L243（后者口径正确） | new（R15 H1 方向化改写引入） |
| R2-R6-04 | Major | L226 | R6-05 修复失败：rollup 仍称 "newly significant"、"the third and fourth significant paired inferences"，同段又称 "rollups are descriptive re-views rather than new tests"；推断语言与非检验声明同段并存 | 二选一：删显著性语言仅留描述性（含 p 值移备注），或增表行并声明推断地位（R1 原期望不变） | main.tex L226 vs Table L140-166（无 rollup 行）；results/powrep_rollups.json | R1 回归（R6-05） |
| R2-R6-05 | Major | L67、L196、L54 pilot 分句 | R6-02 修复失败：pilot n=30 < n_ceil=50 的功效 caveat 仍只在远端（L131、L245），三个声明位（Intro L67 "supports H1 inferentially"、Results L196 同样措辞、摘要 L54）句内无 n/n_ceil 标签 | 声明句内加 "(n=30 of required 50, observed)" 或等效标签 | main.tex L67/L196/L54 vs L131；results/power_update_120.json（n_ceil=50） | R1 回归（R6-02） |
| R2-R6-06 | Nit | L54 | 语法："the other three are stratum-local observed significance"（are＋名词短语） | 改为 "have stratum-local observed significance" 或 "are stratum-locally significant" | main.tex L54 | new（不阻塞） |
| R2-R6-07 | Nit | L239 | 括号不配对："…readings (pilot, …, extended local-new (pool composition pre-specified; … control);" ——两开一闭，外层 "(pilot…" 未闭合（LaTeX 可编译，纯写作缺陷） | 补闭合括号或拆句 | main.tex L239 括号逐数：open 2 / close 1 | new（不阻塞） |
| R2-R6-08 | Minor | L196/198 vs L141 | R6-08 部分回归：正文 L196/198 用 "tolerant-correct"，表注 L141 为 "guarded (v3.1) basis"；pilot/holdout 数值虽不受 guard 影响（L204），标签仍需版本标定句 | 加一句版本标定（pilot/holdout tolerant＝guarded；cloud-new 起 guarded 为报告基准） | main.tex L141/L196/L198/L200/L204 | R1 回归（R6-08，不阻塞） |
| R2-R6-09 | Minor | L239 | R6-10 部分回归：alone 已删（0 命中），但 "the phenomenon is not single-model" 仍无家族限定（实为 deepseek＋qwen2.5/qwen2 同家族两模型＋执笔模型） | license 句加 "within the studied (same-family) models" 限定 | main.tex L239 vs L104/L110 | R1 回归（R6-10，不阻塞） |
| R2-R6-10 | Minor | L224/L226 | R6-06 未闭合：单臂与 rollup 同挂 observed 标签，"何种 discordant 规模下 observed 可表述为 significant paired inference" 的判定标准仍未成文 | 加一句区分原则（或 rollup 与单臂同降描述性） | main.tex L224/L226 | R1 回归（R6-06，不阻塞） |
| R2-R6-11 | Nit | L54/L161/L224/L226 | R6-07 未修：同一 p 值三写法（0.0005/0.00049/全精度；0.016/0.0156） | 定舍入规则（建议正文 4 位有效数字，附录全精度）并对齐 | main.tex L54/L161/L226；C44（0.00048828125） | R1 回归（不阻塞） |

## 3. 计数与收敛判定

- Critical：0（新 0）
- Major：5（新 3：R2-R6-01/02/03；R1 回归 2：R2-R6-04/05）—— 阻塞投稿，未收敛
- Minor：3（均为 R1 回归：R2-R6-08/09/10）—— 不阻塞，可投后修
- Nit：4（新 2：R2-R6-06/07；R1 回归 2：R2-R6-11；R6-11 长句部分并入 R2-R6-01）—— 不阻塞
- **是否收敛：否**。R15 落地了 7 项（Holm 限定、in-sample、67-of-68、alone 删除、H1 拆分、BI-G06、附录指针），但 license 句（L239，论文最关键的许可声明段）存在新自相矛盾＋旧强因果词残留，摘要数字墙未动，rollup 与 pilot 功效 caveat 两处 R1-Major 修复失败。下一轮只需复核五个 Major 的措辞补丁（预计小改），建议 R3 仍由 R6-writing 单项验收，无需全员重审。
