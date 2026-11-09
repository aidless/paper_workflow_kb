# FAILURE_MODES

STATUS: WORK-IN-PROGRESS — not A yet

LEDGER_CENSUS: n=84 verified=81 inconclusive=1 superseded=2 draft=0 blocked=0 other=0

These are ways this workbench fails or is easy to misread. None of them is a new experimental result.

## Adjudication over-fire

A flip is a row the exact matcher rejects and the guard accepts. Over-fire is a flip whose content the adjudication marks incorrect: the guard accepted a wrong answer. A zero on one arm is a count for that arm, not a property of the matcher.

Recorded zeros, read from the sealed JSON:

- `results/r30_boolq_seal.json`: `over_fire` 0 on 55 flips (BoolQ main arm, qwen2:7b, Chinese gold mapping).
- `results/r30_boolq_gemma_seal.json`: `over_fire` 0 on 45 flips (gemma3:4b). One collection timeout, `boolq-1159`, is stored in `error_ids` and is outside every denominator.
- `results/r32_enyesno_seal.json`: `over_fire` 0 on 35 flips (native Yes/No mapping). `n_miss` is 0 on that arm; the seal records that as mapping dependence, not as the same discrimination result as the Chinese mapping.

Recorded non-zeros, same definition, kept as negative or boundary results:

- `results/r26_seal.json`: TriviaQA `splits.trivia.over_fire` 3 of 28 flips; EntityQuestions `splits.entity.over_fire` 2 of 32 flips; `combined.total_over_fire` 5; `combined.adopt_v34` false because the miss drop is 2, under the frozen bar of 5. v3.3 stays the baseline.
- Claim C16: the cloud-new substring rule accepted `O` for gold `O2`. That row is an incorrect adjudication, not a hidden success.

Adjudication can also miss an over-fire. Several arms are a single rater (C23 discloses a failed independent judge). C61 records every listed judge configuration as HOLD, including an adversarial false-positive rate of 0.9 for gemma3:4b. Those HOLDs are why a guard is not "enabled" by the calibration file.

## Fresh collection is ollama-only

`scripts/r30_collect_boolq.py`, `scripts/r30_collect_boolq_gemma.py`, and `scripts/r32_collect_enyesno.py` POST to `http://localhost:11434`. A clone without that local ollama cannot regenerate answers. The offline path does not call those scripts. It rescores the frozen jsonl already in `results/` and `evidence/`.

Failures during collection stay in the jsonl as `error` rows. They are not dropped and not imputed. The gemma arm's one timeout is the example above.

## The canonical ledger check is outside this clone

`scripts/verify_claim_ledger.py` is a shell. It walks parent directories for a different copy of itself and, if it finds none, exits 3 with `CANONICAL_NOT_FOUND`. That exit is not a pass. CI asserts the exit is 3 so a future edit cannot turn the shell into a silent success.

`scripts/check_ledger_census.py` only counts table rows and checks that cited paths exist. The current census is the `LEDGER_CENSUS` line above: 84 rows, 81 verified, 1 inconclusive (C08), 2 superseded (C33, C45), no draft and no blocked. It is not "84 PASS".

`reports/ledger.md` is a stored report from a run that had the canonical verifier. It is not re-executed here. Older notes that say 77 active verified, or 82 entries, describe earlier snapshots of the table.

## Manifest and the author-worktree gates

`evidence_manifest.json` (created 2026-10-10) lists 614 paths. On this tree, 54 of those paths are absent: backup copies, raw rater logs, `data_r26` corpora and their download logs, `data_boolq/BoolQ.zip`, and `submission/*.zip`. Present files also already disagreed with the manifest before this change, including `CLAIM_LEDGER.md` and `paper/main.pdf`. The manifest was not rebuilt. Rebuilding it would either drop the missing paths or pretend the author-tree bytes were still here.

`gates_config.json` still runs that manifest check and the ledger shell. It is the author-worktree list. It is not the clone-green list. `python3 scripts/run_acceptance_gates.py gates_config.json` is expected to fail on a fresh clone. CI runs `gates_offline.json` instead. Failing the author-worktree list is not reported as acceptance.

## Historical absolute paths

Frozen snapshots still contain authoring-machine paths. They were not rewritten: editing those bytes would split the files from the claim trail.

- `evidence/kb/` indexes and `LITERATURE_REVIEW.md` cite `/data3/Research/...`. The same `/data3/` strings are in the `anc/` copies. Counts for the anc copies are in `anc/README.md`.
- Claim C05 names the source card under `/data3/Research/01_论文区/`. That cell is a pointer to a file that is not in the clone.
- `scripts/label_match_v3.py` records the path it was vendored from. The running code is the in-tree file.
- `scripts/seal_R25_numbers.py` and `scripts/r3_stats_recompute.py` used to set their root to `~/F:\deepseek/paper_workflow_kb`, which does not resolve on a clone. Both now use the repository root. Their numeric assertions were not edited.
- `anc/README.md` used to list one `/home/` hit in `LITERATURE_REVIEW.md`. That string is not in the current `anc/` tree, so the row was removed.

## What a green offline run is not

A green `gates_offline.json` means the census matches, the headline JSON matches the ledger and the README block, and the listed seal scripts exit 0. It does not mean the paper was accepted, that a package was published, or that every claim row was field-checked. There is no PyPI release and no acceptance status in this repository.
