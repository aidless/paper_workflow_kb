# ROUND_R4 — goal第三轮：等渗+第四层+第三次O2（2026-09-07）

## 新证据

1. 等渗回归（scripts/isotonic.py → results/isotonic.json，C21）：手写PAV+5折CV；
   pilot单块退化；holdout样本内-0.0107但CV 0.2552；cloud样本内-0.0043但CV 0.1991且CV NLL恶化；
   负结果，以CV为准。
2. 第四层local-new（qwen2:7b同60题）：采集scripts/local_new60.py（qwen3:4b首采失败：
   思考模式60空回，文件已删，改qwen2:7b一次成功，60/60零error）→
   evidence/local_new60_raw.json（5行无置信度）；分析scripts/analyze_local60.py →
   results/{local_new,flips_local60,analysis_180,power_local60}.json（C22）：
   exact 48/60=0.8，guarded 53/60=0.8833，5翻转0.0833，McNemar p=0.0625 ns，
   ECE 0.1255→0.0345（等宽分箱，55行），n_ceil=217；合并180：134/159/25（0.1389），仅描述。
3. 在会话裁决5/5（evidence/local_adjudication.json，C23）；
   qwen3:4b独立judge失败（单字指令复述，输出弃置）；local_judge.py保留作失败仪器记录。
4. 手稿四层同步：标题N=180、摘要/导言/方法（local层+分箱披露+功效217×2）/结果（表新增行、
   local段、守卫段重框、合并180、温度/等渗段）/讨论/局限/未来/附录；STATE_SNAPSHOT同步
   （H4证伪、N=180、instrument教训）。
5. 数字扫描新增注记1条（表0.1255 vs 正文McNemar p=0.125，不同量纲既有类，第4条）：
   可读性优先保留， acceptance门为report-only，保持绿。

## 第三次O2（四层稿）

- qwen3:4b两次失格（无JSON+任务幻觉；拒答占位），已落盘为失败记录。
- deepseek-r1:7b一次成功：N4/S6/Si7/C8（加权5.85），分数行逐字验证；
  R1-strict：5.5/7.0/8.0/8.5（加权7.0）。精确一致0/4，|Δ|=1.1 → UNSTABLE。
- 三轮R2：5.8→7.2→5.9；独立侧N≤5.5、S≤7.5天花板明确。8分线：仅C双模型达线。

## 门禁（终态见封存命令输出）

- ledger 23/0/1 WARN；gates 9/9；manifest 107+（重建）；numbers report-only（4注记同类）；
  stats/style/taint/hallucination/TMLR全绿；C1–C7全PASS（n180包）；PDF重编0 error；provenance已记。
- compile静态4E仍模板宏误报（权威实编0 error）。

## 下轮

- 用户资源项：judge金集/功效复测/理论化三选一（见SELF_ASSESSMENT§8分线判定）。
- 自主项：local-new独立异源确认的可合规judge（deepseek-r1作judge？其已作R2终评，再作裁决judge有角色重叠，需披露）。
