# ROUND_R19.md — REVIEW_R4回应＋修复轮（R19 P2）

## 审稿到达（R4-R1：C0/M5/m11/n1；去重4唯一Major）
1. hetero ECE指针（R1-M＋R2-m＋R3-m＋R4-n同源）→ E6/E7/E7b/E14：一处修复关闭四角色。
2. GOLD-100 58/58分母（R5-M真发现）→ E3/E11＋C58订正为55/55（3排除一致具名）＋C59。
3. 摘要GOLD-25误列lr18-42（R6-M＋R7-M同源，高置信）→ E2。
4. 摘要fail-to-repair绝对化（R6-M）→ E4（no consistent repair＋阳性例外）。
5-12. Minors/Nit：hetero混口径注（E7）、guard注记中性化＋hr18笔误（G3，重跑数字全同）、headline嵌套限定（E1/E5）、Holm具名排除（E12）、lr18-46 four（E10；审稿“两处”半误，单改）、five定义＋pilot carve-out（E9a/E9b；附带收紧fails everywhere→both informative）、摘要grader限定（E3）、BI四类风险（E13）。

## 验证
- verify_r4_response.py 14/14（numbers轴）；fidelity轴逐条对原文。
- 验收门9/9；manifest 312/0/0；账本59 claims（C59新增，taint clean）。

## 成本表
| 轮次 | 角色数 | 模型调用数 | 缩减？ | 触发依据 | 备注 |
|---|---|---|---|---|---|
| R4-R1 | 8（7扇出＋R8主审） | 7 workflow＋主审语义核验 | 否（默认全量；R18大改后首轮） | — | C+M=5，defect-dense |
| R4-R2 | 8（7扇出＋R8主审） | 7 workflow＋主审caption复验 | 否（保持；首轮C+M=5不满足缩减条件） | C+M=5＞1 | 闭环验证轮：只验关闭＋改动域新扫 |

## no_code消融
- 未做（本轮为修复验证轮；稿件正文关键数字/方法/基线均在正文内可核，R3轮已确认正文自足；记为deferred，不阻塞）。

## O2-r10（R19 P4）
- R1-strict先落盘（8.0/9.5/9.0/9.5，加权8.925→8.9；Si 9.0凭hetero＋GOLD-100＋R4新证据恢复r8水平，规则7；N/S/C维持亦凭无新证据类别则不升）。
- R2 deepseek-r1:7b本地temp0（rater2_r10对称严格prompt）：8.5×4，加权8.5；理由泛化（四维同模板"negative findings"，与正文多处负结果矛盾），分辨力记低；直接JSON无think（与r6-r9同模式）。
- Agreement：精确一致0/4，|Δ总分|=0.4；两模型未经校准（无同分布gold set，不硬启）→ UNSTABLE-adjacent。
- 8分线：双侧全≥8（N 8.0/8.5、S 9.5/8.5、Si 9.0/8.5、C 9.5/8.5），R8后第二次达成（noisy pass，分数不是结论）。
- 落盘：evidence/rater1_r10.json、rater2_r10（prompt/raw/json）、SELF_ASSESSMENT r10、rounds_consistency.jsonl（r5-r10回填，均为0.0）。
- 额外调用：R4-R2 workflow 7＋ollama R2 1次（后台job bash-1，exit 0）＋R1-strict主审1。
