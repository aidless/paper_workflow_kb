"""Power-rep LOOSE rerun: same 157 batch2 questions, local qwen2:7b.

Same-question cross-model loose arm (local-new paradigm under loose prompt).
Golds user-approved (全做, round 24). Trace ids: powLL-###.

Run locally in background:
nohup python3 paper_workflow_kb/scripts/local_powrep157_loose.py paper_workflow_kb > /tmp/local_powrep157_loose.log 2>&1 &
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from batch2_power_rep import BATCH2

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2:7b"
QA = [("powLL-%03d" % (i + 1), q, g) for i, (q, g) in enumerate(BATCH2)]
assert len(QA) == 157, len(QA)


def ask(question):
    prompt = f"{question}请简短回答（不要解释）。答完后另起一行写置信度0-1，例如：0.9"
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False,
                         "options": {"temperature": 0, "num_predict": 80}}).encode(),
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
            pred = lines[0].strip()[:80]
            m = re.search(r"0?\.\d+|1\.0|1(?!\d)", resp)
            conf = float(m.group(0)) if m else 0.8
            if conf > 1:
                conf = 0.8
            err = None
        except Exception as e:
            pred, conf, err = "", 0.0, str(e)
        rows.append({"trace_id": tid, "source": "power-rep-loose-local",
                     "model": MODEL, "question": q, "predicted_label": pred,
                     "gold_answer": gold, "confidence": conf, "error": err})
        if i % 20 == 0 or i == len(QA):
            print(f"{i}/{len(QA)} {tid}: pred={pred!r} gold={gold!r}",
                  flush=True)
    json.dump(rows, open(os.path.join(kb, "evidence", "local_powrep157_loose_raw.json"),
                         "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE evidence/local_powrep157_loose_raw.json")


if __name__ == "__main__":
    main(sys.argv[1])
