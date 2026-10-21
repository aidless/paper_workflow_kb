# -*- coding: utf-8 -*-
"""R30 BoolQ collection (PREREG_R30_BOOLQ Amendment A2, FROZEN prompt/model).

gemma3:4b temp0 num_predict 60, model digest pinned per run.
Output: results/r30_answers_boolq_gemma.jsonl (id/prediction/model/digest).
Idempotent: skips ids already present without error.
"""
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"
OUT = HERE / "results" / "r30_answers_boolq_gemma.jsonl"
LOG = HERE / "results" / "r30_collect_boolq_gemma.log"

PROMPT = ("阅读以下英文短文并回答问题。用最短答案回答（不要解释）。"
          "答完后另起一行写置信度0-1，例如：0.9\n\n短文：%s\n\n问题：%s")


def digest():
    body = {"model": MODEL}
    req = urllib.request.Request("http://localhost:11434/api/show",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    return hashlib.sha256(
        json.dumps(d.get("details", {}), sort_keys=True).encode()).hexdigest()[:16]


def ask(question, passage):
    body = {"model": MODEL, "prompt": PROMPT % (passage, question),
            "stream": False,
            "options": {"temperature": 0, "num_predict": 60}}
    req = urllib.request.Request(OLLAMA, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)["response"]


def main():
    sample = [json.loads(l) for l in
              (HERE / "evidence" / "r30_boolq_sample.jsonl").read_text(
                  encoding="utf-8").splitlines() if l.strip()]
    assert len(sample) == 100, len(sample)
    done = {}
    if OUT.exists():
        for l in OUT.read_text(encoding="utf-8").splitlines():
            if l.strip():
                d = json.loads(l)
                if not d.get("error"):
                    done[d["id"]] = d
    dg = digest()
    log = open(LOG, "a", encoding="utf-8")
    n_new = 0
    for s in sample:
        if s["id"] in done:
            continue
        try:
            resp = ask(s["question"], s["passage"])
            done[s["id"]] = {"id": s["id"], "prediction": resp,
                             "model": MODEL, "digest": dg}
        except Exception as e:  # noqa: BLE001 - recorded, never fabricated
            done[s["id"]] = {"id": s["id"], "prediction": "",
                             "model": MODEL, "digest": dg,
                             "error": "%s: %s" % (type(e).__name__, e)}
        n_new += 1
        log.write("%s ok=%s\n" % (s["id"], "error" not in done[s["id"]]))
        log.flush()
        if n_new % 10 == 0:
            OUT.write_text("\n".join(json.dumps(done[k], ensure_ascii=False)
                                     for k in sorted(done)) + "\n",
                           encoding="utf-8")
    OUT.write_text("\n".join(json.dumps(done[k], ensure_ascii=False)
                             for k in sorted(done)) + "\n", encoding="utf-8")
    print("collected=%d total=%d -> %s" % (n_new, len(done), OUT.name))


if __name__ == "__main__":
    main()