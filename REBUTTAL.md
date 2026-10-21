# Response to reviewers (round 2) — FINAL (user-confirmed 2026-09-08, ready to paste into OpenReview)

Manuscript: label-matcher flip study on small open-source QA pipelines (revision R25).
No new experiments were run for this revision except sealed recomputation;
no reported number moves. All counts below are recomputed by a single script
per claim and sealed in `results/`.

## N1 (count unification) — FIXED

- Reviewer concern: the manuscript reports 106 judged / 99 confirmed, but the
  flip-row census sums to 102; an older "67 of 68" figure looks stale.
- Our response: Both numbers are correct under different, now explicitly defined
  counting conventions. 106 = every row ever submitted to any judge pass,
  including 4 non-flip probe rows carried as controls (R18 lr18-42 plus
  hetero-family gr18-41/42/45, all judge- and guard-rejected); 102 = flip rows.
  Confirmed = rows accepted correct on content in the final ruling (99).
  The "67 of 68" figure was frozen before the R18/hetero extensions and has been
  replaced everywhere.
- Evidence: `results/adjudication_recount_R25.json` — total_judged 106,
  total_flip_rows 102, total_confirmed 99, nonflip_probe_rows 4
  (scripts/seal_R25_numbers.py, the sole recomputation).
- Manuscript change: Methods now carries a canonical adjudication-accounting
  paragraph (judged vs confirmed conventions + the 106/102/99/4 rollup);
  Abstract, Contributions (ii), the R18 27-row and hetero 11-row passages use
  the same convention in all four places.

## N2 (accuracy-regime distinction) — FIXED

- Reviewer concern: high flip counts on the R18 loose-replication and
  hetero-family strata partly reflect model output failure, not pure matcher
  strictness; the pooled flip rate must not be presented as a pure matcher effect.
- Our response: Agreed, and the manuscript now says so explicitly. On the
  high-accuracy strata (exact accuracy 0.6333–0.925) at most 8 rows per stratum
  remain wrong after adjudicated tolerant matching (0/6/8/7/8), so flips there
  are matcher strictness on otherwise-correct output. On the R18
  loose-replication (exact 0.25, 21 of 60 still wrong) and hetero-family
  (exact 0.35, 31 of 60 still wrong) strata, the flip counts partly reflect
  model failure; the cross-domain loose layer sits between (exact 0.4167,
  15 of 60 still wrong). Guarded-accuracy claims are reported per stratum and
  no pooled flip rate is interpreted as a pure matcher effect.
- Evidence: `results/regime_R25.json` — per-stratum wrong-after-guarded values
  (pilot 0, holdout-main 6, cloud-new 8, local-new 7, local-big 8, xloose 15,
  r18 21, hetero-gemma 31).
- Manuscript change: new "Accuracy-regime distinction" paragraph in Discussion.

## N3 (guard false negatives) — FIXED

- Reviewer concern: the guard's false-negative rate outside the flip set is
  unquantified and its bias direction undisclosed.
- Our response: Quantified in both directions. The guard rejects 140 of 1062
  rows on the adjudicated basis (all exact-reject by nesting). On the 38
  GOLD-100 non-flip rows, 9 are guard false negatives (conditional rate 9/38 =
  0.2368; the GOLD-100 set is stratified, so no population rate is claimed).
  The misses make reported guarded accuracy conservative — a lower bound on
  semantic accuracy. No new guard version is cut in this revision; the 9 rows
  stay on record as regression targets.
- Evidence: `results/guard_fn_R25.json` — guard_reject_pool 140,
  gold100_guard_false_negatives 9, conditional_fn_rate_nonflip 0.2368,
  direction "conservative (lower bound)".
- Manuscript change: Limitations now quantifies both figures and the direction;
  no guard code changed.

## N4 (contributions framing) — FIXED

- Reviewer concern: Contributions read as overstated; power/Holm items do not
  belong there and the full adjudication decomposition is missing.
- Our response: Contributions rewritten in descriptive framing. Item (ii) is now
  the full 99/106 decomposition; power and Holm are removed as contribution
  items (Holm is audit-only, see N5).
- Evidence: claim ledger C65–C68 (68/68 PASS, verify_claim_ledger.py).
- Manuscript change: Contributions section rewritten; no contribution item lacks
  a ledger entry.

## N5 (Holm accounting) — FIXED

- Reviewer concern: the main-text Multiplicity paragraph implies inferential
  license the nested design does not support.
- Our response: The main text is compressed to a single audit-only sentence
  (Holm-Bonferroni ordering retained as a sealed audit artifact with no
  inferential license; the guarded matcher nests the exact matcher so c = 0 by
  construction). The full sealed ordering and sensitivity checks stay in the
  appendix Holm-accounting section. A stale "seventeen" count is corrected to
  "eighteen".
- Evidence: appendix Holm-accounting section (sealed ordering, untouched).
- Manuscript change: Multiplicity paragraph compressed; appendix section kept.

## C3 follow-up (cross-scale scope) — SCOPE RESTATED BY DESIGN

- Reviewer concern: no 70B-plus or closed model tested; do conclusions
  generalize to frontier models?
- Our response: They are not claimed to. Small open-source models (4B–7B) are
  the study population by design: they are the deployable class where
  exact-match scoring is still the default pipeline and where full local
  reproducibility is attainable. Cross-scale generalization to frontier models
  is out of scope, not a pending experiment. This is a scope statement, not a
  capability apology.
- Evidence: design record (local-only collection; model digests in evidence).
- Manuscript change: Limitations/Future-work paragraph restated accordingly
  (4B–7B target population; frontier explicitly out of scope).

## C4 follow-up (grading provenance) — DISCLOSED

- Reviewer concern: the only human grading is by the author; second-rater
  identity, overlap, and the reliability-vs-validity status need disclosure.
- Our response: Disclosed in four places. The second rater is an external human
  volunteer, not an author (30-item overlap; agreement 29/30 = 0.9667, Wilson
  95% CI 0.8333–0.9941, Cohen kappa = 0.91; sole divergence H64 adjudicated
  against the author as a grading slip). Kappa is framed as reliability, not
  validity. Independent external-human grading beyond the 30-item overlap is
  listed as future work, and the pre-existing sentence implying the author is
  the only human grader has been corrected.
- Evidence: `grades_rater2_user2.csv` + `results/rater2_kappa.json`
  (n_graded 30, agree 29, cohens_kappa 0.9112).
- Manuscript change: four disclosure sites (Abstract grading sentence, Methods
  kappa sentence, GOLD-100 paragraph, Limitations validity clause).

## P2 (length and density) — FIXED

- Reviewer concern: abstract over the venue word limit; Methods snapshot is one
  dense block.
- Our response: The abstract is now 254 words, within the limit (down from 519).
  The Methods snapshot block is split into four paragraphs, with the N = 1002 /
  N = 1062 readings on separate lines.
- Evidence: abstract word count recomputed from `paper/main.tex` (254);
  number-consistency scan reports/numbers.md.
- Manuscript change: abstract compressed; Methods reformatted. No numbers changed.

## Global notes

- Every number in this letter traces to a sealed recomputation listed above;
  the claim ledger stands at 68/68 PASS and acceptance gates at 10/10 PASS.
- Machine verification (number/stats/style/TMLR/ledger/taint/hallucination scans
  + compile gate) is green on the submitted PDF (16 pages, compiled locally).
- Known residual risks we disclose rather than hide: (i) independent
  external-human grading beyond the 30-item overlap is future work (C4);
  (ii) pilot 30/50 and local-big 160/720 remain under the placeholder OR = 4
  ceilings; (iii) the 9 guard false-negative rows are documented regression
  targets, not fixed rows.
