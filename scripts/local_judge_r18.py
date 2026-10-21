"""Heterogeneous judge for the 27 R18 loose-rep flips (local deepseek-r1:7b, temp 0).

Collection model is qwen2.5:7b (cloud); judge is a different family (local).
Reads flip list from paper_workflow_kb/results/r18_loose_rep.json with questions
from paper_workflow_kb/evidence/r18_loose_rep60_raw.json; writes
paper_workflow_kb/evidence/r18_judge.json. Verdict parsed from the LAST
line containing CORRECT/INCORRECT (reasoning models think aloud).

Precedent (xdomain): same-line confidence leaks (是的。0.9) may draw
first-pass rejections as a protocol artifact; if so, a stripped second
pass re-judges exactly those rows with both passes kept on record
(scripts/local_judge_r18_pass2.py).

Usage: python3 paper_workflow_kb/scripts/local_judge_r18.py paper_workflow_kb
"""
import json
import os
import sys
import urllib.request

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:7b"


def judge(question, predicted, gold):
    prompt = (
        "You are a strict semantic-equivalence judge for QA answers. "
        "Question: " + question + " "
        "Decide whether the predicted answer expresses the correct answer in gold "
        "(semantic equivalence, NOT string equality). "
        "Numeric answers match if relative error < 0.5%%. "
        "Chinese negation synonyms (不会/不是/否) match; affirmation synonyms (会/是/yes/是的) match. "
        "Unit suffixes (年/元/米/小时/公里/秒/分钟/天/张/升/纳米) and polite particles do not change meaning. "
        "A full-name or title containing the gold name (e.g. 东坡居士 contains 东坡) matches. "
        f"Predicted answer: {predicted}. Gold answer: {gold}. "
        "End your reply with exactly one word on its own line: CORRECT or INCORRECT."
    )
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False,
                         "options": {"temperature": 0, "num_predict": 600}}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=600) as r:
        out = json.load(r)["response"]
    verdict = "ERROR"
    for line in reversed(out.strip().split("\n")):
        u = line.strip().upper()
        if "INCORRECT" in u:
            verdict = "incorrect"
            break
        if "CORRECT" in u:
            verdict = "correct"
            break
    return verdict, out[:500]


def main(kb):
    res = json.load(open(os.path.join(kb, "results", "r18_loose_rep.json"),
                         encoding="utf-8"))
    raw = json.load(open(os.path.join(kb, "evidence", "r18_loose_rep60_raw.json"),
                         encoding="utf-8"))
    by_id = {r["trace_id"]: r for r in raw}
    flips = res["loose_rep"]["flips"]
    assert len(flips) == 27, len(flips)
    rows = []
    for i, fl in enumerate(flips, 1):
        q = by_id[fl["trace_id"]]["question"]
        try:
            v, _ = judge(q, fl["predicted"], fl["gold"])
            err = None
        except Exception as e:
            v, err = "ERROR", str(e)
        rows.append({"trace_id": fl["trace_id"], "question": q,
                     "predicted": fl["predicted"], "gold": fl["gold"],
                     "judge_verdict": v, "error": err})
        print(f"{i}/{len(flips)} {fl['trace_id']}: {v}", flush=True)
    json.dump(rows, open(os.path.join(kb, "evidence", "r18_judge.json"), "w",
                         encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE evidence/r18_judge.json")


if __name__ == "__main__":
    main(sys.argv[1])
