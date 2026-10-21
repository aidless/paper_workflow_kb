# WORKING_NOTES.md

- 论文标题: KB-grounded Manuscript from 130-paper Obsidian Library
- Phase: 0 收据
- 范围 / 假设:
- 开放问题:
- 证据包入口:

## 2026-09-07 c-cell 根因（pilot 级，不进账本）
- 现象：code-pilot-04（`//` vs `//`）exact 真、guarded（v3 tolerant）假。
- 根因：`label_match_v3.norm` 第 23 行剥离 `/`（`[,，。\s/、;；]+`），双侧归一后皆为空串；
  `tolerant_match` 第 50–51 行空串守卫（2026-08 防空答案误接受）直接 return False。
  而 pilot 分析用的 exact 口径是 `norm(a)==norm(g)`（`''==''` 为真），故出现 exact 真/guarded 假。
- 定性：窄边（双侧归一为空），非语义分歧；v3.1 守卫未动此分支。
- 若理论化（charter A）立项：可考虑 v3.2（双侧 raw 非空但归一皆空时回退 raw 比较）＋410 行全回归；
  未经立项不得改 matcher（改动即新版本，需 ablation/全层重跑）。本条仅为立项输入。
