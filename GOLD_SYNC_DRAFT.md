# 手稿同步草稿（GOLD 解盲轮用，不直接改 paper/）

> 本文件是解盲轮的施工单：retest 段数字已定可直接用；gold 段为骨架，
> 待 `analyze_gold.py` 跑出真数后填空。真正改 `paper/main.tex` 时走
> paper-writing-agent Phase 4 修改轮（ROUND 记录 + 四扫重跑）。

## R1：retest 稳定性段（数字已定，C32）

- 云端 test-retest（同 60 题、同模型 qwen2.5:7b、同 prompt/temperature 0）：
  exact 字串一致 59/60（0.9833），guarded 一致 60/60（1.0），
  翻转集合 test/retest 5/5 同一集合，McNemar 退化（b=c=0，p=1.0，披露），
  置信平均绝对漂移 0.0107。
- 唯一字串差异（光速题）：`300000`/0.9 → `299792.458`/0.458，同为
  exact 错/guarded 对，翻转状态不变，C16 裁决延续；置信漂移离群（0.442，
  占均值漂移大部）照实披露。
- 证据：`results/retest60.json`（`analyze_retest.py` 唯一重算）。

## R2：gold 金集段（骨架，待填真数）

- GOLD-25 盲化设计：14 条全翻转普查（含题干）＋ 11 条 seeded 抽样（无题干，
  存疑出口），顺序打乱，判词零泄露，映射密封（`evidence/gold_key.json`）。
- 解盲结果（待填）：一致率 ___/___（存疑___条单列），Wilson 95% CI ___，
  有题干 ___/14 vs 无题干 ___/11。
- 若一致率 ≥0.90：S 校准主张得金集支撑，单评局限（C23/C27）部分关闭，
  但仍保留"金集即翻转富集stub，非随机抽样"边界句。
- 若一致率 <0.90：逐条列 disagreement，明确定位 judge 规则偏差，
  S 降级为 hedge，不冲 8 分线。
- 对照组说明：exact 非翻转条目作答与参考逐字相同，对 overturn 质量零信息量，
  故未占名额（分析计划预注册已披露）。

## R3：解盲轮施工清单（按序）

1. 用户判定串 → 填入 CSV → `analyze_gold.py` → `results/gold_agreement.json`。
2. 账本 C33（gold 一致率真数）→ manifest 重建 → gates 重跑（须 9/9）。
3. 按本草稿 R1/R2 改 `paper/main.tex`（Phase 4 修改轮）→ 四扫（数字一致性/
   写作风格/TMLR 合规/账本验证）→ PDF 重编 0 error。
4. 第六次 O2（对称严格：R1-strict + R2 新模型）→ 判 8 分线。
5. 封存：submission 包刷新（n410→含 gold/retest 描述以稿为准）→ C1–C7 全 PASS。
