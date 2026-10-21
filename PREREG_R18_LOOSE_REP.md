# Pre-registration — R18 P0-data(b): 独立 loose-regime 复现集

> 落盘时间先于采集（诚实顺序）。编辑 C2 的直接回应：docstring intent 不算 pre-reg，
> 这次是真 pre-reg：问题集、模型、prompt、分析口径全部先写后跑。

## 设计

- **问题集**：60 个全新短答案问题（见 `scripts/r18_loose_rep60.py` 中 R18_QA），三类各 20：
  A. 量词/单位换算（新实体：令/刀纸张数、吨水升数、纪/世/半世纪/平方公里/
  分秒/周小时/天分钟/年天/时辰/海里/立方千米/毫升/升-立方厘米/微米/微秒）；
  B. 改写是非问（新动物实体 20 个：章鱼/蝴蝶/龙虾/水母/乌贼/考拉/鸭嘴兽/
  啄木鸟/鸵鸟/蚂蚁/蜜蜂/螳螂/白蚁/萤火虫/蜈蚣/蝎子/扇贝/海豹/信天翁/壁虎）；
  C. 名号变体（新人物 20 个，未在既有层出现）。
- **去重门**：`check_batch_dedup` 同口径（exact-norm + hint-stripped core）零碰撞，
  exit 0 才能采集；gold 用户 10% 抽查通过才能分析（沿 batch1/2 前例）。
- **模型/prompt**：云机 ollama `qwen2.5:7b`，temperature 0，与 xdomain-loose **逐字同一**
  loose prompt（`请简短回答（不要解释）。答完后另起一行写置信度0-1，例如：0.9`），
  同一解析规则（首行答案 + 首个置信度浮点）。
- **判定口径（描述性框架，M1 之后无 McNemar 推断）**：
  - 主度量：guarded v3.2 口径 flip 率 + b/c 计数（描述性，无 p 值推断）。
  - flip 集 → 异构 judge（local deepseek-r1:7b）逐行 adjudication。
  - 方向性预期：paraphrase-surface 问题上 loose flip 率高于可比 tight 层
    （xdomain 前例 20/60 vs 1/60）。
  - **证伪/降级条件**：若 flip 率 <5% 或 contrast 缺席（如 powrep 前例 tight10 vs
    loose7），如实报告为 question-type-dependent 边界，不做 spin，不计核心结论。

## 封存

原始记录 `evidence/r18_loose_rep60_raw.json`；分析脚本复用 `analyze_xdomain.py` 同族口径；
seal + SHA-256 后入账本；旧证据 hash 不动。
