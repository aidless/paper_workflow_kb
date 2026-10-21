"""v3.3 CJK single-char substring guard: library (R22 promotion).

v3.2 (label_match_v32.tolerant_match_v32) stays authoritative and untouched.
v3.3 = v3.2 body verbatim + ONE extra guard in the substring branch only
(mirror of the v3.1 short-ASCII formula guard).

Guard definition (exact, disclosed in Methods):
  in the substring branch, block acceptance iff the sides differ AND
  min(len(a2), len(g2)) == 1 AND the single-char side matches ^[\\u4e00-\\u9fff]$
  (CJK). Blocked pairs fall through to the numeric branch (which rejects them:
  single CJK chars never parse as numbers).
Untouched: empty-guard raw-fallback (sealed U1: '//' vs '//' accepts),
negation-synonym (不会/不会 vs 否, 会 vs 是), echo-inclusion (multi-char
substring), EN-synonym, CN-fragment, numeric-equivalence, exact branches.
ASCII/numeric single chars: formula guard already covers short-ASCII pairs;
single digits still reach the numeric branch.

Promotion basis: R22-P1 global diff (scripts/guard_v33_global_diff.py):
1700 sealed pairs, 8 diffs, all single-CJK-substring class, 0 OTHER.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v31 import (  # noqa: E402
    norm, SUFFIXES, SYNONYMS, _parse_cn_num, _EN_SYNONYMS_NORM,
    _NEG_PREFIXES, _POS_PREFIXES, _SHORT_ASCII, _CN_RE,
)

__all__ = ["tolerant_match_v33", "V33_RULE"]

_CJK_SINGLE = re.compile(r"^[\u4e00-\u9fff]$")

V33_RULE = ("substring-branch CJK single-char guard: block iff sides differ "
            "and min(len)==1 with the single-char side CJK; "
            "v3.1 formula guard and v3.2 raw-fallback retained")


def tolerant_match_v33(a, g) -> bool:
    """v3.2 tolerant_match_v32 + CJK single-char guard in substring branch."""
    a2, g2 = norm(a), norm(g)
    if not a2 or not g2:
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
    # substring branch with v3.1 formula guard + v3.3 CJK single-char guard
    if len(g2) >= 2 and _parse_cn_num(g2) is None and (g2 in a2 or a2 in g2):
        formula_guarded = (a2 != g2 and _SHORT_ASCII.match(a2) and _SHORT_ASCII.match(g2)
                           and min(len(a2), len(g2)) <= 2)
        cjk_single = (a2 != g2 and min(len(a2), len(g2)) == 1
                      and _CJK_SINGLE.match(a2 if len(a2) == 1 else g2)
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
