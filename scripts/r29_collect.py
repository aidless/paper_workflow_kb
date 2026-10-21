# -*- coding: utf-8 -*-
"""R29 top-up collection (PREREG_R29_POWER). qwen2:7b temp0, short-answer prompt
same as local-big. Idempotent. Output: results/r29_answers_topup.jsonl
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2:7b"
POOL = HERE / "evidence" / "r29_topup_560.json"
OUT = HERE / "results" / "r29_answers_topup.jsonl"


def ask(question):
    prompt = f"{question}请用最短答案回答（不要解释）。答完后另起一行写置信度0-1，例如：0.9"
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "think": False,
                         "options": {"temperature": 0, "num_predict": 60}}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=240) as r:
        return json.load(r)["response"]


def parse(resp):
    lines = [l.strip() for l in resp.splitlines() if l.strip()]
    ans = lines[0] if lines else ""
    floats = [float(m) for m in re.findall(r"(?<![0-9.])(?:0(?:\.\d+)?|1(?:\.0+)?)(?![0-9.])", resp)]
    conf = floats[-1] if floats else None
    return ans, conf


def main():
    pool = json.loads(POOL.read_text(encoding="utf-8"))
    done = {}
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                done[r["trace_id"]] = r
    rows = list(done.values())
    for i, item in enumerate(pool, 1):
        tid = f"r29-topup-{i:03d}"
        if tid in done and not done[tid].get("error"):
            continue
        try:
            resp = ask(item["q"])
            ans, conf = parse(resp)
            rows.append({"trace_id": tid, "source": "r29-topup", "model": MODEL,
                         "question": item["q"], "gold_answer": item["gold"], "by": item["by"],
                         "expr": item.get("expr", ""), "predicted_label": ans,
                         "confidence": conf, "error": None, "raw": resp})
        except Exception as e:  # noqa: BLE001
            rows.append({"trace_id": tid, "source": "r29-topup", "model": MODEL,
                         "question": item["q"], "gold_answer": item["gold"], "by": item["by"],
                         "expr": item.get("expr", ""), "predicted_label": "",
                         "confidence": None, "error": f"{type(e).__name__}: {e}"[:200]})
        OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                       encoding="utf-8")
        print(f"{tid}: ok={rows[-1]['error'] is None}", flush=True)
    print("done")


if __name__ == "__main__":
    main()