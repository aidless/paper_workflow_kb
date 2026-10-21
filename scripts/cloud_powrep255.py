"""Power-rep P1 cloud collection: batch1 (98) + batch2 (157) = 255 rows.

Same protocol as cloud_new60 (qwen2.5:7b, temp 0, short answer + confidence).
Golds NOT yet user-approved: rows whose golds fail the pending spot-check
will be discarded before analysis (pre-registered). Trace ids: pow1-### (batch1),
pow2-### (batch2).

Upload to /tmp, run: nohup python3 /tmp/cloud_powrep255.py > /tmp/cloud_powrep255.log 2>&1 &
"""
import json
import sys
import urllib.request

sys.path.insert(0, "paper_workflow_kb/scripts")
from batch1_power_rep import BATCH1
from batch2_power_rep import BATCH2

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"
QA = [("pow1-%03d" % (i + 1), q, g) for i, (q, g) in enumerate(BATCH1)] + \
     [("pow2-%03d" % (i + 1), q, g) for i, (q, g) in enumerate(BATCH2)]
assert len(QA) == 255, len(QA)


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
        rows.append({"trace_id": tid, "source": "power-rep",
                     "model": MODEL, "question": q, "predicted_label": pred,
                     "gold_answer": gold, "confidence": conf, "error": err})
        if i % 25 == 0 or i == len(QA):
            print(f"{i}/{len(QA)} {tid}: pred={pred!r} gold={gold!r}",
                  flush=True)
    json.dump(rows, open("/tmp/cloud_powrep255.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("WROTE /tmp/cloud_powrep255.json")


if __name__ == "__main__":
    main()
