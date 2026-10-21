# ROUND_R27 — 补强 P1 理论化（Measurement-error formalization）

> 目标：MISSION_R27_29 的 P1，补 N（novelty）。日期 2026-09-11。

## 结果 vs 验收标准（P1 gate）

- 目标：main.tex 新增形式化小节，含 ≥1 条可证伪预测 + 与既有数据逐条方向对照；账本新增 claim 且 verified；无数字移动。
- **达成**：
  1. `paper/main.tex` 新增 `\subsection{Measurement-error formalization}`（插于 Matchers 之后、Outcomes 之前）——把 matcher 形式化为二值算子 e/t（flip=e=0∧t=1，t=R 析取），翻转由「答案变体空间 × R 类型覆盖」两独立因子决定，导出三条可证伪预测。
  2. 账本新增 **C72**（verified），证据字段锚定 results/ablation.json（7/4/3/1/1）、results/math40.json（0/40）、results/local_en.json（0/30）。
  3. 无新实验、无新数字（纯理论层，引用既有 sealed 文件）。

## 三条预测（post-hoc 如实披露）

- (i) 退化变体空间→零翻转：math 0/40 ✓、code-format probe 单 c-cell（existence proof）。
- (ii) 覆盖缺失→零翻转：**前瞻，未被既有数据钉死**——local-en 0/30 记「天然规范」非覆盖变体检验，留给 R28。
- (iii) 覆盖变体→正翻转且归因随规则覆盖：消融 7/4/3/1/1 + 中文层正翻转（至 43.3% loose-rep）✓。

## 产出物

- `paper/main.tex`（新增形式化小节）
- `CLAIM_LEDGER.md`（C72 verified）
- `STATE_SNAPSHOT.md`（R27_P1_THEORY 行）
- `scripts/append_c72.py`（C72 追加脚本，可复跑）
- `evidence_manifest.json`（重建 411→423 条目）

## 验证

- `verify_claim_ledger.py`：72 PASS / 0 FAIL / 1 WARN（WARN 为既有 inconclusive 条目，非本轮引入）。
- `run_acceptance_gates.py`：10/10 PASS（首跑 manifest 对账 FAIL → 重建 manifest 后收敛）。
- `scan_number_consistency.py`：19 处 table-vs-prose 精度 mismatch 均为既有历史遗留，本小节未引入新 mismatch。

## 失败 + 原因 + 纠正

- 首跑门禁 manifest hash reconciliation FAIL：本轮改 main.tex/账本/快照并新增脚本，未同步重建 manifest。纠正：`build_evidence_manifest.py . --out evidence_manifest.json`（423 条目）后重跑，10/10 PASS。
- 账本追加曾因中文引号 edit 匹配失败：改走 `scripts/append_c72.py` 幂等追加，避开引号编码陷阱。

## 下一步（P2 / R28）

跨域证据：用非 QA 任务验证预测 (ii)（覆盖缺失→零翻转），兼复现 (i)。需预注册（PREREG_R28）+ 本地 qwen2:7b 作答 + 裁决（少量标注预算抽检）+ seal。