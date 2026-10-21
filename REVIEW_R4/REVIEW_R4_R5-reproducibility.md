# REVIEW_R4_R5-reproducibility.md — R4 Round 1 (fanned, independent JSON)

- verdict: minor-revision
- prevClosure: R3基线保持；仅审查R18新增及独立重算。
- summary: R18四新脚本齐全可重跑（seal_merged_hetero/guard_synth/dispose_n157/decode_gold100需按docstring传参；seal_holm/recompute_ece_unified复现封存值）；独立重算通过（merged 1062/830/922/92；hetero 29/60=0.4833；三组Wilson；b=24口径p=2/2^24）；digest/seed未钉、去重门、judge未校准、欠功效、CJK未补丁均已披露。1 Major（真发现）。

## Issues
- [Major] R4-R5-01 GOLD-100“58/58确认翻转”分母错误 @摘要与结果段：包构成55确认＋7排除=62翻转项，一致58/62；4分歧皆vindicated排除，另3一致（H34/H47/H85）亦排除项。“58/58 confirmed”把3排除误划入confirmed，真值55/55（62-4=58=55确认＋3排除一致，与key 55/7一致）。→ 回应：FIX，E3/E11＋C58订正（55/55＋3排除一致具名）＋C59记录。独立验算：verify_r4_response.py gold100-confirmed-55断言。

## Raw reviewer JSON
（severityCounts本角色 Major 1。）
