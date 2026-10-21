"""Power-rep P1 local collection: batch2 (157) on qwen2:7b (local-new paradigm).

Same 157 questions as cloud batch2 arm (same-question cross-model design).
Same protocol as local_new60 (temp 0, short answer + confidence).
Golds pending user spot-check; rejected rows discarded before analysis.
Trace ids: powL-###.

Run locally in background:
nohup python3 paper_workflow_kb/scripts/local_powrep157.py paper_workflow_kb > /tmp/local_powrep157.log 2>&1 &
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from batch2_power_rep import BATCH2

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2:7b"
QA = [("powL-%03d" % (i + 1), q, g) for i, (q, g) in enumerate(BATCH2)]
assert len(QA) == 157, len(QA)


def ask(question):
    prompt = f"{question}请用最短答案回答（不要解释）。答完后另起一行写置信度0-1，例如：0.9"
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False,
                         "options": {"temperature": 0, "num_predict": 60}}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)["response"]


def main(kb):
    import re
    rows = []
    for i, (tid, q, gold) in enumerate(QA, 1):
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
        rows.append({"trace_id": tid, "source": "power-rep-local",
                     "model": MODEL, "question": q, "predicted_label": pred,
                     "gold_answer": gold, "confidence": conf, "error": err})
        if i % 20 == 0 or i == len(QA):
            print(f"{i}/{len(QA)} {tid}: pred={pred!r} gold={gold!r}",
                  flush=True)
    json.dump(rows, open(os.path.join(kb, "evidence", "local_powrep157_raw.json"),
                         "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE evidence/local_powrep157_raw.json")


if __name__ == "__main__":
    main(sys.argv[1])
