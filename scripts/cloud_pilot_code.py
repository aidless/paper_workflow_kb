"""Cloud PILOT probe: does the exact-vs-guarded flip phenomenon appear in a
code-QA domain? (feasibility for a cross-domain charter, NOT claim evidence)

12 short Python-fact questions, same collection protocol as cloud_new60
(qwen2.5:7b, temp 0, short answer + confidence line). Analysis compares
exact vs guarded (v31) counts only; no ledger claim is drawn from n=12.
Upload to /tmp, run: nohup python3 /tmp/cloud_pilot_code.py > /tmp/cloud_pilot_code.log 2>&1 &
"""
import json
import urllib.request

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"

QA = [
    ("Python中表示空值的关键字是？只答关键字。", "None"),
    ("Python中列表的长度函数是？只答函数名。", "len"),
    ("Python中定义函数的关键字是？只答关键字。", "def"),
    ("Python中整数除法（向下取整）的运算符是？只答运算符。", "//"),
    ("Python中字符串拼接用哪个运算符？只答运算符。", "+"),
    ("Python中判断对象类型的函数是？只答函数名。", "type"),
    ("Python中打开文件的函数是？只答函数名。", "open"),
    ("Python中捕获异常的关键字是？只答关键字。", "try"),
    ("Python中定义类的关键字是？只答关键字。", "class"),
    ("Python中导入模块的关键字是？只答关键字。", "import"),
    ("Python中布尔真值的字面量是？只答字面量。", "True"),
    ("Python中注释用的符号是？只答符号。", "#"),
]
assert len(QA) == 12, len(QA)


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
        rows.append({"trace_id": f"code-pilot-{i:02d}", "source": "code-pilot",
                     "model": MODEL, "question": q, "predicted_label": pred,
                     "gold_answer": gold, "confidence": conf, "error": err})
        print(f"{i}/12 {rows[-1]['trace_id']}: pred={pred!r} gold={gold!r} conf={conf}", flush=True)
    json.dump(rows, open("/tmp/cloud_pilot_code.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("WROTE /tmp/cloud_pilot_code.json")


if __name__ == "__main__":
    main()
