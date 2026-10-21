# ROUND_R21 — judge 校准＋第二 grader 包＋guard v33 预实验

## 到达记录
- R20 已封存（manifest 334/0/0，验收门 9/9，MISSION 冻结）；goal-8f8dffb2 round 内连续推进 R21。
- MISSION 当前阶段：P1 完成（pilot 96 对）；本轮做 P2 本地新跑＋P3 汇总＋grader 包＋R22-pre。

## 改动
1. **P2 本地新跑**（scripts/local_judge_gold100_p2.py）：GOLD-100 62 flip 行 × qwen2:7b＋gemma3:4b
   ＝124 calls，与 local_judge.py 同 prompt/temp0；人类 gold＝作者盲评；**124/124 零 ERROR**。
   VRAM 逐出颠簸致首 call 慢（5.7GiB 卡、qwen2 需 4.3GiB），fd/socket＋server log 确认 mid-request，
   非卡死。evidence/gold100_p2_verdicts.json。
2. **P3 校准汇总**（scripts/judge_calib_report.py → results/judge_calib_report.json）：
   r1@local 64对 FNR 0.0/FPR 1/3；qwen-cloud 21对＋qwen-local 11对零错分（分母过小）；
   P2-qwen2 62对 FNR 0.0351（2/57，echo H02/H28）/FPR 0.0（0/5)/agree 0.9677；
   P2-gemma3 62对 FNR 0.1228（7/57)/FPR 0.6（3/5，恰 H62/H68/H71 单字 CJK，与 guard 同类过接受）/agree 0.8387。
   **五 judge 全 HOLD**（使能规则 FNR<15%且FPR<10%且人类判错分母≥10；qwen2 的 FPR 分母仅 5）。
   校准不解锁，S cap 维持；temperature scaling/ECE 因二值无 confidence 不适用（D1 已明示）。
   账本 C61（ledger 62/0/1，C08 WARN 前存）。
3. **第二 grader 包**（scripts/build_rater2_pack.py）：7 排除普查＋23  seeded 随机（seed 20260909），
   盲 ID S01..S30（16 flip-confirmed＋7 excluded＋7 nonflip）；gold100_rater2_pack.csv＋
   密封 evidence/rater2_key.json（不随包交付）。κ 脚本（scripts/rater2_kappa.py）自检 κ=1.0 PASS；
   真跑 gated 待第二真人（D3：绝不用模型冒充）。判读动作留用户侧。
4. **R22-pre guard v33**（scripts/guard_v33_preexperiment.py → results/guard_v33_PREEXPERIMENTAL.json）：
   substring 分支内 CJK 单字 guard（与 v3.1 公式 guard 并列；否定/echo/数值/精确分支不动）。
   sealed 120 **零附带改动**（McNemar b=c=0，p=1.0）、回归三项绿、GOLD-100 恰 4 单字行翻转为拒
   （与用户盲评一致）、H47/H85 echo 维持接受（与用户一致）、H34 维持拒。
   返工 2 次（首版误伤否定分支→只进 substring；重写漏公式 guard 致 O/O2 回弹→补回双 guard）。
   verdict＝PROMOTE-CANDIDATE；**promotion＝换测量仪器，留 R22 另起轮次，本轮不 promote**。
   账本 C62。

## 验证
- ledger 62/0/1（C61/C62 PASS；C08 WARN 前存）；judge_calib_report exit 0；κ 自检 PASS；v33 exit 0。
- 六扫＋manifest 见封存节。

## 封存
- manifest canonical 重建后 **347/0/0**（334＋13 新增：P2 verdicts、calib report、rater2 pack＋key、
  v33 pre json、4 新脚本、ROUND_R21.md 等；中途 scoped 脚本误写 repo-root 前缀→改 canonical builder，
  门内纠正）。
- acceptance **9/9**（gates_history.jsonl 已 record；config_sha256=b3e66a165457… 不变）。
- PHASE5_SEAL.json 三哈希更新（ledger 62/0/1；manifest 347/0/0；R20 seal 作废）。
- MISSION 冻结；后续改动另起 R22。

## 成本
- 模型调用 124（全本地 ollama，不涉云）；工具轮次约 30。

## 遗留（非本轮阻塞）
- 用户侧：G2 重编 main.pdf（R20 STALE-PDF TODO 未动）；第二 grader 判读（包已备，grades_rater2_user2.csv 待填）；
  公开建仓（R20 artifact 草案已备）。
- R22：v33 promotion（换仪器：sealed 全重跑＋正文/账本更新＋McNemar 新旧对照）＋对抗负例补 FPR 分母；
  R23：重投封存。
