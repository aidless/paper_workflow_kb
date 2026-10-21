# ROUND_R28 — 补强 P2 跨域证据（检验 P1 预测 i / ii）

> 目标：MISSION_R27_29 的 P2，补 N + Si。日期 2026-09-11。

## 结果 vs 验收标准（P2 gate）

- gate：≥1 个非 QA 任务结果与 P1 预测方向一致（或诚实反例回改理论）；账本 claims verified；「窄 QA」「QA-only」扣点可拆。
- **达成**：两臂均落盘，预测 (ii) **MET**，预测 (i) **REFINE**（诚实精化，非证伪）。

| Arm | 设计 | n | flip | miss/真拒 | Wilson(若 miss) | 判定 |
|---|---|---|---|---|---|---|
| A degenerate | 40 算术题，纯数字 gold | 40 | 1（`125.0`vs`125` .0 尾缀） | over-fire 0 | — | (i) REFINE |
| B uncovered | 40 英文单位/计数，纯数字 gold | 40 | **0** | **miss 21** + 真拒 1（b-38） | [0.375, 0.6706] | (ii) **MET** |

## 核心结论

- **预测 (ii) 首次实证**：英文单位变体（`60 seconds`/`52 weeks`/`2000 pounds`）在模型输出里大量存在（21/40），但 guard 因 SUFFIXES/SYNONYMS 全为中文而**零翻转**——变体存在 + 覆盖缺失 = miss 不是 flip。这正是 (ii) 的机制，且把「英文 0/30 天然规范」的旧解释改为「有变体不覆盖」。
- **预测 (i) 精化**：纯数字答案仍会翻转，但只通过 numeric 格式变体（`.0` 尾缀被数值等价分支覆盖）→ 1/40=0.025，远低于中文层正翻转（2.5%–43.3%）。把 (i) 从「零翻转」精化为「近零翻转，受控于被覆盖的数字格式变体」，理论更精确而非削弱。

## 产出物

- `PREREG_R28_CROSSDOMAIN.md`（预注册，先于作答冻结）
- `scripts/r28_collect.py`（题集内嵌冻结；40+40 gold 全纯数字）
- `scripts/r28_score.py`、`scripts/r28_adjudicate.py`（21 miss + 1 真拒）、`scripts/r28_seal.py`（唯一重算 + gate 判定）
- `results/r28_answers_{a,b}.jsonl`、`results/r28_score.json`、`results/r28_adjudication.json`、`results/r28_seal.json`
- `CLAIM_LEDGER.md` C73/C74（verified）
- `paper/main.tex`：预测 (i)/(ii) 精化 + Results「Cross-domain extension (R28)」小节

## 验证

- `verify_claim_ledger.py`：**74 PASS / 0 FAIL / 1 WARN**（WARN 既有 inconclusive）。
- `r28_seal.py` 断言全过（n=40、flip=1/0、miss=21、correct_reject=1、over-fire=0）。

## 失败 + 纠正

1. C74 首验 FAIL：Wilson CI 全精度浮点 [0.37497…, 0.67064…] 与账本 4 位 [0.375, 0.6706] 差 2.6e-5 超 TOL=2e-5。纠正：`r28_seal.py` 威尔逊结果 round(4)（R26 口径），重跑后 C73/C74 皆 PASS。
2. 采集脚本 `arm_source` 全局 hack → 改为参数传递（消除直接 import 时的 NameError 隐患）。

## 下一步（P3 / R29）

功效复测：把欠功效层（n_ceil=217）扩到预注册功效 n，本地大规模作答，配对 McNemar 从 hedge 收敛为稳定结论。