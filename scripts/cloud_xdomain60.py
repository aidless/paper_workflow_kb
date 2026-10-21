"""Cross-domain new layer: 60 fresh short-answer questions (cloud collection).

Three fresh 20-item blocks (measure-word conversions / yes-no inverted phrasing /
name variants on new entities). Same protocol as cloud_new60 (qwen2.5:7b, temp 0,
short answer + confidence line). Golds hand-listed below (provenance: hand).

Upload to /tmp, run: nohup python3 /tmp/cloud_xdomain60.py > /tmp/cloud_xdomain60.log 2>&1 &
"""
import json
import urllib.request

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"

QA = [
    # A. measure-word conversions (gold: bare number)
    ("一刻钟等于多少分钟？只答数字。", "15"),
    ("一旬等于多少天？只答数字。", "10"),
    ("一打等于几个？只答数字。", "12"),
    ("一罗等于几打？只答数字。", "12"),
    ("一斤等于多少克？只答数字。", "500"),
    ("一两等于多少克？只答数字。", "50"),
    ("一公斤等于多少克？只答数字。", "1000"),
    ("一米等于多少厘米？只答数字。", "100"),
    ("一公里等于多少米？只答数字。", "1000"),
    ("一平方米等于多少平方厘米？只答数字。", "10000"),
    ("一升等于多少毫升？只答数字。", "1000"),
    ("一吨等于多少公斤？只答数字。", "1000"),
    ("一小时等于多少秒？只答数字。", "3600"),
    ("一天等于多少小时？只答数字。", "24"),
    ("一周等于多少天？只答数字。", "7"),
    ("一年有多少个月？只答数字。", "12"),
    ("一世纪等于多少年？只答数字。", "100"),
    ("一双等于几只？只答数字。", "2"),
    ("一对等于几个？只答数字。", "2"),
    ("半打等于几个？只答数字。", "6"),
    # B. yes-no inverted phrasing (gold: 是/否)
    ("蜘蛛是昆虫吗？只答是或否。", "否"),
    ("鲸鱼是鱼吗？只答是或否。", "否"),
    ("蝙蝠会飞吗？只答是或否。", "是"),
    ("企鹅会飞吗？只答是或否。", "否"),
    ("竹子是草吗？只答是或否。", "是"),
    ("花生是坚果吗？只答是或否。", "是"),
    ("西红柿是水果吗？只答是或否。", "是"),
    ("土豆是蔬菜吗？只答是或否。", "是"),
    ("乌龟是两栖动物吗？只答是或否。", "否"),
    ("青蛙是两栖动物吗？只答是或否。", "是"),
    ("蚊子是昆虫吗？只答是或否。", "是"),
    ("蜗牛有外壳吗？只答是或否。", "是"),
    ("鱼用鳃呼吸吗？只答是或否。", "是"),
    ("鸟类是恒温动物吗？只答是或否。", "是"),
    ("蛇是恒温动物吗？只答是或否。", "否"),
    ("月亮自己会发光吗？只答是或否。", "否"),
    ("太阳是恒星吗？只答是或否。", "是"),
    ("地球是行星吗？只答是或否。", "是"),
    ("水在零摄氏度会结冰吗？只答是或否。", "是"),
    ("铁会被磁铁吸引吗？只答是或否。", "是"),
    # C. name variants on new entities
    ("李白字什么？只答表字。", "太白"),
    ("杜甫字什么？只答表字。", "子美"),
    ("苏轼号什么？只答别号。", "东坡"),
    ("关羽字什么？只答表字。", "云长"),
    ("刘备字什么？只答表字。", "玄德"),
    ("曹操字什么？只答表字。", "孟德"),
    ("诸葛亮字什么？只答表字。", "孔明"),
    ("鲁迅原名是什么？只答姓名。", "周树人"),
    ("巴金原名是什么？只答姓名。", "李尧棠"),
    ("老舍原名是什么？只答姓名。", "舒庆春"),
    ("冰心原名是什么？只答姓名。", "谢婉莹"),
    ("茅盾原名是什么？只答姓名。", "沈德鸿"),
    ("中国的首都是哪里？只答地名。", "北京"),
    ("日本的首都是哪里？只答地名。", "东京"),
    ("法国的首都是哪里？只答地名。", "巴黎"),
    ("端午节是农历哪一天？只答日期。", "五月初五"),
    ("中秋节是农历哪一天？只答日期。", "八月十五"),
    ("春节是农历哪一天？只答日期。", "正月初一"),
    ("清明节是农历还是公历节日？只答农历或公历。", "公历"),
    ("重阳节是农历哪一天？只答日期。", "九月初九"),
]
assert len(QA) == 60, len(QA)


def ask(question):
    prompt = f"{question}请用最短答案回答（不要解释）。答完后另起一行写置信度0-1，例如：0.9"
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False,
                         "options": {"temperature": 0, "num_predict": 60}}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=240) as r:
        return json.load(r)["response"]


def main():
    import re
    rows = []
    for i, (q, gold) in enumerate(QA, 1):
        try:
            resp = ask(q)
            lines = resp.strip().split("\n")
            pred = lines[0].strip()[:60]
            m = re.search(r"0?\.\d+|1\.0|1(?!\d)", resp)
            conf = float(m.group(0)) if m else 0.8
            if conf > 1:
                conf = 0.8
            err = None
        except Exception as e:
            pred, conf, err = "", 0.0, str(e)
        rows.append({"trace_id": f"xdomain-{i:02d}", "source": "xdomain",
                     "model": MODEL, "question": q, "predicted_label": pred,
                     "gold_answer": gold, "confidence": conf, "error": err})
        print(f"{i}/60 {rows[-1]['trace_id']}: pred={pred!r} gold={gold!r} conf={conf}",
              flush=True)
    json.dump(rows, open("/tmp/cloud_xdomain60.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("WROTE /tmp/cloud_xdomain60.json")


if __name__ == "__main__":
    main()
