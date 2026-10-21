# GOLD-100 专家标注包（真人 grading，盲评）

## 做什么
逐行判断 response 是否表达了 reference 的正确答案（语义等价，非字符串相等），
在 `你的判定(对/错)` 列填 对 或 错。可在"备注"列留理由（可选）。

## 规则
- 不要查本论文任何结果文件/账本（盲评；trace_id 已隐去，顺序已打乱）。
- 题干为空的行只看 response/reference 两列判定（与 GOLD-25 stemless 同类）。
- 完成后另存为 `grades_gold100_user.csv`（同目录），通知 agent 解码。

## 构成（供解码后核对， grading 时无需关心）
100 项＝7 个已知分歧翻转＋55 个已确认翻转（分层抽样）＋38 个非翻转行
（含两判皆错行，测负例一致性）。key 封存于 evidence/gold100_key.json。
预计 30-40 分钟。
