# paper_workflow_kb — Label Matcher Choice Moves Measured Accuracy in Short-Answer QA

> A TMLR-grade stratified descriptive study with adjudication and a guard patch.
> The central methodological finding: **the correctness label is part of the
> measurement instrument** — which string matcher you choose moves the measured
> accuracy and the calibration metrics that inherit it.

**Status:** complete, submission-ready (manuscript under anonymous review; not yet
publicly released). **License:** MIT (code) / CC-BY-4.0 (data, docs, pre-registration).

---

## What problem does this solve?

Calibration and accuracy papers routinely report accuracy and expected calibration
error (ECE) *as if the correctness labels were fixed*. In short-answer QA the label
comes from a programmatic **matcher** — and the matcher is part of the measuring
instrument:

- A **brittle exact matcher** marks semantically correct answers wrong
  (`"8848.86米"` vs `"8848"`, `"不会"` vs `"否"`) → depresses accuracy, inflates ECE.
- A **tolerant matcher** reverses those calls → the calibration conclusion **moves
  with the matcher**.

There is no single "true" correctness; the choice of matcher is a measurement
decision with measurable consequences. This study measures those consequences and
shows the matcher choice is not a cosmetic detail.

## Why it matters

- It **quantifies a silent threat** to every calibration / accuracy result that uses
  a programmatic matcher: 92 of 232 (39.7%) rows the exact matcher calls wrong are
  adjudicated-correct answers the guarded matcher recovers — a bounded, known-denominator
  rate that does **not** depend on the nested-construction assumption.
- It **delivers a reproducible method**: a one-rule guard patch that reproduces the
  120-row adjudication exactly in-sample (one fix, zero regressions), with a synthetic
  probe measuring its boundary and a theorem proving its monotonicity.
- Every number is tied to an evidence file + field in `CLAIM_LEDGER.md`; no number is
  written from memory; refutations and negative results are reported, not hidden.

## What this study does (method)

1. **Instrument the matcher** — three graders: exact, semantic-tolerant, and a guarded
   revision (v3.3) that nests the exact one (so reverse flips are zero by construction).
2. **Measure one descriptive estimand** — the flip asymmetry D1 between
   exact-wrong/guarded-right (b) and exact-right/guarded-wrong (c). No significance
   test is run on D1: under nesting c=0 is a definitional tautology, so any McNemar
   p-value would be a tautology too. A procedural adjudication gate requires every
   flip to be judged before any calibration claim.
3. **Adjudicate** — 99 of 106 rows put to judges (102 flips + 4 probes).
4. **Cross-validate** — a blinded 25-item gold set, a 100-item stratified extension
   (90/100, κ=0.91), a retest reproducing the flip set, and a second-model arm.

## Key results (all from `CLAIM_LEDGER.md`, each traceable to an evidence file)

| Result | Value | Evidence |
|---|---|---|
| Paired comparisons, fifteen strata | **1062** (+412 regime-contrast excluded) | `results/merged_1062.json` |
| Adjudicated guarded accuracy | **922 / 1062** | `results/merged_1062.json` |
| Exact-match errors recovered by guard | **92 / 232 = 39.7%** (Wilson 33.6–46.1) | `results/merged_1062.json`, `results/guard_fn_R25.json` |
| Adjudication agreement | **99 / 106** | Methods (claim ledger) |
| Blinded gold set (25 items) | **24 / 25** (divergence G06) | `results/gold_guarded_agreement.json` |
| 100-item extension (author-graded) | **90 / 100** (88/100 adjudicated; all 62 flip rows agree) | `results/gold100_agreement.json` |
| Second rater agreement | **29 / 30, κ = 0.91** | gold100 grading pack |
| Guard false negatives (conservative direction) | **9** (make guarded accuracy a lower bound) | `results/guard_fn_R25.json` |
| Knowledge base (Obsidian) | 75 batch-review + 51 cards + 4 arXiv = **130** notes | `evidence/kb/` |

**Honest negative/refuted results (reported, not hidden):** temperature scaling gives
no consistent ECE repair (NLL down, ECE up); isotonic regression does not improve
held-out ECE (CV worse); a cross-domain loose-prompt layer shows the prompt-regime
contrast is question-type-dependent; BoolQ exact-zero is shown to be a *mapping
artifact* (a native-language mapping arm gives exact 15/60). These are all recorded in
`CLAIM_LEDGER.md` as verified claims, not silently dropped.

## What this study does **not** prove

- **No inferential claim on D1.** The nested construction makes c=0 a tautology; no
  significance is claimed on the flip asymmetry. The study is *descriptive*.
- **No claim of a general matcher.** The exact/guarded asymmetry is measured on
  short-answer QA; the cross-domain and BoolQ layers show it does **not** transfer
  uniformly (question-type-dependent; mapping-artifact-dependent).
- **No claim that the guard is complete.** The 100-item extension found 9 guard false
  negatives (plus one author slip H64); the guarded accuracy is a **lower bound** on
  semantic accuracy, not an estimate.
- **No population rate claim.** The 39.7% is a bounded descriptive rate on fifteen
  strata, not a target-population sample (see `results/guard_fn_R25.json`:
  `no_population_rate_claim: true`).
- **No publication-readiness of the manuscript** — it is under anonymous review;
  venue names are targets, not submissions.

## Repository layout

```
paper_workflow_kb/
├── paper/main.tex                # Manuscript (445 lines, TMLR style)
├── CLAIM_LEDGER.md               # Every claim → evidence file + field + status (85+ entries)
├── evidence_manifest.json        # Hash-locked evidence manifest (590 files PASS)
├── evidence/                     # Raw adjudication, judge, collection records
├── results/                      # Sealed JSON results (the recompute targets)
├── scripts/                      # 183 analysis/collection/seal/audit scripts
├── LITERATURE_REVIEW.md          # KB-grounded literature review (130-note pool)
├── KB_GROUNDING.md               # Obsidian KB snapshot grounding
├── MISSION_R27_29_REQUALIFICATION.md
├── STATE_SNAPSHOT.md             # Research state machine (hypothesis lifecycle)
├── SELF_ASSESSMENT.md            # TMLR four-dimension self-assessment (O2)
└── PREREG_R*.md                  # Pre-registration documents (R18/R26/R28-R32)
```

## Quick start

```bash
pip install -r requirements.txt     # numpy==2.5.2, scipy==1.18.1 (torch NOT required)

# 1. Verify the claim ledger: every claim's number is traceable to an evidence file
python3 scripts/verify_claim_ledger.py .

# 2. Reconcile the evidence manifest (hash-locked provenance)
python3 scripts/build_evidence_manifest.py . --verify evidence_manifest.json

# 3. Full acceptance gate suite (config-driven, 10 gates)
python3 scripts/run_acceptance_gates.py gates_config.json
```

## Reproduce every reported number

Every number in the manuscript and README is registered in `CLAIM_LEDGER.md` with its
evidence file + field and its "how to verify" recipe. The canonical recompute path:

```bash
# The ledger verifier is the single gate — it re-derives each claim's value from the
# evidence file and fails on any mismatch (0 FAIL required):
python3 scripts/verify_claim_ledger.py . --out reports/ledger.md

# A dedicated recompute script reproduces the abstract's headline arithmetic
# byte-for-byte (0.40 = 24/60, 43.3% = flip_rate, 0.25/0.65/0.6425/0.2425):
python3 scripts/recompute_r18_arithmetic_20261013.py
```

Most aggregate results are produced by a named `scripts/*.py` (each `verify_claim_ledger.py`
entry names the single script that recomputes it — e.g. `scripts/analyze_new60.py`,
`scripts/analyze_powrep.py`, `scripts/seal_theorems.py`). The `--seal` flag on these
scripts writes the result JSON; re-running it reproduces the file.

> **Provenance discipline.** No number in the paper is written from memory. Each one
> is either (a) a sealed JSON value in `results/` or `evidence/`, or (b) recomputed by
> a named script. The manuscript build (main.pdf) is not part of the recompute gate —
> the gate verifies the *numbers*, not the typesetting.

## Tests

The repo's "tests" are the acceptance gates and the self-contained audit scripts (there
is no pytest suite — the study's artifacts are sealed JSON + verifier scripts). Run:

```bash
python3 scripts/run_acceptance_gates.py gates_config.json   # 10 gates
python3 scripts/verify_claim_ledger.py .                     # claim-ledger 0 FAIL gate
```

> **Known working-tree state (honest):** the acceptance gates report **7/10 PASS** on
> the current working tree. The 3 FAILs are pre-existing conditions from later
> working-tree edits, not regressions introduced here:
> - **manifest hash reconciliation** — hash mismatches on files edited after the
>   manifest was sealed (CLAIM_LEDGER.md, paper/main.tex, LITERATURE_REVIEW.md, etc.)
>   plus one missing `data_r26/triviaqa-rc.tar.gz`;
> - **taint scan** — claim C85 references `results/merged_1062.json` which is present,
>   but the taint source `evidence/tainted.json` is absent so no taint is detected;
> - **R25 recount seal** — `scripts/seal_R25_numbers.py` asserts against adjudication
>   records whose working-tree state differs from the sealed baseline.
> These are **not** re-sealed or papered over: re-sealing the manifest would alter
> research evidence. They are reported as-is. The claim-ledger gate (`verify_claim_ledger.py`)
> passes (0 FAIL).

## Citation

Not yet publicly released (anonymous review). Cite the manuscript draft:
Liu, Z. (2026). *Label Matcher Choice Moves Measured Accuracy in Short-Answer QA: A
Stratified Descriptive Study with Adjudication and a Guard Patch.* Manuscript draft, TMLR.

仓库有两层内容，都来自同一项研究——**短答案 QA 中，label matcher（exact vs. tolerant/guard）的选择本身会移动测得的准确率**（"翻转"：exact 口径拒绝、guard 口径接受的行）。稿件为 `paper/main.tex`（TMLR 模板，标题 *Label Matcher Choice Moves Measured Accuracy in Short-Answer QA: A Stratified Descriptive Study with Adjudication and a Guard Patch*，附已编译的 `paper/main.pdf`）。

**论文工作流层**（方法论主体）：

- `CLAIM_LEDGER.md`：声明↔证据账本，82 条声明条目，每条绑定 evidence 文件与字段，状态分 draft / verified / inconclusive / blocked；负结果与 inconclusive 显式保留，不隐藏。
- `STATE_SNAPSHOT.md`：研究状态快照（假设生命周期、实验史、反思）。
- `PREREG_*.md`：8 份预注册（采样种子、提示词、gold 映射、判定规则先冻结，事后不改）。
- `ROUND_*.md`：33 份轮次记录（R0–R33，个别轮号无独立文件），含诚实披露的负结果与未达标轮（如 R30 的 O2 双模型重评未过双侧 8 分线）。
- `REBUTTAL.md`、`REVIEW_R1`–`REVIEW_R4/`：审稿回复与外部审阅记录。
- `reports/`：机器检查报告（引文、编译、合规、幻觉扫描、数字/统计一致性等）。
- `gates_config.json` + `scripts/run_acceptance_gates.py`：验收门禁（10 门）；`evidence_manifest.json`：证据清单哈希对账。

**实验层**：D2-60 起步（pilot + holdout 各 30）→ 云端新层与异源独立 judge → matcher 消融 → 温度缩放/等渗回归（均为负结果，照实封存）→ 预注册外部验证（TriviaQA-RC + EntityQuestions 各 200 题）→ 跨域（数学 40 题、英文单位 40 题）→ 功效复测（合并 n=720，McNemar p=3.81e-06）→ **BoolQ 公开是非臂** → 英文 Yes/No 臂（R32）。

预注册见 `PREREG_R30_BOOLQ.md`（先于任何采样冻结）：

1. **采样**：SuperGLUE BoolQ dev（`val.jsonl`，3270 行）按 gold 类分层取 50 True + 50 False，种子 `20260912`。样本封存于 `evidence/r30_boolq_sample.jsonl`。
2. **作答**：本地 ollama `qwen2:7b`（temperature 0），中文指令 + 英文短文，gold 映射冻结为 True→`是` / False→`否`。
3. **打分**：exact 与 guard v3.3 双口径；flip = exact 拒 + guard 受。
4. **裁决**：翻转行与拒行全部逐条人工裁决（语义等价标准；over-fire 计数），逐行包见根目录 `r30_flip_pack_boolq*.csv` / `r30_miss_pack_boolq*.csv`。
5. **封存**：`scripts/r30_seal_boolq.py` 唯一重算，结果 `results/r30_boolq_seal.json`。

主臂结果：exact 0、guard 55、flip 55（全部内容正确、over-fire 0）；拒 45 行普查：miss 31（`Yes.`/`No.` 句点变体）+ 正确拒 14；flip 率 0.55、miss 率 0.6889。第二模型臂（Amendment A2，`gemma3:4b`）：flip 45/99、miss 39/54，方向复现、量级更低；1 行采集超时如实披露、不进分母。结论：被 matcher 规则覆盖的是非变体（会/不会/yes/no）翻转、未覆盖变体（True/False）miss——数据集内判别检验成立（账本 C78/C82），描述性、不入 Holm、不做功效主张。

下表全部数字**逐字段取自 `results/*_seal.json` 与 `analysis_d2.py` 本机实跑输出**（2026-11-10 复算，脚本从冻结作答唯一重算并断言计数）；每行末列给出可复算来源：

| 实验 | n | exact 接受 | guard/tolerant 接受 | flips | flip 率 | over-fire | miss / 拒行普查 | 关键统计 | 来源（seal / 脚本） |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| D2-60 pilot（qwen2 本地） | 30 | 19 | 30 | 11 | 0.3667 | — | — | McNemar p=9.77e-04 | `analysis_d2.py` 实跑 |
| D2-60 holdout | 30 | 19 | 24 | 5 | 0.1667 | — | — | McNemar p=0.0625（NS） | 同上 |
| D2-60 pooled | 60 | 38 | 54 | 16 | 0.2667 | — | — | b=16/c=0，p=3.05e-05；ECE10 exact 0.3473 vs tolerant 0.0893 | 同上 |
| R26 外部 EntityQuestions（guard33） | 200 | 25 | 57 | 32 | 0.16 | 2 | miss 0/60 抽样 [0, 0.0602] | v34 候选：增量 0 | `results/r26_seal.json` |
| R26 外部 TriviaQA-RC（guard33） | 200 | 95 | 123 | 28 | 0.14 | 3 | miss 2/60 抽样 [0.0092, 0.1136] | v34 miss_drop=2 < 采纳线 5 → **负结果：不采纳 v34** | 同上 |
| R28 跨域·数学臂（退化空间） | 40 | 39 | 40 | 1 | 0.025 | 0 | — | 1 flip = `125.0` 数值格式变体；verdict REFINE | `results/r28_seal.json` |
| R28 跨域·英文单位臂（未覆盖） | 40 | 18 | 18 | 0 | 0.0 | 0 | miss 21/40 [0.375, 0.6706] | p_ii MET（判别条件成立） | 同上 |
| R29 功效复测（合并 6 层） | 720 | — | — | 19 | 0.0264 | 5（除法误差新类） | — | **McNemar 精确 p=3.81e-06**，b=19/c=0，H1 维持 | `results/r29_power_seal.json` |
| R30 BoolQ 主臂（qwen2:7b） | 100 | 0 | 55 | 55 | 0.55 | 0 | miss 31 + 正确拒 14（miss 率 0.6889 [0.5434, 0.8047]） | 判别成立 DISCRIMINATION HOLDS | `results/r30_boolq_seal.json` |
| R30 BoolQ 第二模型臂（gemma3:4b） | 99* | 0 | 45 | 45 | 0.4545 | 0 | miss 39 + 正确拒 15（miss 率 0.7222 [0.5911, 0.8238]） | 方向复现；*1 行采集超时披露、不进分母 | `results/r30_boolq_gemma_seal.json` |
| R32 英文原生 Yes/No（qwen2:7b） | 60 | 15 | 50 | 35 | 0.5833 [0.4573, 0.6994] | 0 | miss 0/10 | 原生 yes/no 也翻转 → 判别不限于中文映射 | `results/r32_enyesno_seal.json` |

负结果与未达标轮照实入表：R26 v34 未采纳、R28 数学臂 REFINE、R30 O2 双模型重评未过双侧 8 分线（见 `ROUND_R30.md`）；完整轮次史见 `ROUND_*.md` 与 `STATE_SNAPSHOT.md`。

```text
$ python3 scripts/r30_seal_boolq.py
{
 "n": 100,
 "n_exact": 0,
 "n_guard": 55,
 "n_flips": 55,
 ...
 "miss_rate": 0.6889,
 "verdict": "DISCRIMINATION HOLDS: covered yes/no synonym variants flip 55/55
 correct with zero over-fire; uncovered trailing-period variants miss 31/45"
}

$ python3 analysis_d2.py        # pooled 节选
"n": 60, "n_exact": 38, "n_tolerant": 54, "acc_exact": 0.6333, "acc_tolerant": 0.9,
"flip_rate": 0.2667, "mcnemar_b": 16, "mcnemar_c": 0,
"mcnemar_p_two": 3.0517578125000014e-05,
"ece10_exact": 0.3473, "ece10_tolerant": 0.0893
```

注：快速开始第 4/5 步在纯克隆环境按 README「环境绑定」说明会产生显式失败
（manifest 对账报 missing/hash mismatch、ledger 闸 exit 3 `CANONICAL_NOT_FOUND`），
这是设计内行为，不是脚本缺陷。

打分/封存/分析脚本基本为纯标准库实现；`requirements.txt`（numpy、scipy）仅部分数值脚本需要。以下命令均在仓库根目录执行，且已验证可跑：

```bash
# 0) 环境（可选，仅个别数值脚本需要）
pip install -r requirements.txt   # numpy==2.5.2, scipy==1.18.1

# 1) 复算 BoolQ 主臂打分（无需模型，读仓库内冻结的采集结果）
python3 scripts/r30_score_boolq.py

# 2) 复算 BoolQ 两臂封存（含 Wilson CI 与裁决对账，打印 verdict）
python3 scripts/r30_seal_boolq.py
python3 scripts/r30_seal_boolq_gemma.py

# 3) D2-60 主分析（exact vs tolerant + McNemar + ECE）
python3 analysis_d2.py

# 4) 证据清单哈希对账（见下方"环境绑定"说明）
python3 scripts/build_evidence_manifest.py . --verify evidence_manifest.json

# 5) 验收门禁（10 门；ledger 闸依赖仓外正本，纯克隆环境不完整，见下）
python3 scripts/run_acceptance_gates.py gates_config.json
```

- **模型采集依赖本机 ollama**：`scripts/r30_collect_boolq*.py` 等采集脚本请求 `http://localhost:11434`（`qwen2:7b` / `gemma3:4b`）。仓库只含冻结的采集产物；重采集需自备该环境。
- **ledger 校验正本在仓外**：`scripts/verify_claim_ledger.py` 是薄壳，向上级目录查找作者工作树中的正本实现；纯克隆环境会以 exit 3（`CANONICAL_NOT_FOUND`）退出，这是显式失败而非误报通过。
- **manifest 对账是作者完整工作树口径**：`evidence_manifest.json` 覆盖含 `*.bak`、重型语料等未上传文件，仅对仓内子集运行会报 missing/hash mismatch——仓库是投稿工作流的阶段性快照，部分根目录文档在作者机上比仓内版本更新。
- **外部数据集不随仓分发**：`data_r26/` 仅保留 SHA-256 与来源说明（TriviaQA-RC、EntityQuestions 官方包过大，重采样需自行放置官方包）；`data_boolq/BoolQ/` 为 SuperGLUE BoolQ 官方包解包，SHA 锁定见 `data_boolq/SHASUMS.txt`。
- **知识库快照**：`evidence/kb/` 是作者 130 篇 Obsidian 文献库的冻结快照（见 `KB_GROUNDING.md`），源库不入仓。
- **论文编译**：`paper/` 需 XeLaTeX + Noto Serif CJK SC 字体（`main.tex` 使用 xeCJK 渲染中文示例）。
- 部分历史 evidence/results 文件按字节原样保留，内含作者机绝对路径（`anc/README.md` 有披露表）。

```
paper/                 TMLR 稿件（main.tex/main.pdf/main.bib + tmlr 模板）
scripts/               200+ 脚本：采样/采集/打分/裁决/封存/门禁/扫描（每条声明一个唯一重算脚本）
evidence/              冻结证据：冻结样本、原始作答、裁决、独立 judge 输出、知识库快照
results/               打分与分析结果、各轮 seal JSON、逐行作答 jsonl
reports/               机器检查报告（引文/编译/合规/幻觉/数字一致性等）
data_boolq/            SuperGLUE BoolQ 官方包解包（val/train/test.jsonl）+ SHASUMS
data_r26/              外部数据集来源与 SHA-256（档案本身不入仓）
anc/                   按 CLAIM_LEDGER 指针逐字拷贝的伴随工件（见 anc/README.md）
REVIEW_R1–R4/          外部审阅记录
CLAIM_LEDGER.md        声明↔证据账本（82 条）
STATE_SNAPSHOT.md      研究状态快照
PREREG_*.md            8 份预注册
ROUND_*.md             33 份轮次记录
REBUTTAL.md            审稿回复
gates_config.json      验收门禁配置（10 门）
evidence_manifest.json 证据清单（哈希对账）
r30_*_pack_*.csv 等    BoolQ/TriviaQA/EntityQuestions/Yes-No 逐行裁决包
gold*/grades_*         人工盲评包与回收评分
```

- 结果以各 `results/*_seal.json` 为准：seal 脚本从原始作答唯一重算并断言冻结计数，数字一律可追溯到账本条目（`CLAIM_LEDGER.md` 的"证据文件+字段"列）。
- 根目录 `*_pack_*.csv` 是给人看的逐行裁决包（翻转行/拒行），对应机器裁决结果在 `results/*_adjudication_*.json`。
- 失败路径照实保留：采集超时/模型失格等以 `error` 字段记录在 jsonl 中，不删除、不插补。

MIT（见 `LICENSE`）。
