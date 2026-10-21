"""Cross-domain layer 2: same 60 questions, LOOSE prompt (paraphrase surface).

Rationale (written before seeing layer-2 data): layer 1 (tight format constraints)
suppressed paraphrase (1 flip / 60). Same questions, loose instruction
("请简短回答，不要解释") lets unit suffixes / synonymy / name variants surface,
which is exactly the v3.2 tolerance band. Prediction: more b-cell flips than
layer 1; McNemar per-layer (likely ns at n=60, disclosed); adjudication of the
combined flip set by a heterogeneous judge.

Upload to /tmp, run: nohup python3 /tmp/cloud_xdomain60_loose.py > /tmp/cloud_xdomain60_loose.log 2>&1 &
"""
import json
import urllib.request

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"

# Same questions as cloud_xdomain60.py, format hints stripped.
QA = [
    ("一刻钟等于多少分钟？", "15"),
    ("一旬等于多少天？", "10"),
    ("一打等于几个？", "12"),
    ("一罗等于几打？", "12"),
    ("一斤等于多少克？", "500"),
    ("一两等于多少克？", "50"),
    ("一公斤等于多少克？", "1000"),
    ("一米等于多少厘米？", "100"),
    ("一公里等于多少米？", "1000"),
    ("一平方米等于多少平方厘米？", "10000"),
    ("一升等于多少毫升？", "1000"),
    ("一吨等于多少公斤？", "1000"),
    ("一小时等于多少秒？", "3600"),
    ("一天等于多少小时？", "24"),
    ("一周等于多少天？", "7"),
    ("一年有多少个月？", "12"),
    ("一世纪等于多少年？", "100"),
    ("一双等于几只？", "2"),
    ("一对等于几个？", "2"),
    ("半打等于几个？", "6"),
    ("蜘蛛是昆虫吗？", "否"),
    ("鲸鱼是鱼吗？", "否"),
    ("蝙蝠会飞吗？", "是"),
    ("企鹅会飞吗？", "否"),
    ("竹子是草吗？", "是"),
    ("花生是坚果吗？", "是"),
    ("西红柿是水果吗？", "是"),
    ("土豆是蔬菜吗？", "是"),
    ("乌龟是两栖动物吗？", "否"),
    ("青蛙是两栖动物吗？", "是"),
    ("蚊子是昆虫吗？", "是"),
    ("蜗牛有外壳吗？", "是"),
    ("鱼用鳃呼吸吗？", "是"),
    ("鸟类是恒温动物吗？", "是"),
    ("蛇是恒温动物吗？", "否"),
    ("月亮自己会发光吗？", "否"),
    ("太阳是恒星吗？", "是"),
    ("地球是行星吗？", "是"),
    ("水在零摄氏度会结冰吗？", "是"),
    ("铁会被磁铁吸引吗？", "是"),
    ("李白字什么？", "太白"),
    ("杜甫字什么？", "子美"),
    ("苏轼号什么？", "东坡"),
    ("关羽字什么？", "云长"),
    ("刘备字什么？", "玄德"),
    ("曹操字什么？", "孟德"),
    ("诸葛亮字什么？", "孔明"),
    ("鲁迅原名是什么？", "周树人"),
    ("巴金原名是什么？", "李尧棠"),
    ("老舍原名是什么？", "舒庆春"),
    ("冰心原名是什么？", "谢婉莹"),
    ("茅盾原名是什么？", "沈德鸿"),
    ("中国的首都是哪里？", "北京"),
    ("日本的首都是哪里？", "东京"),
    ("法国的首都是哪里？", "巴黎"),
    ("端午节是农历哪一天？", "五月初五"),
    ("中秋节是农历哪一天？", "八月十五"),
    ("春节是农历哪一天？", "正月初一"),
    ("清明节是农历还是公历节日？", "公历"),
    ("重阳节是农历哪一天？", "九月初九"),
]
assert len(QA) == 60, len(QA)


def ask(question):
    prompt = f"{question}请简短回答（不要解释）。答完后另起一行写置信度0-1，例如：0.9"
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False,
                         "options": {"temperature": 0, "num_predict": 80}}).encode(),
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
            pred = lines[0].strip()[:80]
            m = re.search(r"0?\.\d+|1\.0|1(?!\d)", resp)
            conf = float(m.group(0)) if m else 0.8
            if conf > 1:
                conf = 0.8
            err = None
        except Exception as e:
            pred, conf, err = "", 0.0, str(e)
        rows.append({"trace_id": f"xloose-{i:02d}", "source": "xdomain-loose",
                     "model": MODEL, "question": q, "predicted_label": pred,
                     "gold_answer": gold, "confidence": conf, "error": err})
        print(f"{i}/60 {rows[-1]['trace_id']}: pred={pred!r} gold={gold!r} conf={conf}",
              flush=True)
    json.dump(rows, open("/tmp/cloud_xdomain60_loose.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("WROTE /tmp/cloud_xdomain60_loose.json")


if __name__ == "__main__":
    main()
