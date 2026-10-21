"""4th stratum (local-new): same 60 fresh questions, local qwen2:7b temp 0.

Cross-model replication layer (disclosed new stratum, stratified inference
only): different model vs cloud-new (qwen2.5:7b) — same family, different
generation/capacity, local host. (First attempt with qwen3:4b failed:
thinking-mode responses unparseable as short answers; 60 empty rows discarded,
script now uses qwen2:7b which follows the short-answer format.)
Parsing rule (disclosed): answer = first non-empty response line;
confidence = last float in [0,1] found in the response (prompt asks for it
last); failures recorded with error field, never fabricated.
Writes evidence/local_new60_raw.json incrementally (resume-safe: skips
trace_ids already present).
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from cloud_new60 import QA  # noqa: E402  (same 60 questions + golds)

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2:7b"
OUT = HERE / "evidence" / "local_new60_raw.json"


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


def main() -> None:
    done = {}
    if OUT.exists():
        for r in json.loads(OUT.read_text(encoding="utf-8")):
            done[r["trace_id"]] = r
    rows = []
    for i, (q, gold) in enumerate(QA, 1):
        tid = f"local-new-{i:02d}"
        if tid in done and not done[tid].get("error"):
            rows.append(done[tid])
            continue
        try:
            resp = ask(q)
            ans, conf = parse(resp)
            rows.append({"trace_id": tid, "source": "local-new", "model": MODEL,
                         "question": q, "gold_answer": gold, "predicted_label": ans,
                         "confidence": conf, "error": None, "raw": resp})
        except Exception as e:  # noqa: BLE001 - recorded, never fabricated
            rows.append({"trace_id": tid, "source": "local-new", "model": MODEL,
                         "question": q, "gold_answer": gold, "predicted_label": "",
                         "confidence": None, "error": f"{type(e).__name__}: {e}"[:200]})
        OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{tid}: ok={rows[-1]['error'] is None}", flush=True)
    print(f"WROTE {OUT} n={len(rows)}")


if __name__ == "__main__":
    main()
