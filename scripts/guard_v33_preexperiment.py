"""R22-PRE: guard v33 experimental CJK single-char substring guard (NOT authoritative).

v3.2 stays authoritative and untouched. v33 adds ONE experimental rule in the
substring branch (mirror of the v3.1 short-ASCII formula guard):
  block substring acceptance iff the sides differ AND min(len(a2),len(g2))==1
  AND the single-char side is CJK (matches [\\u4e00-\\u9fff]).
Rationale: single CJK char (白/太白, 牧/牧之, 玄/玄德, 子/子美, 唐/唐朝)
over-accepts: a one-char fragment is not a correct answer. ASCII/numeric
single chars unaffected (formula guard already covers short-ASCII; single
digits still need numeric branch).

Pre-experiment protocol (read-only on sealed evidence):
- Recompute guarded outcomes on d2_60 (60) + cloud_new60 (60) with v33;
  report changed rows, McNemar v32-vs-v33, regression checklist
  (cloud-new-42 stays rejected; pilot-03, cloud-new-48 stay accepted).
- GOLD-100 flip-excluded 7 rows: report v33 verdict vs adjudicated basis.
- Writes results/guard_v33_PREEXPERIMENTAL.json ONLY. Sealed results,
  matcher library, and paper numbers untouched. Exit nonzero on violated
  regression expectation.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v32 import tolerant_match_v32 as v32  # noqa: E402
from label_match_v31 import (  # noqa: E402
    norm, SUFFIXES, SYNONYMS, _parse_cn_num, _EN_SYNONYMS_NORM,
    _NEG_PREFIXES, _POS_PREFIXES, _SHORT_ASCII, _CN_RE,
)
import re  # noqa: E402
from stats import exact_mcnemar  # noqa: E402

_CJK = re.compile(r"^[\u4e00-\u9fff]$")

V33_RULE = ("PRE-EXPERIMENTAL: v3.2 body verbatim + ONE extra guard in the "
            "SUBSTRING branch only (mirror of the v3.1 short-ASCII formula guard): "
            "block acceptance iff sides differ and min(len)==1 with the single-char "
            "side CJK. Empty-guard raw-fallback, negation-synonym (不会/否), "
            "echo-inclusion, numeric and exact branches untouched.")


def tolerant_match_v33(a, g) -> bool:
    """v32 body verbatim + CJK single-char guard inside substring branch only."""
    a2, g2 = norm(a), norm(g)
    if not a2 or not g2:
        # v3.2 empty-guard raw-fallback (sealed regression U1: '//' vs '//' accepts)
        if str(a).strip() and str(g).strip() and not a2 and not g2:
            return str(a).strip() == str(g).strip()
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
    # substring branch with v3.1 formula guard + v33 CJK single-char guard
    if len(g2) >= 2 and _parse_cn_num(g2) is None and (g2 in a2 or a2 in g2):
        formula_guarded = (a2 != g2 and _SHORT_ASCII.match(a2) and _SHORT_ASCII.match(g2)
                           and min(len(a2), len(g2)) <= 2)
        cjk_single = (a2 != g2 and min(len(a2), len(g2)) == 1
                      and _CJK.match(a2 if len(a2) == 1 else g2)
                      and _parse_cn_num(a2) is None)
        if not (formula_guarded or cjk_single):
            return True
        # else: fall through to numeric branch (rejects formula pairs/fragments)
    av, gv = _parse_cn_num(a2), _parse_cn_num(g2)
    if av is not None and gv is not None:
        if abs(av - gv) < 1e-6:
            return True
        if abs(av - gv) / max(abs(gv), 1.0) < 0.005:
            return True
    return False


def main():
    rows60 = [json.loads(l) for l in
              (HERE / "evidence" / "d2_60.jsonl").read_text(encoding="utf-8").splitlines()
              if l.strip()]
    rowsnew = json.loads((HERE / "evidence" / "cloud_new60_raw.json").read_text(encoding="utf-8"))

    def get(r):
        return (str(r.get("predicted_label", "")), str(r.get("gold_answer", "")))

    all_rows = ([(r["trace_id"], r["source"]) + get(r) for r in rows60]
                + [(r["trace_id"], r["source"]) + get(r) for r in rowsnew])
    changed = []
    v33_out = {}
    for tid, src, a, g in all_rows:
        o32 = bool(v32(a, g))
        o33 = tolerant_match_v33(a, g)
        v33_out[tid] = o33
        if o32 != o33:
            changed.append({"trace_id": tid, "source": src, "predicted": a, "gold": g,
                            "v32": o32, "v33": o33})
    # regression checklist
    assert v33_out.get("cloud-new-42") is False, "O vs O2 must stay rejected"
    assert v33_out.get("pilot-03") is True, "pilot-03 must stay accepted"
    assert v33_out.get("cloud-new-48") is True, "cloud-new-48 must stay accepted"
    b = sum(1 for ch in changed if ch["v32"] is False and ch["v33"] is True)
    c = sum(1 for ch in changed if ch["v32"] is True and ch["v33"] is False)
    p_two, _ = exact_mcnemar(b, c)
    # GOLD-100 flip-excluded 7 under v33
    key = json.loads((HERE / "evidence" / "gold100_key.json").read_text(encoding="utf-8"))
    import csv
    grows = {r["id"].strip(): r for r in
             csv.DictReader(open(HERE / "grades_gold100_user.csv", encoding="utf-8-sig"))}
    excl = []
    for hid, k in key["mapping"].items():
        if k["kind"] == "flip-excluded":
            r = grows[hid]
            excl.append({"h_id": hid, "predicted": r["response"], "gold": r["reference"],
                         "user": r["你的判定(对/错)"].strip(),
                         "v32": bool(v32(r["response"], r["reference"])),
                         "v33": tolerant_match_v33(r["response"], r["reference"]),
                         "adjudicated_basis": "错(exact)"})
    four_single = [e for e in excl if e["h_id"] in ("H62", "H68", "H71", "H82")]
    # H47/H85 are multi-char echo inclusions: v33=True there is CORRECT policy
    # (user blind grading 对), not a miss. Success = 4 singles flip + zero
    # collateral changes on sealed 120 + regression green.
    promote = (all(e["v33"] is False for e in four_single) and len(changed) == 0)
    out = {"matcher": "v33 PRE-EXPERIMENTAL (" + V33_RULE + ")",
           "n_rows": len(all_rows), "n_changed_vs_v32": len(changed), "changed": changed,
           "mcnemar_v32_vs_v33": {"b": b, "c": c, "p_two": p_two},
           "regression": {"cloud-new-42_rejected": True, "pilot-03_kept": True,
                          "cloud-new-48_kept": True},
           "gold100_flip_excluded_under_v33": excl,
           "verdict": ("PROMOTE-CANDIDATE" if promote else "HOLD")}
    (HERE / "results" / "guard_v33_PREEXPERIMENTAL.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
