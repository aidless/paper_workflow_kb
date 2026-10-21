# ROUND_R11 — 对抗审稿输入处置（P0 修完，P1/P2 排队）

## R11修订轮执行记录（2026-09-07，用户"全做"）
### P1（全部落地）
- 摘要986→330词；cloud-new改guarded口径（4/60，ECE 0.1067→0.1692＋flattery注记），全文单口径。
- 术语：powered-extension→local-big；powered pool→pre-specified pool；
  顺手修两处"pre-specified pre-specified"重叠；"only powered inference"→"only pre-registered powered inference"（两处）。
- Holm-Bonferroni（`scripts/seal_holm.py`→`results/holm.json`，17检验）：
  幸存loose＋pilot；pool第3步止（0.0039＞0.00333）；license收窄为联合控制下两层成立。
- 代码声明段（supplementary＋on request＋acceptance补链接）。
### P2（全部落地）
- TikZ配图`fig:acc`（13层exact/guarded准确率并列柱；`\usepackage{tikz}`新增；编译待TeX）。
- 公式：ECE定义＋McNemar精确双侧公式（与实现一致，已核对）。
- jargon：G006→adjudication gate（3处）；R3→third adjudication round；
  code-domain pilot→code-format probe（3处，区别30-row pilot）。
- loose"2 of 412 excluded"系伪句——原始记录零错，手稿改"412/412零错"，C42加【订正】注记。
- Q1（ECE机械性→limitations）、Q2（双侧理由→Methods）、Q3（双bin制保留理由：重分箱改写哈希证据）。
- W4循环性明示（guard段＋out-of-sample支撑：10/10新题＋470行零差异回归）。
### 验证
- 账本45/0/1WARN（C45 Holm）；门禁9/9；manifest 224条；zip 164文件零真泄漏。
- seal已刷新（`PHASE5_SEAL.json`）。
### OPEN（需用户/TeX环境）
- PDF仍旧版（本地＋云端无TeX）：有TeX机器`pdflatex main`→重打zip→重算seal。
- 第九次O2未跑：R11改动值得一次重评，要跑回一声。

---

## 输入
外部审稿（自称第十一轮 rater，N7.0/S8.0/Si7.5/C6.0=7.4；未经校准声明已作）。
按对抗流程：逐条验真后再修，不照单全收。

## 验真结论
- 属实：PDF过期（410-Row，CreationDate 14:45，早于tex 17:16改动）；
  zip混入rater全套＋STATE_SNAPSHOT/WORKING_NOTES/kb索引/writing_session/gates_history
  （SELF_ASSESSMENT/ROUND_不在包内，审稿意见夸大了一处）；
  bib仅1真引用＋2模板残留；67/68口径矛盾（21+9+21+10+7=68行过裁决，67判对，
  云new-42单列 excluded）；abstract 986词（比说的700更糟）。
- 存疑未动：C分歧（读者体验 vs 诚实同口径）属评分口径差，不改稿。

## 已修（P0）
1. `prepare_submission.py`排除规则补洞（rater子串/STATE/WORKING/GOLD_SYNC/analysis_plan
   前缀、writing_session/gates_history/LITERATURE/KB文件、evidence/kb目录）；
   方法judge脚本保留。重打`submission_tmlr_n942.zip`：199→162文件，零泄漏
   （两误报为方法脚本，保留）。
2. 67/68：abstract＋贡献两处改为"rows put to judges processed, 67 confirmed
   correct on content"，不引入裸68。
3. bib：删Bengio/Hinton残留，修goodfellow重作者，加Guo17/Nixon19/SQuAD/BERTScore/
   MT-Bench五条公开引用（cite全解析）；Related Work重锚定公开文献，保留scout
   新颖性（C07）与hedge，内部行话"Phase~5"改 plain。
- 账本44/0/1WARN；门禁9/9；manifest 221条；seal已刷新。

## 未修（OPEN）
- P0-1：PDF重编译（本地＋云端均无TeX）。zip内PDF仍旧版，seal已注记；
  需TeX环境：pdflatex main → 重打zip → 重算seal → 传OpenReview（人工）。
- P1/P2（下轮）：abstract 986→200词；powered-extension/Local-big撞名；
  abstract cloud-new raw/guarded双口径；多重比较段；公开代码链接；图与公式。
