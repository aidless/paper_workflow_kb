"""Power-rep LOOSE rerun: same 255 questions, paraphrase-regime prompt (cloud).

Rationale: tight arms came back flip-thin (b=3/255 cloud); per the xdomain
lesson, instruction format controls the paraphrase surface. Same questions,
loose prompt. Golds user-approved (全做, round 24). Trace ids: pow1L-###,
pow2L-###.

Upload batch files + this script to /tmp/powscripts and run from there:
nohup python3 paper_workflow_kb/scripts/cloud_powrep255_loose.py > /tmp/cloud_powrep255_loose.log 2>&1 &
"""
import json
import sys
import urllib.request

sys.path.insert(0, "paper_workflow_kb/scripts")
from batch1_power_rep import BATCH1
from batch2_power_rep import BATCH2

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"
QA = [("pow1L-%03d" % (i + 1), q, g) for i, (q, g) in enumerate(BATCH1)] + \
     [("pow2L-%03d" % (i + 1), q, g) for i, (q, g) in enumerate(BATCH2)]
assert len(QA) == 255, len(QA)


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
        rows.append({"trace_id": tid, "source": "power-rep-loose",
                     "model": MODEL, "question": q, "predicted_label": pred,
                     "gold_answer": gold, "confidence": conf, "error": err})
        if i % 25 == 0 or i == len(QA):
            print(f"{i}/{len(QA)} {tid}: pred={pred!r} gold={gold!r}",
                  flush=True)
    json.dump(rows, open("/tmp/cloud_powrep255_loose.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("WROTE /tmp/cloud_powrep255_loose.json")


if __name__ == "__main__":
    main()
