# Review Round R2 — R7 伦理 审稿报告（R15 修改版复核）

- 日期：2026-09-08 ｜ 论文：Exact versus Tolerant Label Matching…（264 行，R15 修改版）
- 审稿角色：R7 伦理（独立工作，未与其他角色交流，未修改手稿）
- 输入：`paper_workflow_kb/paper/main.tex`、`paper_workflow_kb/ROUND_R15.md`、`paper_workflow_kb/REVIEW_R1/REVIEW_R1_R7-ethics.md`、`paper_workflow_kb/results/gold_guarded_agreement.json`、`paper_workflow_kb/grades_gold25_user.csv`
- 独立审稿声明：本报告独立完成。

## 1. R1 回归复核（逐项）

| R1 ID | R15 落地情况 | 判定 |
|---|---|---|
| R7-01 GOLD-25 矛盾披露 | 落地。摘要 L55、方法 L119、结果 L232、讨论 L239、Limitations L245 五处一致 24/25 + Wilson CI [0.805,0.993] + G06/cloud-new-42 具名；与 `gold_guarded_agreement.json`（agree=24, n=25, G06 `guarded_correct:false`/`user_grade:对`, wilson [0.8046,0.9929]）逐项吻合；BI L252–253 支点同步修正为 G06 残余风险 | PASS，无回归 |
| R7-02 "independently graded" 夸大 | **未落地**：L119 "was graded independently item by item"、L232 "independent item-by-item grading" 原样保留；且 L232 新增 "an independent second grading" 把同一人盲评包装成独立二评；评分者=作者（user）的身份在 Methods/Limitations 全文零披露（证据文件名与 CSV 备注 `user-confirmed` 反证） | 回归 → R2-R7-01（升级 Major，理由见下） |
| R7-03 COI/资助/受试者声明 | **未落地**：全文 264 行 grep `conflict\|funding\|IRB\|human subject\|consent` 零命中（R15 改动清单亦未列入）；2–3 句显式声明仍缺席 | 回归 → R2-R7-02（维持 Minor） |
| BI 模板首句删除 | 落地：BI L252 起始 "Over-trusting a tolerant matcher…"，无模板腔首句 | PASS |
| 双盲干净度 | PASS：无作者名/邮箱/机构/GitHub 残留（仅模板注释 L32–L36）；L119 "authoring model is muse-spark" 系模型披露，不识别人类作者身份 | PASS |
| guard 安全主张诚实度 | PASS：guard "exactly in-sample" + 环形披露（L55/L123/L239），L123 circularity 段完整（事后构造＋样本外支撑＋未测 targeting 如实写）；无 "guardrail 验证" 拔高措辞 | PASS |

## 2. 问题清单（只含 R1 回归；本轮伦理域内无 NEW Critical/Major）

| ID | 严重度 | 位置 | 问题 | 期望 | 证据链接 | new / R1 回归 |
|---|---|---|---|---|---|---|
| R2-R7-01 | Major | L119（"graded independently item by item"）；L232（"independent item-by-item grading"、"an independent second grading beyond the in-session single rater"）；Methods 金段＋L245 全文缺评分者身份句 | 盲评者即作者（user）却以 "independent(ly)" 申报两次＋新增一次：CSV 备注列与证据文件证明 25 格均为同一用户所判（G06 亦为该用户判"对"），"independent second grading" 的 "second" 只是同一人的盲法重判，不构成独立评分者；确认偏误风险未被读者可见。R15 动过 L119/L232 两句却逐字保留 "independent"，且新增一处同类措辞，属修复失败＋表述面扩大，故 R1-Minor 升级为 Major（一词＋一句即可修，非上纲上线） | (a) 三处 "independent(ly)" 改为 "blinded"（如 "was graded blinded item by item by the author"）；(b) Methods 金段或 Limitations 加一句评分者身份与盲法（"Grading was done by the author (single rater), blinded via shuffled order with verdicts sealed in evidence/gold_key.json; no second independent rater"） | `grades_gold25_user.csv` 备注列（25 行 "user-confirmed"）；`results/gold_guarded_agreement.json`（`user_grade` 字段、G06 行）；`paper/main.tex` L119、L232 | R1 回归（R1-R7-02 修复失败） |
| R2-R7-02 | Minor | 全文（264 行内无 COI/资助/受试者显式句；grep 零命中） | 无资助、无冲突、无人类受试者（模型输出＋作者自评）、题目自编无许可负担——全部靠推断，无一句显式表态；TMLR 惯例要求显式声明而非读者推断 | 加 2–3 句显式声明（如 "No external funding; no competing interests; no human subjects (all judgments are author grades of model outputs); self-authored items, no licensing burden"），位置 Limitations 末或 Availability 旁 | 全文 grep `conflict\|funding\|IRB\|human subject\|consent` 零命中；R1-R7-03 | R1 回归（R1-R7-03 未修） |

## 3. 狩猎 NEW 问题结论

- 伦理域内 R15 引入的新增文本（24/25 重构五处、BI G06 句 L253、in-sample 降级、regime-contrast 改写）逐一核对，均诚实无拔高；L239 "control knob" 一词残留系措辞一致性问题，属 R3/R6 写作域（且 L80/L241 已用 regime contrast），R7 不另立案。
- "Blinded" 程序本身真实（乱序＋`gold_key.json` 密封），不质疑；G06 恰为作者判错而 guard 判对的实例，反而坐实"需具名单人评分者"的 R2-R7-01 立场。
- **NEW Critical：0；NEW Major：0。**

## 4. 计数与收敛判定

- Critical：0 ｜ Major：1（R1 回归升级） ｜ Minor：1（R1 回归维持） ｜ Nit：0
- NEW（R1 未提过）：0
- 是否收敛：**未收敛**—— R2-R7-01（Major）为投前必修，但修复成本极低（一词替换×3＋一句身份声明），修后无需再审伦理全量，R3 由他角顺带确认措辞即可。
