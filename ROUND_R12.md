# ROUND_R12 — 第九次O2（R11后重评，2026-09-07）

## O2（R1-strict-r9 8.8 vs R2-r9 5.75，UNSTABLE九连）
- R1（`evidence/rater1_r9.json`，盲写）：8.0/9.5/8.5/9.5。Si 9.0→8.5是本轮唯一诚实下调
  （Holm家族控制下只剩两层）；C 9.0→9.5（摘要/术语/口径/公式/图/代码声明）。
- R2（本地deepseek-r1:7b temp0，`evidence/rater2_r9_prompt.txt`→raw log＋json）：
  5/6/7/4，加权5.75。理由多为"压缩prompt没展开"（first report细节、guard演示、
  单脚本、异质机制——全在正文，不在330词摘要里），属prompt压缩伪影；
  C项"技术性太强"与R8"C完整"直接矛盾（同一稿），确认rater噪声主导。
- 九轮R2序列 5.8/7.2/作废/8.8/5.35/8.6/7.65/8.95/5.75：方差±3.2，O2 stops being informative；
  建议后续改投：影子rater只记异议点，不再计分（计分制对该rater已失效）。
- 8分线：R1侧四维全≥8守住；R2侧本轮未过。Phase 5封存状态不动（R8已封存；
  R11改动已进zip的是tex，PDF仍OPEN）。

## 验证
- 账本45/0（本轮未新增主张条目，无需C46）；门禁待重跑；manifest待重建。
