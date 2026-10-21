# ROUND_R15 —— 对抗审稿R1-R8去重清单全修（2026-09-08，用户"需要"开轮）

## 审稿输入
- REVIEW_R1/ R1-R8独立报告：2 Critical（R1-01 H1检验错位、R4-01 novelty vs L01）+ 30 Major（去重后主攻10项）。
- 本轮前置核验（全部一手证据，非模型自省）：
  - G06参照系：gold_key.json G06 trace=cloud-new-42；guard_v31.json单改动=cloud-new-42；flips_new60.json含42（5 raw flips全入stem）；grades用户判对 → 预注册"全25 guarded正确"假设确假。R5-01/R7-01成立。
  - L01：LITERATURE_REVIEW.md L01三档值=同一pilot（exact 63.3/0.363→裁决100/0.0037）。R4-01成立。
  - 2609.01671：arXiv API实查（标题/作者/摘要），scout数字吻合，可引。
  - n_ceil：power_update_120/local60/big160全用观测discordant rate（0.3667/0.1667/0.0833/0.025）→ 事后无疑。R1-07成立。
  - tempscale口径：analyze_new60.py系等宽分箱，tempscale系等频，但cloud-new T=1两边同为0.1692 → 数值巧合，无数字错配。R1-05b以"evidence"回应（加注），不改数。
  - N=942十三层直加验算无重叠（30+30+60+60+30+160+40+60+60+20+78+157+157=942）；重叠仅存在于rollup解释层。R2-03以披露回应。

## 修改（tex 42处＋bib 1条＋新证据1份；数字仅GOLD一项更正，其余措辞层）
1. **H1方向化（R1-01）**：H1改为配对非对称命题（McNemar适用的方向检验）；5%降为G006描述性bar；全文14处"supports H1 descriptively"机械改写（assert计数：2处2x、余1x）。
2. **GOLD 24/25（R5-01/R7-01）**：新证据results/gold_guarded_agreement.json（scripts/recompute_gold_guarded.py，assert：唯一分歧=G06、24/25、stem13/14）；摘要/方法/结果/讨论/license五处24/25 [0.805,0.993]；67→67 of 68 judged rows（2处）。
3. **摘要Holm限定（R1-06/R2-01/R6-01）**：五显著句后加"Holm下存活2层（pilot、xloose），余三层局部观测显著"。
4. **功效诚实化（R1-07）**：n_ceil标注post-hoc敏感性；pool"唯一预注册功效推断"降级为"仅组成预指定＋Holm出局＋局部观测显著"（方法/结果/license三处）。
5. **pilot50去p（R1-08）**：rollup删p值保留b/c＋cross-model描述性标注；holdout108与PowLocalNew单臂显著措辞调平（R2-02）；rollup重叠披露（R2-03）。
6. **ECE口径（R1-05/R3-01）**：不重分箱（sealed证据哈希不动，within-stratum比较口径自洽，无跨层ECE声称）；表注加分箱对照句；guard targeting未测披露；tempscale巧合注。
7. **RW（R4-01/02/03）**：hakim2026ranked入bib＋动机段；L01 delta段（同一pilot＋四点delta）；scout协议指针。
8. **可复现披露（R5-02/05）**：模型digest/seed未pin＋pilot采集脚本失传（d2_60逐行provenance保留）入Future work前段；公开仓库仍on-request（R5-04 evidence回应：无法凭空mint）。
9. **Guard/knob降级（R1-02/R3-03/06）**：guard加in-sample（2处）；"control knob"→"regime contrast"（2处）；Broader Impact支点随G06披露同步修正。
10. **写作零碎（R6）**："alone"删；附录指针加gold_guarded＋账本C09--C48。

## 验证（已跑，2026-09-08）
- stats exit 0（p全对；McNemar/比例复算一致）；ledger **48 PASS / 0 FAIL / 1 WARN**（C46精度修到0.80456过TOL=2e-5；WARN系旧C08 inconclusive）；style 0 findings；taint clean（48 claims）；hallucination 0 cite errors（hakim key可解）0 missing method files；number exit 0 stale 0；tmlr **0 FAIL**（G7由WARN→PASS，78词；G9 PASS）。
- compile gate FAIL = 旧静态解析器噪声（\pairbar的#1-#4误报4条＋sec:标签零引用5条；\ref/\cite真实键全解），R15未动图与label，原样记录。
- manifest重建243条 → **--verify 243 PASS / 0 FAIL**；门禁 **9/9 PASS**（config_sha256=b3e66a165457…），已record（log写入后重建＋重记）。
- PDF未重编（本机无TeX；改动无新宏包，\cite1增＋文本句，编译风险低，用户侧latexmk）。

## 未收敛项（诚实）
- R2微调轮仍需跑（新Critical/Major是否引入）。
- Phase 5前：文献新鲜度重跑（LITERATURE_REVIEW 2026-09-07，~10-07过期）、投稿zip重打。
