# ROUND_R6 — 云端迁移：全量重算 14/14 复现＋judge 确认（2026-09-07）

## 执行（seetacloud-h3，RTX 3090，python 3.10+scipy，模型 qwen2.5:7b/1.5b）

1. 打包 236 KB（去 submission/pdf/pycache）上传；云端解包重跑全部重算脚本。
   初跑 2 失败系工作目录（analyze_new60/ablation 需 workspace 根跑），重跑全绿。
2. 云端 judge 确认（新脚本 scripts/cloud_confirm_judge.py，就地写 evidence/cloud_judge_confirm2.json，
   封存文件只读）：qwen2.5:7b temp0 原 prompt 重裁 21 翻转 → 16/16＋4/5（O/O2 判错），零偏离。
3. prompt 敏感事件：缩写 prompt 版曾使 pilot-30 翻为 incorrect；原 prompt tie-break 3/3 CORRECT。
   系 prompt 敏感非模型不稳定；确认文件为原 prompt run。全程披露。
4. 字节对账：13/14 直接一致；ablation.json 不一致暴露其非脚本自举（n_* 顶层键系旧手工产物）。
   修复：脚本补规范顺序 n_* 键 → 本地重跑与封存字节一致 → 上云重跑三地一致。
   analysis_120 哈希抄写笔误经文件直传 diff 纠正（文件本就一致）。终态 14/14（results/cloud_repro.json）。
5. 落账 C28（14/14）/ C29（21 确认＋prompt 事件）；手稿 Methods 加两句（确认＋复现），数字零改动。

## 门禁（终态）

- ledger 29/0/1 WARN；gates 9/9；manifest 见终检；stats/style/taint/hallu/TMLR 全绿；
- numbers 表述对账 8 条逐条审计全为数字邻近误报（2609 双 ID、0.0/p=1.0 vs p=0.0010、
  p=0.0039 vs ECE 0.0037、p=0.125 vs ECE 0.1255×2、0.8/0.80、0.05 阈值 vs ECE 0.0492）；
- C1–C7（submission_tmlr_n370.zip）全 PASS；PDF 重编 0 error。

## O2 说明

本轮为 corroboration-only（数字零改动，N 故事不变），未重跑 O2。
8 分槽位维持 6/8（N 双侧未达线）； blocker 仍为 N（理论化/第二题型家族）。
