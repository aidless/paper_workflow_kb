"""R3 R2-statistics acceptance: independent recomputation (stdlib only)."""
import json
import math
import os

BASE = "~/F:\\deepseek/paper_workflow_kb"
RES = os.path.join(BASE, "results")


def mcnemar_two_sided(b, c):
    n = b + c
    if n == 0:
        return 1.0
    s = sum(math.comb(n, k) for k in range(0, min(b, c) + 1))
    return min(1.0, 2.0 * s / 2**n)


def wilson(x, n, z=1.96):
    p = x / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d, (c + m) / d)


print("== McNemar exact two-sided ==")
for b, c in [(11, 0), (9, 0), (20, 0), (19, 0), (12, 0), (7, 0),
              (6, 0), (5, 0), (4, 0), (2, 0), (1, 0), (0, 0)]:
    print(f"b={b:>2} c={c} -> p={mcnemar_two_sided(b, c)!r}")

print("== Wilson 24/25 ==")
lo, hi = wilson(24, 25)
print(f"lo={lo!r} hi={hi!r} rounded={[round(lo, 3), round(hi, 3)]}")

print("== Holm step3 ==")
print(f"threshold={0.05 / (17 - 3 + 1)!r} pool_p={mcnemar_two_sided(9, 0)!r} "
      f"stop={mcnemar_two_sided(9, 0) > 0.05 / (17 - 3 + 1)}")

print("== N / flips / merged rate ==")
n_list = [30, 30, 60, 60, 30, 160, 40, 60, 60, 20, 78, 157, 157]
f_list = [11, 5, 4, 5, 0, 4, 0, 1, 20, 0, 2, 1, 7]
print(f"N={sum(n_list)} flips={sum(f_list)} rate={sum(f_list) / sum(n_list):.4f}")

print("== JSON cross-check ==")
for fn in ["powrep.json", "powrep_rollups.json", "holm.json",
           "gold_guarded_agreement.json", "combined_qwen2.json",
           "xdomain_sensitivity.json"]:
    p = os.path.join(RES, fn)
    print(f"{fn}: {'FOUND' if os.path.exists(p) else 'MISSING'}")


def load(fn):
    with open(os.path.join(RES, fn), encoding="utf-8") as f:
        return json.load(f)


try:
    d = load("powrep.json")
    print("powrep keys:", list(d.keys()) if isinstance(d, dict) else type(d))
    print(json.dumps(d, indent=1)[:1500])
except Exception as e:
    print("powrep read err:", e)

try:
    d = load("powrep_rollups.json")
    print("rollups keys:", list(d.keys()) if isinstance(d, dict) else type(d))
    print(json.dumps(d, indent=1)[:1500])
except Exception as e:
    print("rollups read err:", e)

try:
    d = load("holm.json")
    print(json.dumps(d, indent=1)[:1200])
except Exception as e:
    print("holm read err:", e)

try:
    d = load("gold_guarded_agreement.json")
    print(json.dumps(d, indent=1)[:800])
except Exception as e:
    print("gold read err:", e)

try:
    d = load("combined_qwen2.json")
    print(json.dumps(d, indent=1)[:800])
except Exception as e:
    print("combined read err:", e)
