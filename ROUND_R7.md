# ROUND_R7 — goal第七轮：第二题型家族（云端数学40）＋第五次O2（2026-09-07）

## 新证据

1. cloud-math（scripts/cloud_math40.py → evidence/cloud_math40_raw.json，
   scripts/analyze_math40.py → results/{math40,analysis_410}.json，C30）：
   云端 qwen2.5:7b temp0，40/40 无错无空；exact=guarded=37/40=0.925；
   零翻转 → McNemar 退化（b=c=0，p=1.0，披露）；等宽分箱 ECE 0.025 双基准一致；
   H1 在本层不支持（0.0）：纯数字题无单位/同义/名称抓手，现象具题型依赖。
   G006 零翻转免裁决；功效上限零不一致对无从计算，未代入假设效应。
2. N=410（220 QA 七层 ＋ 190 校准行）；合并描述 349/378/29（0.8512/0.922/0.0707）。
3. 手稿七层同步：标题/摘要/导言交付段/贡献(vi)/数据快照/功效段/表新行/数学段/
   合并段/许可段/局限/附录指针；快照 H1c 边界证伪、N=410 登记。

## 第五次O2（落定：R1-strict-r5 7.9 vs R2-r5 5.35，UNSTABLE）

- R2-r5：qwen3:4b 四连失格（prose无JSON），改 deepseek-r1:7b 一次成功：
  N4/S6/Si5/C8（5.35；post-think JSON；`evidence/rater2_r5.json`＋raw log）。
- R1-strict-r5：7.0/8.0/8.5/9.0（7.9；数学边界未实质移分，照实保留）。
- 精确一致 0/4，|Δ|=2.55 → UNSTABLE；8分线仅 C 双侧达线。
- 五轮独立侧：5.8/7.2/5.9作废/8.8/5.35；R4 的 8.8 确认为上离群；
  独立 N 硬顶 7.5（中位4–5.5）、S 硬顶 9.0（中位6–7.5）。
- 数学边界未移动独立 N（rater读作复现瑕疵）：N出路仅剩理论化或跨域立项；
  S出路需人工金集或大批量复测。详见 SELF_ASSESSMENT.md（五轮版）。

## 门禁（手稿同步后终态，O2前）

- ledger 30/0/1 WARN；numbers 8条（4既有＋4数字邻近误报，已审计：0.1255/0.125、
  0.0037/0.0039、0.125/0.1255、0.0/0.0010 皆不同量纲邻近）；stats/style/taint/hallu/TMLR全绿；
- PDF 重编 0 error；provenance 已记；manifest+gates+投稿包（n410）见封存节。
