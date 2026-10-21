"""Hetero-flip adjudication: local qwen2.5:7b (hetero family vs gemma3:4b).

Collection model is gemma3:4b; judge is qwen family (pre-reg gate: flip rate
0.1833 > 5%). Same one-word prompt as the cloud qwen-judge precedent
(scripts/cloud_judge.py). Reads flips from results/r18_heteromodel.json,
writes evidence/r18_heteromodel_judge.json.

Usage: python3 paper_workflow_kb/scripts/local_judge_heteromodel.py paper_workflow_kb
"""
import json
import os
import sys
import urllib.request

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"


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
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False,
                         "options": {"temperature": 0, "num_predict": 10}}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        out = json.load(r)["response"].strip().upper()
    if "INCORRECT" in out:
        return "incorrect"
    if "CORRECT" in out:
        return "correct"
    return "ERROR"


def main(kb):
    hm = json.load(open(os.path.join(kb, "results", "r18_heteromodel.json"),
                        encoding="utf-8"))
    raw = json.load(open(os.path.join(kb, "evidence",
                                      "r18_heteromodel_gemma60_raw.json"),
                         encoding="utf-8"))
    by_id = {r["trace_id"]: r for r in raw}
    flips = hm["heteromodel"]["flips"]
    assert len(flips) == 11, len(flips)
    rows = []
    for f in flips:
        tid = f["trace_id"]
        assert not tid.endswith(":c-cell"), tid
        q = by_id[tid]["question"]
        try:
            v = judge(q, f["predicted"], f["gold"])
            err = None
        except Exception as e:
            v, err = "ERROR", str(e)
        rows.append({"trace_id": tid, "question": q, "predicted": f["predicted"],
                     "gold": f["gold"], "judge_verdict": v, "error": err})
        print(f"{tid}: {v}", flush=True)
    json.dump({"model": MODEL, "temperature": 0, "n": len(rows), "rows": rows},
              open(os.path.join(kb, "evidence", "r18_heteromodel_judge.json"),
                   "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE evidence/r18_heteromodel_judge.json")


if __name__ == "__main__":
    main(sys.argv[1])
