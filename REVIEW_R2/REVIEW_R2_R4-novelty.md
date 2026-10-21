# Review Round R2 — R4 新颖性 审稿报告

- 日期：2026-09-08 ｜ 论文：Exact versus Tolerant Label Matching…（R15 修改版，main.tex 264 行）
- 审稿角色：R4 新颖性 ｜ R15 说明：paper_workflow_kb/ROUND_R15.md ｜ R1 基线：REVIEW_R1/REVIEW_R1_R4-novelty.md
- 独立审稿声明：本报告独立完成，未与其他角色交流；只审稿，未修改手稿。

## 1. 引用硬核验结论（hakim2026ranked，R15 新增引用）

**结论：通过，非凑数/错引。**

- 存在性：`paper/main.bib` L43 `@misc{hakim2026ranked}` 存在；正文 L85 `\citep{hakim2026ranked}` key 一致，可解（ROUND_R15 验证 hallucination 0 cite errors 与此一致）。
- 作者/年/题：bib（Hakim, Safayat Bin & Song, Houbing Herbert；2026；Ranked by the Matcher: A Reproducibility Audit of Knowledge Graph Extraction from Threat Reports；eprint 2609.01671）与 LITERATURE_REVIEW.md L202 记录逐项对上；年份 2026 与 arXiv 编号 2609.x（2026-09）自洽。
- 文中数字：L85（8 协议 / 11 of 45 逆转 / F1 0.16–0.70 / 机械 matcher ≤71% / LLM judge 86%）与 LITERATURE_REVIEW L202 及基线池 L99 逐字一致。
- 定位诚实性：同句明确 "Its domain is security extraction rather than QA calibration, so it is cited as independent motivation, not as a comparable effect size" —— 与 LITERATURE_REVIEW L99/L203 的"必引但非可跑基线"口径一致，无效应量挪用。
- 独立复核边界：primary-source（arXiv API 实查）依赖 ROUND_R15 L9 前置核验记录；本轮未重复抓取，仅核验 bib↔正文↔LITERATURE 三方一致。
- 残留瑕疵见 R2-R4-05（Nit）。

## 2. "首次/first" 措辞扫描结论

grep（case-insensitive：first|novel|unprecedented|pioneer）全文：**零无支撑优先权声明残留**。

- 命中仅 4 类：程序性 "first three strata"（L76/L106）、"first collection attempt"（L109）、"first pass"（L222）、"first 120 rows"（L204）——均为流程描述，非优先权主张。
- 主 novelty 句（L87）保持 hedged（"we are not aware of"）；第二处 "to our knowledge"（L89）已按 R4-06 要求显式降级（"that claim is inconclusive and hedged pending a final pre-submission literature re-screen"）。
- 但 L87 引入新的 process-language 残留，见 R2-R4-01。

## 3. R1 回归核对

| R1 ID | 状态 |
|---|---|
| R4-01（L01 delta） | ✅ 已修复：L89 写清"同一 30 行"＋四点 delta（十三层复制、第二 judge 家族、guard fix、power 复制臂） |
| R4-02（必引 2609.01671） | ✅ 已修复（见 §1） |
| R4-03（scout 可核查性） | ⚠️ 部分失败 → R2-R4-02（指针错配＋manifest 缺口仍在） |
| R4-04（guard in-sample 进 contribution 句） | ⚠️ 失败 → R2-R4-03（披露仍只在 Methods，不在 contribution 句） |
| R4-05（vi null 堆砌） | ✅ 已修复：L80 (vi) 括号内明示 "(effect present on cross-domain paraphrase styles, absent on replication questions)"，且 "control knob"→"regime contrast" |
| R4-06（第二 to-our-knowledge） | ✅ 已修复（见 §2） |

## 4. 问题清单（只报 R1 未提过的新问题＋修复失败项）

| ID | 严重度 | 位置 | 问题 | 期望 | 证据链接 | new / R1 回归 |
|---|---|---|---|---|---|---|
| R2-R4-01 | Major | main.tex L87 | 投稿正文泄漏审稿流程语言："This novelty sentence stays hedged (``we are not aware of'') as required."——"as required" 指审稿要求，属 process meta-commentary，不可出现在 TMLR 投稿中。R15 新增措辞引入的新问题。 | 删除该半句，仅保留 hedged novelty 句本身（"we are not aware of…"自足，无需自我评价）。 | main.tex L87 | new |
| R2-R4-02 | Major | main.tex L87；证据链 | 中央 novelty 句的审计指针错配：L87 把 "374 records, 11 double hits" 归于 `scripts/incr_scout_0907.py`，但该脚本 docstring（"One-off arXiv increment scout (2026-08-08 → 2026-09-07)…Prints machine-readable summary"）与 LITERATURE_REVIEW L221-225 确认它是 **44 篇补充屏**；374/11 屏的真实脚本是仓根 `arxiv_incremental.py` + `scout_c07_screen.py` + `scout_c07_abstracts.py`（LITERATURE_REVIEW L191-214），三者均在 paper_workflow_kb 之外且 manifest 零命中（manifest 全文 grep "scout" 仅命中 `scripts/incr_scout_0907.py`；"arxiv" 零命中）。R4-03 要求的"三脚本＋374 清单＋11 裁决表入 manifest"仍未落地，定量表述的审计链不闭合。 | 二选一：(a) 修正指针为真实三脚本并将其＋374 清单＋11 裁决表入 manifest（含 verify）；(b) 删定量数字退回定性 hedge。 | main.tex L87；scripts/incr_scout_0907.py L1-12；LITERATURE_REVIEW.md L191-214 vs L221-225；evidence_manifest.json | R1 回归（R4-03 部分修复失败） |
| R2-R4-03 | Major | main.tex L80 (iii) vs L123 | Contribution (iii) 仍无 in-sample 限定词："a one-rule guard that reproduces the adjudication exactly"；in-sample 披露只在 Methods L123（"in-sample by construction"）。R1 R4-04 明确要求"把 in-sample 写进 contribution 句"，该要求未被执行（ROUND_R15 L22 自述第 9 项"guard 加 in-sample（2 处）"即 L123 与 Broader Impact，而非 contribution 句）。 | L80 (iii) 改为 "…reproduces the adjudication exactly in-sample…" 或等效 post-hoc 口径。 | main.tex L80 / L123；REVIEW_R1 R4-04；ROUND_R15.md L22 | R1 回归（R4-04 修复失败） |
| R2-R4-04 | Minor | main.tex §Related work；LITERATURE_REVIEW L209/L224 | 方法相邻候选 2608.07827（token-probability 聚合＋Platt/isotonic）、2608.20511（binned ECE 批评）及弱相关 2608.12100（标签噪声 thesis）在正文零提及、无排除句；排除理由仅存在于 LITERATURE_REVIEW，不在投稿件内。以 screen 支撑 novelty 句的论文，审稿人会要求文内一笔带过。 | 可选：Related work 加一句排除语（如 "Token-aggregation confidence [..] and ECE-critique [..] do not report same-batch matcher flips, so neither is a counterexample"）或正式引用。 | LITERATURE_REVIEW.md L209/L224；main.tex L85-87 | new |
| R2-R4-05 | Nit | main.bib L43-49 | hakim2026 条目为裸 @misc（缺 howpublished/doi/url，eprint 写法 TMLR 可接受但单薄；且为 2026-09 当月 arXiv，可备注版本日期）。 | 可选：补 `howpublished={arXiv:2609.01671}` 或 note（含访问/版本号）。 | main.bib L43-49 | new |

## 5. 计数与收敛判定

- Critical：0 ｜ Major：3（new 1：R2-R4-01；R1 回归 2：R2-R4-02、R2-R4-03）｜ Minor：1 ｜ Nit：1
- 是否收敛：**否**。R1 六项中四项已修（R4-01/02/05/06），但 R2 仍有 3 个投前必修项；好消息是全部为单句/指针级修改（无结构性返工），修完后 R3 只需做指针与措辞确认即可收敛。
