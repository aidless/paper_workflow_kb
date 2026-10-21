# -*- coding: utf-8 -*-
"""R32 English yes/no arm seal (PREREG_R32_ENYESNO R2/R3; C84 candidate).

Unique recomputation from the RAW answers (not from any intermediate file),
asserting the frozen counts across sample / answers / score / adjudication, then
applying the preregistered R3 decision rules.

Two scope facts are recorded here rather than smoothed over:
 1. PREREG R1 says "同 100 行规模" while the frozen design section R2 says a new
    60-row sample (30+30). R2 is the executed design; the inconsistency is
    disclosed, not silently resolved.
 2. R2 scopes the reject audit to "拒 <=60". The single longest reject here is
    150 chars, so the audit was run as a census of ALL 10 rejects -- a superset
    of the preregistered scope, which is the safe direction.
 3. The answer-form decomposition (bare / period / extended) was NOT preregistered.
    It is reported because with a native gold mapping the guard resolves
    "Yes." through its substring branch, whereas against the Chinese mapping it
    did not -- so the flip/miss split is otherwise uninterpretable.

Descriptive only: no Holm entry, no power claim, no paired test. Neither the R30
main arm (C78) nor the A2 second-model arm (C82) is retried or rewritten.

Output: results/r32_enyesno_seal.json
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from label_match_v3 import norm  # noqa: E402
from label_match_v33 import tolerant_match_v33  # noqa: E402
from r32_adjudicate_enyesno import polarity  # noqa: E402
from r32_collect_enyesno import PROMPT  # noqa: E402  (single source of truth)

# The frozen instruction must survive verbatim into the collection script, and
# the sealed prompt string is imported rather than retyped so the record cannot
# drift from what was actually sent.
FROZEN_INSTRUCTION = ("Answer with the shortest answer, then confidence on "
                      "a new line")
assert FROZEN_INSTRUCTION in PROMPT, PROMPT

Z95 = 1.959963984540054


def wilson95(x, n):
    p = x / n
    denom = 1 + Z95 * Z95 / n
    center = (p + Z95 * Z95 / (2 * n)) / denom
    half = Z95 * math.sqrt(p * (1 - p) / n + Z95 * Z95 / (4 * n * n)) / denom
    return (round(center - half, 4), round(center + half, 4))


def main():
    # --- sample: frozen shape + disjointness from the R30 100 rows ---
    sample = [json.loads(l) for l in
              (HERE / "evidence" / "r32_enyesno_sample.jsonl").read_text(
                  encoding="utf-8").splitlines() if l.strip()]
    assert len(sample) == 60, len(sample)
    assert sum(1 for s in sample if s["gold"] == "Yes") == 30
    assert sum(1 for s in sample if s["gold"] == "No") == 30
    r30_ids = {json.loads(l)["id"] for l in
               (HERE / "evidence" / "r30_boolq_sample.jsonl").read_text(
                   encoding="utf-8").splitlines() if l.strip()}
    overlap = sorted({s["id"] for s in sample} & r30_ids)
    assert not overlap, overlap

    answers = {}
    for l in (HERE / "results" / "r32_answers_enyesno.jsonl").read_text(
            encoding="utf-8").splitlines():
        if l.strip():
            d = json.loads(l)
            answers[d["id"]] = d
    assert len(answers) == 60, len(answers)
    assert {a["model"] for a in answers.values()} == {"qwen2:7b"}
    digests = {a["digest"] for a in answers.values()}
    assert len(digests) == 1, digests

    # --- recompute exact / guard / flip / reject from raw answers ---
    n_scored = n_exact = n_guard = n_flips = 0
    forms = {"bare": 0, "period_variant": 0, "extended": 0, "other": 0}
    errors = []
    flip_correct = over_fire = 0
    for s in sample:
        a = answers[s["id"]]
        if a.get("error") or not a.get("prediction"):
            errors.append(s["id"])
            continue
        lines = [l.strip() for l in
                 str(a["prediction"]).splitlines() if l.strip()]
        pred = lines[0] if lines else ""
        e = norm(pred) == norm(s["gold"])
        g = tolerant_match_v33(pred, s["gold"])
        n_scored += 1
        n_exact += e
        n_guard += g
        n_flips += (not e) and g
        n = norm(pred)
        forms["bare" if n in ("yes", "no") else
              "period_variant" if n in ("yes.", "no.") else
              "extended" if n.startswith("yes") or n.startswith("no") else
              "other"] += 1
        if (not e) and g:
            pol = polarity(pred)
            if (pol == "yes" and s["gold_bool"] is True) or \
               (pol == "no" and s["gold_bool"] is False):
                flip_correct += 1
            else:
                over_fire += 1

    assert not errors, errors
    assert n_scored == 60, n_scored
    assert n_exact == 15, n_exact
    assert n_guard == 50, n_guard
    assert n_flips == 35, n_flips
    assert forms == {"bare": 17, "period_variant": 1, "extended": 42,
                     "other": 0}, forms
    assert flip_correct == 35 and over_fire == 0, (flip_correct, over_fire)

    # --- cross-check the adjudication pack ---
    adj = json.loads((HERE / "results" / "r32_adjudication_enyesno.json")
                     .read_text(encoding="utf-8"))
    assert adj["n_flips"] == n_flips
    assert adj["n_flip_correct"] == flip_correct and adj["n_over_fire"] == 0
    assert adj["n_rejects"] == 10 and adj["n_miss"] == 0
    assert adj["n_correct_reject"] == 10, adj["n_correct_reject"]
    assert adj["model"] == "qwen2:7b"

    n_rejects = 10
    payload = {
        "arm": "R32 English native yes/no (PREREG_R32_ENYESNO)",
        "model": "qwen2:7b",
        "model_digest": sorted(digests)[0],
        "n": 60,
        "n_true": 30, "n_false": 30,
        "overlap_with_r30_sample": 0,
        "n_scored": n_scored,
        "n_errors": len(errors),
        "n_exact": n_exact,
        "exact_rate": round(n_exact / n_scored, 4),
        "exact_wilson95": wilson95(n_exact, n_scored),
        "n_guard": n_guard,
        "n_flips": n_flips,
        "flip_rate_scored": round(n_flips / n_scored, 4),
        "flip_wilson95": wilson95(n_flips, n_scored),
        "n_flip_correct": flip_correct,
        "over_fire": over_fire,
        "n_rejects": n_rejects,
        "n_miss": adj["n_miss"],
        "n_correct_reject": adj["n_correct_reject"],
        "reject_census": "all %d rejects (longest %d chars; prereg scoped <=60, "
                         "census is a superset)" % (n_rejects, adj["reject_len_max"]),
        "form_counts_not_preregistered": forms,
        "gold_mapping": "True->Yes / False->No (native, PREREG R2 frozen)",
        "prompt": PROMPT,
        "prompt_frozen_instruction": FROZEN_INSTRUCTION,
        "comparison_r30_main_arm": {"model": "qwen2:7b", "n": 100,
                                    "n_exact": 0, "n_guard": 55, "n_flips": 55,
                                    "n_miss": 31, "n_correct_reject": 14,
                                    "over_fire": 0},
        "decision_rule_1_exact_zero": (
            "SUPPORTED: exact 15/60 = 0.25 under the native mapping vs 0/100 "
            "under True->是/False->否. R30's exact-zero is a mapping artifact; "
            "the R30 hedge is upgraded to a mechanism conclusion."),
        "decision_rule_2_discrimination": (
            "NOT the same form: 0 misses here. With a native gold the guard "
            "resolves the trailing-period variant through its substring branch "
            "(the single Yes./No. row became a flip), whereas against the "
            "Chinese mapping that class was uncovered (R30 miss 31). Recorded "
            "as mapping dependence, per PREREG R3."),
        "scope": ("descriptive observed-status; no Holm entry, no power claim, "
                  "no paired test; different rows and n (60 vs 100) so the arm "
                  "comparison is not paired; R30 (C78) and A2 (C82) sealed "
                  "numbers neither retried nor rewritten"),
        "disclosure_prereg_inconsistency": (
            "PREREG R1 says 'same 100-row scale', R2 freezes a new 60-row "
            "sample. R2 was executed as the frozen design section; the "
            "inconsistency is disclosed rather than silently resolved."),
    }
    (HERE / "results" / "r32_enyesno_seal.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
