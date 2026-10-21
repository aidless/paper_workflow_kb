"""Local independent judge for local-new flips: qwen3:4b (think off), temp 0.

Heterogeneous w.r.t. authoring model (qwen2:7b). Same semantic-equivalence
standard as cloud_judge.py. Verdict parsed by CORRECT/INCORRECT keyword
(robust to rambling). Writes evidence/local_judge_new60.json.
"""
import json
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen3:4b"


def judge(predicted, gold):
    prompt = (
        "You are a strict semantic-equivalence judge for QA answers. "
        "Decide whether the predicted answer expresses the correct answer in gold "
        "(semantic equivalence, NOT string equality). "
        "Numeric answers match if relative error < 0.5%%. "
        "Chinese negation synonyms (不会/不是/否) match; affirmation synonyms (会/是/yes) match. "
        "Unit suffixes (年/元/米/小时/公里/秒) and book-title brackets do not change meaning. "
        "A trailing confidence number appended to an otherwise correct answer does not change meaning. "
        f"Predicted answer: {predicted}. Gold answer: {gold}. "
        "IMPORTANT: output exactly one word, CORRECT or INCORRECT, with no explanation. Your entire response must be that single word."
    )
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "think": False,
                         "options": {"temperature": 0, "num_predict": 400}}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=240) as r:
        out = json.load(r)["response"].strip().upper()
    return ("correct" if "CORRECT" in out and "INCORRECT" not in out else "incorrect"), out[:200]


def main():
    flips = json.loads((HERE / "results" / "flips_local60.json").read_text(encoding="utf-8"))
    rows = []
    for row in flips:
        try:
            v, raw = judge(row["predicted"], row["gold"])
            err = None
        except Exception as e:  # noqa: BLE001
            v, raw, err = "ERROR", "", str(e)[:200]
        rows.append({"trace_id": row["trace_id"], "predicted": row["predicted"],
                     "gold": row["gold"], "local_verdict": v, "error": err})
        print(f"{row['trace_id']}: {v}", flush=True)
    (HERE / "evidence" / "local_judge_new60.json").write_text(
        json.dumps({"model": MODEL, "think": False, "temperature": 0, "n": len(rows),
                    "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("WROTE evidence/local_judge_new60.json")


if __name__ == "__main__":
    main()
