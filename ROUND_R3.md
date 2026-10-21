# ROUND_R3 — goal第二轮：Si修复证据+对称O2（2026-09-07）

## 新证据（本轮唯一新增声明来源）

1. v3.1子串守卫（scripts/label_match_v31.py → results/guard_v31.json，C19）：
   120行仅改1行（cloud-new-42 O/O2拒绝），pilot-03与cloud-new-48零回归；
   守卫输出集合=裁决标签集合（cloud-new 52/60=0.8667，4翻转0.0667 p=0.125 ns）；
   裁决ECE 0.1692照实报（raw 0.0492被误接受美化，属诚实上调）。
2. 温度缩放对照（scripts/tempscale.py → results/tempscale.json，C20）：
   T*=0.207/6.3983/1.7756，NLL全降但ECE未改善（0.205→0.2805，0.1692→0.2272），负结果照实。
3. 手稿同步：Methods（守卫规则+温度设计）、Results（守卫段+温度段）、
   Discussion（守卫Future→Done、温度ECE-fix不许可）、Abstract（最后重写对齐）、
   Contributions（v）、Appendix指针；STATE_SNAPSHOT（H2证实/H3证伪）同步。

## 对称O2（同严格prompt，互盲，含新证据）

- R1-strict：5.0 / 7.0 / 7.5 / 8.5（加权6.7；锚定风险已披露）。
- R2-sym：5.5 / 7.5 / 8.0 / 9.5（加权7.2；原输出evidence/rater2_sym_raw.log，干净版rater2_sym.json；理由中功效数字误记已披露）。
- 精确一致 0/4 → UNSTABLE（主规则）；|Δ总分| 0.5、各维 ≤ 1.0（较上轮2.2大幅收敛）。
- R2 轮间：5.8→7.2（N+2/S+1/Si+2），Si达8.0。8分线（双模型各维≥8）：N✗/S✗/Si半✓/C✓，未达成。

## 门禁（本轮终态）

- ledger 20/0/1 WARN（C08既有）；gates 9/9；manifest见终检；numbers exit0（0.8/0.80既有格式注记，
  不同量纲）；stats/style/taint/hallucination全绿；TMLR全PASS；C1-C7全PASS；
  PDF已重编（0 error）；provenance已记。
- compile静态4E仍为模板宏误报（权威实编0 error），不动模板。

## 下轮（缺口按成本排序）

1. 等渗回归对照（纯本地，可自主）：补齐Si最后一半（R1-strict 7.5→8）。
2. pilot补至50或judge金集≥20（需用户：模型/人工grading）。
3. N跨题型复现或理论化（大工作，单独立项）。
