# REVIEW_R4_R1-methodology.md — R4 Round 1 (fanned, independent JSON; archived verbatim below)

- verdict: minor-revision
- prevClosure: R3 convergence holds for old content; only R18-new content reviewed.
- summary: R18新增五项全部独立重算通过（hetero raw 21/32、11翻转、裁决29/60、8翻转、ECE 0.5143/0.381；merged 830/922/92、N=1062分层加总闭合；GOLD-100 86/100与88/100及Wilson区间吻合；guard合成与n=157数值吻合）；嵌套构造经代码核对成立（exact接受蕴含guarded接受，退化空行为唯一例外，v3.2已闭合），hetero单轮裁决与异家族设计有效，judge文件干净。1 Major＋3 Minor，均为文字/指针级。

## Issues
- [Major] R4-R1-01 hetero ECE证据指针失实 @表注＋Methods：ece_unified.json仅14层无hetero，数字为真（同函数独立重算一致）。期望：改指r18_heteromodel.json/adjudication或纳入统一重算；C52十四层表述澄清。证据：ece_unified.json strata键；r18_heteromodel.json ece10_exact 0.5143；adjudication adjudicated_ece_equalwidth 0.381；seal_heteromodel.py同函数。→ 回应：FIX，E6/E7/E7b/E14（repoint方案；同函数经grep确证seal_heteromodel.py L15与recompute_ece_unified.py同引analyze_xdomain.ece_equal_width）。
- [Minor] R4-R1-02 hetero行ECE混口径未注 @主表：exact列raw、guarded列adjudicated，表注仅标翻转。期望：与R18行标注对齐。→ 回应：FIX，E7（caption加exact-raw/guarded-adjudicated注）。
- [Minor] R4-R1-03 guard_synth R_excluded注记措辞 @R_excluded.note：lr18-54/55定性accepted-but-wrong夸大确定性（作者注记判对）。期望：中性表述，规则不变。→ 回应：FIX，G3（accepted-but-excluded＋作者注记；重跑数字全同）。
- [Minor] R4-R1-04 headline嵌套无保留 @摘要L53/引言L64 vs L119/L249有限定。期望：补on non-degenerate rows限定。→ 回应：FIX，E1/E5。

## Raw reviewer JSON
（主审归档：severityCounts本角色 Major 1 / Minor 3；verdict minor-revision；anti-bias自检通过。）
