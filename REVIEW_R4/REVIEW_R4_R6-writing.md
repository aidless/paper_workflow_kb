# REVIEW_R4_R6-writing.md — R4 Round 1 (fanned, independent JSON)

- verdict: needs-major-revision
- prevClosure: R3基线为R18前状态；仅审查R18新增并独立重算。
- summary: R18数字独立重算全吻合（N=1062加总、flips 92、830/922；统一ECE六层；R18 0.6425→0.2425；hetero 0.5143→0.381；附录等频；GOLD-100 Wilson；n=157；guard-synth）。2 Major＋1 Minor；其余口径（raw/adjudicated标注、附录审计、hedge）到位。

## Issues
- [Major] R4-R6-01 摘要GOLD-25句把lr18-42列为分歧 @摘要：GOLD-25唯一分歧G06（agree=24，per_item仅G06 disagree），lr18-42不在25项集（R18层/GOLD-100语境）。→ 回应：FIX，E2（删lr18-42，注其归属100项扩展）。
- [Major] R4-R6-02 摘要“fail to repair”绝对化 @摘要 vs C56/正文：PowLocalNew iso-CV held-out ECE 0.0668→0.0277且NLL改善，五个held-out唯一阳性；正文hedge为no consistent repair。→ 回应：FIX，E4（与正文一致＋阳性例外）。
- [Minor] R4-R6-03 摘要“58 of 58”省略分母 @摘要 vs 正文58/62。→ 回应：FIX，E3（55/55＋58/62全口径，与R4-R5-01同修）。

## Raw reviewer JSON
（severityCounts本角色 Major 2 / Minor 1。）
