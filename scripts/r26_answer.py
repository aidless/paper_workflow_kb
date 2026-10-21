"""R26 answering (PREREG_R26_EXTERNAL R3).

qwen2:7b via local ollama, temp 0, short-answer prompt (same template family
as cloud_new60.py, English rendering for English questions).
Reads evidence/r26_*_sample.jsonl, writes results/r26_answers_*.jsonl
(question id + prediction verbatim + model digest). Resume-safe: skips ids
already present.
"""
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
EV = HERE / "evidence"
RES = HERE / "results"
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2:7b"
PROMPT = ("%s\nAnswer with the shortest possible answer (no explanation). "
          "Then on a new line write your confidence 0-1, e.g.: 0.9")


def model_digest():
    body = {"model": MODEL}
    req = urllib.request.Request("http://localhost:11434/api/show",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    return hashlib.sha256(
        json.dumps(d.get("details", {}), sort_keys=True).encode()).hexdigest()[:16]


def ask(question):
    body = {"model": MODEL, "prompt": PROMPT % question, "stream": False,
            "options": {"temperature": 0, "num_predict": 200}}
    req = urllib.request.Request(OLLAMA, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)["response"]


def run(split):
    src = EV / ("r26_%s_sample.jsonl" % split)
    rows = [json.loads(l) for l in src.read_text().splitlines() if l.strip()]
    outp = RES / ("r26_answers_%s.jsonl" % split)
    done = {}
    if outp.exists():
        for l in outp.read_text().splitlines():
            if l.strip():
                d = json.loads(l)
                done[d["id"]] = d
    digest = model_digest()
    print("model=%s digest=%s split=%s n=%d resume=%d" %
          (MODEL, digest, split, len(rows), len(done)), flush=True)
    with outp.open("a") as f:
        for r in rows:
            if r["id"] in done:
                continue
            try:
                resp = ask(r["question"])
            except Exception as e:
                print("ERROR %s: %r" % (r["id"], e), flush=True)
                continue
            f.write(json.dumps({"id": r["id"], "prediction": resp,
                                "model": MODEL, "digest": digest},
                               ensure_ascii=False) + "\n")
            f.flush()
            print("answered %s (%d chars)" % (r["id"], len(resp)), flush=True)


if __name__ == "__main__":
    RES.mkdir(exist_ok=True)
    run(sys.argv[1] if len(sys.argv) > 1 else "entity")
