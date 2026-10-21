# ROUND R16 — R2 十二簇修复（措辞/披露层，数字零触碰）

脚本：`r16_fixes.py`（全替换带 assert 计数；abstract 字数 assert 150–250）+ 1 处 edit（L241 漏网 knob）+ 1 处 edit（L87 路径显式化）。备份：/tmp/main_r15_backup.tex。

## 簇→动作
- A：license 句重写（five→nominally significant in five counted readings + 计数集声明句：PowLocalNew 单臂不计入、raw-cloudnew 非 guarded 口径不计入；括号嵌套修平）；(i) 删 pilot-50 出 met 清单；control knob→regime contrast；not single-model 加同家族限定
- B：knob 全文 sweep（6 处断言 + L241 漏网 1 处），验收 grep knob=0
- C：L75+L214 meeting→post-hoc（同一 claim 两处，expect=2）
- D：L119+L230 flip sets→raw-basis 标注 + O2 误接受 + guarded 4 and 4（retest60.json 实查：flip_set 5/5 含氧气 O2 题，guarded_agreement=1.0）
- E：independent→heterogeneous（云端判官）/blinded（金标）；L119 方法段 + L232 结果段双处作者盲评披露（grades CSV 有"你的判定"列为证）；残留 3 处合法（independently supports/independent motivation/independent calibration-improvement）
- F：摘要 433→**243 词**（four in-family nominal + two out-of-family rollups + Holm 2 存活；删 null 枚举/边界层/c=0 展开，body 保留）
- G：L87 审计指针修正（LITERATURE L221-225 实查：374 屏=仓根 scout_c07_screen.py，44 篇=incr_scout_0907.py）+ 流程语言半句删除 + 路径显式化
- H：contribution(iii) 加 in-sample 限定；J：L226 newly→nominally + Holm-family 外声明；K：L138 云端 14/14 加作用域限定（cloud_repro.json 实查 14 文件确为前 xdomain 时代）
- L：C33 加 supersede 注（状态 superseded-by-C46，证据仍验 PASS，审计痕迹保留）；L262 falsified 标记；p 统一 0.00049；L216 trigger→bar；docstring 通胀两处改 documented intent；b=21 加 descriptive sum；999/1000 改 within tolerance；L196/198 加 guarded 等价注；COI/资助/受试者一句
- 未动（可选）：R2-R4-04 排除句、R2-R4-05 bib howpublished

## 机器检查（R16 实跑）
- stats exit 0 · style 0 findings · tmlr exit 0（0 FAIL；G9 WARN 系缺 evidence/protocol.md，改前已存）· ledger **48/0/1**（WARN=旧 C08；C33 supersede 后仍 PASS）· taint 0 · hallu 0 cite errors（3 missing 系 paper/ 相对路径旧 artifact，无新增）· numbers exit 0 stale 0（16 条误配注=扫描器噪声类）· manifest **252 PASS / 0 FAIL**
- 纠正记录：R2 轮 number exit 1（19 误配）→ R16 exit 0（摘要重写消掉 3 对）；R15 "number exit 0" 与 R2 "exit 1" 的矛盾解释：扫描器对摘要数字墙敏感，F 簇重写后回到 exit 0
- PDF 仍为旧版（本机无 TeX，需用户侧 latexmk -pdf；无新宏包，风险低）

## 收敛状态：R16 落子完毕；按 Phase 4.5 需派 R3 轮（建议 R6 单项验收 + R2-stats/R3-exp 计数簇确认 + R7/E 披露确认，其余角色可免，全员重审可选）
