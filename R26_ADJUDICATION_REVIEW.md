# R26 裁决复审报告（作者独立重判）

复审对象：`r26_flip_pack_entity.csv` / `r26_miss_pack_entity.csv` /
`r26_flip_pack_trivia.csv` / `r26_miss_pack_trivia.csv`（共 180 行）。
判定标准回炉至 PREREG_R26_EXTERNAL R4：**verdict 对照 gold alias 集判语义等价**
（"逐条对照 alias 判 miss/真拒"），等价于"prediction 与 ≥1 gold alias 语义一致"。

复审人 = 作者本人（单裁判）。本次未引入独立第二裁判——这是已知局限，
final 语义 gold 仍建议人工抽检 borderline 行。复审不改变抽样/协议/v3.4 决策规则。

## 一、已执行的修正（1 处，推翻初判 draft）

| id | 初判 | 复审 | 理由 |
|---|---|---|---|
| `trivia-odql_8784` | correct | **incorrect** | 预测 `"Vanessa atalanta"` 复述题干学名而非答出俗名 `Red Admiral`；guard 被 alias 集内 `"Vanessa atalanta (Red Admiral)"` 条目 echo 放行 → over-fire |

同步更新 `scripts/fill_r26_verdict.py`（V 字典对应条目），保证脚本重跑 = CSV 现状。

## 二、复审后最终 verdict（对 v3.4 采用门）

| pack | 行数 | correct | incorrect | 含义 |
|---|---|---|---|---|
| flip entity（guard 受） | 32 | 30 | 2 | 2 over-fire |
| flip trivia（guard 受） | 28 | 25 | **3** | 3 over-fire |
| miss entity（guard 拒） | 60 | 0 | 60 | 0 真 miss |
| miss trivia（guard 拒） | 60 | 2 | 58 | 2 真 miss |

- **over-fire = 5**（entity 2 + trivia 3）
- **miss = 2**（entity 0/60，trivia 2/60：`qb_6127` 数字+单位后缀、`tb_1099` 顺序颠倒）

## 三、v3.4 决策（不变：负结果）

v3.4 相对 v3.3 增量：entity 0，trivia +2（123→125）。总 miss 降 **2 < 5**，
不满足采用门 (a)，故 **v3.4 不切版，v3.3 保持基准**。结论方向不因本次修正改变。

## 四、gold 标注噪声（单列披露，不进主数字）

以下三行预测语义并未答错，是 EntityQuestions 本身标注错配，导致按"对照 alias"
字面判定被记为 `incorrect`（guard 拒得对）。已单独披露，不影响 v3.4 采用决策。

| id | 问题 | 预测 | gold | 噪声类型 |
|---|---|---|---|---|
| `entity-P176-4` | BMW Vision ConnectedDrive 生产商 | BMW Group | Arman Ansari（设计师） | gold 标错生产商 |
| `entity-P136-4` | Miss Congeniality 2 的音乐类型 | Pop and dance | comedy film | 模板问 music、gold 是 film genre |
| `entity-P136-1` | Edge of the Axe 的音乐类型 | Heavy metal | horror film | 同上 |

敏感性分析：若把 `P176-4` 计为真 miss（预测实际正确），entity miss 0/60 → 1/60，
总 miss 2 → 3，仍 **< 5**，v3.4 依旧不采用。方法章/Limitations 各补一句
"EntityQuestions 采样含 P136/P176 属性标注噪声，3 行单列，不影响结论"。

## 五、borderline 行（维持 incorrect，理由一致）

以下预测与 gold 不等价但语义相邻，按"预测须等价于 gold alias"从严判 incorrect。
任何人复核时若倾向放宽，会改变 miss 绝对数但**不会翻转 v3.4 负结果**。

- 上级行政/泛化 vs 具体 gold：`entity-P131-8`(Iran vs 省)、`P131-5`、`P740-7`(Italy vs Florence)、
  `P276-0`(France vs Abbeville)、`P159-6`(Tokyo vs Nakano-ku)、`P106-5`(musician vs songwriter)、
  `P800-3`(poet vs 具体作品)、`P800-4`(electronic music vs Lost Horizons)
- 相关但非等价实体：`entity-P127-5`(Sony Corp vs SIE)、`P170-6`(Besson 电影 vs Surnow 电视)、
  `trivia-qg_4165`(Narcotics vs Cocaine)、`qz_3440`(Anna Wintour vs Vogue)、
  `qg_581`(Vitamin D vs Calcium)、`qw_12886`(Alençon 出生地 vs Lisieux 关联地)

## 六、复审结论

初判 draft 整体稳健（179/180 维持）；唯一实质纠错为 `trivia-odql_8784` 的 echo over-fire
误判，使 over-fire 由 4 → 5。gold 噪声与 borderline 均不改变 R26 负结果：**v3.4 不切版，
v3.3 保持基准**。账本 C69/C70/C71 待 seal 后写入。