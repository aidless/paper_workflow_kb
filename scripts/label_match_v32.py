"""v3.2 raw-fallback: library (charter A, P0).

v3.1 (label_match_v31.guarded_tolerant_match) stays authoritative and untouched.
v3.2 adds ONE rule at the empty-guard: when BOTH raw answers are non-blank
but BOTH norm to empty (the '//' vs '//' class: norm strips '/'), fall back
to stripped-raw equality instead of rejecting. All other empty cases still
reject (inherits the 2026-08 empty-answer guard).

Rule definition (exact, for Methods disclosure):
  if (not a2 or not g2):
      if str(a).strip() and str(g).strip() and not a2 and not g2:
          return str(a).strip() == str(g).strip()
      return False
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v31 import (  # noqa: E402
    norm, SUFFIXES, SYNONYMS, _parse_cn_num, _EN_SYNONYMS_NORM,
    _NEG_PREFIXES, _POS_PREFIXES, _SHORT_ASCII, _CN_RE,
)
import re  # noqa: E402

__all__ = ["tolerant_match_v32", "V32_RULE"]


V32_RULE = ("empty-guard raw-fallback: both raw non-blank but both norm empty "
            "-> stripped-raw equality; else reject")


def tolerant_match_v32(a, g) -> bool:
    """v3.1 guarded_tolerant_match + v3.2 empty-guard raw-fallback."""
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
    if len(g2) >= 2 and _parse_cn_num(g2) is None and (g2 in a2 or a2 in g2):
        guarded = (a2 != g2 and _SHORT_ASCII.match(a2) and _SHORT_ASCII.match(g2)
                   and min(len(a2), len(g2)) <= 2)
        if not guarded:
            return True
    av, gv = _parse_cn_num(a2), _parse_cn_num(g2)
    if av is not None and gv is not None:
        if abs(av - gv) < 1e-6:
            return True
        if abs(av - gv) / max(abs(gv), 1.0) < 0.005:
            return True
    return False
