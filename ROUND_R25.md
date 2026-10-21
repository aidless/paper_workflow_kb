# ROUND R25 — 审稿 round-2 回应（N1–N5、C3/C4 续、P2）

- 范围：纯文字＋指针修改，无新实验、无新模型调用、无数值改动（封存数全部重算一致）。
- 证据新增：`scripts/seal_R25_numbers.py`（唯一重算）→ `results/adjudication_recount_R25.json`（106/102/99/4）、
  `results/guard_fn_R25.json`（140／38／9／0.2368）、`results/regime_R25.json`（八层 wrong-after）。
- 账本：C65–C68 新增，68/68 PASS。门禁：新增 R25 recount 常驻门，10/10 PASS。manifest 370/0/0。

## 逐条回应

- **N1（P0，计数统一）**：106＝102 翻转行＋4 非翻转探针行（R18 lr18-42 控制＋hetero gr18-41/42/45），
  confirmed＝99。Methods 立 canonical 口径段；摘要／Contributions(ii)／R18 27行／hetero 11行四处统一；
  旧"67 of 68"为 R18/hetero 前冻结数，已替换。审稿人算的 102＝翻转行口径，与本文 106＝judged 口径一致，
  现已在正文明示，不再是"不一致"。
- **N2（P0，regime 区分）**：Discussion 新增 Accuracy-regime 段。高层 exact≥0.63、裁决后仍错≤8行/层；
  R18（0.25→21/60仍错）、hetero（0.35→31/60仍错）翻转部分系模型失败；xloose 居间。不断言 pooled 纯 matcher 效应。
- **N3（P1，guard FN）**：Limitations 量化——guard 拒 140/1062；GOLD-100 非翻转行条件率 9/38（分层集，不作总体率主张）；
  方向保守（guarded accuracy 为下界）；不切 v3.4，9 行留档作回归靶。
- **N4（P1，贡献重述）**：Contributions 改 descriptive framing，(ii) 重写为 99/106 全分解；power/Holm 不再作贡献项。
- **N5（P1，Holm）**：正文 Multiplicity 压缩为一句 audit-only，完整段移入附录 Holm accounting 节；L131 seventeen→eighteen。
- **C3 续**：结论限定 small open-source 级（无 70B+/closed），跨尺度泛化列未来工作（Discussion(ii)＋Future work）。
- **C4 续**：四处披露第二 rater＝外部志愿者真人（非作者）；κ＝reliability 非 validity；超 30 项 overlap 的独立外部 grading 列未来工作；
  修正"唯一人类 grading 是作者"旧句。
- **P2**：摘要 519→284 词；Methods 快照巨段拆分为 4 段（含 N=1002/N=1062 分行，顺带消除 stats 扫描同行 n 冲突）。

## 返工记录

1. apply_R25 初版摘要断言 ≤310 失败（实际 421）→ 追加 compress_abstract_R25.py 二次压缩至 284。
2. 全部门禁首跑 7/10：manifest 须重建（预期内）；ledger C68 wrong-after 派生数直引 arms 失败→改立 regime_R25.json 显式字段；
   stats 同行 n 冲突（E12 分段把 N=1002/N=1062  expose 到失去 versus 豁免的行）→ R18/hetero 句分行。
3. edit 工具 stale-read 报错一次（apply 脚本已重写 tex）→ 重读后改。

## 验收

- 10/10 PASS（含新 R25 门）；ledger 68/0/1；manifest 370/0/0；seal 已转 R25。
- 审稿 HTML 已重建并验 9 个 R25 哨兵句。
- 用户侧未变：G2（PDF 重编）、公开建仓、上传；R23 投稿 zip 已 stale（早于 R24/R25 tex）。

## R25b 构建补记（TeX 工具链 + PDF 重编，2026-09-08）
- 起因：用户要求找 TeX 工具并重编 PDF（旧 main.pdf 为 9-7 版，早于 R22/R24/R25）。
- 动作：安装 TinyTeX（~/.TinyTeX，TeX Live 2026）+ tlmgr 补包（eso-pic/natbib/lm/pgf/xecjk 等）；发现正文裸下划线（PREREG_*.md、evidence/*.json 等文件名）致 xelatex 报错，脚本 scripts/fix_tex_underscores.py 转义 301 处（数字字符数 1033=1033，正文数字零改动）。
- 结果：xelatex+bibtex 全链 exit 0、零错误；main.pdf 16 页，关键数（99 of 106 / 922 of 1062 / 0.0866 / κ=0.91）与 CJK（不会/否/支持/雅加达）均渲染正常；旧版留存 paper/main_20260907.pdf.bak。
- 门禁 10/10 PASS；manifest 373 条（删编译副产品 .aux/.log/.out/.bbl/.blg 后重建）。注意：manifest 须用全量脚本在 paper_workflow_kb 内重建（非 scoped 版），否则 reconciliation 门失败。
- G2（无 PDF 工具链）就此关闭：本机可编 PDF。

## R25c 范围宣言（2026-09-08，用户指令）
- 用户：只研究小模型。Limitations 中 C3 表述由"道歉式局限 + 跨尺度泛化是 future work"改为"scope by design"：4B–7B 是目标总体（可部署、exact-match 仍是默认管线、本地可全复现）；frontier 泛化明确 out of scope，不再承诺。
- 含义：审稿人 C3 的回应立场升级（不是"做不到"，是"不做"）；环境缺口清单中 API key / frontier 两项注销；R26 新实验只在小模型总体内设计（本地 ollama 现有模型即总体抽样框）。
- 数字零改动；门禁重跑见本轮。
