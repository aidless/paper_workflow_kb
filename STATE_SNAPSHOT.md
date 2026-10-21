# STATE_SNAPSHOT.md — 科研状态快照（E104，InnovatorBench InternalSummarizeAction 模式）

> 用途：写作各阶段（Phase 1 登记 → Phase 2 起草 → Phase 4 修改）强制维护的
> "科研工作台"状态机。claim ledger 管"声明↔证据"的静态对账；本快照管
> "研究进程"的动态状态——当前要超越的基线、假设生命周期、实验史、反思。
> 终稿交付前，claim ledger 与快照必须一致（快照里已证实的假设才能以
> 强断言出现；实验中或待办的假设只能 hedge 或 inconclusive，见 E095）。

## 状态字段（每轮修改后更新）

| 字段 | 内容 | 示例 |
|---|---|---|
| `state_of_the_art` | 本工作要超越的基线（论文+数值），可追溯到文献综述 | "2504.02902：迭代校准 ECE 0.38（raw）" |
| `hypotheses` | 假设清单 + 生命周期标记（待办/实验中/已证实） | "H1：演化后统一校准最低 raw ECE [已证实]" |
| `key_knowledge` | 关键领域知识/约束（含反例） | "温度缩放对退化分布分桶无效（E083）" |
| `reflection` | 对已做实验的反思（什么没控制好） | "三臂实验单 seed，非统计裁决" |
| `experiment_history` | 已跑实验（配置→结果→证据文件） | "armA: 演化后校准 ECE 0.0703 → three_arm_result.json" |
| `recent_actions` | 最近的动作（写了什么/改了什么） | "补 B1 幻觉扫描 + 回归 24/24" |
| `open_questions` | 未决问题（对应 claim ledger 的 inconclusive） | "机制解释缺消融 → 降级 inconclusive" |

## 假设生命周期规则

- `待办`：已登记未实验 → 正文不得提及（或只能作为 future work）；
- `实验中`：实验进行中/已有初步结果未复核 → 正文 hedge；
- `已证实`：证据文件 + 独立重算通过 → 可强断言，且 claim ledger 对应条目必须 verified；
- 任何假设状态变更必须在 `experiment_history` 记录触发证据（文件路径）。

## 本任务实例状态（2026-09-07 D2-60快照）

| 字段 | 内容 |
|---|---|
| `state_of_the_art` | L01 pilot三档翻转：exact 63.3%/0.363 → tolerant 86.7%(v1)/0.1297 → adjudicated 100%/0.0037 |
| `hypotheses` | H1 翻转率>5%（配对exact-vs-tolerant，同行配对）[部分已证实]：pilot 36.67% SUPPORT且McNemar p=0.0010显著（11翻转独立judge 11/11判对）；holdout-main 16.67%描述性SUPPORT，5翻转独立judge 5/5判对，但McNemar p=0.0625 ns→配对显著性hedge；cloud-new 8.33%描述性SUPPORT，5翻转独立judge 4/5判对（1误判O vs O2），McNemar p=0.0625 ns→hedge；local-new 8.33%描述性SUPPORT（同题跨模型复现），5翻转在会话5/5判对，p=0.0625 ns→hedge；local-en 0%（边界条件，H1不成立）；local-big 2.5%描述性未达（p=0.125 ns）；H1b 功效池配对方向[已证实]：预指定qwen2:7b合并220行（n≥217）b=9/c=0/p=0.0039显著，但描述性0.0409未达，两读数并报；H1c 数学 family[已证伪边界]：云端40题零翻转，现象具题型依赖；N=410七层（预注册120由前三层兑现，其余为注册后扩展；pool复用local-new行系预指定视图）；H2 守卫可复现裁决[已证实]：v3.1一规则120行仅改1行零回归，守卫输出=裁决标签集合；H3 温度缩放改善ECE[已证伪]：NLL降但ECE升，属负结果；H4 等渗回归改善held-out ECE[已证伪]：样本内微降但CV升（含过拟合），属负结果 |
| `key_knowledge` | verify_labels.py内嵌tolerant为旧子集（60行仅检出10翻转），v3+R3权威检出16翻转；云端异源独立judge（qwen2.5:7b temp0）16/16+4/5与在会话裁决一致；tolerant子串规则对短化学式过匹配（O vs O2）已被v3.1守卫修复；local-new独立judge尝试失败（qwen3:4b单字指令不服从，输出弃置），该层为单评；先验层等频分箱、live层等宽分箱（皆10-bin，数字不变）；消融归因：同义7/数值容差4/单位后缀3/子串1/否定前缀1 |
| `reflection` | 跨模型/跨题池化McNemar无效，仅做分层描述；两组巧合（19/30与48/60+53/60）不作合并推断；三层n_ceil=217欠功效，结论hedge；qwen3:4b两次失格（采集思考空回、裁决指令复述），同代小模型当作者与judge皆不可靠，qwen2:7b格式服从可作采集层 |
| `experiment_history` | d2_60快照（30 pilot deepseek-v4-flash + 30 holdout-main qwen2.5:7b）→ analysis_d2.py → results/{exact,tolerant,flips,analysis}.json；云端新层60条live（qwen2.5:7b temp0）→ scripts/analyze_new60.py → results/cloud_new.json + 120行合并analysis_120.json；独立judge→ evidence/cloud_judge_16.json + cloud_judge_new60.json；消融→ results/ablation.json；goal-R2守卫→ scripts/label_match_v31.py → results/guard_v31.json（120行改1行零回归）；温度缩放→ scripts/tempscale.py → results/tempscale.json（NLL降/ECE升负结果）；等渗→ scripts/isotonic.py → results/isotonic.json（CV负结果）；goal-R3本地新层（qwen2:7b同60题，qwen3:4b首采失败弃置）→ scripts/local_new60.py + analyze_local60.py → evidence/local_new60_raw.json + results/{local_new,flips_local60,180行合并analysis_180,power_local60}.json；在会话裁决→ evidence/local_adjudication.json（5/5）；goal-R4大题池（160题gold可复算，英文池30）→ scripts/make_bigpool.py → evidence/qa_pool_{big,en}.json → scripts/collect_pool.py → evidence/local_{big,en}_raw.json → scripts/analyze_big_en.py → results/{local_big,local_en,combined_qwen2}.json + power_big160.json；在会话裁决→ evidence/big_adjudication.json（4/4）；goal-R7云端数学40题（第二题型家族，零翻转）→ scripts/cloud_math40.py → evidence/cloud_math40_raw.json → scripts/analyze_math40.py → results/{math40,410行合并analysis_410}.json |
| `recent_actions` | 8分攻坚：云端独立重裁16/16+新层60条+N=120合并+消融；ledger补C13-C18（18 PASS/0 FAIL）；main.tex三层重写+ vigor硬件声明；适配gates_config真实门（9/9 PASS）；Phase 3六扫全绿；goal-R1：O2双模型UNSTABLE（R2 3.5/6.5/6.0/9.5）+C2 tectonic PDF；goal-R2：守卫v3.1+温度缩放（C19/C20）+对称O2（R1-strict 6.7 vs R2-sym 7.2，Si达8）；goal-R3：等渗CV负结果（C21）+第四层local-new跨模型复现（C22/C23）+对称O2三轮5.9（UNSTABLE）；goal-R4：英文零翻转边界（C24）+功效扩展160（C25）+220功效池p=0.0039（C26）+big裁决4/4（C27）+云端14/14复现（C28/C29）；goal-R7：数学零翻转第二家族（C30），手稿七层N=410同步，第五次O2执行中 |
| `open_questions` | 双模型O2分歧（N/S/Si）：四轮独立侧5.8/7.2/5.9作废/8.8，N 7.5为新高但未达线；数学家族+410七层后第五次重评执行中；S仍缺judge金集（人工） |
| `gold_retest_R8` | GOLD-25解盲25/25（Wilson 95% CI 0.8668–1.0；有题干14/14，无题干11/11；覆盖四翻转层；翻转富集stub非随机抽样，只界定翻转层overturn质量）；云端retest同60题guarded一致1.0、翻转集合5/5重合、漂移0.0107（McNemar退化披露）；手稿Methods/Results/Discussion/Abstract/附录六处同步；S单评局限部分关闭（extension翻转行得独立第二评分）；第六次O2待执行 |
| `R19_REVIEW_R4_O2` | REVIEW_R4收敛（R4-R1 C0/M5/m11/n1，去重4唯一Major全FIX：hetero-ECE改指/E2摘要G06单分歧/E4 no-consistent-repair/C58订正55-55＋8 Minor文字级；R4-R2七角色acceptable零新问题；R8主审表/TikZ逐格语义核验）；O2-r10：R1 8.0/9.5/9.0/9.5=8.9 vs R2 deepseek-r1 8.5×4=8.5（理由泛化），精确一致0/4、\|Δ\|=0.4，两模型未经校准→UNSTABLE-adjacent；8分线双侧全过（R8后第二次，noisy pass）；账本59条（C59）；manifest 329/0/0；验收门9/9 |
| `R26_EXTERNAL` | 预注册外部验证（PREREG_R26_EXTERNAL，种子 20260908 冻结）：TriviaQA-RC + EntityQuestions 各 200 题，qwen2:7b temp0 作答，exact/guard33 对 alias 集打分，翻转逐条裁决（over-fire）+ guard 拒抽 60/集判 miss；seal（scripts/seal_R26.py → results/r26_seal.json）entity exact 25/guard 57/miss 0/60（Wilson [0.0,0.0602]）/over-fire 2；trivia exact 95/guard 123/miss 2/60（[0.0092,0.1136]）/over-fire 3；v3.4 候选合 miss 降 2、over-fire 增量 0 → 未达采用门（miss≥5）→ **负结果不切版**；adjudication 复审（R26_ADJUDICATION_REVIEW.md）单处纠错 over-fire 4→5；账本 C69/C70/C71 verified；纸面 R6：Methods 增 External validation 段 + Limitations 增公开集局限两句 + writing_session 溯源；manifest 411 条目 ruleset、gates 10/10、compile PASS；投稿包未重建（结论先行） |
| `R27_P1_THEORY` | 补强 P1 理论化（MISSION_R27_29，目标双侧 8）：main.tex 新增 Measurement-error formalization 小节——matcher 形式化为二值算子 e/t（flip=e=0∧t=1，t=R 析取），翻转=答案变体空间×R类型覆盖两独立因子；三可证伪预测 (i) 退化变体→零翻转（math 0/40）、(ii) 覆盖缺失→零翻转（前瞻留 R28 检验）、(iii) 覆盖变体→正翻转且归因随规则覆盖（消融 7/4/3/1/1 + 中文层至 43.3%）；post-hoc 如实披露（predictive framework 非 pre-registered hypothesis）；账本 C72 verified；无新实验纯理论层 |
| `R28_CROSSDOMAIN` | 补强 P2 跨域（PREREG_R28_CROSSDOMAIN，先于作答冻结）：本地 qwen2:7b 两臂——Arm A 数学 40 题 flip 1/40（r28-a-08「125.0」vs「125」numeric .0 尾缀，over-fire 0，预测 i 精化为「近零翻转」）；Arm B 英文单位 40 题 flip 0、miss 21/40=0.525（Wilson [0.375,0.6706]）、correct_reject 1（b-38 骰子点数）；预测 ii 成立（flip=0 且 miss>0＝变体存在＋覆盖缺失证据）；账本 C73/C74 verified；main.tex 增 Cross-domain extension 小节 + 精化预测 i/ii 对照；无云依赖纯本地 |
| `R29_POWER` | 补强 P3 功效复测（PREREG_R29_POWER）：local-big 160→720（topup 560 题：computed 420 算术 + hand 140 首都，div 39 全整除，gold 可复算）；合并 720 行 flip 19/720=0.0264、McNemar b19/c0/p=3.81e-06 显著（H1 维持不降级）；裁决 14 flip_correct（.0 尾随 + 地名市/城/特区变体 + 置信度尾）+ 5 over_fire（整除除法模型算错、误差<0.5% 被 numeric 容差误接受，新 over-fire 类）；n=720 达 n_ceil 欠功效消除；账本 C75 verified；main.tex Limitations/Future work 更新 + over-fire 新类记录；无云依赖纯本地 |
| `R30_O2` | 补强 P4 O2 重评（R30）：R1=qwen2.5:7b（替代不可用 muse-spark，已披露）N9.5/S9/Si8.5/C8 加权 8.925；R2=deepseek-r1:7b N7/S9/Si7/C8.5 加权 7.85；S 双侧 9、C 双侧达标、N/Si 双侧未达（R2 harsh 侧 N7「无定理」、Si7「Holm 失败」）；重封投稿包未完成（本机无 LaTeX）；三块补强全部 sealed（C72-C75 verified）、门禁 10/10 |
| `R31_THEOREM` | 补强 P5 定理（用户决策：补定理＋公开数据集第二题型）：Measurement-error 小节新增 Theorem 1（规则追加单调性：纯析取追加⇒接受/翻转单调不减、miss 单调不增；v3.3→v3.4 在 400/400 R26 行零违反、增量 2；guard 追加修订显式排除适用域，8/1700 接受→拒绝全单字 CJK）＋ Theorem 2（数值容差 over-fire 边界：错值相对误差落 (0,0.005)⇒数值分支接受；5/5 R29 行重算在内）；seal_theorems.py 唯一重算；账本 C76/C77 verified；门禁 10/10，manifest 461 |
| `R30_BOOLQ` | 补强 P6 公开是非臂（PREREG_R30_BOOLQ 冻结在先）：SuperGLUE BoolQ dev 分层 50/50（种子 20260912），qwen2:7b temp0 中文指令，gold True→是／False→否；exact 0／guard 55／flip 55（全对、over-fire 0）；拒 45 普查：miss 31（Yes./No. 句点变体）＋正确拒 14；flip 率 0.55，miss 率 0.6889（Wilson [0.5434,0.8047]）；单数据集内覆盖翻转／未覆盖 miss 判别成立；描述性、不入 Holm；账本 C78 verified；正文增 Public yes/no arm 小节；门禁 10/10，manifest 480 |
| `R31_HETEROJ2` | hetero 第二独立 judge（PREREG_R31_HETEROJUDGE 冻结在先＋Amendment A1 行集修正）：第三家族 deepseek-r1:7b 重判同一 11 行，一裁 prompt 逐字复用、think 允许；与一裁一致 8/11（分歧 gr18-42/56，ERROR gr18-09）、与作者封存结论一致 8/11；已排除行分歧 1/3 不触发 Limitations；封存不推翻、跨家族可靠性证据；账本 C79 verified；正文 hetero 段落补句；门禁 10/10，manifest 492 |
| `R31_CLOSE` | 收官：O2-R14 双侧四维全过 8（N 9.5/9.5、S 9.5/9.5、Si 9/9、C 9/8.5，最大分差 0.5）；R31 包重封（XeTeX 三遍零错误，r31 zip 334 文件、匿名 0 命中；上传未执行）；账本 81 条目校验全过（78 active verified＋C33/C45 superseded 历史＋C08 inconclusive 出口，0 FAIL）；门禁 10/10，manifest 499 |
| `R32_REVIEWFIX` | 外部审阅 M1–M7＋minors 全修（零新实验）：口径统一（78 active＋2 sup＋1 inc＝81 条目；C81 立账后更新）、定理改 instrument lemmas＋shallow 注记、BoolQ exact-zero hedge、core 上传包 325 文件 9.0MB（原语料 SHASUMS＋SOURCE.md 替代，构建 exhaust 排除）、manifest 对账零缺口（507/325）、keywords＋清单全文＋上传指定、分数禁引确认；账本 C81 verified（81 条目校验全过）；门禁 10/10，manifest 507 |
| `R32_A2_GEMMA` | BoolQ 第二模型臂（PREREG_R30_BOOLQ Amendment A2 冻结在先，主臂封存后追加）：同 100 冻结行／同中文指令／同 True→是・False→否 映射，换 gemma3:4b temp0 重采重打分；exact 0/99、guard 45、flip 45（Yes→是 21＋No→否 24，全内容正确、over-fire 0）；拒 54 普查：miss 39＋正确拒 15（无裸 1/1.0）；flip 率 0.4545、miss 率 0.7222（Wilson [0.5911,0.8238]）；1 行 boolq-1159 采集超时如实披露、不进分母；方向在第二模型族复现、量级低于主臂（45 vs 55）；不入 Holm、无功效/配对主张、不改写 C78；账本 C82 verified；正文 BoolQ 小节增 Second model family (Amendment A2) 段 |
| `R32_CLOSE` | 终封收官：main.tex 三遍 XeTeX 重编零错误零未定义引用（20 页），BoolQ 第二模型段已渲染进 PDF（pdftotext 验）；core 包重封 339 文件 5.5MB（0 重复）；R32 抓出并修正两处真实缺陷——包内遗留应排除的 `data_boolq/BoolQ.zip`（4.1MB）已剔除、正文 110 行引用的 `evidence/hakim_song_2609.01671.pdf` 缺失已补齐；补入 C82 证据 12 项＋PREREG_R32；对账 531 vs 338、缺口分类逐项命名（含 blind-material 2 与 audit-scan-report 5 显式不给）、未解释 0；匿名 0 命中；账本 82 条目校验 82 PASS / 0 FAIL；四扫报告仅过程（历轮同，不入包）；上传未执行（保护层） |

## 时机

- Phase 1（claim ledger 登记）时初始化快照；
- 每次 Phase 2 起草/Phase 4 修改轮后更新（与 ledger 同批）；
- Phase 3 机器检查把 `open_questions` 与 claim ledger 的 inconclusive 条目对账；
- Phase 5 交付前：快照 `hypotheses[PROVEN]` ↔ ledger `verified` ↔ 正文强断言三处一致。
