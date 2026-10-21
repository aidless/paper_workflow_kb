# ROUND_R9 — A+B 立项轮：P0/P1/P2/P3（2026-09-07）

## P0 matcher v3.2（PASS）
- `scripts/label_match_v32.py`（v3.1只读未动）：空守卫加raw回退。
- `results/guard_v32.json`：470行回归diff=0，U1–U5全过。
- 诚实注记：diff=0＝零影响，不包装成修复。

## P1 形式理论（PASS）
- `results/code_pilot.json`：v3.1下exact12/guarded11/c一例；v3.2下12/12闭合。
- 账本C34/C35/C36；手稿Methods规则段＋Discussion理论段＋Limitations hedge。
- 校验器语法坑三处（数值格版本串/`file ->`前缀/tid负数解析），已修。

## P2 跨域新层（PASS）
- tight 1/60（p1.0 ns）vs loose 20/60（b20c0，p1.9e-6显著），同60题。
- 异源裁决deepseek-r1:7b：首轮16/3/2，泄露归因有对照；第二轮5/5；内容21/21。
- 账本C37/C38；手稿N=530九层50翻转全同步；v3.1=v3.2在120行零差异。

## P3 第七次O2（落定：R1-strict-r7 8.7 vs R2-r7 7.65，UNSTABLE）
- R1：8.0/9.0/9.0/9.0（N＋1.0凭理论＋跨域真实增量，S＋0.5凭第二裁决家族；Si/C维持）。
- R2：6.5/7.5/8.5/9.5（理由绑定好转但harsh回摆，R6 8.6→R7 7.65）。
- 精确一致0/4（|Δ|=1.5/1.5/0.5/0.5）→ UNSTABLE。
- 8分线：N✗（R2 6.5）/ S✗（R2 7.5）/ Si✓✓（9.0/8.5，第一次双侧过线）/ C✓✓。**未达成，不封存**。

## 门禁（终态实测）
- ledger 38 PASS / 0 FAIL / 1 WARN（C08既有）；gates 9/9；manifest 188条重建对账。
- compile_gate静态降级FAIL既有（新增行零ref/cite/label，已验）。

## 诚实结论
Si由跨域显著关闭；N/S差的是数学理论＋功效层（R2理由点名：跨层不一致、欠功效、
描述性无定理）。下一立项包：功效复制（欠功效层增n至ceil）＋数学理论化。
Autonomous部分到此为止，等立项。
