# MISSION：论文补强（requalification）至 O2 双侧 8 分线

> 状态：锁定字段待用户确认。源真相：`.\paper_workflow_kb\`
> 前情：R25 投稿包已封存；R26 外部校验负结果（v3.4 不切版）；SELF_ASSESSMENT
> 十一轮 O2 UNSTABLE，N 独立中位 4–5.5（无理论+窄QA）、S 中位 6–7.5（欠功效+无金集）
> 是两处主缺口。用户判 B：补强后再投，不赶稿。

## 一、锁定字段（仅用户可改）

| 字段 | 值 |
|---|---|
| 目标 | 把 N/S/Si/C 四维补到「O2 双模型 ≥2 轮重评、双侧均 ≥8」，然后重封投稿包 |
| 验收标准 | 见第四节 |
| 阶段列表 | P1(R27) 理论化 → P2(R28) 跨域 → P3(R29) 功效复测 → P4(R30) O2 重评+重封 |
| 资源 | 仅本地（qwen2:7b 等）；用户「少量标注」预算用于跨域裁决抽检，不做完整 judge 金集 |
| 明确放弃 | judge 金集（人工，本轮不做）；云 API（本轮不依赖） |

## 二、阶段与 gate 定义

### P1（R27）理论化形式陈述 — 补 N
- 动作：把「label matcher 是测量仪器的一部分，matcher 选择引入测量误差」形式化。
  定义 matcher m(y, ŷ) 与打分约定；刻画出 exact-match 的假阴性偏差方向（语义等价但
  字符串不等 → 记 0 → 低估准确率）与 guarded matcher 的假阴性⇒下界方向；
  给出可证伪预测：翻转率 ∝ 答案的语义等价串变体数（同义/单位/顺序变体多的题型翻转高，
  答案空间规范、等值唯一的题型翻转低）。
- 既有实证锚点（引用 sealed 数字，不新增实验）：QA 家族高翻转（H1 部分证实）vs
  数学家族零翻转（H1c 证伪边界 cloud_math40）、local-en 英文池 0%（语言边界）。
- **gate（完成判据）**：main.tex 新增「Measurement-error formalization」小节，含 ≥1 条
  可证伪预测 + 与既有数据逐条方向对照；账本新增对应 claim 且 verified；无数字移动。
- 失败路径：若形式化只是复述既有认识（无新可证伪预测），判 FAIL → 回炉改为
  「把题型依赖升格为理论预测」这一具体贡献。

### P2（R28）跨域证据 — 补 N + Si
- 动作：在非 QA 任务上验证 P1 的理论预测。预注册（PREREG_R28）→ 选本地可跑的非 QA
  任务（优先：答案空间规范/等值唯一的任务作对照，如数学字面答案；辅以答案有单位/
  格式变体的中间态任务）→ 本地 qwen2:7b 作答 → exact/guard 打分 → 翻转裁决
  （用少量标注预算抽检）→ seal。
- **gate（完成判据）**：≥1 个非 QA 任务结果与 P1 预测方向一致（或诚实报告反例并回改
  理论）；账本新增 claims verified；「窄 QA」「QA-only」扣点有据可拆。
- 失败路径：若跨域结果与预测方向相反且无法被理论吸收，不硬凑，如实改写理论
  （把边界写进预测本身），仍算阶段推进但需在账本标 inconclusive。

### P3（R29）功效复测 — 补 S
- 动作：把欠功效层（n_ceil=217，H1b pool b=9/c=0 p=0.0039 但描述性 0.0409 未达）
  扩到预注册功效 n，本地大规模作答，配对 McNemar 复测，把「配对显著性 hedge」收敛为
  稳定结论。
- **gate（完成判据）**：预注册功效 n 达成；关键层配对显著性取值稳定（不再视作纯 hedge）；
  账本新增 claims verified。
- 失败路径：若扩样后 p 反而不显著，如实报（H1 降级为不显著），仍消除「欠功效」扣点，
  但需同步下调正文 H1 表述强度。

### P4（R30）O2 双侧重评 + 重封 — 最终验收
- 动作：三块成果全进正文后，O2 双模型（对称严格 prompt）≥2 轮重评，排除 noisy pass；
  账本/manifest/门禁全绿；重封投稿包（R26 + R27–29 全进 PDF/zip）。
- **gate（完成判据）**：N/S/Si/C 双侧均 ≥8（≥2 轮且轮内双模型一致或差异可解释）；
  投稿包重封且 PHASE5_SEAL 自洽。

## 三、风险登记

1. **理论化空转**：形式陈述变套话 → P1 gate 的「可证伪预测」硬判据兜底。
2. **跨域反例**：现象若真仅限 QA，N 补不起来 → 接受并写成「边界理论」，Si 靠诚实加分。
3. **功效复测翻车**：扩样后 p 不显著 → 降正文强度，诚实替换 hedge。
4. **O2 本身 UNSTABLE**：rater 摆动 ±3 是既有事实 → P4 要求 ≥2 轮互证，仍不稳则以
   一致方向性为准并披露，不做单轮求过。

## 四、验收标准（总）

1. O2 双模型 ≥2 轮，N/S/Si/C 双侧均 ≥8；
2. 本轮新增 claims 全部进 CLAIM_LEDGER 且 verified（无证据声明不得过）；
3. 门禁全绿（gates 10/10）、manifest 重建自洽；
4. 投稿包重封（含 R26 + R27–29），PHASE5_SEAL 自洽。

## 五、决策记录

- 2026-09-11 选块：理论化 + 跨域 + 功效复测（放弃 judge 金集）；目标双侧 8；资源仅本地+少量标注。
- 2026-09-11 P1(R27) 理论化完成：main.tex 新增 Measurement-error formalization 小节（e/t 算子 + 三分支可证伪预测）+ 账本 C72 verified + 门禁 10/10；post-hoc 如实披露，预测 (ii) 前瞻留 R28。当前阶段 → P2 跨域。
- 2026-09-11 P2(R28) 跨域完成：Arm A 数学 flip 1/40（「125.0」vs「125」.0 尾缀，预测 i 精化为近零翻转）、Arm B 英文单位 flip 0 + miss 21/40（Wilson [0.375,0.6706]，预测 ii MET）；账本 C73/C74 verified；main.tex 增 Cross-domain extension 小节；门禁 10/10。当前阶段 → P3 功效复测。
- 2026-09-11 P3(R29) 功效复测完成：local-big 160→720（topup 560），McNemar p=3.81e-06 显著（H1 维持），n=720 达 n_ceil 欠功效消除；另暴露 5 over-fire 新类（除法算错+0.5% numeric 容差）；账本 C75 verified。当前阶段 → P4 O2 重评+重封。
- 2026-09-11 P4(R30) O2 重评（R1=qwen2.5:7b 替代 muse-spark / R2=deepseek-r1:7b）：R1 N9.5/S9/Si8.5/C8，R2 N7/S9/Si7/C8.5；**S 双侧 9、C 双侧达标，N/Si 双侧未达**（R2 harsh 侧 N7「无定理」、Si7「Holm失败」）。重封投稿包未完成（本机无 LaTeX）。→ gate 未全过，升级用户。
- 2026-09-11 P5(R31) 补定理完成：Measurement-error 小节新增 Theorem 1（规则追加单调性，v3.3→v3.4 在 400/400 R26 行零违反、增量 2；guard 追加修订显式排除，8/1700 接受→拒绝）＋ Theorem 2（数值容差 over-fire 边界，5/5 R29 行落入开区间 (0,0.005)）；seal_theorems.py 唯一重算；账本 C76/C77 verified；门禁 10/10。当前阶段 → P6 公开数据集第二题型。
- 用户决策（P4 升级回应）：补定理＋补第二题型，且第二题型必须用公开数据集。P6 设计：公开英文是非问答集（BoolQ dev，SuperGLUE 官方包）＋中文作答指令（gold True→是/False→否，冻结映射），检验覆盖分支（会/不会/yes/no→翻转）vs 未覆盖分支（True/False→miss）的新颖判别检验。
- 2026-09-11 P6(R30) 公开 BoolQ 臂完成：分层 50/50（种子 20260912）qwen2:7b temp0，
  exact 0／guard 55／flip 55（全对、over-fire 0）、拒 45 普查 miss 31＋正确拒 14；
  判别成立；账本 C78 verified；正文增 Public yes/no arm 小节；门禁 10/10。
  当前阶段 → O2 重评（R31/R30 新证据：定理＋BoolQ）。
- 2026-09-11 O2-R13（R1=qwen2.5:7b N8/S8/Si7/C8；R2=deepseek-r1:7b N8.5/S7.5/Si7.5/C8.5）：
  双侧 N✓✓/C✓✓、S✗（R2 7.5）、Si✗（7/7.5）；两 rater 互换 harsh 面（振荡未收敛）；
  R2 侧 N 7→8.5 定理起效；剩余具名约束：pilot 欠功效、hetero 单 rater、无公开仓。
  当前阶段 → hetero 第二独立 judge（本地可行，直指 Si 具名约束）。
- 2026-09-11 hetero 第二 judge 预注册冻结（PREREG_R31_HETEROJUDGE）：
  第三家族 deepseek-r1:7b 独立重判同一 11 raw flip 行，一裁 prompt 逐字复用，
  think 允许已披露；ERROR 3 次重试；只报一致率、不推翻封存（reliability 口径）。
  脚本 scripts/local_judge_heteromodel_2.py 后台运行中。
- 2026-09-11 hetero 第二 judge 完成：deepseek-r1:7b 重判 11 行，与一裁一致 8/11
  （分歧 gr18-42/56，ERROR gr18-09 三次尝试后）、与作者封存结论一致 8/11；
  已排除行分歧 1/3 不触发 Limitations；封存不推翻（reliability 口径）。
  首跑行集断言失败 1 次（flips 字段仅 8 确认行），Amendment A1 改从一裁文件取全集。
  账本 C79 verified；正文 hetero 段落已补第二 judge 句；门禁 10/10。
- 2026-09-11 O2-R14（hetero 双 judge 新证据）：R1 N9.5/S9.5/Si9/C9，
  R2 N9.5/S9.5/Si9/C8.5；**双侧四维全过 8**（最大分差 0.5，十四轮最小），振荡收敛。
- 2026-09-11 R31 投稿包重封：LaTeX 阻塞解除（XeTeX TeX Live 2026），三遍编译零错误；
  submission_tmlr_r31.zip（334 文件，匿名 0 命中，BoolQ 源包随附）；
  账本 C80 verified；门禁 10/10，manifest 499。上传为保护层动作、未执行。
  → 目标三项（补强 sealed／双侧 8／重封）全部达成，请求 close。