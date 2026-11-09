# paper_workflow_kb

[![CI](https://github.com/aidless/paper_workflow_kb/actions/workflows/static-checks.yml/badge.svg)](https://github.com/aidless/paper_workflow_kb/actions/workflows/static-checks.yml)

STATUS: WORK-IN-PROGRESS — not A yet

**Problem**

Label-matcher choice (exact string vs tolerant/guard) moves measured short-answer QA accuracy, including a public BoolQ yes/no arm.
The study is descriptive: a flip is a frozen row the exact matcher rejects and the guard accepts, not a causal effect and not proof the guard is right.
Public yes/no arms stay outside the Holm family, with no power claim and no paired test, because the guard nests the exact matcher and the reverse cell is zero by construction.

This is an in-progress TMLR workbench (`paper/main.tex`), not an accepted paper and not a package. There is no PyPI release. The claim table is in `CLAIM_LEDGER.md` (Chinese). Live row count:

LEDGER_CENSUS: n=84 verified=81 inconclusive=1 superseded=2 draft=0 blocked=0 other=0

Negative and inconclusive rows stay in that table. C08 is inconclusive. C21 records isotonic regression whose cross-validated ECE did not improve. C71 records the v3.4 candidate as not adopted (`combined.adopt_v34` false). C33 and C45 are superseded history, not current conclusions.

<!-- SEAL_DRIFT
results/r30_boolq_seal.json n=100 n_exact=0 n_guard=55 n_flips=55 flip_rate=0.55 over_fire=0 n_miss=31 n_correct_reject=14 miss_rate=0.6889 miss_wilson95[0]=0.5434 miss_wilson95[1]=0.8047
results/r30_boolq_gemma_seal.json n_scored=99 n_errors=1 n_exact=0 n_guard=45 n_flips=45 over_fire=0 n_miss=39 n_correct_reject=15 flip_rate_scored=0.4545 miss_rate=0.7222
results/r32_enyesno_seal.json n=60 n_exact=15 exact_rate=0.25 n_guard=50 n_flips=35 over_fire=0 n_miss=0 n_correct_reject=10 overlap_with_r30_sample=0
results/merged_1062.json n=1062 n_exact=830 n_guarded_adjudicated=922 n_flips=92
results/r26_seal.json combined.miss_drop=2 combined.overfire_increase=0 combined.adopt_v34=false combined.total_over_fire=5
results/isotonic.json strata.holdout-main.ECE_raw=0.205 strata.holdout-main.ECE_isotonic_cv5=0.2552 strata.cloud-new.ECE_raw=0.1692 strata.cloud-new.ECE_isotonic_cv5=0.1991
-->

## Offline path and live path

Offline seals reread frozen answers. They do not call a model. From a fresh clone, with the system Python and no network install:

```bash
python3 scripts/check_ledger_census.py
python3 scripts/check_seal_drift.py
python3 scripts/r30_score_boolq.py
python3 scripts/r30_seal_boolq.py
python3 scripts/r30_seal_boolq_gemma.py
python3 scripts/r32_seal_enyesno.py
python3 scripts/seal_R25_numbers.py
python3 scripts/seal_R26.py
python3 scripts/seal_merged_hetero.py
python3 scripts/run_acceptance_gates.py gates_offline.json
```

`gates_offline.json` is the clone-green list. CI (`.github/workflows/static-checks.yml`) runs that list, plus Python syntax and JSON parsing. It also runs `scripts/verify_claim_ledger.py` and requires exit 3 (`CANONICAL_NOT_FOUND`). Exit 3 is the honest miss, not a pass.

Live collection is separate and will fail without a local ollama at `http://localhost:11434`:

```bash
python3 scripts/r30_collect_boolq.py          # qwen2:7b, not part of CI
python3 scripts/r30_collect_boolq_gemma.py    # gemma3:4b
python3 scripts/r32_collect_enyesno.py        # native Yes/No mapping
```

`requirements.txt` (numpy, scipy) is only for some numeric scripts. The commands above use the standard library.

## What is not green on a clone

`python3 scripts/run_acceptance_gates.py gates_config.json` is the author-worktree list of 10 checks. On a clone it fails: the ledger shell cannot see its canonical implementation, and `evidence_manifest.json` does not match this tree (54 listed paths are absent, and some present files already differed). Do not read that failure as a scientific result, and do not read a skipped check as a pass.

`reports/ledger.md` is a stored verifier report. It is not re-run here. `STATE_SNAPSHOT.md` and `ROUND_R32_CLOSE.md` still quote the row total from the close of R32, which was before C83 and C84 were added.

`analysis_d2.py` rewrites `results/analysis.json` and sibling files. It is not in the offline gate.

## Layout

```
paper/            TMLR draft (XeLaTeX + Noto Serif CJK SC to compile)
scripts/          sample, collect, score, adjudicate, seal, gates
evidence/         frozen samples, raw answers, adjudications, kb snapshot
results/          seal JSON; headline numbers live here
data_boolq/       SuperGLUE BoolQ unpack + SHASUMS
data_r26/         TriviaQA-RC and EntityQuestions source notes and hashes; the corpora are not in the repo
CLAIM_LEDGER.md   claim table
PREREG_*.md       preregistrations
ROUND_*.md        round notes, including negative rounds
FAILURE_MODES.md  over-fire, ollama-only collection, external ledger check
gates_offline.json
gates_config.json author-worktree gates, not clone-green
```

## Gaps that keep this at WORK-IN-PROGRESS

1. Field-level verification of all 84 rows needs the canonical ledger program, which is not in this clone.
2. `evidence_manifest.json` is a historical snapshot and was not rebuilt. Hash reconciliation is not a clone pass.
3. `gates_config.json` is not the CI gate. CI covers the offline seals and the exit-3 ledger shell only.
4. Frozen kb indexes and `LITERATURE_REVIEW.md` still embed `/data3/...` paths. See `FAILURE_MODES.md`.
5. Manuscript consistency items already on record in `.aris/verdicts/` (stale claim-range wording, judge-count wording, severed limitation sentences) are unchanged. This change does not edit experimental scores.
6. Compiling `paper/main.tex` needs XeLaTeX and a CJK font. That is outside the offline seal path.
7. TriviaQA-RC and EntityQuestions tarballs are not shipped. Resampling those arms needs the official packages named in `data_r26/SOURCE.md`.

## License

MIT (`LICENSE`).
