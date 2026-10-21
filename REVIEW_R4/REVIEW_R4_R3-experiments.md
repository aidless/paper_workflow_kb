# REVIEW_R4_R3-experiments.md — R4 Round 1 (fanned, independent JSON)

- verdict: minor-revision
- prevClosure: R3已收敛；仅复查R18新增；已披露局限不重复报。
- summary: 五项新增独立重算全吻合（merged 1062/830/922/92；GOLD-100 Wilson到4位小数；Holm排序与停止阈值；guard_synth 12/12、12/12、8/8与R类92/92、7排除=1+1+3+2闭合；n=157两臂T*与ECE/CV-NLL一致、唯一阳性诚实；六类失败模式逐类披露计数闭合；99/106可还原）。无NEW C/M；3 Minor。

## Issues
- [Minor] R4-R3-01 lr18-46计数 @L230与L253：正文两处写three attempts，证据四文件各一ERROR、rollup reads 4个ERROR。→ 回应：FIX，E10；注：经全文grep，“three attempts”仅L230一处，L253无此句——审稿“两处”指证半误，属实单改（fidelity轴回退记录）。
- [Minor] R4-R3-02 five分母未定义 @L212与Discussion：可数isotonic held-out CV为4（holdout/cloud/powcloudnew/powlocalnew），temp为样本内；five无法还原。→ 回应：FIX，E9a/E9b（five=五个iso 5折CV检验，逐项列出＋pilot退化carve-out；“fails everywhere”收为both informative strata）。
- [Minor] R4-R3-03 ece_unified十五/十四指针（同R4-R1-01）。→ 回应：FIX，E6/E7/E7b/E14。

## Raw reviewer JSON
（severityCounts本角色 Minor 3；长短/同族归一自检通过。）
