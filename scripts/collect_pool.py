"""Generic pool collector (qwen2:7b temp 0, local). Usage:
python3 scripts/collect_pool.py <pool.json> <out_raw.json> <trace_prefix> <source_name>
Same prompt/parse contract as local_new60.py (disclosed). Resume-safe.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2:7b"


def ask(question, english=False):
    tail = ("Answer with the shortest answer (no explanation). Then on a new line "
            "write confidence 0-1, e.g.: 0.9" if english else
            "请用最短答案回答（不要解释）。答完后另起一行写置信度0-1，例如：0.9")
    prompt = f"{question}{tail}"
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({"model": MODEL, "prompt": prompt, "stream": False,
                         "options": {"temperature": 0, "num_predict": 60}}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=240) as r:
        return json.load(r)["response"]


def parse(resp):
    lines = [l.strip() for l in resp.splitlines() if l.strip()]
    ans = lines[0] if lines else ""
    floats = [float(m) for m in re.findall(r"(?<![0-9.])(?:0(?:\.\d+)?|1(?:\.0+)?)(?![0-9.])", resp)]
    return ans, (floats[-1] if floats else None)


def main():
    pool = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out_p = Path(sys.argv[2])
    prefix, source = sys.argv[3], sys.argv[4]
    done = {}
    if out_p.exists():
        for r in json.loads(out_p.read_text(encoding="utf-8")):
            done[r["trace_id"]] = r
    rows = []
    english = prefix.startswith("en")
    for i, item in enumerate(pool, 1):
        tid = f"{prefix}-{i:03d}"
        if tid in done and not done[tid].get("error") and done[tid].get("predicted_label"):
            rows.append(done[tid])
            continue
        try:
            resp = ask(item["q"], english)
            ans, conf = parse(resp)
            rows.append({"trace_id": tid, "source": source, "model": MODEL,
                         "question": item["q"], "gold_answer": item["gold"],
                         "gold_by": item.get("by"), "predicted_label": ans,
                         "confidence": conf, "error": None})
        except Exception as e:  # noqa: BLE001
            rows.append({"trace_id": tid, "source": source, "model": MODEL,
                         "question": item["q"], "gold_answer": item["gold"],
                         "gold_by": item.get("by"), "predicted_label": "",
                         "confidence": None, "error": f"{type(e).__name__}: {e}"[:200]})
        out_p.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{tid}: ok={rows[-1]['error'] is None} pred={rows[-1]['predicted_label'][:20]!r}",
              flush=True)
    print(f"WROTE {out_p} n={len(rows)}")


if __name__ == "__main__":
    main()
