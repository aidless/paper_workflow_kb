"""R21-P2: run local judges (qwen2:7b, gemma3:4b) on GOLD-100 62 flip rows.

Same semantic-equivalence prompt as scripts/local_judge.py (temp 0).
predicted=response, gold=reference from grades_gold100_user.csv;
human gold = user's blind verdict (user grading is the human rater here).
Flip rows selected via evidence/gold100_key.json kind in
(flip-confirmed, flip-excluded). Per R21-R2: ERROR rows dropped with note,
never imputed. Writes evidence/gold100_p2_verdicts.json.
"""
import csv
import json
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OLLAMA = "http://localhost:11434/api/generate"
MODELS = ["qwen2:7b", "gemma3:4b"]

PROMPT_TMPL = (
    "You are a strict semantic-equivalence judge for QA answers. "
    "Decide whether the predicted answer expresses the correct answer in gold "
    "(semantic equivalence, NOT string equality). "
    "Numeric answers match if relative error < 0.5%%. "
    "Chinese negation synonyms (不会/不是/否) match; affirmation synonyms (会/是/yes) match. "
    "Unit suffixes (年/元/米/小时/公里/秒) and book-title brackets do not change meaning. "
    "A trailing confidence number appended to an otherwise correct answer does not change meaning. "
    "Predicted answer: {predicted}. Gold answer: {gold}. "
    "IMPORTANT: output exactly one word, CORRECT or INCORRECT, with no explanation. "
    "Your entire response must be that single word."
)


def judge(model, predicted, gold):
    prompt = PROMPT_TMPL.format(predicted=predicted, gold=gold)
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({"model": model, "prompt": prompt, "stream": False,
                         "options": {"temperature": 0, "num_predict": 400}}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        out = json.load(r)["response"].strip().upper()
    v = "correct" if "CORRECT" in out and "INCORRECT" not in out else "incorrect"
    return v, out[:200]


def main():
    key = json.loads((HERE / "evidence" / "gold100_key.json").read_text(encoding="utf-8"))
    rows = list(csv.DictReader(open(HERE / "grades_gold100_user.csv", encoding="utf-8-sig")))
    flips = [r for r in rows
             if key["mapping"][r["id"].strip()]["kind"] in ("flip-confirmed", "flip-excluded")]
    assert len(flips) == 62, len(flips)
    out_rows = []
    for r in flips:
        hid = r["id"].strip()
        human = 1 if r["你的判定(对/错)"].strip() == "对" else 0
        kind = key["mapping"][hid]["kind"]
        for m in MODELS:
            try:
                v, raw = judge(m, r["response"], r["reference"])
                err = None
            except Exception as e:  # noqa: BLE001
                v, raw, err = "ERROR", "", str(e)[:200]
            out_rows.append({"trace_id": hid, "model": m, "kind": kind,
                             "predicted": r["response"], "gold": r["reference"],
                             "human_says_correct": human,
                             "judge_verdict": v, "raw": raw, "error": err})
            print(f"{hid} {m}: {v}", flush=True)
    ok = sum(1 for x in out_rows if x["judge_verdict"] != "ERROR")
    (HERE / "evidence" / "gold100_p2_verdicts.json").write_text(
        json.dumps({"models": MODELS, "n_flip_rows": len(flips), "n_calls": len(out_rows),
                    "n_ok": ok, "temperature": 0,
                    "prompt": "same-as-local_judge.py",
                    "rows": out_rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"WROTE evidence/gold100_p2_verdicts.json n_ok={ok}/{len(out_rows)}")


if __name__ == "__main__":
    main()
