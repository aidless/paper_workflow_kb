"""7th stratum (cloud-math): 40 fresh MATH questions, cloud qwen2.5:7b temp 0.

Second question family (R2-N critique: single short-answer QA type).
Numeric answers only (unambiguous, short); same answer+confidence prompt and
parse rule as cloud_new60.py (answer=first line, confidence=last float).
Runs ON the cloud host (upload + ssh exec); writes evidence/cloud_math40_raw.json
incrementally (resume-safe).
"""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"
OUT = HERE / "evidence" / "cloud_math40_raw.json"

# 40 fresh math questions, short unambiguous numeric golds
QA = [
    ("12乘以13等于几？只答数字。", "156"), ("144除以12等于几？只答数字。", "12"),
    ("15的平方是几？只答数字。", "225"), ("2的10次方是几？只答数字。", "1024"),
    ("100减去37等于几？只答数字。", "63"), ("25乘以4等于几？只答数字。", "100"),
    ("1000除以8等于几？只答数字。", "125"), ("9的立方是几？只答数字。", "729"),
    ("50的20%是几？只答数字。", "10"), ("200的15%是几？只答数字。", "30"),
    ("1/2加1/4等于几（小数）？只答数字。", "0.75"), ("3/4化为小数是几？只答数字。", "0.75"),
    ("圆周率取3.14，直径10的圆周长是几？只答数字。", "31.4"),
    ("边长7的正方形面积是几？只答数字。", "49"),
    ("长8宽5的长方形面积是几？只答数字。", "40"),
    ("17加28加35等于几？只答数字。", "80"), ("1000减333等于几？只答数字。", "667"),
    ("11乘以11等于几？只答数字。", "121"), ("13乘以17等于几？只答数字。", "221"),
    ("2乘以3乘以5等于几？只答数字。", "30"), ("100除以4再乘以3等于几？只答数字。", "75"),
    ("60的一半再加10等于几？只答数字。", "40"), ("90减少1/3后是几？只答数字。", "60"),
    ("7天等于几小时？只答数字。", "168"), ("2小时等于几分钟？只答数字。", "120"),
    ("3天等于几小时？只答数字。", "72"), ("1周加3天共几天？只答数字。", "10"),
    ("5打鸡蛋有几个（一打12个）？只答数字。", "60"), ("4双袜子有几只？只答数字。", "8"),
    ("一箱24瓶水，3箱有几瓶？只答数字。", "72"), ("每排9人，6排有几人？只答数字。", "54"),
    ("100元买35元的东西找回几元？只答数字。", "65"), ("50元买两件20元的东西找回几元？只答数字。", "10"),
    ("19加21等于几？只答数字。", "40"), ("45减18等于几？只答数字。", "27"),
    ("6乘以9等于几？只答数字。", "54"), ("72除以9等于几？只答数字。", "8"),
    ("5的4次方是几？只答数字。", "625"), ("10的3次方是几？只答数字。", "1000"),
    ("123加456等于几？只答数字。", "579"),
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


def parse(resp):
    lines = [l.strip() for l in resp.splitlines() if l.strip()]
    ans = lines[0] if lines else ""
    floats = [float(m) for m in re.findall(r"(?<![0-9.])(?:0(?:\.\d+)?|1(?:\.0+)?)(?![0-9.])", resp)]
    return ans, (floats[-1] if floats else None)


def main() -> None:
    done = {}
    if OUT.exists():
        for r in json.loads(OUT.read_text(encoding="utf-8")):
            done[r["trace_id"]] = r
    rows = []
    for i, (q, gold) in enumerate(QA, 1):
        tid = f"cloud-math-{i:02d}"
        if tid in done and not done[tid].get("error"):
            rows.append(done[tid])
            continue
        try:
            resp = ask(q)
            ans, conf = parse(resp)
            rows.append({"trace_id": tid, "source": "cloud-math", "model": MODEL,
                         "question": q, "gold_answer": gold, "predicted_label": ans,
                         "confidence": conf, "error": None})
        except Exception as e:  # noqa: BLE001
            rows.append({"trace_id": tid, "source": "cloud-math", "model": MODEL,
                         "question": q, "gold_answer": gold, "predicted_label": "",
                         "confidence": None, "error": f"{type(e).__name__}: {e}"[:200]})
        OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{tid}: ok={rows[-1]['error'] is None}", flush=True)
    print(f"WROTE {OUT} n={len(rows)}")


if __name__ == "__main__":
    main()
