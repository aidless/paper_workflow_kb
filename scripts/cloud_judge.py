"""Cloud independent judge: re-adjudicate all 16 flips with qwen2.5:7b temp 0.
Reads flips from local results/flips.json (uploaded), queries ollama API,
writes cloud_judge.json with per-row verdict + agreement vs same-session ruling.
"""
import json, urllib.request

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"

def judge(predicted, gold):
    prompt = (
        "You are a strict semantic-equivalence judge for QA answers. "
        "Decide whether the predicted answer expresses the correct answer in gold "
        "(semantic equivalence, NOT string equality). "
        "Numeric answers match if relative error < 0.5%%. "
        "Chinese negation synonyms (不会/不是/否) match; affirmation synonyms (会/是/yes) match. "
        "Unit suffixes (年/元/米/小时/公里/秒) do not change meaning. "
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
    return "correct" if "CORRECT" in out and "INCORRECT" not in out else "incorrect"

def main():
    flips = json.load(open("/tmp/flips_in.json", encoding="utf-8"))
    # flips.json shape: list of {trace_id, predicted, gold, ...} or dict; normalize
    if isinstance(flips, dict):
        rows = flips.get("flips", flips.get("rows", []))
    else:
        rows = flips
    results = []
    for row in rows:
        tid = row.get("trace_id", "?")
        pred = row.get("predicted", row.get("predicted_label", ""))
        gold = row.get("gold", row.get("gold_answer", ""))
        try:
            v = judge(pred, gold)
            err = None
        except Exception as e:
            v, err = "ERROR", str(e)
        results.append({"trace_id": tid, "predicted": pred, "gold": gold,
                        "cloud_verdict": v, "error": err})
        print(f"{tid}: {v}", flush=True)
    json.dump({"model": MODEL, "temperature": 0, "n": len(results),
               "rows": results},
              open("/tmp/cloud_judge.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("WROTE /tmp/cloud_judge.json")

if __name__ == "__main__":
    main()
