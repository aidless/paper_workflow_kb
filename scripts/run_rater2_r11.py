"""R2 tenth-O2 run: local deepseek-r1:7b, temp 0, symmetric strict prompt.

Reads paper_workflow_kb/evidence/rater2_r11_prompt.txt, writes
evidence/rater2_r11_raw.log (full response) and evidence/rater2_r11.json
(extracted JSON). Post-think JSON extraction: last {...} block.

Usage: python3 paper_workflow_kb/scripts/run_rater2_r11.py paper_workflow_kb
"""
import json
import os
import re
import sys
import urllib.request

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:7b"


def main(kb):
    prompt = open(os.path.join(kb, "evidence", "rater2_r11_prompt.txt"),
                   encoding="utf-8").read()
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False,
                         "options": {"temperature": 0,
                                     "num_predict": 2000}}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=1800) as r:
        out = json.load(r)["response"]
    open(os.path.join(kb, "evidence", "rater2_r11_raw.log"), "w",
         encoding="utf-8").write(out)
    m = list(re.finditer(r"\{[^{}]*\"N\"[^{}]*\}", out, re.S))
    assert m, "no JSON score block found"
    scores = json.loads(m[-1].group(0))
    assert set(scores) >= {"N", "S", "Si", "C"}, scores.keys()
    json.dump(scores, open(os.path.join(kb, "evidence", "rater2_r11.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(scores, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
