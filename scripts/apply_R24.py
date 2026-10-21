"""R24-P2: paper text updates for rater2 kappa + H64 adjudication.

Each replacement asserts exactly-one match. Numbers: kappa 0.9112 (29/30,
Wilson 0.8333-0.9941) from results/rater2_kappa.json; 10->9 FN recharacterization
(H64 author slip, decode/P2 numbers unchanged).
"""
import sys

P = "paper/main.tex"
t = open(P, encoding="utf-8").read()

EDITS = [
 # 1. abstract: 10 -> 9 + slip; author-graded -> + second rater kappa
 ("all 62 flip rows agree, the 7 further agreements being excluded rows decided on the exact basis; 10 guard false negatives on non-flip rows disclosed as a limitation)",
  "all 62 flip rows agree, the 7 further agreements being excluded rows decided on the exact basis; 9 guard false negatives on non-flip rows disclosed as a limitation plus one author grading slip (H64) adjudicated against the author)"),
 ("A 100-item stratified extension (graded blindly by the author) grades 90 of 100",
  "A 100-item stratified extension (graded blindly by the author, with a blinded second rater agreeing 29 of 30, Cohen $\\kappa=0.91$) grades 90 of 100"),
 # 2. L119 judge-calib clause: single-rater retained -> measured reliability
 ("no judge enabled, single-rater limitation retained)",
  "no judge enabled; author grades carry measured reliability (Cohen $\\kappa=0.91$ vs a blinded second rater on a 30-item subset, sole divergence H64 adjudicated against the author; results/rater2\\_kappa.json))"),
 # 3. L119 GOLD-100 tail: 10 -> 9
 ("GOLD-100 is stratified by design (not a random sample), contributes 10 guard false negatives outside the flip set plus 1 sampled gold",
  "GOLD-100 is stratified by design (not a random sample), contributes 9 guard false negatives outside the flip set (plus one author slip H64 adjudicated against the author) plus 1 sampled gold"),
 # 4. L119 stale: awaiting grading -> graded pointer (grades landed R20, decoded R22)
 ("is built and awaiting human grading (gold100_grading_pack.csv, GOLD100_README.md, evidence/gold100_key.json, decode scripts/decode_gold100.py); no GOLD-100 number is reported until the grades land.",
  "was graded blindly by the author (gold100_grading_pack.csv, grades_gold100_user.csv, GOLD100_README.md, evidence/gold100_key.json, decode scripts/decode_gold100.py; results/gold100_agreement.json); see the GOLD-100 paragraph below for the decoded numbers."),
 # 5. L240: remaining 10 -> 9 + H64 slip paragraph; drop 支持/是 from FN list
 ("The remaining 10 divergences are guard false negatives on non-flip rows the grader accepts (unit and 朝-suffix variants, Jakarta/雅加达 transliteration, 支持/是 synonymy, echo-plus-confidence-leak rows): a new limitation, since the flip-centric design does not surface matcher misses outside the flip set.",
  "The remaining 9 divergences are guard false negatives on non-flip rows the grader accepts (unit and 朝-suffix variants, Jakarta/雅加达 transliteration, echo-plus-confidence-leak rows): a new limitation, since the flip-centric design does not surface matcher misses outside the flip set. A tenth apparent divergence (H64, ``支持'' vs ``是'') is an author grading slip, not a matcher miss: the blinded second rater rejects it with the guard (S09 grades 错), so the human gold is adjudicated 错 (2:1 with guard consistency); decode and P2-calibration numbers are unchanged (the decode keys off the recorded author grade vs guarded outcomes, and P2 covers flip rows only, H64 being a nonflip)."),
 # 6. L240 H34: both-wrong -> both-raters triple agreement
 ("(H34, agreed as both-wrong;",
  "(H34, agreed as both-wrong by both blinded raters, triple-consistent with the guard's formula rejection;"),
 # 7. L240 H09: second rater independently flagged
 ("(H09 reference 是; ginger is a rhizome, not a root) and is corrected post-hoc to 否 in R20",
  "(H09 reference 是; ginger is a rhizome, not a root --- a blinded second rater independently flagged the same botanical dispute while still grading the response-vs-gold cell 错 under the stated gold) and is corrected post-hoc to 否 in R20"),
 # 8. L253 limitations: 10 -> 9 + reliability clause
 ("extension strata single-rater with the failed qwen3:4b attempt disclosed)",
  "extension strata single-rater with the failed qwen3:4b attempt disclosed, but author grades carry measured reliability (second-rater $\\kappa=0.91$ on 30 items))"),
 ("GOLD-100 is stratified by design (not a random sample), contributes 10 guard false negatives outside the flip set plus 1 sampled gold",
  "GOLD-100 is stratified by design (not a random sample), contributes 9 guard false negatives outside the flip set (plus the H64 author slip) plus 1 sampled gold"),
 # 9. L261 residual risk: ten -> nine + slip
 ("ten guard false negatives outside the flip set, the lr18-54/55 echo-instrument divergence",
  "nine guard false negatives outside the flip set plus one author slip (H64), the lr18-54/55 echo-instrument divergence"),
 # 10. L270 appendix: 10 -> 9 + slip
 ("7 excluded agree on exact basis, 10 guard false negatives, 1 wrong gold",
  "7 excluded agree on exact basis, 9 guard false negatives plus 1 author slip (H64), 1 wrong gold"),
]

MERGED = ("GOLD-100 is stratified by design (not a random sample), contributes 10 guard false negatives outside the flip set plus 1 sampled gold",
    "GOLD-100 is stratified by design (not a random sample), contributes 9 guard false negatives outside the flip set (plus the H64 author slip) plus 1 sampled gold", 2)
JOBS = [(e[0], e[1], 1) for e in EDITS if not e[0].startswith("GOLD-100 is stratified")] + [MERGED]
for old, new, cnt in JOBS:
    n = t.count(old)
    assert n == cnt, f"match count {n} (want {cnt}): {old[:70]!r}"
    t = t.replace(old, new)

# final sentinels
assert t.count("10 guard false negatives") == 0
assert t.count("ten guard false negatives") == 0
assert t.count("The remaining 10 divergences") == 0
assert t.count("awaiting human grading") == 0
assert "kappa=0.91" in t
open(P, "w", encoding="utf-8").write(t)
print(f"R24-P2 paper edits applied: {len(EDITS)} (all single-match asserted)")
