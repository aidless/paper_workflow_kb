# Artifact / public-repo draft (R20-3, DRAFT — 公开动作由用户执行)

本文档是未来公开仓库的结构草案＋脱敏清单。acceptance 仍为 "code available
on request"；改口为公开链接必须等用户实际建仓后。

## 目标仓库布局（映射）
- `paper/` → `paper/`（main.tex, main.bib, math_commands.tex, tmlr.sty/bst；main.pdf 由 CI 重编，不入库 stale 二进制）
- `scripts/` → `src/`（核心重算链，全部 stdlib-only，除 numpy/scipy 外零第三方依赖）
- `results/*.json` + `evidence/*.json` → `results/`, `evidence/`（封存 JSON 直接入库）
- `gold100_grading_pack.csv`, `grades_gold100_user.csv`, `evidence/gold100_key.json` → `gold/`（盲评三件套；grades 为真人判定，公开前需作者确认）
- `CLAIM_LEDGER.md`, `evidence_manifest.json` → 根目录（账本＋清单即审计入口）
- `requirements.txt`（R20 已按实测 pin：numpy==2.5.2, scipy==1.18.1）
- 不入库：ROUND_*/REVIEW_*/SELF_ASSESSMENT（FM-26 过程文档）、submission/*.zip、
  .r*/tmp_r*/.verify*（FM-28 脚手架）、失败尝试 raw（54 行 thinking-mode 已声明丢弃）

## 最小复算链（公开后 CI 应跑）
1. `python3 scripts/decode_gold100.py .` → results/gold100_agreement.json（86/88 双口径）
2. `python3 scripts/verify_holm_hetero_sensitivity.py .` → claim_holds=true
3. 验收门脚本（gates_config.json）全绿；manifest `build_evidence_manifest.py --verify` 0 dirty

## 公开前脱敏检查（用户建仓时逐项勾）
- [ ] 真人 grades 文件可公开（grades_gold100_user.csv／grades_gold25_user.csv 作者确认）
- [ ] 无本地绝对路径／用户名（grep `liuzewen\|F:\\deepseek\|/home/` 全仓 0 命中）
- [x] LICENSE 选定（用户 2026-09-08 决策：MIT；建仓时放入 LICENSE 文件）
- [ ] main.pdf 用 SOURCE_DATE_EPOCH 重编（FM 字节复现），替换 stale 二进制
- [ ] acceptance 由 "on request" 改为仓库链接（正文＋OpenReview 表单同步）

## 已知缺口（R21/R22 补）
- judge 校准集（R21 采 200–300 已标 pair，temperature scaling＋ECE/Brier）
- 第二 grader 独立子集＋Cohen κ（R21，需第二真人）
- guard v2（R22，修 NMS-normalize CJK 盲区＋McNemar 新旧对比）
