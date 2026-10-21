# ROUND R18 — Major Revision log

基线：R17（Phase 5 封存态；编辑独立终审 Reject→Major Revision）。
本轮性质：框架级重构 + P0 新数据 + P1 正文集成。旧证据 hash 冻结（holm v1 留档），新数据独立封存。

## P0-data(b) 预注册（先于采集，诚实顺序）

`PREREG_R18_LOOSE_REP.md`（采集前落盘，真 pre-reg，回应编辑 C2）。

## 到达记录

- [x] P0-text：标题/摘要/H1/McNemar 重构 + 机器检查 9/9（R18 首轮）
- [x] P0-data(b)：60 问新 loose 复现集（云机 qwen2.5:7b，60/60 零错）+ dedup exit 0
  + 用户 10% gold 抽查 6/6 + seal（results/r18_seal.json，16 文件）
- [x] R18 adjudication：四轮全留档（pass1 17/27 → pass2 泄露剥离 +5 → pass2b retry →
  pass2c 双语解析修复中文作答漏检）；终局 24/27 确认（23 judge＋1 作者补 46）；
  排除 42（guard FP#2：牧/牧之 CJK 片段，guard 漏检，不打静默补丁）、54/55
  （echo 全包含而 judge 拒绝，仪器不一致如实报告）；裁决数：翻转 24/60、
  guarded 39/60、ECE 0.2425（results/r18_adjudication.json；seal 已更新）
- [x] P1-正文集成：14 层表＋TikZ 第 14 对柱＋N=1002＋merged 重算（809/893/84/0.0838）
  ＋license/asymmetry/multiplicity（Holm v2：18 比较，幸存 r18/xloose/pilot，
  v1 留档 holm_v1_17.json）＋limitations＋appendix 指针＋账本 C49–C51（C45 转 superseded）
- [x] P1-1 统一分箱（C6）：scripts/recompute_ece_unified.py＋results/ece_unified.json。
  发现三口径并存（等频／floor等宽 legacy／upper-edge等宽 canonical）＋legacy
  bins.index 混叠 quirk（quirk-faithful 复现 0.1067，差 0.0008，outcome 一致）。
  主表改 canonical：holdout 0.3517→0.3317／0.205→0.165；cloud-new 0.1067→0.1075／
  0.1692→0.0558（证伪"0.1692 巧合"：同函数同标签）；local-new guarded
  0.0345→0.0782；local-big 0.033→0.0413／0.0458→0.0542；余层不变。
  tempscale 等宽下转混合结果（holdout 改善 0.165→0.1147，cloud 恶化
  0.0558→0.1384，无一致修复）；isotonic 样本内坍缩到 0.0（无信息量已披露），
  CV 仍恶化（0.1934 对 0.165；0.1172 对 0.0558）。正文 16 处＋附录等频表＋
  账本 C52/C53（C11/C15/C19/C20/C21/C22/C25 加统一口径注记，C20 claim 改混合表述）。
- [x] 本轮机器检查（P1-1 后）：ledger 53/0/1、stats exit 0、style 0、taint 0（53 claims）、
  hallu exit 0、numbers exit 0（stale 0；near-miss 既有噪声类）、manifest 重建 284/0/0
- [x] P1-2 数据（C3）：mini-pre-reg 先行（PREREG_R18_HETEROMODEL.md）→ r1 尝试失败
  （54 行首行全 `<think>`，`think:False` 被无视，qwen3:4b 先例重演；部分文件保留为
  失败记录，不入分析）→ Amendment A1 切 gemma3:4b（异家族＋异规模 4B，一点覆盖
  family/scale）→ 60/60 零错 → 描述性 11 翻转（0.1833，b11c0；exact 21/60→guarded
  32/60）→ 异构 judge（本地 qwen2.5:7b，one-word 前例）8/11 确认；排除 41/42/45
  （白/子/玄单字片段，guard 漏检类第三、四 exemplar，与 lr18-42 同类）→ 裁决
  29/60（0.4833）、翻转 8/60、ECE 0.381（results/r18_heteromodel_adjudication.json）。
  失败尝试＋Amendment＋四脚本全留档。
- [x] P1-2b 正文集成（第 15 层，N=1002→1062）：表第 15 行＋TikZ 第 15 对柱＋
  merged 封存重算 scripts/seal_merged_hetero.py（assert 830/922/92 通过，
  results/merged_1062.json）＋摘要/引言/方法/结果/license/asymmetry/Holm/
  limitations/contributions/evidence-pointers 全同步＋账本 C54。
  （纠正：自拟初稿 0.4417 系凭空数，已废弃，以 het 文件 0.5143 为准。）
- [x] 本轮机器检查（P1-2b 后）：ledger 54/0/1、stats 0、style 0、taint 0（54 claims）、
  hallu 0、numbers exit 0（stale 0）、manifest 重建 298/0/0
- [x] P2-1 guard synthetic（C5）：scripts/guard_synth.py＋results/guard_synth.json。
  公式召回12/12、精度12/12、接受集12/12零误伤；CJK 8/8漏检（构造性，无补丁）；
  真实92确认全接受＋3锚＋G06被拦截＋6已知漏检；v3.1/v3.2在131行零差异。
  正文6处＋账本C55。C5关闭（原unmeasured改为已测量）。
- [x] P2-2 n=157处置（M6）：scripts/dispose_n157.py＋results/tempiso_n157.json。
  PowCloudNew T*约1无动作、iso CV恶化；PowLocalNew temp恶化但iso CV改善
  （0.0668到0.0277，五个held-out唯一阳性，照实报告）；大n不救一致性。
  正文3处＋账本C56。M6关闭。
- [x] P1-3 GOLD-100包（C4）：scripts/build_gold100.py（seed100）→
  gold100_grading_pack.csv＋GOLD100_README.md＋evidence/gold100_key.json
  （100项＝7排除＋55确认＋38非翻转，79有题干）；解码scripts/decode_gold100.py
  门控待grades；账本C57（仅包构成）；正文pending句＋指针。grading待真人。
- [x] 本轮机器检查（P2/P1-3后）：ledger 57/0/1、stats 0、style 0、taint 0
  （57 claims）、hallu 0、numbers exit 0（stale 0）、manifest 重建 307/0/0
- [x] GOLD-100真人grading→解码（C4关闭）：用户16错（常识/计算/化学/古人字四类，
  逐项内容核对全按protocol正确）→grades_gold100_user.csv→decode（decoder扩展
  adjudicated口径：assert两排除集与封存一致）：guarded口径86/100（0.7786-0.9147；
  题干71/79；翻转58/62），确认翻转58/58全接受，4翻转分歧皆排除项同被拒
  （H62/H68/H71/H82 vindicated；H34双方皆错一致）；裁决口径88/100
  （0.8019-0.93），仅分歧H47/H85（echo排除项，盲评站guard/作者注记、反密封排除）；
  余10分歧皆guard非翻转行假阴性（朝后缀/Jakarta音译/支持同义/echo+leak）→新limitation；
  另1采样gold事实错（H09 reference是，生姜为根茎）。正文5处（结果段＋摘要＋
  方法/限制两处＋指针）＋账本C58。
- [x] 本轮机器检查（GOLD-100解码后）：ledger 58/0/1、stats 0、style 0、taint 0
  （58 claims）、hallu 0、numbers exit 0（stale 0）、manifest 重建 309/0/0
- [x] R18收官：终检封存（Phase 5门）——用户批准执行：manifest先验308/1/0
  （ROUND_R18.md日志追加致hash漂移）→重建→309/0/0；全扫描重跑
  （ledger 58/0/1、numbers/stats exit 0 stale 0、style/taint/hallu 0）；
  PHASE5_SEAL.json已更新（R17 superseded）→manifest再重建→终验309/0/0。
  本轮冻结，后续改动另起轮次。
- [ ] P0-data(a)：pilot-top20 —— 用户已决策取消（见上）

## 纠正记录（≤3 次/门，超限升级）

- R18-01：dedup 初版 11 碰撞（powrep-loose 已用题）→ 60 题全换，一次纠正通过。
- R18-02：stats 扫描被新写字面 N=50 触发同行冲突 → 改写为 "30-row stratum" 描述，一次纠正。
- R18-03：r18_adjudicate 导入名错误（guarded_match→tolerant_match_v32）＋自实现 exact
  改复用 norm（与 layer 同函数）＋缩进事故 → 三次内收敛（门内）。
- R18-04：C45/C50 ledger FAIL（holm.json 已变＋values 列混入 trace-id）→ C45 转指
  holm_v1_17.json 记 superseded-by-C51，C50 values 去 trace-id → 51/0/1。
- R18-05：统一分箱发现三口径并存（属 C6 深化发现，非事故）：canonical 取
  upper-edge-inclusive（Guo 式）；legacy quirk 以 quirk-faithful 复现证明
  outcome 一致；local-new 初 assert 失败一次即定位到 binner 差异（门内一次纠正）。
- R18-06：CLAIM_LEDGER.md edit 工具 stale-read 冲突（bash append 改了文件）→
  改走单 python 脚本批量注记（门内一次纠正）。
- R18-08：guard_synth 排除集期望误设7/7全接受→实为6接受＋G06被拦截
  （与注记自述一致，期望写错）；一次纠正。
- R18-09：gold100确认池92/99之辨（92主regime＋7 loose，judged 106确认99；
  与正文99/106一致）；nonflip quota overshoot（wrong预取超q）→min限幅；
  两次纠正，门内。
- R18-10：C55/C57 ledger FAIL（guard_synth.json缺results.前缀＋CSV非JSON值检查）
  →evref加前缀＋key增counts块重跑→57/0/1；一次纠正。
