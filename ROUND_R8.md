# ROUND_R8 — 解盲轮：GOLD-25（25/25）＋retest 手稿同步（2026-09-07）

## 新证据

1. GOLD-25 解盲（C33）：用户独立判定 25/25 全对，一致率 1.0，
   Wilson 95% CI [0.8668, 1.0]；有题干 14/14、无题干 11/11；
   per_item strata 覆盖 local-big 4 / cloud-new 5 / local-new 5 /
   pilot+holdout 11。分支预案走 ≥0.90 强主张支。
   边界：金集为翻转富集（普查＋seeded 翻转抽样），非随机抽样，
   25/25 只界定翻转层 overturn 质量。
2. Retest（C32）：同 60 题同模型同 prompt，exact 字串一致 0.9833（60 对），
   guarded 一致 1.0，翻转集合 5/5 同一集合，McNemar 退化（b=c=0，p=1.0），
   置信平均漂移 0.0107；唯一差异（光速题）翻转状态不变，C16 裁决延续。
3. 手稿同步（本轮）：Methods 裁决段＋Results 新增段＋Discussion 许可/局限＋
   Abstract 一句＋附录指针（C09--C33）；数字全部取自 C32/C33 已覆盖值，
   新增字面量走账本校验（WARN 审计，不增 FAIL）。

## 门禁（终态实测）

- ledger 33 PASS / 0 FAIL / 1 WARN（WARN=C08 inconclusive，既有）；
  gates 9/9；manifest 160 条重建对账；
- numbers 报告 exit 0（新增字面量 0.867 为 CI 舍入，账本容差已对；其余新增
  数字全部账本覆盖）；stats/style/taint/hallu 全绿；TMLR exit 0；
- compile_gate：本机无 TeX，静态降级 FAIL 为既有（新增行零
  \ref/\cite/\label，已验）；既有轮次 PDF 重编 0 error 的结论沿用，
  Phase 5 前须在有 TeX 环境重编确认；
- provenance 已记（含 manifest 哈希订正条目）。

## O2 预告（P3，本轮改稿冻结后）

- 第六次 O2：R1-strict（本模型）＋ R2 新模型（规则不变：异源、失格换备选）。
- 判据：S 是否过 8（gold＋retest 后）；N 独立 7.5 顶预期不变。

## 第六次O2（落定：R1-strict-r6 8.2 vs R2-r6 8.6，UNSTABLE）

- R1-strict-r6：N7.0 / S8.5 / Si9.0 / C9.0（8.225→8.2；S＋0.5、Si＋0.5
  均凭新证据，N/C 无新证据维持）。
- R2-r6：deepseek-r1:7b 本地 temp0，对称严格 prompt
 （`evidence/rater2_r6_prompt.txt`）：N9 / S9 / Si7 / C10（8.6；
  `evidence/rater2_r6_raw.log` 734B 直接 JSON＋`evidence/rater2_r6.json`）。
  理由证据绑定差（“多层显著”失实），同模型相对 R3/R5 大摆动。
- 精确一致 0/4（|Δ|=2.0/0.5/2.0/1.0）→ UNSTABLE；8分线：
  N✗（R1 7.0）/ S✓✓ / Si✗（R2 7）/ C✓✓。**未达成，不封存**。
- 诚实结论：gold＋retest 关闭了 S，但 N 与 Si 各差一票且分属两侧；
  O2 方差本身（同模型 ±3 摆动）使分数不能当结论。下一步需立项包
  （理论化/跨域）， autonomous 部分到此为止。
