from __future__ import annotations
# Vendored copy of /data3/deepseek/DELIVERY_calibration/03_scripts/label_match.py
# paper_workflow_kb verify_labels.py embeds an older subset; v3 is authoritative here.
import re

__all__ = ["norm", "tolerant_match", "SUFFIXES", "SYNONYMS"]

_CN_UNIT = {"万": 1e4, "亿": 1e8}

# Unicode 下标 → 数字（H₂O → H2O; 2026-08-16 v3）
_SUBSCRIPTS = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
# 英文同义词/拼写变体（2026-08-16 v3）: 化学名 ↔ 中文名、常见拼写变体
EN_SYNONYMS = {
    "ascorbic acid": "抗坏血酸",
    "shakespear": "莎士比亚",
    "shakespeare": "莎士比亚",
}
_CN_RE = re.compile(r"[\u4e00-\u9fff]+")


def norm(s) -> str:
    s = str(s).strip().lower().translate(_SUBSCRIPTS)
    return re.sub(r"[,，。\s/、;；]+", "", s)


# norm 后的英文同义词表(key 已去空格小写; 须在 norm 定义后)
_EN_SYNONYMS_NORM = {norm(k): v for k, v in EN_SYNONYMS.items()}


SUFFIXES = ["年", "元", "米", "小时", "公里", "秒", "约", "的"]
SYNONYMS = {"不会": "否", "不是": "否", "会": "是", "yes": "是", "no": "否"}
_NEG_PREFIXES = ("不是", "不会")
_POS_PREFIXES = ("是", "会")


def _parse_cn_num(s: str):
    """解析含中文数量单位的数字串: '30万'->300000, '1亿'->1e8; 失败返回 None。"""
    m = re.fullmatch(r"([-+]?\d+(?:\.\d+)?)(万|亿)?", s)
    if not m:
        return None
    v = float(m.group(1))
    if m.group(2):
        v *= _CN_UNIT[m.group(2)]
    return v


def tolerant_match(a, g) -> bool:
    """语义容错匹配：归一化 → 剥离单位后缀 → 同义词 → 前置否定/肯定 → 子串 → 数值等价。"""
    a2, g2 = norm(a), norm(g)
    if not a2 or not g2:
        return False  # 空答案永远判错(2026-08: 空串是任何串的子串, 曾致空答案被接受)
    if a2 == g2:
        return True
    for suf in SUFFIXES:
        a2 = a2.replace(suf, "")
        g2 = g2.replace(suf, "")
    if a2 == g2:
        return True
    if SYNONYMS.get(a2) == g2:
        return True
    # v3: 英文同义词/拼写变体（"ascorbic acid" ↔ "抗坏血酸"; "shakespear" → "莎士比亚"）
    en_val = _EN_SYNONYMS_NORM.get(a2)
    if en_val is not None and en_val == g2:
        return True
    # v3: 中英混排——答案同时含 ASCII 字母与中文、且 gold 为中文时,
    #   用答案的中文部分再匹配("H 氢元素" → "氢元素" 与 gold "氢")
    #   (是/否 已由上方 SYNONYMS/前置词分支处理, 此处可安全放行单字 gold)
    if re.search(r"[a-z]", a2) and _CN_RE.search(a2):
        cn_a = "".join(_CN_RE.findall(a2))
        if cn_a:
            if cn_a == g2 or g2 in cn_a:
                return True
            if len(g2) >= 2 and cn_a in g2:
                return True
    # 前置否定/肯定 token: "不是，光年是长度单位" 表达 "否"（R3 row 27 类）
    if g2 in ("否", "是"):
        for p in _NEG_PREFIXES:
            if a2.startswith(p) and g2 == "否":
                return True
        for p in _POS_PREFIXES:
            if a2.startswith(p) and g2 == "是":
                return True
    # 子串/全名: "威廉·莎士比亚" 含 "莎士比亚"（R3 row 3 类; 长度 >= 2 防 '是'/'否' 误触发）
    # 负例精度修复(2026-08): gold 为纯数值时禁止子串规则——"2997920" 含 "299792"、
    # "1000" 含 "100" 等数量级错误会被误接受; 数值一律走下方数值等价分支。
    if len(g2) >= 2 and _parse_cn_num(g2) is None and (g2 in a2 or a2 in g2):
        return True
    # 数值等价: 精确(1e-6) 或 中文数字/相对容差(0.5%, R3 row 5/7 类)
    av, gv = _parse_cn_num(a2), _parse_cn_num(g2)
    if av is not None and gv is not None:
        if abs(av - gv) < 1e-6:
            return True
        if abs(av - gv) / max(abs(gv), 1.0) < 0.005:
            return True
    return False
