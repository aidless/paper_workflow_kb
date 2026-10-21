# REVIEW_R4_summary.md — R4 Round 1（R18大改后首轮全员重审）

- 范围：R18新增（hetero第15层、C58 GOLD-100、C56 n=157、C55探针、C52/C53统一口径）；旧内容沿R3收敛基线，不重复报。
- 方式：7角色workflow独立扇出（JSON-only、反偏置自检）＋R8主审执行（R8降级：scan_figure_claims＋逐格语义核验）。
- 计数：Critical 0 / Major 5（去重后4唯一：hetero-ECE指针×4角色同源、58/58分母、摘要lr18-42×2角色同源、摘要fail-to-repair）/ Minor 11 / Nit 1。failedRoles无。
- verdicts：acceptable×1（novelty）/ minor-revision×4 / needs-major-revision×2（writing、ethics，均为摘要文字问题）。
- 双轴核验（B2）：numbers轴 scripts/verify_r4_response.py 14断言全过；fidelity轴逐条对证据原文——R4-R3-01“两处”半误（仅L230一处），R4-R1-03注记typo附带查出hr18→gr18（计算无辜，纯字符串）。
- 回应：4唯一Major＋8 Minor/Nit全FIX（正文E1-E14、guard_synth G1-G3＋重跑数字全同、C58订正55/55＋C59）；无数值改动、无新实验、无rebuttal（Critical/Major只许fix/evidence）。
- 回归：六扫（ledger/taint/hallu/stats/style/tmlr）＋验收门9/9 PASS；manifest重建312/0/0。numbers --fail-on-stale exit 1系19个跨层近似数over-match（与R18同类，无一来自R19新数字，门配置report-only项PASS）；compile FAIL系TeX缺席＋4未定义引用/5孤儿标签（正文仅2个\ref且皆有label，我改动零\ref/\label，前存非新引）。
- 收敛状态：本轮为defect-dense首轮（C+M=5），按成本自适应规则再审保持8角色（7扇出＋R8主审），见ROUND_R19。
