# paper_workflow_kb

[![CI](https://github.com/aidless/paper_workflow_kb/actions/workflows/static-checks.yml/badge.svg)](https://github.com/aidless/paper_workflow_kb/actions/workflows/static-checks.yml)

> **English TL;DR**: A complete research workbench for a TMLR submission studying whether the choice of label matcher (exact vs. tolerant/guard) shifts measured accuracy in short-answer QA, including a BoolQ yes/no arm. It ships an 82-entry claim-to-evidence ledger, preregistrations, round records with disclosed negative results, frozen captures, and 10 acceptance gates; rerun seals such as `python3 scripts/r30_seal_boolq.py` without a model. Honest boundaries are explicit: fresh collection requires a local ollama, and the canonical ledger check lives outside the repository.

一篇 TMLR 在研稿件的完整科研工作台：声明账本、预注册、冻结证据、封存结果与验收门禁，外加 SuperGLUE BoolQ 公开数据集上的是非问答（yes/no）实验臂。

## 这是什么

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

### BoolQ 实验（R30 主臂 + R32 Amendment A2 第二模型臂）

预注册见 `PREREG_R30_BOOLQ.md`（先于任何采样冻结）：

1. **采样**：SuperGLUE BoolQ dev（`val.jsonl`，3270 行）按 gold 类分层取 50 True + 50 False，种子 `20260912`。样本封存于 `evidence/r30_boolq_sample.jsonl`。
2. **作答**：本地 ollama `qwen2:7b`（temperature 0），中文指令 + 英文短文，gold 映射冻结为 True→`是` / False→`否`。
3. **打分**：exact 与 guard v3.3 双口径；flip = exact 拒 + guard 受。
4. **裁决**：翻转行与拒行全部逐条人工裁决（语义等价标准；over-fire 计数），逐行包见根目录 `r30_flip_pack_boolq*.csv` / `r30_miss_pack_boolq*.csv`。
5. **封存**：`scripts/r30_seal_boolq.py` 唯一重算，结果 `results/r30_boolq_seal.json`。

主臂结果：exact 0、guard 55、flip 55（全部内容正确、over-fire 0）；拒 45 行普查：miss 31（`Yes.`/`No.` 句点变体）+ 正确拒 14；flip 率 0.55、miss 率 0.6889。第二模型臂（Amendment A2，`gemma3:4b`）：flip 45/99、miss 39/54，方向复现、量级更低；1 行采集超时如实披露、不进分母。结论：被 matcher 规则覆盖的是非变体（会/不会/yes/no）翻转、未覆盖变体（True/False）miss——数据集内判别检验成立（账本 C78/C82），描述性、不入 Holm、不做功效主张。

## Results（实验结果汇总）

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

### 快速开始实测（2026-11-10，纯克隆环境）

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

## 快速开始

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

### 环境绑定与诚实边界

- **模型采集依赖本机 ollama**：`scripts/r30_collect_boolq*.py` 等采集脚本请求 `http://localhost:11434`（`qwen2:7b` / `gemma3:4b`）。仓库只含冻结的采集产物；重采集需自备该环境。
- **ledger 校验正本在仓外**：`scripts/verify_claim_ledger.py` 是薄壳，向上级目录查找作者工作树中的正本实现；纯克隆环境会以 exit 3（`CANONICAL_NOT_FOUND`）退出，这是显式失败而非误报通过。
- **manifest 对账是作者完整工作树口径**：`evidence_manifest.json` 覆盖含 `*.bak`、重型语料等未上传文件，仅对仓内子集运行会报 missing/hash mismatch——仓库是投稿工作流的阶段性快照，部分根目录文档在作者机上比仓内版本更新。
- **外部数据集不随仓分发**：`data_r26/` 仅保留 SHA-256 与来源说明（TriviaQA-RC、EntityQuestions 官方包过大，重采样需自行放置官方包）；`data_boolq/BoolQ/` 为 SuperGLUE BoolQ 官方包解包，SHA 锁定见 `data_boolq/SHASUMS.txt`。
- **知识库快照**：`evidence/kb/` 是作者 130 篇 Obsidian 文献库的冻结快照（见 `KB_GROUNDING.md`），源库不入仓。
- **论文编译**：`paper/` 需 XeLaTeX + Noto Serif CJK SC 字体（`main.tex` 使用 xeCJK 渲染中文示例）。
- 部分历史 evidence/results 文件按字节原样保留，内含作者机绝对路径（`anc/README.md` 有披露表）。

## 仓库结构

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

## 数据与结果说明

- 结果以各 `results/*_seal.json` 为准：seal 脚本从原始作答唯一重算并断言冻结计数，数字一律可追溯到账本条目（`CLAIM_LEDGER.md` 的"证据文件+字段"列）。
- 根目录 `*_pack_*.csv` 是给人看的逐行裁决包（翻转行/拒行），对应机器裁决结果在 `results/*_adjudication_*.json`。
- 失败路径照实保留：采集超时/模型失格等以 `error` 字段记录在 jsonl 中，不删除、不插补。

## License

MIT（见 `LICENSE`）。
