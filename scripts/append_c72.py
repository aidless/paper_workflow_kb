# -*- coding: utf-8 -*-
"""追加 C72（R27-P1 测量误差形式化）到 CLAIM_LEDGER.md 末尾。幂等：末尾已是 C72 则跳过。"""
import io

PATH = "CLAIM_LEDGER.md"
C72 = (
    "| C72 | 测量误差形式化（R27-P1，理论层无新数字）：matcher 为二值算子 exact e / tolerant t"
    "（flip = e=0 且 t=1，t = 规则集 R 的析取）；翻转由「答案变体空间 × R 类型覆盖」两独立因子决定；"
    "三条可证伪预测——(i) 退化变体空间→零翻转（math 0/40）、(ii) 覆盖缺失→零翻转（前瞻，R28 检验）、"
    "(iii) 覆盖变体→正翻转且归因随规则覆盖（消融 7/4/3/1/1 + 中文层正翻转至 43.3%）；"
    "post-hoc 形式化如实披露 | "
    "results/ablation.json -> n_synonym / n_numeric_tolerance / n_unit_suffix / n_substring / n_neg_prefix; "
    "results/math40.json -> n_flips / n; results/local_en.json -> n_flips / n | "
    "7 / 4 / 3 / 1 / 1 / 0 / 40 / 0 / 30 | "
    "纯引用既有 sealed 文件无新实验；三预测方向人工对照核验；"
    "P(ii) 无强实证支撑（local-en 0/30 记“天然规范”非覆盖变体检验）留 R28；"
    "P(i) 另有 code-format probe c-cell 单一观测作 existence proof；"
    "post-hoc 声明为 predictive framework 而非 pre-registered hypothesis，正文 Measurement-error formalization 小节 | verified |"
)

with io.open(PATH, encoding="utf-8") as f:
    text = f.read()

if C72 in text:
    print("C72 already present, skip")
else:
    if not text.endswith("\n"):
        text += "\n"
    text += C72 + "\n"
    with io.open(PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("C72 appended")