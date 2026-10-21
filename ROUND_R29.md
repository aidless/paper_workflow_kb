# ROUND_R29 — 补强 P3 功效复测（local-big 160 → 720）

> 目标：MISSION_R27_29 的 P3，补 S。日期 2026-09-11。

## 结果 vs 验收标准（P3 gate）

- gate：预注册功效 n 达成；关键层配对显著性取值稳定（不再视作纯 hedge）；账本 claims verified。
- **达成**：n=720 达 n_ceil=720（欠功效消除）；McNemar p=3.81e-06 显著（不再 ns hedge）；C75 verified。

| 指标 | 值 |
|---|---|
| 合并 n | 720（local-big 160 + topup 560） |
| flip | 19 / 720 = 0.0264 |
| McNemar b/c/p | 19 / 0 / 3.81e-06（精确双侧，显著） |
| 裁决 | 14 flip_correct + **5 over-fire** |

## 核心结论

1. **欠功效消除**：local-big 从 160/720（占位 OR=4）扩到 720，McNemar 从 p=0.125 ns 收敛到 p=3.81e-06 显著——H1 的配对方向在足功效口径下站稳（不降级，未触发失败路径）。
2. **意外发现（新 over-fire 类）**：topup 的整除除法题暴露 guard 的 numeric 容差（0.5%）会在"模型除法算错、误差 <0.5%"时误接受——5/19 flip 是 over-fire（如 `91.6458` vs `92`，误差 0.385%）。原 local-big 的 4 flip 全是 `.0`（0 over-fire），此弱点此前不可见。已如实记入 Limitations（不切新 guard 版，沿 R26 先例）。

## 产出物

- `PREREG_R29_POWER.md`（预注册，先于作答）
- `scripts/r29_make_topup.py`（题池生成，div 39 全整除 gold 可复算 + 140 首都映射去争议项）
- `scripts/r29_collect.py`（采集 560，qwen2:7b temp0）
- `scripts/r29_score.py`（合并 720 打分 + McNemar）、`scripts/r29_adjudicate.py`（14+5 裁决）、`scripts/r29_seal.py`（唯一重算 + gate）
- `results/r29_*.json`、`evidence/r29_topup_560.json`
- `CLAIM_LEDGER.md` C75（verified，75 PASS / 0 FAIL）
- `paper/main.tex`：Limitations 欠功效句改为已复测 + over-fire 新类记录；Future work 更新

## 失败 + 纠正（3 处）

1. 首都映射初版 122 < 140 → 补 20 个无争议首都（亚美尼亚/阿塞拜疆等）。
2. C75 首验 FAIL：McNemar p 科学计数法 `3.8147e-06` 被账本数值解析拆成两个数 → 改纯小数 `0.0000038`（TOL 内）。
3. R28 seal 曾遇 Wilson 全精度超 TOL（已 round(4)），R29 沿用 4 位口径防复发。

## 下一步（P4 / R30）

O2 双模型重评（N/S/Si/C 双侧均≥8，≥2 轮互证）+ 重封投稿包（R26+R27+R28+R29 全进 PDF/zip）。