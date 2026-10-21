# ROUND R3 — R16 版轻量验收（4 角色，非全员重审）

事由：R2 建议 R3 由 R6 单项验收；扩展为 4 个直接相关角色（R6 摘要措辞 / R2-stats 计数簇 / R3 实验措辞 / R7 披露确认）。
基线：R16（`r16_fixes.py` 全断言执行，12 簇；改动日志 ROUND_R16.md；manifest 252/0/0）。
验收判据：各角色确认其 R2 问题已修 + 无 NEW Critical/Major。Minor/Nit 可带入下一轮。

## 到达记录（4 角色）
- [x] R6 writing — **收敛（补丁后关闭）**：4/5 PASS（摘要243词亲算/knob清零/license重写/newly清零，数字全亲手重算match）；R2-R6-05 FAIL经主审直接补丁关闭：L67/L196/摘要L54三处句内pilot标签已加（r3_r6_verify.py复验：三处落地、括号配平、0.0005零命中），摘要247词仍在150–250内；序数Minor顺带消解（L226序数删除，L220 second不再矛盾）。报告 REVIEW_R3_R6-writing.md + r3_r6_verify.py/r3_r6_recalc.py。（单项验收：摘要 150–250 词、license 句无矛盾、knob 清零、数字墙消除）
- [x] R2 statistics — **收敛（新C0/M0/m2）**：R2-R2-01消解关闭（L239计数集声明+穷举+双排除；主审复验：L54摘要"4 in-family（含单臂）+2 rollups族外"=6名义显著−单臂排除=license five，算术闭合；p=0.0156双胞胎已正面承认same strength）；R2-R2-02关闭（L54/L75/L214三处post-hoc）；R2-R2-03关闭（全文0.0005零命中，主审复验确认）。亲手重算12格McNemar+Wilson+Holm+N/flips全✓。残留m01（L220 second跳过pool，前存非新引）+ m02（without a power conclusion措辞可选补强），均不阻塞。报告 REVIEW_R3_R2-statistics.md。
- [x] R3 experiments — **收敛（C0/M0/m1/n0）**：4/4修好（knob零命中/摘要five已删+族外披露/三处统一/口径标注+披露；retest/McNemar 10组亲手重算吻合；R2 Minor/Nit顺带全过）。唯一Minor R3-R3-01（L226序数悬空）已由主审顺手改（删序数）关闭。报告 REVIEW_R3_R3-experiments.md。

## 收敛状态：4/4 到齐，R3收敛——NEW Critical 0 / NEW Major 0；R2全部Major已关。残留仅可选Minor（R3-R7-m01、R3-stats m02），建议不单独成轮。（D retest 口径 / C pilot-50 矛盾 / B knob sweep）
- [x] R7 ethics — **收敛（C0/M0/m1/n0）**：R2-R7-01 CLOSED（三处rater-independent→blinded L119/L232，Blinding note L232 + 摘要L55，主审亲手grep+Wilson重算差<1e-12；R16主审复验：全文independent仅剩L85/L245合法非评分者用法）；R2-R7-02 CLOSED（COI一句L249，主审复验命中）。NEW 0；仅非阻塞Minor（second grading措辞，可不修）。报告 REVIEW_R3_R7-ethics.md。

## 收敛状态：4/4 到齐，R3收敛
