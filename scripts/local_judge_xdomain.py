"""Heterogeneous independent judge for the 21 xdomain flips (local deepseek-r1:7b, temp 0).

Collection model is qwen2.5:7b (cloud); judge is a different family (local).
Reads flip lists from paper_workflow_kb/results/xdomain.json, writes
paper_workflow_kb/evidence/xdomain_judge.json. Verdict parsed from the LAST
line containing CORRECT/INCORRECT (reasoning models think aloud).

Usage: python3 paper_workflow_kb/scripts/local_judge_xdomain.py paper_workflow_kb
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
        "Unit suffixes (年/元/米/小时/公里/秒/分钟/天) and polite particles (。的/居士/农历/日) do not change meaning. "
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
    xd = json.load(open(os.path.join(kb, "results", "xdomain.json"), encoding="utf-8"))
    flips = ([dict(f, layer="tight", question=q)
              for f, q in []] +
             [{"trace_id": f["trace_id"], "predicted": f["predicted"],
               "gold": f["gold"], "layer": "tight",
               "question": r["question"]}
              for f in xd["tight"]["flips"]
              for r in json.load(open(os.path.join(
                  kb, "evidence", "cloud_xdomain60_raw.json"), encoding="utf-8"))
              if r["trace_id"] == f["trace_id"]] +
             [{"trace_id": f["trace_id"], "predicted": f["predicted"],
               "gold": f["gold"], "layer": "loose",
               "question": r["question"]}
              for f in xd["loose"]["flips"]
              for r in json.load(open(os.path.join(
                  kb, "evidence", "cloud_xdomain60_loose_raw.json"), encoding="utf-8"))
              if r["trace_id"] == f["trace_id"]])
    assert len(flips) == 21, len(flips)
    rows = []
    for fl in flips:
        try:
            v, _ = judge(fl["question"], fl["predicted"], fl["gold"])
            err = None
        except Exception as e:
            v, err = "ERROR", str(e)
        rows.append({"trace_id": fl["trace_id"], "layer": fl["layer"],
                     "predicted": fl["predicted"], "gold": fl["gold"],
                     "judge_verdict": v, "error": err})
        print(f"{fl['trace_id']}: {v}", flush=True)
    json.dump({"model": MODEL, "temperature": 0, "n": len(rows),
               "n_correct": sum(1 for r in rows if r["judge_verdict"] == "correct"),
               "n_incorrect": sum(1 for r in rows if r["judge_verdict"] == "incorrect"),
               "rows": rows},
              open(os.path.join(kb, "evidence", "xdomain_judge.json"), "w",
                   encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE evidence/xdomain_judge.json")


if __name__ == "__main__":
    main(sys.argv[1])
