"""Cloud new layer: 60 fresh QA pairs via qwen2.5:7b live (stratum cloud-new).
Same answer-style distribution as d2_60 (numeric+unit, yes/no synonymy, name variants).
Prompts model for short answer + self-confidence; saves raw responses.
Run: nohup python3 /tmp/cloud_new60.py > /tmp/cloud_new60.log 2>&1 &
"""
import json, urllib.request

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"

# 60 fresh questions with short gold answers (same style as d2_60 golds)
QA = [
    ("法国的首都是哪里？只答地名。", "巴黎"), ("日本的首都是哪里？只答地名。", "东京"),
    ("水的化学式是什么？", "H2O"), ("一年有多少天（平年取整）？只答数字。", "365"),
    ("一天有多少小时？只答数字。", "24"), ("珠穆朗玛峰高约多少米（取整）？只答数字。", "8848"),
    ("光速约每秒多少公里？只答数字。", "30万"), ("太阳系最大的行星是？", "木星"),
    ("莎士比亚是哪国人？答：英国。", "英国"), ("会下雨吗（假设不会）？答是或否。", "否"),
    ("这件事你会做吗（假设不会）？答是或否。", "否"), ("这个说法对吗（假设不对）？答是或否。", "否"),
    ("一年有多少个月？只答数字。", "12"), ("一周有多少天？只答数字。", "7"),
    ("1+1等于几？只答数字。", "2"), ("10的平方是几？只答数字。", "100"),
    ("北京是中国的首都吗？答是或否。", "是"), ("水会流动吗？答是或否。", "是"),
    ("鱼会游泳吗？答是或否。", "是"), ("鸟会飞吗（一般情况）？答是或否。", "是"),
    ("长城长约多少公里（取整万）？只答数字。", "2万"), ("长江长约多少公里？只答数字。", "6300"),
    ("黄河长约多少公里？只答数字。", "5400"), ("地球直径约多少公里？只答数字。", "12742"),
    ("月球绕地球一周约多少天？只答数字。", "27"), ("地球绕太阳一周约多少天？只答数字。", "365"),
    ("人民币100元等于多少元？只答数字。", "100"), ("一小时等于多少分钟？只答数字。", "60"),
    ("一分钟等于多少秒？只答数字。", "60"), ("一公里等于多少米？只答数字。", "1000"),
    ("曹雪芹写了哪部小说？只答书名。", "红楼梦"), ("李白是哪个朝代的诗人？", "唐"),
    ("杜甫是哪个朝代的诗人？", "唐"), ("孔子是哪个学派的创始人？", "儒家"),
    ("秦始皇统一六国在哪一年（公元前取整）？只答数字。", "221"),
    ("辛亥革命在哪一年？只答数字。", "1911"), ("新中国成立在哪一年？只答数字。", "1949"),
    ("人有几根手指（双手共）？只答数字。", "10"), ("人有几颗牙齿（成人正常）？只答数字。", "32"),
    ("水的沸点是多少摄氏度？只答数字。", "100"), ("水的冰点是多少摄氏度？只答数字。", "0"),
    ("氧气的化学符号是？", "O2"), ("二氧化碳的化学式是？", "CO2"),
    ("铁的化学符号是？", "Fe"), ("金的化学符号是？", "Au"),
    ("盐的主要成分化学式是？", "NaCl"), ("中国的首都是哪里？只答地名。", "北京"),
    ("美国的首都是哪里？只答地名。", "华盛顿"), ("英国的首都是哪里？只答地名。", "伦敦"),
    ("德国的首都是哪里？只答地名。", "柏林"), ("俄罗斯的首都是哪里？只答地名。", "莫斯科"),
    ("猫会叫吗？答是或否。", "是"), ("狗会跑吗？答是或否。", "是"),
    ("石头会浮在水面吗（一般）？答是或否。", "否"), ("太阳会从西边升起吗？答是或否。", "否"),
    ("一年有四个季节吗？答是或否。", "是"), ("水是液体吗（常温）？答是或否。", "是"),
    ("冰是固体吗？答是或否。", "是"), ("人需要呼吸吗？答是或否。", "是"),
    ("植物需要阳光吗？答是或否。", "是"),
]

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
        rows.append({"trace_id": f"cloud-new-{i:02d}", "source": "cloud-new",
                     "model": MODEL, "question": q, "predicted_label": pred,
                     "gold_answer": gold, "confidence": conf, "error": err})
        print(f"{i}/60 {rows[-1]['trace_id']}: pred={pred!r} gold={gold!r} conf={conf}", flush=True)
    json.dump(rows, open("/tmp/cloud_new60.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("WROTE /tmp/cloud_new60.json")

if __name__ == "__main__":
    main()
