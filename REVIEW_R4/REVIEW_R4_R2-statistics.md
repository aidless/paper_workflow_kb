# REVIEW_R4_R2-statistics.md — R4 Round 1 (fanned, independent JSON)

- verdict: minor-revision
- prevClosure: R3基线保持；仅审查R18新增。
- summary: Table 1十五层accuracy/flips/b/c与源文件一致（hetero 21/60=0.35→29/60=0.4833、8/60=0.1333；R18 15/60=0.25→39/60=0.65、24/60=0.40；merged 830/922/92 of 1062；99/106=16+4+5+4+21+10+7+24+8）；14层统一ECE一致；Wilson三组（86/100→[0.7786,0.9147]、88/100→[0.8019,0.93]、24/25→[0.8046,0.9929]）一致；Holm v2（m=18、幸存r18→xloose→pilot、第4步止于pool p=0.00390625＞0.0033333）一致，R18用裁决口径b=24属保守；raw/guarded/adjudicated双数完整。2 Minor。

## Issues
- [Minor] R4-R2-01 hetero ECE来源标注（同R4-R1-01）。→ 回应：FIX，E6/E7/E7b/E14（同上，一处修复关闭四角色同源问题）。
- [Minor] R4-R2-02 Multiplicity未具名hetero不入族 @Multiplicity段：hetero b=8算术p=0.0078，入族亦不改幸存集与停止步，仅族构成披露缺口。期望：加一句具名排除。证据：holm.json 18项无hetero；C54。→ 回应：FIX，E12。

## Raw reviewer JSON
（severityCounts本角色 Minor 2；anti-bias自检通过。）
