# Review Round R2 — R5 可复现 审稿报告（R15修改版复核）

- 日期：2026-09-08 ｜ 手稿：paper_workflow_kb/paper/main.tex（R15修改版，264行）
- 审稿角色：R5 可复现 ｜ 独立审稿声明：本报告独立完成，未与其他角色交流，未修改手稿。
- 输入：ROUND_R15.md（R15说明）、REVIEW_R1/REVIEW_R1_R5-reproducibility.md（R1报告）、results/gold_guarded_agreement.json、CLAIM_LEDGER.md、evidence_manifest.json。
- 独立重算：Wilson CI 与 per-item 一致率已用独立实现从 json + guard_v31.json + gold_key.json + grades_gold25_user.csv 三源重算（见 §3）。

## 1. 总体判断

- GOLD-25→24/25 全链修复成立：新证据、重算脚本断言、六处正文数字、CI 舍入、stem 分组、唯一分歧 G06 全部对齐；旧数字零残留（§2）。
- 可复现披露三项落地诚实：digest/seed 未 pin（L247）、pilot 采集脚本失传（L247 + d2_60.jsonl 逐行 provenance 实测存在）、无公开仓库链接（L249 明示 not minted + 随投稿补充材料交付）——文字与证据现状一致，无过度承诺。
- R1 六个 Major 中四个已关闭（R5-01、R5-02、R5-04、R5-05），两个修复失败（R5-03 云端 14/14 口径过期、R5-06 “independent” 黄金评分措辞与评分人身份未披露）。
- 新问题 2 个，均为 Minor；无新 Critical/Major。
- Critical 0 ｜ Major 2（均为 R1 回归）｜ Minor 2（均为 NEW）｜ Nit 0 ｜ 是否收敛：**否**（2 个 Major 回归未清）。

## 2. 问题清单

| ID | 严重度 | 位置 | 问题 | 期望 | 证据链接 | new/R1回归 |
|---|---|---|---|---|---|---|
| R2-R5-01 | Major | main.tex L138；results/cloud_repro.json | 云端字节复现 14/14 口径过期且首句过度承诺：L138 “All recomputation scripts were re-executed on the cloud host with byte-identical outputs on 14 of 14 result files”。实测 cloud_repro.json 的 14 文件（analysis.json、cloud_new.json、analysis_120.json、local_new.json、analysis_180.json、guard_v31.json、tempscale.json、isotonic.json、ablation.json、flips.json、flips_new60.json、flips_local60.json、power_update_120.json、power_local60.json）全部早于 xdomain / powrep / rollups / holm / gold_guarded / local_big-en / math40 / combined_qwen2 / retest60 / code_pilot / guard_v32 / analysis_410 时代；R15 对此句零修改（apply_R15.py 无对应 edit，ROUND_R15.md 未提及 R5-03）。“All recomputation scripts” 对新脚本不成立。 | 二选一：(a) 把 cloud_repro_check.py 扩展到全部 sealed 结果文件后重跑并更新 14→实际数；或 (b) 收窄 L138 为 14 个具名旧文件的复现声明，并披露新层（xdomain/powrep/holm/gold_guarded 等）为本地单机重算、无云端字节复现。 | paper_workflow_kb/results/cloud_repro.json（n_files=14，文件清单见上）；paper_workflow_kb/paper/main.tex L138；paper_workflow_kb/scripts/apply_R15.py（无 R5-03 edit） | R1 回归（R1 R5-03 修复失败） |
| R2-R5-02 | Major | main.tex L232（2处）、L80、L55 | GOLD-25 “independent” 措辞保留且评分人身份正文零披露：L232 “independent item-by-item grading agrees 24 of 25” 与 “giving them an independent second grading beyond the in-session single rater”；全文 author 词 toutes 语境均与黄金评分人无关（L39 模板注释、L115 版本、L119/L245 执笔模型与 judge 异源、L239 计数），即评分人 = 作者（user，grades_gold25_user.csv 文件名唯一暗示）从未在正文明示；11/11 stemless 无题干、第三方不可复核一点亦无限定（R1 原诉求两项均未动；apply_R15.py 无对应 edit）。Blinded 程序（key 密封、顺序打乱）为真，但 “independent” 严格夸大评分人独立性。 | “independent item-by-item grading” → “blinded author grading（grader = author/user, key sealed）”；补一句 stemless 11 项无存档题干、第三方不可独立复核的限定；或补独立第二评分人 + 一致率。 | paper_workflow_kb/paper/main.tex L232、L80；全文 author 检索（6处，无一指向黄金评分人）；paper_workflow_kb/grades_gold25_user.csv（25 行全“对”）；REVIEW_R1 R5-06 | R1 回归（R1 R5-06 修复失败） |
| R2-R5-03 | Minor | CLAIM_LEDGER.md C33（L54）vs C46（L67） | 账本新旧 GOLD 条目并存 “verified” 无 supersession 注：C33 仍以 25/25、agreement 1.0、Wilson [0.8668,1.0]、14/14 + 11/11 登记为 verified（证据 results/gold_agreement.json），C46 以 24/25 登记为 verified；重跑 scripts/analyze_gold.py 的用户仍得被证伪的 25/25，账本不阻止误引用。 | C33 状态改为 superseded（或加注 “analyze_gold.py 输出保留为被证伪假设记录，guarded 口径以 C46 为准”）。 | paper_workflow_kb/CLAIM_LEDGER.md L54、L67；paper_workflow_kb/scripts/analyze_gold.py；paper_workflow_kb/results/gold_agreement.json | NEW |
| R2-R5-04 | Minor | main.tex L262（附录 Evidence pointers） | 附录旧 decode 指针无 falsified 标记：“…results/gold_agreement.json (25 of 25 under the all-correct assumption)…; guarded-reference recomputation … (24 of 25)”——“the all-correct assumption” 在附录内无 “falsified on G06 / superseded” 后缀（Methods L119 有完整披露，附录无）。速读读者可直接引用旧指针。 | 附录旧指针加后缀 “(assumption falsified on G06; superseded by the guarded-reference recomputation following)” 或仅保留 guarded 指针为 governing。 | paper_workflow_kb/paper/main.tex L262、L119（对照：L119 有 fails on G06 句） | NEW |

注：R1 R5-07（powrep strip 预清洗，Minor）与 R5-08（requirements 占位，Minor）本轮未深审；其中 R5-08 确认仍 open（requirements.txt 178 字节仍含 “Fill in the pinned versions”，modified 停于 2026-09-07T04:18，未动），维持 Minor 不升级。

## 3. 独立重算结论（R15 GOLD 链，PASS）

- 重算 24/25 Wilson 95% CI：独立实现得 [0.8045552759, 0.9929039496]，与 gold_guarded_agreement.json 逐位一致（差 <1e-12）；正文六处 “0.805 to 0.993” 为正确 3 位舍入（0.80455→0.805，0.99290→0.993）；账本 C46 [0.8046, 0.9929] 为正确 4 位舍入。一致。
- stem 分组：13/14（mine [0.6853, 0.9873] = json），stemless 11/11；per-item recount 24/25，唯一分歧 G06。三源交叉：guard_v31.json changed_single_trace_id = cloud-new-42 且 n_changed_vs_v3 = 1；gold_key.json G06 trace = cloud-new-42（kind flip-stem，故 stem 从 14/14 降为 13/14）；grades_gold25_user.csv 25 行全“对” → vs guarded 一致率 = 24/25。全链闭合。
- 五处 + 附录一致：“24 of 25” 共 7 命中 = L55（摘要）、L119 方法句 ×2（含 “13 of 14 with stems, 11 of 11 stemless” 与翻转富集限定）、L232（结果）、L239（Discussion license）、L245（Limitations 翻转富集）、L262（附录指针 + recompute 脚本）；CI “0.805 to 0.993” 与之同行；“67 of the 68” 恰 2 处（L55、L80），算术核对 21+9+21+10+7=68 judged、20+9+21+10+7=67 confirmed。
- 旧措辞零残留：“25 of 25” 仅 2 处且均在失败披露句内（L119 “…pre-registered decode reports 25 of 25 under its all-guarded-correct assumption…, but that assumption fails on G06…”；L262 附录同式）；旧 CI “0.867 to 1.0”/“0.8668” 零命中；“agreement 1.0” 4 处全部指 retest guarded agreement（L119 方法段 retest 句、L230、L239、L262），与 GOLD 无关。
- 重算脚本断言：recompute_gold_guarded.py 含 assert n=25、唯一 guarded-incorrect=G06、agree=24、stem 13/14、stemless 11/11——与 json 输出互锁，设计正确。
- Manifest：243 条，created 2026-09-07T12:12:34；当前 main.tex sha256 = manifest 记录值（454b8f9792ac8dd8… prefix match，全串 match）；recompute_gold_guarded.py、gold_guarded_agreement.json、apply_R15.py、ROUND_R15.md、CLAIM_LEDGER.md 均在册。证据链完整。
- 披露诚实性：L247 digest/seed 未 pin + pilot/holdout 采集脚本失传 + d2_60.jsonl 逐行 provenance——实测 d2_60.jsonl 首行含 model=deepseek-v4-flash、source_outcome_source=gold_label_relabeled_semantic_v2 等 8 字段，与文字一致，无过度承诺；L249 “no public repository link is minted at submission (materials available on request…)” 与现实一致（未伪造链接）且交付物随补充材料走，R5-04 视为披露关闭。

## 4. 计数与收敛

- Critical 0 ｜ Major 2（R2-R5-01、R2-R5-02，均为 R1 回归）｜ Minor 2（R2-R5-03、R2-R5-04，均为 NEW）｜ Nit 0。
- 是否收敛：否。R1 的 R5-03（复现覆盖）与 R5-06（评分独立性）R15 未修，仍为投前必修；建议 R16 修后 R5 再审（仅复核 R2-R5-01/02/03/04 四条）。

## 5. 自由评语

- 最强的点：GOLD 翻转修得干净——新证据 + 断言脚本 + 六处文字 + 附录指针 + 账本 C46 全对齐，旧数只活在披露句里；这是对抗审稿想要的修法。
- 最担心的点：L138 “All recomputation scripts were re-executed…14 of 14” 在结果文件翻倍后成了全文最易被复现审计抓包的一句；以及 “independent” 一词在盲评程序真实但评分人不独立时仍是投稿风险词。两者都是改一句就能关的 Major，不要拖到投稿后。
