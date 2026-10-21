# ROUND R2 — R15 版微调轮审稿（8 角色独立）

目标：验证 R15 十项修复，扫 NEW Critical/Major。收敛判据：C0 + M0（已知 Minor/Nit 可带）。

## 机器检查（R2 主审本轮实跑，main.tex 自 R15 未动）
- stats exit 0 · style exit 0 · tmlr 0 FAIL（G7=78词 PASS）
- ledger 48/0/1（WARN=旧 C08）· hallucination 0 错误
- number-scan exit 1：19 处 table-vs-prose mismatch 亲验全为扫描器误配（相邻行/跨层错配：2609.01741↔01671 两论文并列、p=0.0010↔0.0005 跨层、rounding），零真错
- 纠正记录：R15 轮报 "number exit 0" 不准（文件未动而本次 exit 1），属扫描器噪声、非手稿回归
- PDF 仍为 19:02 旧版（本机无 TeX，待用户侧重编）

## 到达记录（8 角色）
- [x] 机器检查（上）
- [x] R8 figures — C0/M0/m2/n2：6组独立重算16断言全pass（GOLD 24/25 CI、L151 CN-guarded、L157 XD-loose、5 rollup、PowLocalNew、图柱+N=942）；R15三处全绿，GOLD不应进表；R1的2 Minor+2 Nit原样persist（R2-R8-01缩写、R2-R8-02 ECE分母、R2-R8-03 raw脚注53/60、R2-R8-04 flips符号），本角色收敛无阻塞。
- [x] R7 ethics — C0/M1/m1/N0：[R2-R7-01|Major] L119/L232 三处"independent(ly)"原样保留且新增"independent second grading"；评分者=作者(user-confirmed, grades CSV为证)全文零披露 → 期望三处改blinded + 加一句作者单人盲评声明（R3 修）；[R2-R7-02|Minor] COI/资助/受试者显式声明仍缺席。R7-01（24/25+G06具名五处）与gold_guarded_agreement.json逐项吻合PASS；BI模板首句已删、G06教训句落地；双盲干净。
- [x] R4 novelty — C0/M3/m1/n1：[R2-R4-01|Major|new] L87 泄漏流程语言"This novelty sentence stays hedged…as required"删半句；[R2-R4-02|Major|R1 R4-03回归] L87 审计指针错配（374/11屏归于incr_scout_0907.py实为44篇补充屏；真三脚本在manifest零命中）→ 修正指针+入manifest，或退回定性hedge；[R2-R4-03|Major|R1 R4-04回归] L80 contribution(iii)缺in-sample限定词（披露只在L123）→ 写进contribution句；[R2-R4-04|Minor|new] 2608.07827/20511/12100文内无排除句（可选）；[R2-R4-05|Nit] hakim bib补howpublished（可选）。引用核验：hakim2026ranked通过（bib/key/作者年题/eprint 2609.01671与LITERATURE L202一致，数字逐字吻合，异域动机定位诚实）；"首次/first"零残留；R1的R4-01/02/05/06确认已修。
- [x] R1 methodology — 新C0/新M0（回归m2+新m1/n1）：R15的R1-01 H1方向化/GOLD 24-25/67-68/Holm限定/post-hoc/pilot50去p/ECE口径/hakim+L01/guard披露均验证落地；独立重算5项全一致（Wilson24/25、McNemar b=9→0.00390625/b=20→1.907e-6、67/68、翻转总数60=854-794、Holm止步step3）。残留：R2-R1-01 "control knob"L239/L247（与C42冲突）、R2-R1-02 L216"5% trigger"触发式措辞、R2-R1-03显著序数second/third/fourth与five总数矛盾、R2-R1-04 localnew217 p值0.0005/0.00049舍入。本角色收敛，无阻塞。
- [x] R2 statistics — 新C0/**新M1**：[R2-R2-01|Major|new] "five"计数成员规则未声明：L224许可PowLocalNew单臂(b=7,c=0,p=0.0156)为significant observed-status，与计入five的holdout rollup（同b=7/c=0/p=0.0156逐位相同）地位相同却被排除无解释；另L226 raw-basis cloudnew217 p=0.031为第七个名义显著；five既非全部未校正显著集也非Holm存活集(2个)，L239穷举式表述与L224矛盾 → 期望一句话声明计数集或修正为六。[R2-R2-02|Minor] 摘要L54与L214"meeting n=217"仍无post-hoc限定。[R2-R2-03|Nit] p=0.0005/0.00049舍入。重算stdlib手写公式：McNemar 9格全逐位一致、Wilson 24/25逐位一致、Holm止步step3 survivors 2个、N=942/flips=60/67-68分解；R15数字层零错误。R15修项#2/#3/#4/#5与R1 R2-01/02/03验证落地。本角色未收敛（R2-R2-01投前必修，一句话可修）。
- [x] R6 writing — 新C0/**新M3+回归M2**：[R2-R6-01|Major|new] 摘要433词（13句），数字墙L52–56仍在，远超150–250词；[R2-R6-02|Major|new,R15引入] control knob强因果词残留L239/L247（L80/L241已改regime contrast，最强措辞恰留许可句）；[R2-R6-03|Major|new,R15引入] L239 license句自相矛盾（observed-significance与under joint error control同句）；[R2-R6-04|Major|回归R6-05] L226"newly significant"/"third and fourth"又称"rather than new tests"；[R2-R6-05|Major|回归R6-02] pilot n=30/50 caveat只在远端，声明位句内无标签。Minor×3、Nit×4。已落地7项。**不收敛**（建议R3由R6单项验收）。
- [x] R3 experiments — 新C0/**新M3+回归M1**：R15修复9/10落地（guard in-sample L123、ECE不重分箱L119/L141、0.1692巧合注L206双证据核对属实、GOLD24/25+G06、Holm进摘要、412披露真落地；knob改名部分失败）。[R2-R3-01|Major|回归] knob残留L239/L247等6处；[R2-R3-02|Major|new] rollup双重检验计入five显著但被排除在Holm族外（L54/L226 vs L243）；[R2-R3-03|Major|new] pilot-50上限L239称已达成 vs L245称仍不足 + L226自定描述性拼盘；[R2-R3-04|Major|new] retest混合口径5/5含已知误接受未披露（L230）。Minor×3（docstring预注册通胀L220、b=21双计L241、999/1000边界措辞L224）、Nit×1（p舍入L54）。独立重算6项全对。未收敛，需R16措辞层修复4条Major。
- [x] R5 reproducibility — 新C0/**回归M2**：[R2-R5-01|Major|R1回归] L138云端14/14口径过期（cloud_repro.json 14文件全早于xdomain时代，R15零修改）；[R2-R5-02|Major|R1回归] L232/HOLD"independent"黄金评分保留且评分人=作者正文零披露（与R2-R7-01同根）。[R2-R5-03|Minor|new] 账本C33 25/25与C46 24/25并存verified无supersede注；[R2-R5-04|Minor|new] 附录L262旧decode指针无falsified标记。重算：Wilson 24/25逐位一致、stem 13/14+stemless 11/11+G06三源闭合、"25 of 25"仅2处且均在失败披露句内、manifest 243条哈希匹配。R1六Major中R5-01/02/04/05已关，R5-03/06修复失败。未收敛。

## 收敛状态：未收敛——8/8 到齐，新C0 / 新M8 / 回归M6（含两对同根去重后约12个独立修复簇）。数字层全绿（9组独立重算零错配）；阻塞全在措辞/披露层。R16 清单见终态消息。
