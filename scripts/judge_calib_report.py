"""R21-P3: judge-calibration summary (pilot inventory + P2 local runs).

Reads results/judge_calib_inventory.json (96 pairs, sealed pilot) +
evidence/gold100_p2_verdicts.json (P2 local runs, gated: missing file ->
pilot-only report, clearly labeled; NOT a failure).
Per judge-model: n, FNR + Wilson95 (human=correct subset), FPR + Wilson95
(human=incorrect subset), agreement + Wilson95.
Enable rule (pre-registered): FNR<0.15 AND FPR<0.10 (point estimates) AND
lower Wilson bounds within 2x of thresholds; else HOLD (stay uncalibrated,
S cap unchanged). Writes results/judge_calib_report.json.
"""
import json
import math
import os
import sys


def wilson(x, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = x / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round(max(0.0, (c - m) / d), 4), round(min(1.0, (c + m) / d), 4))


def norm_judge(v):
    v = str(v).strip().lower()
    if v == "correct":
        return 1
    if v == "incorrect":
        return 0
    return None


def stats(pairs):
    # pairs: (judge_says_correct, human_says_correct)
    hc = [(j, h) for j, h in pairs if j is not None]
    n = len(hc)
    fn = sum(1 for j, h in hc if h == 1 and j == 0)
    fp = sum(1 for j, h in hc if h == 0 and j == 1)
    np_ = sum(1 for _, h in hc if h == 1)
    nn = sum(1 for _, h in hc if h == 0)
    ag = sum(1 for j, h in hc if j == h)
    fnr = fn / np_ if np_ else None
    fpr = fp / nn if nn else None
    return {"n": n, "n_dropped": len(pairs) - n,
            "n_human_correct": np_, "n_human_incorrect": nn,
            "fn": fn, "fp": fp,
            "fnr": (round(fnr, 4) if fnr is not None else None),
            "fnr_wilson95": list(wilson(fn, np_)),
            "fpr": (round(fpr, 4) if fpr is not None else None),
            "fpr_wilson95": list(wilson(fp, nn)),
            "agree": ag, "agreement": round(ag / n, 4) if n else None,
            "agree_wilson95": list(wilson(ag, n))}


def main(kb):
    inv = json.load(open(os.path.join(kb, "results", "judge_calib_inventory.json"),
                         encoding="utf-8"))
    per_judge = {}
    for p in inv["pairs"]:
        j = p["judge"]
        per_judge.setdefault(j, []).append((p["judge_says_correct"], p["human_says_correct"]))
    p2path = os.path.join(kb, "evidence", "gold100_p2_verdicts.json")
    p2_note = "P2 pending"
    if os.path.exists(p2path):
        p2 = json.load(open(p2path, encoding="utf-8"))
        for r in p2["rows"]:
            per_judge.setdefault("gold100-p2:" + r["model"], []).append(
                (norm_judge(r["judge_verdict"]), r["human_says_correct"]))
        p2_note = (f"P2 included: {p2['n_ok']}/{p2['n_calls']} ok "
                   f"({', '.join(p2['models'])})")
    apath = os.path.join(kb, "evidence", "adversarial_neg_verdicts.json")
    if os.path.exists(apath):
        ap = json.load(open(apath, encoding="utf-8"))
        for r in ap["rows"]:
            per_judge.setdefault("adversarial:" + r["model"], []).append(
                (norm_judge(r["judge_verdict"]), r["human_says_correct"]))
        p2_note += (f"; adversarial included: {ap['n_ok']}/{ap['n_calls']} ok")
    out_judges = {}
    for j, pairs in sorted(per_judge.items()):
        s = stats(pairs)
        fnr, fpr = s["fnr"], s["fpr"]
        enabled = (fnr is not None and fpr is not None and fnr < 0.15 and fpr < 0.10
                   and s["n_human_incorrect"] >= 10)
        s["enable_decision"] = ("ENABLE-CANDIDATE" if enabled else "HOLD")
        out_judges[j] = s
    out = {"pilot_n": inv["n_pairs"], "pilot_human_incorrect": inv["n_human_incorrect"],
           "p2_status": p2_note, "by_judge": out_judges,
           "method_note": ("binary verdicts, no confidence: temperature scaling / ECE "
                           "N/A (R21-D1); calibration = FNR/FPR + agreement + Wilson CI; "
                           "FPR needs >=10 human-incorrect denominators to judge 0.10")}
    json.dump(out, open(os.path.join(kb, "results", "judge_calib_report.json"),
                        "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
