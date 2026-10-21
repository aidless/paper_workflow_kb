"""v3.4 candidate: v3.3 + token-containment fallback (R26 pre-reg R5, FROZEN).

v3.3 (label_match_v33.tolerant_match_v33) stays authoritative and untouched.
v3.4 = v3.3 accept, else token-containment fallback:

  tokenize: lowercase alphanumeric tokens (unicode word chars), drop empties.
  accept iff gold-token set non-empty AND (gold-tokens <= pred-tokens
  OR pred-tokens <= gold-tokens).

Adoption bar (pre-reg R5): combined miss drop >= 5 rows AND over-fire
increase <= 2 rows on the sealed R26 samples; else negative result, no cut.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v33 import tolerant_match_v33  # noqa: E402

__all__ = ["tolerant_match_v34", "V34_RULE", "tokenize"]

_TOKEN_RE = re.compile(r"\w+", re.UNICODE)

V34_RULE = ("v3.3 accept, else token-containment fallback: gold-token set "
            "non-empty and (gold <= pred or pred <= gold) on lowercased "
            "unicode-word tokens")


def tokenize(s):
    return [t.lower() for t in _TOKEN_RE.findall(str(s))]


def tolerant_match_v34(a, g) -> bool:
    if tolerant_match_v33(a, g):
        return True
    ta, tg = set(tokenize(a)), set(tokenize(g))
    if not tg or not ta:
        return False
    return tg <= ta or ta <= tg
