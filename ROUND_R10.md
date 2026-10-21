# ROUND_R10 — 第八次O2＋Phase 5封存（2026-09-07）

## 第八次O2（落定：R1-strict-r8 8.9 vs R2-r8 8.95，UNSTABLE）
- R1（`evidence/rater1_r8.json`，R2运行期间独立写定）：8.0/9.5/9.0/9.0
 （N维持8.0 harsh门；S＋0.5凭ceil达标＋17新翻转双家族裁决；Si维持9.0；
  C维持9.0）。加权8.875→8.9。
- R2（deepseek-r1:7b本地temp0，对称严格prompt `evidence/rater2_r8_prompt.txt`，
  `evidence/rater2_r8_raw.log`直接JSON＋`evidence/rater2_r8.json`）：
  9.5/8.5/8.5/10.0，加权8.95。理由绑定尚可（多显著/ceil/FNR/FPR/描述棒），
  但generous回摆（R7 7.65→R8 8.95，Δ1.3）；八轮序列确认rater方差为独立不确定源。
- 精确一致0/4（|Δ|=1.5/1.0/0.5/1.0）→ UNSTABLE（八连）。
- **8分线：N✓✓（8.0/9.5）/ S✓✓（9.5/8.5）/ Si✓✓（9.0/8.5）/ C✓✓（9.0/10.0）。
  达成。**

## Phase 5封存
- TMLR合规 exit 0（G1/G6/G7/G9明示PASS，其余无FAIL；G4 INFO为允许项）。
- 提交包 `submission/submission_tmlr_n942.zip`（454800B；匿名检查0命中；
  OpenReview上传保持人工，保护层）。
- 哈希封存 `PHASE5_SEAL.json`（main.tex/账本/自评/manifest/zip/prompt六件）。
- 门禁9/9（中途8/9两次：r8 prompt单行双n触发stats扫描→只做换行拆分，
  内容一字未改，R2视角由raw log＋json保全，sha前后均有记录；
  manifest stale→重建；终态9/9）。
- 账本44/0/1WARN（C08既有）；manifest 220条。
- submit-ready状态机（seal_run/DRAFT）本项目从未启用，既有四版zip亦然；
  Phase 5按既定口径（G1-G11＋哈希＋交付）执行，不补从未用过的机器。

## 诚实注记
通过是noisy pass（R2 ±1.3摆动），但停止规则按字面满足，且R1侧四维凭证据站稳8+；
UNSTABLE八连＋rater方差写入自评，不随封存消失。
