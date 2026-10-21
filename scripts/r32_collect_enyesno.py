# -*- coding: utf-8 -*-
"""R32 English yes/no arm collection (PREREG_R32_ENYESNO R2, FROZEN).

Same model as the R30 main arm (qwen2:7b, temperature 0, num_predict 60) so the
only thing that changes is the language of the instruction and of the gold
mapping — that is the arm's whole point (remove the cross-language confound).

Frozen instruction (PREREG R2, verbatim):
    "Answer with the shortest answer, then confidence on a new line"
Frozen gold mapping: True->Yes / False->No.

Output: results/r32_answers_enyesno.jsonl (id/prediction/model/digest).
Idempotent: skips ids already present without error; failures are recorded,
never imputed (R5 failure path).
"""
import hashlib
import json
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2:7b"
OUT = HERE / "results" / "r32_answers_enyesno.jsonl"
LOG = HERE / "results" / "r32_collect_enyesno.log"

PROMPT = ("Answer with the shortest answer, then confidence on a new line"
          "\n\nPassage: %s\n\nQuestion: %s")


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
              (HERE / "evidence" / "r32_enyesno_sample.jsonl").read_text(
                  encoding="utf-8").splitlines() if l.strip()]
    assert len(sample) == 60, len(sample)
    done = {}
    if OUT.exists():
        for l in OUT.read_text(encoding="utf-8").splitlines():
            if l.strip():
                d = json.loads(l)
                if not d.get("error"):
                    done[d["id"]] = d
    dg = digest()
    print("model=%s digest=%s already=%d" % (MODEL, dg, len(done)))
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
