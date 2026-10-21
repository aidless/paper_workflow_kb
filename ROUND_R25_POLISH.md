# ROUND R25-polish — 投稿前打磨轮（P0–P4）

- 范围：零新实验、零数值改动。P0 staleness 对账＋compile 门修复、P1 终轮横扫、P2 rebuttal 门、P3 G1–G11＋重封 seal、P4 三用户决策落地。
- 冻结语义：数值层未动；R25 seal 因 R25b–e 四个纯文字小修（tex 哈希已变）被 supersede，本轮以 PHASE5_SEAL.json（round=R25-polish）重封。

## P0 staleness 对账
- 发现：`paper/main.pdf`(13:58) 早于 `main.tex`(14:39)；投稿包(14:44)早于 REBUTTAL/SELF_ASSESSMENT。mtime 不可全信，走标准顺序消除疑点。
- `scripts/compile_gate.py` 两处最小修：subprocess 加 `errors="replace"`（pdflatex 日志非 UTF-8 字节致 UnicodeDecodeError 崩）；tex 含 xeCJK/fontspec 且 xelatex 可用时用 xelatex（手稿必需，pdflatex 报 Emergency stop）。修后编译门 PASS（0 错误；2 overfull＋5 orphan-sec-label 警告，非阻塞）。
- 正式 PDF：临时目录 xelatex 三遍＋bibtex，0 错误，16 页，letter(612×792)，落盘 `paper/main.pdf`（新于 tex）。
- FM-24 顺序：重打 `submission_tmlr_r25.zip`(0.7MB) → 重建 manifest(383) → C1–C7 全 PASS → 门禁 10/10 record。

## P1 终轮横扫
- numbers `--fail-on-stale` exit 1：20 条 table-vs-prose 全 triage——19 条舍入显示对/宏参数交叉误配，1 条 arXiv ID 系 scout 表两不同行（2609.01741 另有其文）误配；真值矛盾 0。项目门禁本即 report-only（stale 0），不受影响。
- stats/style/ledger(68/0/1，C08 按设计)/taint/hallucination/figure-claims 全 exit 0。
- tmlr：G1 PASS；G3 2 命中 adjudicated（`deepseek-r1:7b@local` judge 标识符，JSON 键原文，改字断追溯链；同 R25 裁决）；EXTRA TODO＝LICENSE（P4 解决）。
- citations：verifier 缺失（Windows 硬编码路径，本机无 research-kit）→ 沿用既有 documented-degradation 记录；静态替代：7 cite key 与 7 bib 条目一一对应＋hallucination 0 cite errors。
- freshness：stale 0，PASS。

## P2 rebuttal 门
- `scripts/rebuttal_sim.py` 本机缺失；既有 `out/rebuttal_sim/`（15:54，mock 三类 completion/satisfaction 1.00/1.00，gate passed）且 REBUTTAL.md 此后未动 → 结论复用，不重跑空气门。

## P3 G1–G11＋重封
- G1/G2(letter＋xelatex 裁决：xeCJK 强制，几何符合)/G3(包内 0 命中)/G4(仅 XXXX 占位 URL)/G5(0.7MB)/G6(bibtex 净)/G7(~200 词＋风险)/G8(清单在，人项待用户)/G9(单篇 N/A)/G10(同 G3/G4)/G11(门禁＋383/0/0)。
- PHASE5_SEAL.json 重封（round=R25-polish，5 件哈希＋384 manifest；终轮 manifest 重建后条目数 384（＋本记录），一致）。

## P4 用户决策（2026-09-08）
1. LICENSE＝MIT（REPO_DRAFT TODO 消项；"on request"改链接待用户建仓后）。
2. REBUTTAL.md 可投（draft→FINAL 落盘）。
3. 外部 grading 不加，接受 C4 残留（Response letter 已 preempt）。
- 待用户唯一动作：OpenReview 手动上传（zip＋PDF＋粘贴 response），永不自动化。

## 验证
- 终轮链（P4 编辑后重走）：zip 重打 → manifest 383 --verify 383/0/0 → gates 10/10 record → C1–C7 全 PASS。见下。
