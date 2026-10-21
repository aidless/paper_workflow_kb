# -*- coding: utf-8 -*-
"""R28 cross-domain collection (PREREG_R28_CROSSDOMAIN, frozen before answering).

Arm A "degenerate" (predicts zero flips): 40 arithmetic items, pure-numeric gold.
Arm B "uncovered"  (predicts zero flips AND miss>0): 40 English unit/count items,
    gold = pure number, questions phrase the unit to induce an English-unit answer.

Model qwen2:7b, temperature 0. Idempotent (skips already-collected ids).
Output: results/r28_answers_a.jsonl / results/r28_answers_b.jsonl
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2:7b"
OUT_A = HERE / "results" / "r28_answers_a.jsonl"
OUT_B = HERE / "results" / "r28_answers_b.jsonl"

# --- Arm A: arithmetic, CHINESE, gold = pure number (variant space degenerate) ---
ARM_A = [
    ("计算：234 + 567", "801"),
    ("计算：1000 - 456", "544"),
    ("计算：12 × 13", "156"),
    ("计算：144 ÷ 12", "12"),
    ("计算：25 + 75", "100"),
    ("计算：89 - 34", "55"),
    ("计算：15 × 15", "225"),
    ("计算：1000 ÷ 8", "125"),
    ("计算：7 × 9", "63"),
    ("计算：56 + 44", "100"),
    ("计算：200 - 88", "112"),
    ("计算：13 × 7", "91"),
    ("计算：729 ÷ 27", "27"),
    ("计算：350 + 650", "1000"),
    ("计算：90 - 45", "45"),
    ("计算：11 × 11", "121"),
    ("计算：625 ÷ 25", "25"),
    ("计算：128 + 872", "1000"),
    ("计算：300 - 123", "177"),
    ("计算：16 × 16", "256"),
    ("计算：100 ÷ 4", "25"),
    ("计算：47 + 53", "100"),
    ("计算：88 - 29", "59"),
    ("计算：9 × 8", "72"),
    ("计算：512 ÷ 8", "64"),
    ("计算：33 + 67", "100"),
    ("计算：150 - 75", "75"),
    ("计算：14 × 14", "196"),
    ("计算：840 ÷ 7", "120"),
    ("计算：250 + 250", "500"),
    ("计算：99 - 99", "0"),
    ("计算：6 × 7", "42"),
    ("计算：121 ÷ 11", "11"),
    ("计算：500 + 500", "1000"),
    ("计算：1000 - 1", "999"),
    ("计算：12 × 12", "144"),
    ("计算：999 ÷ 3", "333"),
    ("计算：80 + 20", "100"),
    ("计算：77 - 7", "70"),
    ("计算：3 × 3 × 3", "27"),
]

# --- Arm B: English unit/count facts, gold = pure number ---
ARM_B = [
    ("How many seconds are in one minute?", "60"),
    ("How many minutes are in one hour?", "60"),
    ("How many seconds are in one hour?", "3600"),
    ("How many minutes are in one day?", "1440"),
    ("How many seconds are in one day?", "86400"),
    ("How many hours are in one day?", "24"),
    ("How many days are in one week?", "7"),
    ("How many days are in one year?", "365"),
    ("How many weeks are in one year?", "52"),
    ("How many months are in one year?", "12"),
    ("How many inches are in one foot?", "12"),
    ("How many feet are in one yard?", "3"),
    ("How many feet are in one mile?", "5280"),
    ("How many ounces are in one pound?", "16"),
    ("How many pounds are in one US short ton?", "2000"),
    ("How many centimeters are in one meter?", "100"),
    ("How many meters are in one kilometer?", "1000"),
    ("How many grams are in one kilogram?", "1000"),
    ("How many milliliters are in one liter?", "1000"),
    ("How many degrees are in a full circle?", "360"),
    ("How many sides does a triangle have?", "3"),
    ("How many sides does a hexagon have?", "6"),
    ("How many legs does a spider have?", "8"),
    ("How many planets are in the solar system?", "8"),
    ("How many continents are on Earth?", "7"),
    ("How many states are in the United States?", "50"),
    ("How many cards are in a standard deck?", "52"),
    ("How many squares are on a chessboard?", "64"),
    ("How many bits are in one byte?", "8"),
    ("How many keys are on a standard piano?", "88"),
    ("How many bones are in the adult human body?", "206"),
    ("How many teeth does an adult human have?", "32"),
    ("How many colors are in a rainbow?", "7"),
    ("How many years are in a century?", "100"),
    ("How many years are in a decade?", "10"),
    ("How many zeros are in one million?", "6"),
    ("How many zeros are in one billion?", "9"),
    ("How many points are on a standard die?", "21"),
    ("How many letters are in the English alphabet?", "26"),
    ("How many Wonders of the Ancient World were there?", "7"),
]

CN_PROMPT = "{q}请用最短答案回答（不要解释）。答完后另起一行写置信度0-1，例如：0.9"
EN_PROMPT = "{q} Answer in the shortest form (no explanation). Then on a new line write a confidence 0-1, e.g. 0.9"


def ask(question, prompt_template):
    prompt = prompt_template.format(q=question)
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "think": False,
                         "options": {"temperature": 0, "num_predict": 80}}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=240) as r:
        return json.load(r)["response"]


def parse(resp):
    lines = [l.strip() for l in resp.splitlines() if l.strip()]
    ans = lines[0] if lines else ""
    floats = [float(m) for m in re.findall(r"(?<![0-9.])(?:0(?:\.\d+)?|1(?:\.0+)?)(?![0-9.])", resp)]
    conf = floats[-1] if floats else None
    return ans, conf


def run(arm, out_path, prompt_template, source):
    done = {}
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                done[r["trace_id"]] = r
    rows = list(done.values())
    for i, (q, gold) in enumerate(arm, 1):
        tid = f"{source}-{i:02d}"
        if tid in done and not done[tid].get("error"):
            continue
        try:
            resp = ask(q, prompt_template)
            ans, conf = parse(resp)
            rows.append({"trace_id": tid, "source": source, "model": MODEL,
                         "question": q, "gold_answer": gold, "predicted_label": ans,
                         "confidence": conf, "error": None, "raw": resp})
        except Exception as e:  # noqa: BLE001 - recorded, never fabricated
            rows.append({"trace_id": tid, "source": arm_source, "model": MODEL,
                         "question": q, "gold_answer": gold, "predicted_label": "",
                         "confidence": None, "error": f"{type(e).__name__}: {e}"[:200]})
        # rewrite full JSONL (append-friendly, idempotent)
        out_path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                            encoding="utf-8")
        print(f"{tid}: ok={rows[-1]['error'] is None}", flush=True)
    return rows


if __name__ == "__main__":
    arm = sys.argv[1] if len(sys.argv) > 1 else "both"
    if arm in ("a", "both"):
        run(ARM_A, OUT_A, CN_PROMPT, "r28-a")
    if arm in ("b", "both"):
        run(ARM_B, OUT_B, EN_PROMPT, "r28-b")
    print("done")