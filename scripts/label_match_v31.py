"""v3.1 substring guard: library + recomputation (Si fix-method run, goal-R2).

v3 (label_match_v3.tolerant_match) stays authoritative and untouched.
v3.1 adds ONE rule in the substring branch: refuse substring acceptance for
short-ASCII formula-confusable pairs (the O vs O2 class), then falls through
to the numeric-equivalence branch (which rejects O/O2).

Guard definition (exact, disclosed in Methods):
  block substring iff BOTH normed sides match ^[a-z0-9]{1,4}$,
  the sides differ, AND min(len(a2), len(g2)) <= 2.
CJK pairs (pilot-03, cloud-new-48) are non-ASCII -> unaffected by construction.
Pure-numeric gold never reaches substring in v3 -> unaffected.

Outputs results/guard_v31.json with per-stratum guarded metrics +
regression checklist. Exit nonzero on any violated expectation.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v3 import norm, SUFFIXES, SYNONYMS, _parse_cn_num  # noqa: E402
from stats import exact_mcnemar  # noqa: E402

_CN_RE = re.compile(r"[\u4e00-\u9fff]+")
_EN_SYNONYMS_NORM = {norm(k): v for k, v in
                     {"ascorbic acid": "抗坏血酸", "shakespear": "莎士比亚",
                      "shakespeare": "莎士比亚"}.items()}
_NEG_PREFIXES = ("不是", "不会")
_POS_PREFIXES = ("是", "会")
_SHORT_ASCII = re.compile(r"^[a-z0-9]{1,4}$")


def guarded_tolerant_match(a, g) -> bool:
    """v3 tolerant_match + formula guard in the substring branch."""
    a2, g2 = norm(a), norm(g)
    if not a2 or not g2:
        return False
    if a2 == g2:
        return True
    for suf in SUFFIXES:
        a2 = a2.replace(suf, "")
        g2 = g2.replace(suf, "")
    if a2 == g2:
        return True
    if SYNONYMS.get(a2) == g2:
        return True
    en_val = _EN_SYNONYMS_NORM.get(a2)
    if en_val is not None and en_val == g2:
        return True
    if re.search(r"[a-z]", a2) and _CN_RE.search(a2):
        cn_a = "".join(_CN_RE.findall(a2))
        if cn_a:
            if cn_a == g2 or g2 in cn_a:
                return True
            if len(g2) >= 2 and cn_a in g2:
                return True
    if g2 in ("否", "是"):
        for p in _NEG_PREFIXES:
            if a2.startswith(p) and g2 == "否":
                return True
        for p in _POS_PREFIXES:
            if a2.startswith(p) and g2 == "是":
                return True
    # substring branch with v3.1 guard
    if len(g2) >= 2 and _parse_cn_num(g2) is None and (g2 in a2 or a2 in g2):
        guarded = (a2 != g2 and _SHORT_ASCII.match(a2) and _SHORT_ASCII.match(g2)
                   and min(len(a2), len(g2)) <= 2)
        if not guarded:
            return True
        # else: fall through to numeric branch (rejects formula pairs)
    av, gv = _parse_cn_num(a2), _parse_cn_num(g2)
    if av is not None and gv is not None:
        if abs(av - gv) < 1e-6:
            return True
        if abs(av - gv) / max(abs(gv), 1.0) < 0.005:
            return True
    return False


def ece_equal_freq(confs, outs, bins=10):
    """Copied verbatim from analysis_d2.py ece_equal_freq (equal-frequency bins)."""
    pairs = sorted(zip(confs, outs))
    n = len(pairs)
    if n == 0:
        return 0.0
    size = max(1, n // bins)
    tot = 0.0
    for i in range(0, n, size):
        b = pairs[i:i + size]
        c = sum(p[0] for p in b) / len(b)
        a = sum(p[1] for p in b) / len(b)
        tot += abs(a - c) * len(b) / n
    return round(tot, 4)


def main() -> None:
    rows60 = [json.loads(l) for l in
              (HERE / "evidence" / "d2_60.jsonl").read_text(encoding="utf-8").splitlines()
              if l.strip()]
    rowsnew = json.loads((HERE / "evidence" / "cloud_new60_raw.json").read_text(encoding="utf-8"))

    def get(r):
        return (str(r.get("predicted_label", "")), str(r.get("gold_answer", "")),
                float(r.get("confidence", 0.0)))

    all_rows = ([(r["trace_id"], r["source"]) + get(r) for r in rows60]
                + [(r["trace_id"], r["source"]) + get(r) for r in rowsnew])

    import label_match_v3 as v3
    changed = []
    guarded_outcomes = {}
    for tid, src, a, g, c in all_rows:
        v3_out = bool(v3.tolerant_match(a, g))
        g_out = bool(guarded_tolerant_match(a, g))
        guarded_outcomes[tid] = g_out
        if v3_out != g_out:
            changed.append({"trace_id": tid, "source": src, "predicted": a, "gold": g,
                            "v3": v3_out, "v3.1": g_out})

    # Regression checklist (assertions, not assumptions)
    assert guarded_outcomes.get("cloud-new-42") is False, "O vs O2 must now reject"
    assert guarded_outcomes.get("pilot-03") is True, "pilot-03 name pair must stay accepted"
    assert guarded_outcomes.get("cloud-new-48") is True, "cloud-new-48 name pair must stay accepted"

    strata = {}
    for name, tids in (("pilot", [t for t, s, *_ in all_rows if s == "pilot"]),
                       ("holdout-main", [t for t, s, *_ in all_rows if s == "holdout-main"]),
                       ("cloud-new", [t for t, s, *_ in all_rows if s == "cloud-new"])):
        sub = [(t, s, a, g, c) for (t, s, a, g, c) in all_rows if t in set(tids)]
        n = len(sub)
        ex = [int(norm(a) == norm(g)) for _, _, a, g, _ in sub]
        gd = [int(guarded_outcomes[t]) for t, _, _, _, _ in sub]
        b = sum(1 for e, o in zip(ex, gd) if e == 0 and o == 1)
        cc = sum(1 for e, o in zip(ex, gd) if e == 1 and o == 0)
        p_two, _odds = exact_mcnemar(b, cc)
        confs = [c for _, _, _, _, c in sub]
        strata[name] = {"n": n, "n_guarded": sum(gd), "acc_guarded": round(sum(gd) / n, 4),
                        "n_exact": sum(ex), "flips_guarded": b + cc,
                        "flip_rate_guarded": round((b + cc) / n, 4),
                        "mcnemar_b": b, "mcnemar_c": cc, "mcnemar_p_two": p_two,
                        "ece10_guarded": ece_equal_freq(confs, gd)}

    out = {"matcher": "label_match_v31 guarded_tolerant_match (v3 + short-ASCII formula guard)",
           "guard_rule": "block substring iff both normed sides match ^[a-z0-9]{1,4}$, differ, min(len)<=2",
           "n_rows": len(all_rows), "n_changed_vs_v3": len(changed), "changed": changed,
           "changed_single_trace_id": (changed[0]["trace_id"] if len(changed) == 1 else None),
           "regression": {"cloud-new-42_rejected": True, "pilot-03_kept": True,
                          "cloud-new-48_kept": True},
           "strata": strata}
    (HERE / "results" / "guard_v31.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
