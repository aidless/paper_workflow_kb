# -*- coding: utf-8 -*-
"""Hetero-flip second adjudication: local deepseek-r1:7b (third family vs
gemma3:4b collection and qwen2.5:7b first judge).

PREREG_R31_HETEROJUDGE (frozen before judging): same one-word prompt as the
first judge (scripts/local_judge_heteromodel.py), temp 0, think ALLOWED
(disclosed: judging is a reasoning task); strip <think> blocks before the
same parse order (INCORRECT first, then CORRECT). Reads the same 11 raw
flips from results/r18_heteromodel.json, writes
evidence/r18_heteromodel_judge2.json. ERROR rows retried up to 3 attempts.

Usage: python3 paper_workflow_kb/scripts/local_judge_heteromodel_2.py paper_workflow_kb
"""
import json
import os
import re
import sys
import urllib.request

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:7b"
MAX_ATTEMPTS = 3


def judge(question, predicted, gold):
    prompt = (
        "You are a strict semantic-equivalence judge for QA answers. "
        "Question: " + question + " "
        "Decide whether the predicted answer expresses the correct answer in gold "
        "(semantic equivalence, NOT string equality). "
        "Numeric answers match if relative error < 0.5%%. "
        "Chinese negation synonyms (不会/不是/否) match; affirmation synonyms (会/是/yes/是的) match. "
        "Unit suffixes (年/元/米/小时/公里/秒/分钟/天) and polite particles (。的/居士/农历/日/农) do not change meaning. "
        "A full-name or title containing the gold name (e.g. 东坡居士 contains 东坡) matches. "
        f"Predicted answer: {predicted}. Gold answer: {gold}. "
        "Reply with exactly one word: CORRECT or INCORRECT."
    )
    last_out = ""
    for _ in range(MAX_ATTEMPTS):
        req = urllib.request.Request(
            OLLAMA,
            data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False,
                             "options": {"temperature": 0,
                                         "num_predict": 500}}).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=600) as r:
            out = json.load(r)["response"]
        last_out = out
        text = re.sub(r"<think>.*?</think>", "", out, flags=re.S).strip().upper()
        if "INCORRECT" in text:
            return "incorrect", None
        if "CORRECT" in text:
            return "correct", None
    return "ERROR", (last_out[:200] if last_out else "empty")


def main(kb):
    j1 = json.load(open(os.path.join(kb, "evidence",
                                     "r18_heteromodel_judge.json"),
                        encoding="utf-8"))
    assert j1["n"] == 11 and len(j1["rows"]) == 11, j1["n"]
    rows = []
    for f in j1["rows"]:
        tid = f["trace_id"]
        assert not tid.endswith(":c-cell"), tid
        q = f["question"]
        try:
            v, err = judge(q, f["predicted"], f["gold"])
        except Exception as e:  # noqa: BLE001 - recorded, never fabricated
            v, err = "ERROR", "%s: %s" % (type(e).__name__, e)
        rows.append({"trace_id": tid, "question": q, "predicted": f["predicted"],
                     "gold": f["gold"], "judge_verdict": v, "error": err})
        print(f"{tid}: {v}", flush=True)
    json.dump({"model": MODEL, "temperature": 0, "think": "allowed (disclosed)",
               "n": len(rows), "rows": rows},
              open(os.path.join(kb, "evidence", "r18_heteromodel_judge2.json"),
                   "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE evidence/r18_heteromodel_judge2.json")


if __name__ == "__main__":
    main(sys.argv[1])
