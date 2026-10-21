"""Seal guard v3.3 (R22-P2a): regression checklist + authoritative record.

Asserts (exit nonzero on violation):
  R1 O vs O2 still rejected (v3.1 formula guard retained);
  R2 pilot-03 / cloud-new-48 still accepted (multi-char names unaffected);
  R3 U1 '//' vs '//' still accepted (v3.2 raw-fallback retained);
  R4 U4 '//' vs '/' still rejected;
  R5 negation-synonym rows still accepted (不会/不是 vs 否, 会 vs 是);
  R6 the 4 single-CJK GOLD rows now rejected (白/太白, 牧/牧之, 玄/玄德, 子/子美);
  R7 authoritative v33 == pre-experiment v33 on all 1700 global-diff pairs
     (promotion fidelity: no transcription drift).
Writes results/guard_v33.json (authoritative; PRE file stays as history).
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v33 import tolerant_match_v33 as v33, V33_RULE  # noqa: E402
import guard_v33_preexperiment as pre  # noqa: E402
import guard_v33_global_diff as gd  # noqa: E402


def main():
    checks = []
    def ck(name, cond):
        checks.append({"name": name, "pass": bool(cond)})
        assert cond, name
    ck("R1 O/O2 rejected", v33("O", "O2") is False)
    ck("R2a pilot-03 kept", v33("威廉·莎士比亚", "莎士比亚") is True)
    ck("R2b cloud-new-48 kept", v33("华盛顿特区", "华盛顿") is True)
    ck("R3 U1 raw-fallback", v33("//", "//") is True)
    ck("R4 U4 raw differs", v33("//", "/") is False)
    ck("R5a 不会/否", v33("不会", "否") is True)
    ck("R5b 不是/否", v33("不是", "否") is True)
    ck("R5c 会/是", v33("会", "是") is True)
    ck("R6a 白/太白 rejected", v33("白", "太白") is False)
    ck("R6b 牧/牧之 rejected", v33("牧", "牧之") is False)
    ck("R6c 玄/玄德 rejected", v33("玄", "玄德") is False)
    ck("R6d 子/子美 rejected", v33("子", "子美") is False)
    pairs, _ = gd.load_pairs()
    drift = [(s, t) for s, t, a, g in pairs
             if bool(v33(a, g)) != bool(pre.tolerant_match_v33(a, g))]
    ck("R7 no transcription drift (1700 pairs)", len(drift) == 0)
    out = {"matcher": "label_match_v33 tolerant_match_v33 (v3.2 + CJK single-char substring guard)",
           "guard_rule": V33_RULE, "n_checks": len(checks),
           "checks": checks, "n_global_pairs": len(pairs)}
    (HERE / "results" / "guard_v33.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
