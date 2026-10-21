"""Generate powered-extension pools with recomputable golds (goal-R4, autonomous).

BIG (160, Chinese, arithmetic-heavy for zero gold-error risk):
  120 arithmetic/unit items with PROGRAM-COMPUTED golds + 40 hand-listed
  knowledge items (capitals/elements, safest facts, visible below for review).
EN (30, English cross-type stratum): 10 capitals + 10 computed arithmetic +
  10 yes/no (translated semantics).
Gold provenance per item: {"by": "computed"|"hand", "expr": ...} — disclosed.
Writes evidence/qa_pool_big.json + evidence/qa_pool_en.json.
"""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
rng = random.Random(20260907)

BIG = []
# 40 additions a+b (two-digit), gold computed
for _ in range(40):
    a, b = rng.randint(11, 99), rng.randint(11, 99)
    BIG.append({"q": f"{a}加{b}等于几？只答数字。", "gold": str(a + b),
                "by": "computed", "expr": f"{a}+{b}"})
# 25 subtractions (non-negative)
for _ in range(25):
    a, b = rng.randint(20, 200), rng.randint(10, 99)
    if b > a:
        a, b = b, a
    BIG.append({"q": f"{a}减{b}等于几？只答数字。", "gold": str(a - b),
                "by": "computed", "expr": f"{a}-{b}"})
# 20 multiplications (small)
for _ in range(20):
    a, b = rng.randint(3, 25), rng.randint(3, 25)
    BIG.append({"q": f"{a}乘{b}等于几？只答数字。", "gold": str(a * b),
                "by": "computed", "expr": f"{a}*{b}"})
# 15 exact divisions
for _ in range(15):
    b, k = rng.randint(3, 25), rng.randint(3, 25)
    BIG.append({"q": f"{b * k}除以{b}等于几？只答数字。",
                "gold": str(k), "by": "computed", "expr": f"{b * k}/{b}"})
# 20 unit conversions (computed)
for _ in range(10):
    h = rng.randint(2, 48)
    BIG.append({"q": f"{h}小时等于多少分钟？只答数字。", "gold": str(h * 60),
                "by": "computed", "expr": f"{h}*60min"})
for _ in range(10):
    k = rng.randint(2, 50)
    BIG.append({"q": f"{k}公里等于多少米？只答数字。", "gold": str(k * 1000),
                "by": "computed", "expr": f"{k}*1000m"})
# 40 hand-listed knowledge (safest facts)
KNOW = [
    ("荷兰的首都是哪里？只答地名。", "阿姆斯特丹"), ("比利时的首都是哪里？只答地名。", "布鲁塞尔"),
    ("奥地利的首都是哪里？只答地名。", "维也纳"), ("瑞士的首都是哪里？只答地名。", "伯尔尼"),
    ("瑞典的首都是哪里？只答地名。", "斯德哥尔摩"), ("挪威的首都是哪里？只答地名。", "奥斯陆"),
    ("丹麦的首都是哪里？只答地名。", "哥本哈根"), ("芬兰的首都是哪里？只答地名。", "赫尔辛基"),
    ("波兰的首都是哪里？只答地名。", "华沙"), ("希腊的首都是哪里？只答地名。", "雅典"),
    ("葡萄牙的首都是哪里？只答地名。", "里斯本"), ("西班牙的首都是哪里？只答地名。", "马德里"),
    ("意大利的首都是哪里？只答地名。", "罗马"), ("加拿大的首都是哪里？只答地名。", "渥太华"),
    ("澳大利亚的首都是哪里？只答地名。", "堪培拉"), ("新西兰的首都是哪里？只答地名。", "惠灵顿"),
    ("印度的首都是哪里？只答地名。", "新德里"), ("韩国的首都是哪里？只答地名。", "首尔"),
    ("泰国的首都是哪里？只答地名。", "曼谷"), ("越南的首都是哪里？只答地名。", "河内"),
    ("锂的化学符号是？", "Li"), ("钠的化学符号是？", "Na"),
    ("钾的化学符号是？", "K"), ("钙的化学符号是？", "Ca"),
    ("镁的化学符号是？", "Mg"), ("铝的化学符号是？", "Al"),
    ("铜的化学符号是？", "Cu"), ("银的化学符号是？", "Ag"),
    ("锌的化学符号是？", "Zn"), ("金的化学符号是Au吗？答是或否。", "是"),
    ("水是液体吗（常温）？答是或否。", "是"), ("冰是固体吗？答是或否。", "是"),
    ("一年有多少个月？只答数字。", "12"), ("一周有多少天？只答数字。", "7"),
    ("一小时等于多少分钟？只答数字。", "60"), ("一分钟等于多少秒？只答数字。", "60"),
    ("10的平方是几？只答数字。", "100"), ("人有几根手指（双手共）？只答数字。", "10"),
    ("北京是中国的首都吗？答是或否。", "是"), ("猫会叫吗？答是或否。", "是"),
]
for q, g in KNOW:
    BIG.append({"q": q, "gold": g, "by": "hand", "expr": "safest-fact"})
assert len(BIG) == 160, len(BIG)

EN = []
EN_CAP = [("Norway", "Oslo"), ("Sweden", "Stockholm"), ("Finland", "Helsinki"),
          ("Poland", "Warsaw"), ("Greece", "Athens"), ("Portugal", "Lisbon"),
          ("Netherlands", "Amsterdam"), ("Belgium", "Brussels"),
          ("Austria", "Vienna"), ("Switzerland", "Bern")]
for c, cap in EN_CAP:
    EN.append({"q": f"What is the capital of {c}? Answer with the place name only.",
               "gold": cap, "by": "hand", "expr": "capital"})
for _ in range(10):
    a, b = rng.randint(11, 99), rng.randint(11, 99)
    EN.append({"q": f"What is {a} plus {b}? Answer with the number only.",
               "gold": str(a + b), "by": "computed", "expr": f"{a}+{b}"})
EN_YN = [("Is water liquid at room temperature? Answer yes or no.", "yes"),
         ("Is ice solid? Answer yes or no.", "yes"),
         ("Do fish swim? Answer yes or no.", "yes"),
         ("Do birds fly (in general)? Answer yes or no.", "yes"),
         ("Will the sun rise in the west? Answer yes or no.", "no"),
         ("Does a stone float on water (in general)? Answer yes or no.", "no"),
         ("Is Beijing the capital of China? Answer yes or no.", "yes"),
         ("Do cats meow? Answer yes or no.", "yes"),
         ("Do plants need sunlight? Answer yes or no.", "yes"),
         ("Are there four seasons in a year? Answer yes or no.", "yes")]
for q, g in EN_YN:
    EN.append({"q": q, "gold": g, "by": "hand", "expr": "yes-no"})
assert len(EN) == 30, len(EN)

(HERE / "evidence" / "qa_pool_big.json").write_text(
    json.dumps(BIG, ensure_ascii=False, indent=1), encoding="utf-8")
(HERE / "evidence" / "qa_pool_en.json").write_text(
    json.dumps(EN, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"BIG={len(BIG)} (computed={sum(1 for r in BIG if r['by']=='computed')})")
print(f"EN={len(EN)} (computed={sum(1 for r in EN if r['by']=='computed')})")
