# ROUND_R1 — 8分攻坚修改轮（2026-09-07）

## 评审模式
单评审人多角色自查（G003 hold：8角色扇出相对单评审人无显著增益证据，
本轮 defect 密度低，采用单人8角色清单+成本表；若发现新的 Critical/Major
则恢复多角色外审）。

| 角色 | 结论 | 痕迹 |
|---|---|---|
| 方法论 | PASS：分层配对McNemar正确，pooled仅描述；云端新层为披露新层非回填 | main.tex Methods |
| 统计 | PASS带hedge：三层p值重算一致；功效缺口全披露；3个McNemar无校正项，已披露为探索性分层（Minor） | results/power_update_120.json |
| 实验 | FIXED：置信度近退化（42/60@1.0；51/60@0.9）→ Limitations补ECE条件句 | main.tex:148 |
| 新颖性 | PASS：hedged定位+374篇screen+消融机制；窄任务域已披露 | C07/C13 |
| 可复现 | FIXED：云端脚本vendored入paper_workflow_kb/scripts（ablation/analyze_new60/cloud_judge/cloud_new60）；protocol补硬件声明 | gates G9 PASS |
| 写作 | PASS：style 0 findings；同行n/N冲突拆行清零 | reports/stats.md |
| 伦理 | PASS：Broader Impact含risk/harm关键词，G7 PASS | reports/tmlr.md |
| 图表 | OPEN（Minor）：无图，仅Table 1；清晰度不封顶但够C8，列Future Work外事项 |

## 新增问题
- 无新的 Critical/Major（R1 低缺陷密度成立，下一轮维持单人模式）。

## 成本表
roles 1人×8角 × model调用（云端judge 21条约21 calls + 新层60条60 calls + 本地扫描若干）；
收敛加速器未触发（R1 Critical+Major=0，方法/统计无Major，符合shrink条件但本就单人）。

## 门禁
- ledger 18 PASS/0 FAIL；gates 9/9 PASS；manifest 69 PASS/0 FAIL（重建后复核）。
