"""R22-P3: local-judge runs on adversarial negatives (FPR denominators).

Pairs (all human=INCORRECT by sealed author/adjudicated labels):
- 12 formula-confusable (F-class, guard_synth.py DESIGN: chemically distinct,
  TRUE REJECT; e.g. O vs O2, C vs CO, N vs Na);
- 8 CJK single-char fragments (C-class, TRUE REJECT; 4 observed + 4 subtypes).
Human gold provenance: guard_synth.py sealed DESIGN commitment (author-labeled
ground truth, disclosed), NOT invented here. Counts asserted (12/8).

Judges: qwen2:7b, gemma3:4b, deepseek-r1:7b via ollama, temp 0, same
semantic-equivalence prompt as local_judge.py/P2. ERROR rows dropped with
note, never imputed. Writes evidence/adversarial_neg_verdicts.json.
"""
import json
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OLLAMA = "http://localhost:11434/api/generate"
MODELS = ["qwen2:7b", "gemma3:4b", "deepseek-r1:7b"]

# Provenance: scripts/guard_synth.py class F / class C literals (sealed DESIGN).
F = [("O", "O2"), ("H", "H2"), ("C", "CO"), ("N", "N2"), ("O", "O3"),
     ("C", "Ca"), ("P", "Pb"), ("S", "SO2"), ("K", "KCl"), ("C", "Cl"),
     ("N", "Na"), ("F", "Fe")]
C = [("牧", "牧之"), ("白", "太白"), ("子", "子美"), ("玄", "玄德"),
     ("李", "李白"), ("杜", "杜甫"), ("苏", "苏轼"), ("王", "王安石")]

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
    body = {"model": model, "prompt": prompt, "stream": False,
            "options": {"temperature": 0, "num_predict": 400}}
    if model.startswith("deepseek-r1"):
        body["think"] = False
    req = urllib.request.Request(
        OLLAMA, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        out = json.load(r)["response"].strip().upper()
    v = "correct" if "CORRECT" in out and "INCORRECT" not in out else "incorrect"
    return v, out[:200]


def main():
    assert len(F) == 12 and len(C) == 8, (len(F), len(C))
    pairs = [("formula-%02d" % (i + 1), a, g) for i, (a, g) in enumerate(F)] + \
            [("cjkfrag-%02d" % (i + 1), a, g) for i, (a, g) in enumerate(C)]
    rows = []
    for tid, a, g in pairs:
        for m in MODELS:
            try:
                v, raw = judge(m, a, g)
                err = None
            except Exception as e:  # noqa: BLE001
                v, raw, err = "ERROR", "", str(e)[:200]
            rows.append({"trace_id": tid, "model": m, "predicted": a, "gold": g,
                         "human_says_correct": 0, "judge_verdict": v,
                         "raw": raw, "error": err})
            print(f"{tid} {m}: {v}", flush=True)
    ok = sum(1 for x in rows if x["judge_verdict"] != "ERROR")
    (HERE / "evidence" / "adversarial_neg_verdicts.json").write_text(
        json.dumps({"models": MODELS, "n_pairs": len(pairs), "n_calls": len(rows),
                    "n_ok": ok, "temperature": 0, "human_basis": "sealed author labels (guard_synth DESIGN)",
                    "prompt": "same-as-local_judge.py",
                    "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"WROTE evidence/adversarial_neg_verdicts.json n_ok={ok}/{len(rows)}")


if __name__ == "__main__":
    main()
