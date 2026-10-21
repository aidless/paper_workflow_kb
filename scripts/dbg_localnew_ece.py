"""Debug local-new ECE mismatch: compare binners x outcomes."""
import json
import sys
from pathlib import Path

KB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KB / "scripts"))
from analyze_xdomain import ece_equal_width as ece_xd  # noqa
from label_match_v31 import guarded_tolerant_match  # noqa
from label_match_v3 import norm, tolerant_match  # noqa


def ece_new60(confs, outs):
    bins = [[] for _ in range(10)]
    for c, y in zip(confs, outs):
        b = min(int(min(max(c, 0.0), 1.0) * 10), 9)
        bins[b].append((c, y))
    n = len(confs)
    e = 0.0
    for b in bins:
        if b:
            acc = sum(y for _, y in b) / len(b)
            cf = sum(c for c, _ in b) / len(b)
            e += len(b) / n * abs(acc - cf)
    return round(e, 4)


rows = json.loads((KB / "evidence" / "local_new60_raw.json").read_text(encoding="utf-8"))
sub = [r for r in rows if r.get("confidence") is not None]
print("n_conf:", len(sub))
for name, fn in (("v31-guarded", guarded_tolerant_match), ("v3-tolerant", tolerant_match)):
    g = [int(fn(r["predicted_label"], r["gold_answer"])) for r in sub]
    e = [int(norm(r["predicted_label"]) == norm(r["gold_answer"])) for r in sub]
    c = [float(r["confidence"]) for r in sub]
    print(name, "n_guarded_sub:", sum(g), "n_exact_sub:", sum(e))
    print("  xdomain-binner EW_exact:", round(ece_xd(c, e), 4),
          "EW_guarded:", round(ece_xd(c, g), 4))
    print("  new60-binner   EW_exact:", ece_new60(c, e),
          "EW_guarded:", ece_new60(c, g), " <- manuscript 0.1255 / 0.0345")
