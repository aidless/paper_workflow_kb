# ROUND_R22 — guard v33 promotion＋对抗负例＋纸面联动

## 到达记录
- R21 已封存（manifest 347/0/0，验收门 9/9）；goal-8f8dffb2 round 2 内起 R22（MISSION R21-D4 promotion 留本轮）。
- 用户指令"继续"（全做路线图 R22→R23）。

## 改动
1. **P1 全局 diff**（scripts/guard_v33_global_diff.py → results/guard_v33_diff.json）：
   20 文件 1700 对只读，首版 9 diff 含 1 OTHER（code-pilot-04 `//` vs `//`）→ 定位为
   pre-experiment 转写漏 v3.2 raw-fallback（密封回归 U1），补回后 **8 diff 全单字 CJK 类、
   0 OTHER，PROMOTE-GO**。返工 1 次（L1009 候选）。
2. **P2a 转正**（scripts/label_match_v33.py＋scripts/seal_v33.py → results/guard_v33.json）：
   v31/v32 不动；13 断言全过（R1-O/O2 拒、R2 双名锚、R3-U1、R4-U4、R5 否定三行、
   R6-4 singles 拒、R7-1700 对零转写漂移）。
3. **P2b/c 消费者切换**：layer() 单点切 v33（xdomain 内容字节全同，仅 matcher 标签变）；
   r18（raw 27→26，b27→b26，p 1.49e-08→2.98e-08，ece 0.1925→0.2092）与 hetero
   （raw 11→8，b11→b8，p 0.00098→0.0078，ece 0.3310→0.3810）重算；
   两 adjudication 裁决口径全不变（24/39/0.65/0.2425 与 8/29/0.4833/0.381；
   raw 26/8、excluded {54,55}/{41,42,45}）；merged 830/922/92 不变；
   Holm 族（adjudicated 口径）与 hetero-19 敏感性（b=8，claim_holds）不变；
   GOLD key 4 行审计 promotion＋decode **90/62/62/88**（adjudicated 88 不变）；
   guard_synth v33 化：C 类 8/8 拦截（旧 limitation 转实测 fix）、excluded 6 行 2 接受、
   v32→v33 差异 11/130 全单字类；build_gold100 冻结 v32（历史选择不可重建性已声明，
   key/pack 文件不动已验证）。
   不变性论证：全局 diff 覆盖全部 sealed raw（powrep/xdomain/ece/pilot 等零 diff 行），
   未重跑项以覆盖论证记录，ece_unified 仅 r18 basis 标签变（值 0.65/0.2425 不变）。
4. **P3 对抗负例**（scripts/local_judge_adversarial.py → evidence/adversarial_neg_verdicts.json，
   20 对×3 本地 judge，60/60 零 ERROR；人类 gold 为封存作者标定 F/C 类）：
   gemma3 FPR **0.9**（18/20：公式 11＋CJK 7，disqualified）、qwen2 FPR 0.35
   （7/20 全公式类，CJK 0/8）、r1 FPR 0.05（1/20，N/Na）。
   校准报告更新（八条目），**全 HOLD**（预注册规则；S cap 维持）。
   实测结论：v33 guard 在对抗负例上严格占优 gemma3-judge（guard 20/20 拒 vs gemma 2/20）。
5. **P4 纸面联动**：摘要/结果/表/证据指针/方法/讨论/limitations 共 ~30 处改数
   （90/62/62/88、26/8 raw、0.2092/0.3810、8/8 catch、judge 表征段落）；
   账本 C49/C50/C54/C55/C58/C59 修订＋C61 对抗更新＋C63 promotion 记录（63/0/1）；
   verify_r4_response 冻结 R19（历史审计，非门）。

## 验证
- ledger 63/0/1（C08 WARN 前存）；各重算脚本 exit 0（adjudication×2、merged、holm、
  hetero敏感性、synth、decode、inventory 96/7 不变、ece）；验收门见封存节。

## 成本
- 模型调用 60（全本地）；工具轮次约 60。返工 4 次（raw-fallback 漏、ece 注释吞括号、
  C61 锚文本记错、L270 大锚点转义混杂→短锚点）。

## 遗留（→R23，用户侧不变）
- G2 重编 main.pdf（STALE 仍有效）；第二 grader 判读；公开建仓。
- R23：投稿包重打＋重投封存。
