# -*- coding: utf-8 -*-
"""R1 twelfth O2 run (R30 requalification): local qwen2.5:7b, temp 0, symmetric strict prompt.

NOTE: R1 rater previously muse-spark-1.3 (cloud, now unavailable). This R30 run uses
qwen2.5:7b (local) as the R1 replacement; the substitution is disclosed, not hidden.
Reads evidence/rater2_r12_prompt.txt (identical symmetric prompt), writes
evidence/rater1_r12_raw.log + evidence/rater1_r12.json.
"""
import json
import os
import re
import sys
import urllib.request

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"


def main(kb):
    prompt = open(os.path.join(kb, "evidence", "rater2_r12_prompt.txt"),
                   encoding="utf-8").read()
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False,
                         "options": {"temperature": 0, "num_predict": 2000}}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=1800) as r:
        out = json.load(r)["response"]
    open(os.path.join(kb, "evidence", "rater1_r12_raw.log"), "w",
         encoding="utf-8").write(out)
    m = list(re.finditer(r"\{[^{}]*\"N\"[^{}]*\}", out, re.S))
    assert m, "no JSON score block found"
    scores = json.loads(m[-1].group(0))
    assert set(scores) >= {"N", "S", "Si", "C"}, scores.keys()
    scores["rater_model"] = MODEL
    scores["note"] = "R1 rater substituted: muse-spark-1.3 (unavailable) -> qwen2.5:7b (local)"
    json.dump(scores, open(os.path.join(kb, "evidence", "rater1_r12.json"), "w",
                            encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(scores, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
