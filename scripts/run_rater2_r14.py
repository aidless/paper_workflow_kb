# -*- coding: utf-8 -*-
"""R2 fourteenth O2 run (R31 requalification): local deepseek-r1:7b, temp 0, symmetric strict prompt.

Reads evidence/rater2_r14_prompt.txt, writes evidence/rater2_r14_raw.log +
evidence/rater2_r14.json (extracted JSON). Post-think JSON extraction: last block
containing "N".
"""
import json
import os
import re
import sys
import urllib.request

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:7b"


def main(kb):
    prompt = open(os.path.join(kb, "evidence", "rater2_r14_prompt.txt"),
                   encoding="utf-8").read()
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False,
                         "options": {"temperature": 0, "num_predict": 2000}}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=1800) as r:
        out = json.load(r)["response"]
    open(os.path.join(kb, "evidence", "rater2_r14_raw.log"), "w",
         encoding="utf-8").write(out)
    m = list(re.finditer(r"\{[^{}]*\"N\"[^{}]*\}", out, re.S))
    assert m, "no JSON score block found"
    scores = json.loads(m[-1].group(0))
    assert set(scores) >= {"N", "S", "Si", "C"}, scores.keys()
    json.dump(scores, open(os.path.join(kb, "evidence", "rater2_r14.json"), "w",
                            encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(scores, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
