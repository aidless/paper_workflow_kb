# 标签判定器验证报告(G006)

- 数据: paper_workflow_kb/evidence/d2_60.jsonl  |  行数: 60
- exact-match 准确率: 38/60
- tolerant-match 准确率: 48/60
- 翻转集大小: 10  (16.7%)

## 翻转集(逐条待裁决)

| row | trace_id | predicted | gold | exact | tolerant |
|---|---|---|---|---|---|
| 1 | pilot-01 | '1789年' | '1789' | False | True |
| 9 | pilot-09 | '约24小时' | '24' | False | True |
| 13 | pilot-13 | '80元' | '80' | False | True |
| 21 | pilot-21 | '不会' | '否' | False | True |
| 23 | pilot-23 | '不是' | '否' | False | True |
| 25 | pilot-25 | '不是' | '否' | False | True |
| 30 | pilot-30 | '会' | '是' | False | True |
| 53 | holdout-23 | '不会' | '否' | False | True |
| 55 | holdout-25 | '不是' | '否' | False | True |
| 56 | holdout-26 | '不是' | '否' | False | True |

> 每条翻转必须裁决: 语义等价(判对, 修 matcher/标签)或语义不等(判错, 保留 exact)。
> 裁决记录应入证据(outcome_source 标注), 并加 CLAIM_LEDGER 条目使前后数字可追溯。
