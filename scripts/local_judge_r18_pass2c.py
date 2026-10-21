"""R18 adjudication pass 2c: last attempt on the 2 persistent judge ERRORs.

Fix: bilingual verdict parser (r1 sometimes answers in Chinese).
Check negative patterns first (不正确 contains 正确).
Saves raw tails on record. One attempt each; if still unparseable,
rows are reported as judge-ERROR (instrument failure, disclosed).

Usage: python3 paper_workflow_kb/scripts/local_judge_r18_pass2c.py paper_workflow_kb
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.join("paper_workflow_kb", "scripts"))
from local_judge_r18 import OLLAMA, MODEL  # noqa: E402

RETRY = ["lr18-34", "lr18-46"]
NEG = ("INCORRECT", "不正确", "不对", "错误", "不符")
POS = ("CORRECT", "正确", "对的", "相符")


def judge2(question, predicted, gold):
    prompt = (
        "You are a strict semantic-equivalence judge for QA answers. "
        "Question: " + question + " "
        "Decide whether the predicted answer expresses the correct answer in gold "
        "(semantic equivalence, NOT string equality). "
        "Numeric answers match if relative error < 0.5%%. "
        "Chinese negation synonyms match; affirmation synonyms match. "
        "Unit suffixes and polite particles do not change meaning. "
        "A full-name or title containing the gold name matches. "
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
        if any(n.upper() in u for n in NEG):
            verdict = "incorrect"
            break
        if any(p.upper() in u for p in POS):
            verdict = "correct"
            break
    return verdict, out[-300:]


def main(kb):
    rows = json.load(open(os.path.join(kb, "evidence", "r18_judge.json"),
                          encoding="utf-8"))
    by_id = {r["trace_id"]: r for r in rows}
    out = []
    for i, tid in enumerate(RETRY, 1):
        r = by_id[tid]
        try:
            v, tail = judge2(r["question"], r["predicted"], r["gold"])
            err = None
        except Exception as e:
            v, tail, err = "ERROR", "", str(e)
        out.append({"trace_id": tid, "question": r["question"],
                    "predicted": r["predicted"], "gold": r["gold"],
                    "judge_verdict": v, "judge_raw_tail": tail, "error": err})
        print(f"{i}/{len(RETRY)} {tid}: {v} tail={tail[-120:]!r}", flush=True)
    json.dump(out, open(os.path.join(kb, "evidence", "r18_judge_pass2c.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE evidence/r18_judge_pass2c.json")


if __name__ == "__main__":
    main(sys.argv[1])
