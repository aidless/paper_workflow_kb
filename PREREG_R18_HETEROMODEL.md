# Mini pre-registration — R18 P1-2: hetero-family model validation (C3)

> 落盘先于采集。回应编辑 C3（7B 同家族、跨模型名不副实）：换异家族模型，
> 同问题集、同 prompt、同解析，描述性复现。

## 设计

- **问题集**：xdomain 60 问原样（`cloud_xdomain60_loose.QA`，与 tight/loose 两层同一题集），
  不引入新题（dedup 天然通过：问题无新增，模型输出为新行）。
- **模型/prompt/解析**：本地 `deepseek-r1:7b`（deepseek 系，与 qwen 系异家族），temperature 0，
  `think: False`（短答案格式；qwen3:4b 式思考模式空回先例已披露，沿 local-new 成功做法），
  loose prompt 逐字复刻 xdomain-loose，解析规则同 collection 脚本
  （首行答案＋首个置信度浮点，否则 0.8；失败记 error 不编造）。
- **判定口径（描述性，无推断）**：v3.2 基准 flip 率＋b/c 计数；若 flip 率超 5\% 触发
  本论文 adjudication 门，flip 集送异构 judge（本地 `qwen2.5:7b`，与被测模型异家族，
  xdomain 裁决先例）逐行裁决。
- **方向性预期**：paraphrase-surface 题上 flip 率大于零（xdomain-loose 前例 20/60，
  R18 前例 raw 27/60）。
- **降级条件**：若 flip 率近零或 contrast 缺席，如实报告为 model-dependent 边界，
  不做 spin；结论 scope 维持"7B 开源短答案 QA"限定。

## Amendment A1（采集前修正，分析未发生）：模型替换为 gemma3:4b

- deepseek-r1:7b 无视 `think: False`，54 行首行全为 `<think>`（qwen3:4b 式思考空回先例重演；
  部分文件 `evidence/r18_heteromodel60_raw.json` 54 行保留为失败尝试记录，不入分析）。
- 替换为本地 `gemma3:4b`：与 qwen 系异家族**且**异规模（4B vs 7B），单点同时覆盖 C3 的
  family＋scale 两个维度；one-shot 实测短答案格式干净（`60 分钟 / 0.9`）。
- 其余设计不变（同 60 题、同 loose prompt、同解析/v3.2/描述性口径/降级条件）；
  trace 前缀 `gr18-`，输出 `evidence/r18_heteromodel_gemma60_raw.json`。

原始记录 `evidence/r18_heteromodel60_raw.json`（增量写，resume-safe）；
分析复用 `analyze_xdomain.layer` 同族口径；seal 后入账本。
