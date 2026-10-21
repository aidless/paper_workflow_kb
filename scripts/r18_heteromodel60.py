"""R18 P1-2: hetero-family validation - xdomain 60 questions, deepseek-r1:7b local.

Pre-registered in PREREG_R18_HETEROMODEL.md BEFORE collection.
Run in background: nohup python3 paper_workflow_kb/scripts/r18_heteromodel60.py
Resume-safe: appends incrementally, skips trace_ids already present.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

KB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KB / "scripts"))
from cloud_xdomain60_loose import QA  # noqa: E402  (same 60 questions + golds)

assert len(QA) == 60, len(QA)

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"
OUT = KB / "evidence" / "r18_heteromodel_gemma60_raw.json"


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


def main():
    done = {}
    if OUT.exists():
        for r in json.loads(OUT.read_text(encoding="utf-8")):
            done[r["trace_id"]] = r
    rows = []
    for i, (q, gold) in enumerate(QA, 1):
        tid = f"gr18-{i:02d}"
        if tid in done:
            rows.append(done[tid])
            continue
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
        rows.append({"trace_id": tid, "source": "r18-heteromodel-gemma",
                     "model": MODEL, "question": q, "predicted_label": pred,
                     "gold_answer": gold, "confidence": conf, "error": err})
        OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2),
                       encoding="utf-8")
        print(f"{i}/60 {tid}: pred={pred!r} gold={gold!r} conf={conf}",
              flush=True)
    print(f"DONE n={len(rows)} -> {OUT}")


if __name__ == "__main__":
    main()
