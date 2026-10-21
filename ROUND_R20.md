# ROUND_R20 — 完美路线图·速胜轮（H09＋投稿包＋artifact＋Holm）

## 到达记录
- R19 已封存（manifest 329/0/0，验收门 9/9，MISSION 冻结）；用户指令"全做"（R20→R21→R22→R23连续推进；goal-8f8dffb2）。
- PHASE5_SEAL.json 仍为 R18 口径（R19 只经 manifest＋mission 封存）→ 本轮重建覆盖。

## 改动（4 项＋返工 1）
1. **H09 参考订正**：gold100_grading_pack.csv reference 是→否＋备注审计 trail；
   grades_gold100_user.csv 用户文件不动；正文 4 处（结果段重写＋L119/L253/L261 措辞）；
   账本 C58 evidence 注记。decode 重跑**逐字节一致**（86/88 双口径不动）——
   decode 只比用户判定 vs 封存 guarded_outcome，不读 reference 文本。
   （MISSION 初版 D2 曾误预测 88→87，已撤回修正。）
2. **投稿包**：submission/submission_tmlr_r20.zip（218 files；关键 7 文件齐；
   anonym 0 hits）＋ checklist 追加 R20-STALE-PDF（main.pdf 编译于 9-7，早于本轮 tex，
   上传前用户侧 G2 重编）。
3. **artifact**：artifact/REPO_DRAFT.md（布局映射＋最小复算链＋脱敏 5 项＋R21/R22 缺口）；
   requirements.txt 按实测重 pin（numpy==2.5.2, scipy==1.18.1；torch 仅 test_pyramid.py 用，
   非重算链，不引入）。
4. **Holm 全 family 补丁 C60**：scripts/verify_holm_hetero_sensitivity.py——hetero 作第 19
   比较重跑 Holm：幸存 [r18-loose-rep, xdomain-loose, pilot] 不变、停止仍 pool 第 4 步
   （阈值 0.003125 下仍停止）；正文 L251 挂脚本＋结果指针；纯算术完备性，无推断许可。
5. **返工**：C60 初版 evidence 列缺 sealed_m → verifier 误报 FAIL（claim 文本 r18 被解析为
   18.0 而证据值无 18）；补 sealed_m＋值列 18 后 60/0/1。门内纠正，非阻塞。

## 验证
- ledger **60/0/1**(C08 WARN 前存)；decode diff 一致；Holm 脚本 exit 0（assert 全过）。
- 六扫：stats/numbers/taint/hallu/style exit 0（numbers 两条 table-vs-prose 为前存近似数噪声，
  R19 已定性）；compile 静态层（TeX 缺失文档化降级；4 undefined `\ref{#n}` 经查非 main.tex
  内容，本轮零碰 `\ref`/`\label`，前存噪声）。
- acceptance **9/9**（gates_history.jsonl 已 record）；manifest 重建后 **334/0/0**
 （329＋5 新增：r20 zip、holm sensitivity json、verify 脚本、REPO_DRAFT、ROUND_R20.md）。
- seal：PHASE5_SEAL.json 三哈希更新（SELF_ASSESSMENT 自 R18 后 R19-r10 已变，现一并落盘）。

## 成本
- 模型调用 0（全确定性脚本＋文本编辑）；工具轮次约 25。

## 遗留（→R21，非本轮阻塞）
- 用户侧：G2 重编 main.pdf（STALE-PDF TODO）；公开建仓＋LICENSE＋acceptance 改口。
- R21：judge 校准集（需采 200–300 已标 pair；check_judge_calibration.py 已存在脚手架，
  待查）＋第二 grader（需第二真人判量子集）。
