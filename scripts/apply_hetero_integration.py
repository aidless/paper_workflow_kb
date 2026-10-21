"""R18 P1-2b manuscript integration edits (15th stratum). Idempotent asserts."""
import sys

P = "paper_workflow_kb/paper/main.tex"
s = open(P, encoding="utf-8").read()

EDITS = [
# L138 sources sentence
("results/powrep\\_rollups.json (extended strata), and results/combined\\_qwen2.json (pre-specified pool).",
 "results/powrep\\_rollups.json (extended strata), results/combined\\_qwen2.json (pre-specified pool), "
 "results/r18\\_heteromodel.json (hetero-family raw), results/r18\\_heteromodel\\_adjudication.json "
 "(hetero-family adjudicated), and results/merged\\_1062.json (descriptive merged sums)."),
# L138 fourteen files + later-strata list
("The fourteen result files present at that check were re-executed",
 "The fourteen result files present at that check were re-executed"),
("strata added later (cross-domain, power-replication, Holm, gold-guarded) are verified",
 "strata added later (cross-domain, power-replication, Holm, gold-guarded, R18, hetero-family, unified-binning) are verified"),
# hetero results paragraph after R18 paragraph
("guard specificity below the formula-confusable class remains unmeasured and no silent patch is applied.",
 "guard specificity below the formula-confusable class remains unmeasured and no silent patch is applied. "
 "Hetero-family replication (local gemma3:4b, same xdomain 60 questions, verbatim loose prompt, mini-pre-registered): "
 "21 of 60 exact-correct versus 32 of 60 guarded-correct (raw); 11 flips, flip rate 0.1833, b=11, c=0 "
 "(descriptive, no test run). The directional expectation (flips above zero on paraphrase-surface questions "
 "in a different model family) is confirmed descriptively. Adjudication by the heterogeneous judge "
 "(local qwen2.5:7b, temperature 0; evidence/r18\\_heteromodel\\_judge.json; rollup "
 "results/r18\\_heteromodel\\_adjudication.json): 8 of 11 confirmed on content; excluded are gr18-41, gr18-42, "
 "and gr18-45 (single-character fragments accepted against longer golds, the third and fourth guard-missed "
 "exemplars alongside lr18-42; no patch applied). Adjudicated guarded accuracy is 29 of 60 (0.4833), "
 "adjudicated flips 8 of 60 (0.1333), adjudicated ECE 0.381 equal-width. "
 "This stratum is descriptive-only and excluded from the Holm family (no new comparison is added)."),
# asymmetry paragraph: hetero b/c
("R18-loose-rep adjudicated 24/0; pre-specified pool 9/0)",
 "R18-loose-rep adjudicated 24/0; hetero-family adjudicated 8/0; pre-specified pool 9/0)"),
("keep c at zero across 1002 pairs plus 412 regime-contrast rows;",
 "keep c at zero across 1062 pairs plus 412 regime-contrast rows;"),
# contributions (ii): adjudication counts
("21 of 21 cross-domain on content by a second heterogeneous judge family with both passes on record, "
 "10 of 10 power-replication plus 7 of 7 loose-regime by the same second family);",
 "21 of 21 cross-domain on content by a second heterogeneous judge family with both passes on record, "
 "10 of 10 power-replication plus 7 of 7 loose-regime by the same second family, "
 "8 of 11 hetero-family gemma replication by local qwen2.5:7b with three single-character-fragment exclusions);"),
# contributions (vi): cross-model wording
("cross-model, cross-type, second-family, cross-domain, and power-replication extensions",
 "cross-model, cross-type, second-family, cross-domain, cross-family hetero-model, and power-replication extensions"),
# license paragraph: hetero + exemplars
("and a pre-registered loose replication on 60 fresh questions confirms the regime direction descriptively "
 "(raw 27 of 60, adjudicated 24 of 60; 24 of 27 confirmed on content), so the false-positive documentation "
 "now has two exemplars (G06 formula, caught by the guard; lr18-42 CJK fragment, missed by the guard), "
 "the phenomenon is not single-model (within the tested families)",
 "and a pre-registered loose replication on 60 fresh questions confirms the regime direction descriptively "
 "(raw 27 of 60, adjudicated 24 of 60; 24 of 27 confirmed on content), and a hetero-family replication "
 "(gemma3:4b, same 60 questions) contributes 8 adjudicated flips of 60 (raw 11; 8 of 11 confirmed on content), "
 "so the false-positive documentation now has four exemplars (G06 formula, caught by the guard; lr18-42 CJK "
 "fragment plus three hetero-family single-character fragments, missed by the guard), "
 "the phenomenon is not single-model (across qwen, deepseek-judge, and gemma families)"),
# limitations: hetero disclosures
("the R18 judge leaves one row author-ruled (lr18-46, judge-ERROR across three attempts including a bilingual-parser retry, echo format accepted at lr18-47/51) and two echo-containment rows judge-rejected against the author's correct ruling (lr18-54/55 vs accepted lr18-47/51: instrument inconsistency, both excluded from the adjudicated set);",
 "the R18 judge leaves one row author-ruled (lr18-46, judge-ERROR across three attempts including a bilingual-parser retry, echo format accepted at lr18-47/51) and two echo-containment rows judge-rejected against the author's correct ruling (lr18-54/55 vs accepted lr18-47/51: instrument inconsistency, both excluded from the adjudicated set); "
 "the hetero-family stratum is single-rater judged (local qwen2.5:7b) with a documented failed first attempt "
 "(deepseek-r1:7b ignored think:false; 54 thinking-mode rows discarded, never analyzed);"),
]

for old, new in EDITS:
    assert s.count(old) == 1, ("ANCHOR", old[:70], s.count(old))
    s = s.replace(old, new)

open(P, "w", encoding="utf-8").write(s)
print(len(EDITS), "edits ok")
