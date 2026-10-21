# -*- coding: utf-8 -*-
"""ROUND R15 tex revisions (adversarial R1-R8 punch list). Substring replaces
with occurrence asserts; aborts on any mismatch. Run from workspace root:
  python3 paper_workflow_kb/scripts/apply_R15.py
"""
import io
import sys

P = "paper_workflow_kb/paper/main.tex"
t = io.open(P, encoding="utf-8").read()

EDITS = [
 # --- E1: H1 directional reframe (R1-01) ---
 ("H1: the tolerant matcher flips more than 5\\% of exact-matcher conclusions on the same rows. Separately, a procedural gate (not part of H1): each flip must be adjudicated before any calibration claim is made (the adjudication gate).",
  "H1: on the same rows, the tolerant matcher flips exact-wrong answers to correct strictly more often than the reverse direction (paired asymmetry, tested by the exact McNemar test below). Separately, two non-inferential conventions: a descriptive 5\\% flip-rate bar inherited from the label-matcher validation gate (G006: unadjudicated flips above 5\\% block any calibration claim), and a procedural gate (not part of H1): each flip must be adjudicated before any calibration claim is made (the adjudication gate).",
  1),
 ("supports H1 descriptively and inferentially (p=0.0010)",
  "clears the descriptive bar and supports H1 inferentially (p=0.0010)", 1),
 ("supports H1 descriptively (0.1667 exceeds 0.05) but its paired",
  "clears the descriptive bar (0.1667 exceeds 0.05) but its paired", 1),
 ("supports H1 descriptively (0.0833 exceeds 0.05) with a non-significant",
  "clears the descriptive bar (0.0833 exceeds 0.05) with a non-significant", 1),
 ("is supported descriptively only (0.0833 exceeds 0.05)",
  "clears the descriptive bar only (0.0833 exceeds 0.05)", 2),
 ("0 flips, so H1 is not supported there",
  "0 flips, so neither the descriptive bar nor H1 is met there", 1),
 ("H1 is supported both descriptively (0.3667 exceeds 0.05) and inferentially at alpha=0.05.",
  "The flip rate clears the descriptive bar (0.3667 exceeds 0.05) and H1 is supported inferentially at alpha=0.05.", 1),
 ("H1 is supported descriptively only; the paired significance conclusion is hedged.",
  "The descriptive bar is cleared but paired significance is absent; the conclusion stays hedged.", 1),
 ("H1 is not supported here: on clean English short answers",
  "Neither the descriptive bar nor H1 is met here: on clean English short answers", 1),
 ("H1 is not supported descriptively (0.025 below 0.05) on this arithmetic-heavy stratum.",
  "The descriptive bar is missed (0.025 below 0.05) on this arithmetic-heavy stratum.", 1),
 ("The descriptive H1 bar (>5\\%) is missed while the paired test is significant",
  "The descriptive bar (>5\\%) is missed while the paired H1 test is significant", 1),
 ("H1 is not supported on pure numeric questions",
  "Neither the descriptive bar nor H1 is met on pure numeric questions", 1),
 ("H1 is not supported descriptively (0.0167 below 0.05) under tight instructions",
  "The descriptive bar is missed (0.0167 below 0.05) under tight instructions", 1),
 ("H1 is supported both descriptively and inferentially: loosening",
  "The flip rate clears the descriptive bar and H1 is supported inferentially: loosening", 1),
 # --- E3: abstract Holm qualifier (R1-06/R2-01/R6-01) ---
 ("and two post-registration extended strata, holdout 7 of 108 (p=0.0156) and local-new 12 of 217 (p=0.0005), reported with observed-significance status.",
  "and two post-registration extended strata, holdout 7 of 108 (p=0.0156) and local-new 12 of 217 (p=0.0005), reported with observed-significance status. Under Holm-Bonferroni over all seventeen paired tests, two of the five survive (pilot, cross-domain loose); the other three are stratum-local observed significance.", 1),
 # --- E2: GOLD 24/25 (R5-01/R7-01) ---
 ("a blinded 25-item gold set grades 25 of 25 in agreement (Wilson 95\\% CI 0.867 to 1.0)",
  "a blinded 25-item gold set grades 24 of 25 against guarded outcomes (Wilson 95\\% CI 0.805 to 0.993; the single divergence is G06/cloud-new-42, the documented false-positive case the blinded grader accepted while the guarded verdict is incorrect)", 1),
 ("67 confirmed correct on content",
  "67 of the 68 judged rows confirmed correct on content", 2),
 ("A one-rule guard reproduces the full adjudication exactly (one fix, zero regressions)",
  "A one-rule guard reproduces the full adjudication exactly in-sample (one fix, zero regressions)", 1),
 ("a one-rule guard reproduces the 120-row adjudication exactly (one fix, zero regressions)",
  "a one-rule guard reproduces the 120-row adjudication exactly in-sample (one fix, zero regressions)", 1),
 ("a blinded 25-item gold set is graded 25 of 25 in agreement (Wilson 95\\% CI 0.867 to 1.0) across five flip-carrying strata",
  "a blinded 25-item gold set grades 24 of 25 against guarded outcomes (Wilson 95\\% CI 0.805 to 0.993) across five flip-carrying strata, the single divergence being the documented false-positive case", 1),
 ("Blinded gold grading (GOLD-25): independent item-by-item grading agrees 25 of 25 (agreement 1.0, Wilson 95\\% CI 0.867 to 1.0; 14 of 14 with stems, 11 of 11 stemless), covering flips from five flip-carrying strata known at grading time (the cross-domain layers came later).",
  "Blinded gold grading (GOLD-25): independent item-by-item grading agrees 24 of 25 with guarded outcomes (agreement 0.96, Wilson 95\\% CI 0.805 to 0.993; 13 of 14 with stems, 11 of 11 stemless; results/gold\\_guarded\\_agreement.json). The pre-registered decode assumed all 25 guarded-correct; that assumption fails on exactly one item, G06 (trace cloud-new-42, ``O'' vs ``O2''), which the pack builder drew from the raw flip file while the guarded verdict rejects it: the blinded grader accepted the response while guarded says incorrect. The remaining 24 cover flips from five flip-carrying strata known at grading time (the cross-domain layers came later).", 1),
 ("was graded independently item by item (gold\\_grading\\_pack.csv, grades\\_gold25\\_user.csv): 25 of 25 agreement (agreement 1.0, Wilson 95\\% CI 0.867 to 1.0; 14 of 14 with stems, 11 of 11 stemless; scripts/analyze\\_gold.py, results/gold\\_agreement.json)",
  "was graded independently item by item (gold\\_grading\\_pack.csv, grades\\_gold25\\_user.csv): the pre-registered decode reports 25 of 25 under its all-guarded-correct assumption (scripts/analyze\\_gold.py, results/gold\\_agreement.json), but that assumption fails on G06 (trace cloud-new-42, guarded-incorrect), so agreement against guarded outcomes is 24 of 25 (agreement 0.96, Wilson 95\\% CI 0.805 to 0.993; 13 of 14 with stems, 11 of 11 stemless; scripts/recompute\\_gold\\_guarded.py, results/gold\\_guarded\\_agreement.json)", 1),
 ("so the 25 of 25 bounds overturn quality on flip strata only",
  "so the 24 of 25 bounds overturn quality on flip strata only, with the single divergence disclosed above", 2),
 # --- E7: Related Work (R4-01/02/03) ---
 ("Standard background on deep learning follows \\citet{goodfellow2016deep}.",
  "Standard background on deep learning follows \\citet{goodfellow2016deep}. A contemporaneous reproducibility audit of knowledge-graph extraction from threat reports independently supports the matcher-as-instrument view: re-scoring fixed system outputs under eight matching protocols reverses 11 of 45 pairwise orderings (F1 spanning 0.16--0.70), no mechanical matcher (lexical, embedding, or entailment) agrees with multi-reviewer adjudication above 71\\%, while an LLM judge reaches 86\\% \\citep{hakim2026ranked}. Its domain is security extraction rather than QA calibration, so it is cited as independent motivation, not as a comparable effect size.", 1),
 ("This novelty sentence stays hedged (``we are not aware of'') as required.",
  "This novelty sentence stays hedged (``we are not aware of'') as required. The screen protocol is scripts/incr\\_scout\\_0907.py with the adjudicated hit table in LITERATURE\\_REVIEW.md (30-day window, three queries).", 1),
 ("First, same-batch three-matcher comparisons (exact, tolerant v3, adjudicated) can swing from 63.3\\% accuracy and 0.363 ECE under exact matching toward 100\\% accuracy and near-zero ECE after adjudicated relabeling; those magnitudes are cited as positioning context, not as this paper's experiment.",
  "First, the pilot magnitudes themselves motivate the design: exact matching gives 63.3\\% accuracy and 0.363 ECE, rising toward 100\\% accuracy and near-zero ECE after adjudicated relabeling (previously recorded as internal card L01 on the same 30 rows). This paper's delta over L01 is the thirteen-stratum replication, the second judge family, the guard fix, and the power-replication arms.", 1),
 # --- E4: power post-hoc disclosure (R1-07) ---
 ("With observed discordant rates, the required totals are:",
  "With observed discordant rates (post-hoc: each ceiling is computed from the same stratum's observed rate, so these are sensitivity checks rather than pre-data power justifications; analysis\\_plan\\_power\\_rep.md), the required totals are:", 1),
 ("meets its n\\_ceil=217 and is the only pre-registered powered inference in this paper.",
  "meets its post-hoc n\\_ceil=217; only the pool composition was pre-specified, and the reading does not survive Holm (threshold 0.00333), so under joint error control it is stratum-local observed significance (see Multiplicity accounting).", 1),
 ("This is the only pre-registered powered inference in the paper; the four other significant readings carry observed-significance status.",
  "Only the pool composition was pre-specified; under joint error control this reading is stratum-local observed significance like the other four (see Multiplicity accounting).", 1),
 ("extended local-new: one pre-specified plus four observed-significance readings;",
  "extended local-new (pool composition pre-specified; all five observed-significance under joint error control);", 1),
 # --- E5/E9b: pilot50 + rollup language (R1-08/R2-02/R2-03) ---
 ("pilot 11 of 50 flips (b=11, c=0, p=0.0010; cross-model pool of pilot 30 plus PowPilot 20, so this p is descriptive only and the pilot inference rests on the 30-row stratum)",
  "pilot 11 of 50 flips (b=11, c=0; cross-model pool of pilot 30 plus PowPilot 20, descriptive only with no p-value claimed; the pilot inference rests on the 30-row stratum, p=0.0010)", 1),
 ("holdout 7 of 108 (b=7, c=0, p=0.0156, newly significant at alpha=0.05, observed status)",
  "holdout 7 of 108 (b=7, c=0, p=0.0156, significant at alpha=0.05 as a single-arm observation with observed status and no power conclusion)", 1),
 ("These are the third and fourth significant paired inferences in the paper; all carry observed-significance (pilot-class) status because the extension rows are post-registration.",
  "These are the third and fourth significant paired inferences in the paper; all carry observed-significance (pilot-class) status because the extension rows are post-registration, and the rollup rows overlap strata already tested, so rollups are descriptive re-views rather than new tests (cf. Multiplicity accounting).", 1),
 ("(7 flips, 0.0446, b=7, c=0, nominally p=0.0156 but one of four observed arms with few discordant pairs, so no power conclusion is drawn)",
  "(7 flips, 0.0446, b=7, c=0, p=0.0156, significant at alpha=0.05 as a single-arm observation with observed status; one of four observed arms with few discordant pairs, so no power conclusion is drawn)", 1),
 # --- E6: ECE caliber (R1-05/R3-01: disclosure + coincidence note) ---
 ("local-big 156 of 160)}",
  "local-big 156 of 160; prior strata equal-frequency bins, live strata equal-width bins, each exact-vs-guarded comparison within one convention)}", 1),
 ("not from the fit itself; no synthetic targeting test was run, so guard specificity below the observed formula-confusable class is unmeasured.",
  "not from the fit itself; no synthetic targeting test was run, so guard specificity below the observed formula-confusable class is unmeasured.", 0),  # placeholder, replaced below
]

# E9 guard-targeting clause appended to the circularity sentence:
EDITS.append(
 ("not from the fit itself.",
  "not from the fit itself; no synthetic targeting test was run, so guard specificity below the observed formula-confusable class is unmeasured.", 1))
EDITS.append(
 ("The NLL-optimal temperature is not ECE-optimal on these rows; this negative result is reported without a fix claim.",
  "The NLL-optimal temperature is not ECE-optimal on these rows; this negative result is reported without a fix claim. Convention note: the tempscale ECE uses equal-frequency bins throughout while the table uses equal-width bins on live strata; on cloud-new both conventions give 0.1692 at T=1, a numerical coincidence rather than a shared computation.", 1))
# E9 prompt-knob downgrade (R3-03):
EDITS.append(
 ("with instruction format tested (and bounded) as a control knob.",
  "with instruction format varied as a regime contrast (effect present on cross-domain paraphrase styles, absent on replication questions).", 1))
EDITS.append(
 ("and identifies instruction format as an experimental control knob for the paraphrase surface.",
  "and identifies instruction format as a regime contrast for the paraphrase surface rather than a universal knob.", 1))
# E10 misc:
EDITS.append(
 ("matcher choice alone moves the calibration conclusion on adjudicated rows",
  "matcher choice moves the calibration conclusion on adjudicated rows", 1))
# E8 provenance (R5-02/05):
EDITS.append(
 ("Future work: adequately powered replication",
  "Collection provenance: model digests and sampling seeds were not pinned at collection time (live ollama models); the same-question retest bounds single-sample jitter but not cross-version drift. Pilot and holdout-main collection scripts predate the sealed script set (per-row provenance retained in evidence/d2\\_60.jsonl); retained collection scripts start at cloud-new. Future work: adequately powered replication", 1))

fails = []
for old, new, cnt in EDITS:
    c = t.count(old)
    if c != cnt:
        fails.append((cnt, c, old[:90]))
    else:
        t = t.replace(old, new)

if fails:
    print("ASSERT FAILURES:")
    for want, got, s in fails:
        print(f"  want={want} got={got} :: {s}")
    sys.exit(1)

io.open(P, "w", encoding="utf-8", newline="").write(t)
print(f"OK: {len(EDITS)} replacements applied.")
