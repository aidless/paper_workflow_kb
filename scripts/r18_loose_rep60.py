"""R18 P0-data(b): 60 fresh questions, LOOSE prompt (xdomain-loose replica).

Pre-registered in PREREG_R18_LOOSE_REP.md BEFORE collection.
Upload to /tmp, run: nohup python3 /tmp/r18_loose_rep60.py > /tmp/r18_loose_rep60.log 2>&1 &
"""
import json
import urllib.request

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"

# 60 fresh [question, gold], de-duplicated vs all prior rows (see r18_dedup_check.py).
R18_QA = [
    # A. measure-word conversions, new entities (20)
    ("一令纸等于多少张？", "500"),
    ("一纪等于多少年？", "12"),
    ("一世等于多少年？", "30"),
    ("一刀纸等于多少张？", "100"),
    ("半个世纪等于多少年？", "50"),
    ("一平方公里等于多少平方米？", "1000000"),
    ("一分等于多少秒？", "60"),
    ("一周等于多少小时？", "168"),
    ("一天等于多少分钟？", "1440"),
    ("一年等于多少天？", "365"),
    ("一吨水等于多少升？", "1000"),
    ("一天有几个时辰？", "12"),
    ("一时辰等于几小时？", "2"),
    ("一个时辰等于多少分钟？", "120"),
    ("一海里等于多少米？", "1852"),
    ("一立方千米等于多少立方米？", "1000000000"),
    ("一毫升等于多少立方厘米？", "1"),
    ("一升等于多少立方厘米？", "1000"),
    ("一微米等于多少纳米？", "1000"),
    ("一微秒等于多少纳秒？", "1000"),
    # B. rephrased yes-no, new animal entities (20)
    ("章鱼有八条腿吗？", "是"),
    ("白蚁是昆虫吗？", "是"),
    ("萤火虫会发光吗？", "是"),
    ("蝴蝶是昆虫吗？", "是"),
    ("蜈蚣是昆虫吗？", "否"),
    ("蝎子是昆虫吗？", "否"),
    ("龙虾是鱼吗？", "否"),
    ("水母是鱼吗？", "否"),
    ("扇贝是鱼吗？", "否"),
    ("乌贼会喷墨吗？", "是"),
    ("海豹是哺乳动物吗？", "是"),
    ("考拉是哺乳动物吗？", "是"),
    ("鸭嘴兽是哺乳动物吗？", "是"),
    ("信天翁会飞吗？", "是"),
    ("啄木鸟会飞吗？", "是"),
    ("鸵鸟会飞吗？", "否"),
    ("蚂蚁是昆虫吗？", "是"),
    ("壁虎会断尾吗？", "是"),
    ("蜜蜂会酿蜜吗？", "是"),
    ("螳螂是昆虫吗？", "是"),
    # C. name variants, new persons (20)
    ("陶渊明字什么？", "潜"),
    ("杜牧字什么？", "牧之"),
    ("李贺字什么？", "长吉"),
    ("王勃字什么？", "子安"),
    ("孟浩然字什么？", "浩然"),
    ("王昌龄字什么？", "少伯"),
    ("高适字什么？", "达夫"),
    ("陈子昂字什么？", "伯玉"),
    ("温庭筠字什么？", "飞卿"),
    ("李商隐字什么？", "义山"),
    ("岳飞字什么？", "鹏举"),
    ("辛弃疾字什么？", "幼安"),
    ("陆游字什么？", "务观"),
    ("文天祥字什么？", "履善"),
    ("海瑞字什么？", "汝贤"),
    ("戚继光字什么？", "元敬"),
    ("徐霞客名什么？", "弘祖"),
    ("蒲松龄字什么？", "留仙"),
    ("吴敬梓字什么？", "敏轩"),
    ("郑板桥原名是什么？", "燮"),
]
assert len(R18_QA) == 60, len(R18_QA)


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
    for i, (q, gold) in enumerate(R18_QA, 1):
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
        rows.append({"trace_id": f"lr18-{i:02d}", "source": "r18-loose-rep",
                     "model": MODEL, "question": q, "predicted_label": pred,
                     "gold_answer": gold, "confidence": conf, "error": err})
        print(f"{i}/60 {rows[-1]['trace_id']}: pred={pred!r} gold={gold!r} conf={conf}",
              flush=True)
    json.dump(rows, open("/tmp/r18_loose_rep60.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("WROTE /tmp/r18_loose_rep60.json")


if __name__ == "__main__":
    main()
