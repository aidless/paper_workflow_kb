# -*- coding: utf-8 -*-
"""R29 top-up pool (PREREG_R29_POWER, frozen before answering).

420 computed arithmetic (add:sub:mul:div ~ 105:171:105:39, div = exact division) +
140 hand capitals (gold from an embedded, de-contested country->capital map).
Seed fixed for reproducibility. Gold is str(int(...)) for arithmetic.
Output: evidence/r29_topup_560.json  (list of {q, gold, by, expr})
"""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "evidence" / "r29_topup_560.json"
SEED = 20260911

# --- capital map (de-contested; administrative/Judicial disputes excluded) ---
CAPITALS = {
    "中国": "北京", "日本": "东京", "韩国": "首尔", "蒙古": "乌兰巴托", "朝鲜": "平壤",
    "越南": "河内", "老挝": "万象", "柬埔寨": "金边", "泰国": "曼谷",
    "马来西亚": "吉隆坡", "新加坡": "新加坡", "印度尼西亚": "雅加达", "菲律宾": "马尼拉",
    "文莱": "斯里巴加湾市", "印度": "新德里", "巴基斯坦": "伊斯兰堡", "孟加拉国": "达卡",
    "尼泊尔": "加德满都", "不丹": "廷布", "阿富汗": "喀布尔", "伊朗": "德黑兰",
    "伊拉克": "巴格达", "沙特阿拉伯": "利雅得", "也门": "萨那", "阿曼": "马斯喀特",
    "阿联酋": "阿布扎比", "卡塔尔": "多哈", "科威特": "科威特城", "巴林": "麦纳麦",
    "约旦": "安曼", "黎巴嫩": "贝鲁特", "叙利亚": "大马士革", "土耳其": "安卡拉",
    "哈萨克斯坦": "阿斯塔纳", "乌兹别克斯坦": "塔什干", "吉尔吉斯斯坦": "比什凯克",
    "塔吉克斯坦": "杜尚别", "土库曼斯坦": "阿什哈巴德",
    "俄罗斯": "莫斯科", "英国": "伦敦", "法国": "巴黎", "德国": "柏林", "意大利": "罗马",
    "西班牙": "马德里", "葡萄牙": "里斯本", "荷兰": "阿姆斯特丹", "比利时": "布鲁塞尔",
    "卢森堡": "卢森堡", "瑞士": "伯尔尼", "奥地利": "维也纳", "波兰": "华沙",
    "捷克": "布拉格", "斯洛伐克": "布拉迪斯拉发", "匈牙利": "布达佩斯",
    "罗马尼亚": "布加勒斯特", "保加利亚": "索非亚", "希腊": "雅典", "阿尔巴尼亚": "地拉那",
    "北马其顿": "斯科普里", "塞尔维亚": "贝尔格莱德", "克罗地亚": "萨格勒布",
    "斯洛文尼亚": "卢布尔雅那", "波黑": "萨拉热窝", "黑山": "波德戈里察",
    "乌克兰": "基辅", "白俄罗斯": "明斯克", "摩尔多瓦": "基希讷乌", "立陶宛": "维尔纽斯",
    "拉脱维亚": "里加", "爱沙尼亚": "塔林", "芬兰": "赫尔辛基", "瑞典": "斯德哥尔摩",
    "挪威": "奥斯陆", "丹麦": "哥本哈根", "冰岛": "雷克雅未克", "爱尔兰": "都柏林",
    "埃及": "开罗", "利比亚": "的黎波里", "突尼斯": "突尼斯", "阿尔及利亚": "阿尔及尔",
    "摩洛哥": "拉巴特", "苏丹": "喀土穆", "埃塞俄比亚": "亚的斯亚贝巴", "肯尼亚": "内罗毕",
    "坦桑尼亚": "多多马", "乌干达": "坎帕拉", "卢旺达": "基加利", "尼日利亚": "阿布贾",
    "加纳": "阿克拉", "塞内加尔": "达喀尔", "马里": "巴马科", "尼日尔": "尼亚美",
    "乍得": "恩贾梅纳", "喀麦隆": "雅温得", "刚果民主共和国": "金沙萨", "安哥拉": "罗安达",
    "赞比亚": "卢萨卡", "津巴布韦": "哈拉雷", "莫桑比克": "马普托", "马达加斯加": "塔那那利佛",
    "美国": "华盛顿", "加拿大": "渥太华", "墨西哥": "墨西哥城", "危地马拉": "危地马拉城",
    "古巴": "哈瓦那", "海地": "太子港", "多米尼加": "圣多明各", "巴拿马": "巴拿马城",
    "哥斯达黎加": "圣何塞", "哥伦比亚": "波哥大", "委内瑞拉": "加拉加斯", "厄瓜多尔": "基多",
    "秘鲁": "利马", "巴西": "巴西利亚", "智利": "圣地亚哥", "阿根廷": "布宜诺斯艾利斯",
    "乌拉圭": "蒙得维的亚", "巴拉圭": "亚松森",
    "澳大利亚": "堪培拉", "新西兰": "惠灵顿", "巴布亚新几内亚": "莫尔兹比港", "斐济": "苏瓦",
    "亚美尼亚": "埃里温", "阿塞拜疆": "巴库", "格鲁吉亚": "第比利斯", "索马里": "摩加迪沙",
    "几内亚": "科纳克里", "塞拉利昂": "弗里敦", "利比里亚": "蒙罗维亚", "多哥": "洛美",
    "刚果共和国": "布拉柴维尔", "加蓬": "利伯维尔", "马拉维": "利隆圭", "纳米比亚": "温得和克",
    "博茨瓦纳": "哈博罗内", "厄立特里亚": "阿斯马拉", "洪都拉斯": "特古西加尔巴",
    "尼加拉瓜": "马那瓜", "萨尔瓦多": "圣萨尔瓦多", "牙买加": "金斯敦",
    "特立尼达和多巴哥": "西班牙港", "圭亚那": "乔治敦",
}

assert len(CAPITALS) >= 140, f"need >=140 capitals, got {len(CAPITALS)}"


def make_arithmetic(rng):
    rows = []
    # add 105
    for _ in range(105):
        x, y = rng.randint(11, 99), rng.randint(11, 99)
        rows.append({"q": f"{x}加{y}等于几？只答数字。", "gold": str(x + y),
                     "by": "computed", "expr": f"{x}+{y}"})
    # sub 171
    for _ in range(171):
        x, y = rng.randint(11, 999), rng.randint(1, 999)
        if y > x:
            x, y = y, x
        rows.append({"q": f"{x}减{y}等于几？只答数字。", "gold": str(x - y),
                     "by": "computed", "expr": f"{x}-{y}"})
    # mul 105
    for _ in range(105):
        x, y = rng.randint(11, 99), rng.randint(2, 9)
        rows.append({"q": f"{x}乘以{y}等于几？只答数字。", "gold": str(x * y),
                     "by": "computed", "expr": f"{x}*{y}"})
    # div 39 (exact division: x = y * z)
    added = 0
    while added < 39:
        y = rng.randint(2, 99)
        z = rng.randint(2, 99)
        x = y * z
        if x > 9999:
            continue
        rows.append({"q": f"{x}除以{y}等于几？只答数字。", "gold": str(z),
                     "by": "computed", "expr": f"{x}/{y}"})
        added += 1
    assert len(rows) == 420, len(rows)
    return rows


def make_hand(rng):
    countries = list(CAPITALS.keys())
    rng.shuffle(countries)
    countries = countries[:140]
    return [{"q": f"{c}的首都是哪里？只答地名。", "gold": CAPITALS[c],
             "by": "hand", "expr": ""} for c in countries]


def main():
    rng = random.Random(SEED)
    rows = make_arithmetic(rng) + make_hand(rng)
    assert len(rows) == 560, len(rows)
    # sanity: all gold non-empty, arithmetic gold are ints
    for r in rows:
        assert r["gold"], r
        if r["by"] == "computed":
            int(r["gold"])
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    n_computed = sum(1 for r in rows if r["by"] == "computed")
    n_hand = sum(1 for r in rows if r["by"] == "hand")
    n_div = sum(1 for r in rows if r["expr"] and "/" in r["expr"])
    print(f"total={len(rows)} computed={n_computed} hand={n_hand} div={n_div}")


if __name__ == "__main__":
    main()