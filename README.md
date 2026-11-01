# paper_workflow_kb — Label Matcher Choice Moves Measured Accuracy in Short-Answer QA

> A TMLR-grade stratified descriptive study with adjudication and a guard patch.
> The central methodological finding: **the correctness label is part of the
> measurement instrument** — which string matcher you choose moves the measured
> accuracy and the calibration metrics that inherit it.

**Status:** complete, submission-ready (manuscript under anonymous review; not yet
publicly released). **License:** MIT (code) / CC-BY-4.0 (data, docs, pre-registration).

---

## What problem does this solve?

Calibration and accuracy papers routinely report accuracy and expected calibration
error (ECE) *as if the correctness labels were fixed*. In short-answer QA the label
comes from a programmatic **matcher** — and the matcher is part of the measuring
instrument:

- A **brittle exact matcher** marks semantically correct answers wrong
  (`"8848.86米"` vs `"8848"`, `"不会"` vs `"否"`) → depresses accuracy, inflates ECE.
- A **tolerant matcher** reverses those calls → the calibration conclusion **moves
  with the matcher**.

There is no single "true" correctness; the choice of matcher is a measurement
decision with measurable consequences. This study measures those consequences and
shows the matcher choice is not a cosmetic detail.

## Why it matters

- It **quantifies a silent threat** to every calibration / accuracy result that uses
  a programmatic matcher: 92 of 232 (39.7%) rows the exact matcher calls wrong are
  adjudicated-correct answers the guarded matcher recovers — a bounded, known-denominator
  rate that does **not** depend on the nested-construction assumption.
- It **delivers a reproducible method**: a one-rule guard patch that reproduces the
  120-row adjudication exactly in-sample (one fix, zero regressions), with a synthetic
  probe measuring its boundary and a theorem proving its monotonicity.
- Every number is tied to an evidence file + field in `CLAIM_LEDGER.md`; no number is
  written from memory; refutations and negative results are reported, not hidden.

## What this study does (method)

1. **Instrument the matcher** — three graders: exact, semantic-tolerant, and a guarded
   revision (v3.3) that nests the exact one (so reverse flips are zero by construction).
2. **Measure one descriptive estimand** — the flip asymmetry D1 between
   exact-wrong/guarded-right (b) and exact-right/guarded-wrong (c). No significance
   test is run on D1: under nesting c=0 is a definitional tautology, so any McNemar
   p-value would be a tautology too. A procedural adjudication gate requires every
   flip to be judged before any calibration claim.
3. **Adjudicate** — 99 of 106 rows put to judges (102 flips + 4 probes).
4. **Cross-validate** — a blinded 25-item gold set, a 100-item stratified extension
   (90/100, κ=0.91), a retest reproducing the flip set, and a second-model arm.

## Key results (all from `CLAIM_LEDGER.md`, each traceable to an evidence file)

| Result | Value | Evidence |
|---|---|---|
| Paired comparisons, fifteen strata | **1062** (+412 regime-contrast excluded) | `results/merged_1062.json` |
| Adjudicated guarded accuracy | **922 / 1062** | `results/merged_1062.json` |
| Exact-match errors recovered by guard | **92 / 232 = 39.7%** (Wilson 33.6–46.1) | `results/merged_1062.json`, `results/guard_fn_R25.json` |
| Adjudication agreement | **99 / 106** | Methods (claim ledger) |
| Blinded gold set (25 items) | **24 / 25** (divergence G06) | `results/gold_guarded_agreement.json` |
| 100-item extension (author-graded) | **90 / 100** (88/100 adjudicated; all 62 flip rows agree) | `results/gold100_agreement.json` |
| Second rater agreement | **29 / 30, κ = 0.91** | gold100 grading pack |
| Guard false negatives (conservative direction) | **9** (make guarded accuracy a lower bound) | `results/guard_fn_R25.json` |
| Knowledge base (Obsidian) | 75 batch-review + 51 cards + 4 arXiv = **130** notes | `evidence/kb/` |

**Honest negative/refuted results (reported, not hidden):** temperature scaling gives
no consistent ECE repair (NLL down, ECE up); isotonic regression does not improve
held-out ECE (CV worse); a cross-domain loose-prompt layer shows the prompt-regime
contrast is question-type-dependent; BoolQ exact-zero is shown to be a *mapping
artifact* (a native-language mapping arm gives exact 15/60). These are all recorded in
`CLAIM_LEDGER.md` as verified claims, not silently dropped.

## What this study does **not** prove

- **No inferential claim on D1.** The nested construction makes c=0 a tautology; no
  significance is claimed on the flip asymmetry. The study is *descriptive*.
- **No claim of a general matcher.** The exact/guarded asymmetry is measured on
  short-answer QA; the cross-domain and BoolQ layers show it does **not** transfer
  uniformly (question-type-dependent; mapping-artifact-dependent).
- **No claim that the guard is complete.** The 100-item extension found 9 guard false
  negatives (plus one author slip H64); the guarded accuracy is a **lower bound** on
  semantic accuracy, not an estimate.
- **No population rate claim.** The 39.7% is a bounded descriptive rate on fifteen
  strata, not a target-population sample (see `results/guard_fn_R25.json`:
  `no_population_rate_claim: true`).
- **No publication-readiness of the manuscript** — it is under anonymous review;
  venue names are targets, not submissions.

## Repository layout

```
paper_workflow_kb/
├── paper/main.tex                # Manuscript (445 lines, TMLR style)
├── CLAIM_LEDGER.md               # Every claim → evidence file + field + status (85+ entries)
├── evidence_manifest.json        # Hash-locked evidence manifest (590 files PASS)
├── evidence/                     # Raw adjudication, judge, collection records
├── results/                      # Sealed JSON results (the recompute targets)
├── scripts/                      # 183 analysis/collection/seal/audit scripts
├── LITERATURE_REVIEW.md          # KB-grounded literature review (130-note pool)
├── KB_GROUNDING.md               # Obsidian KB snapshot grounding
├── MISSION_R27_29_REQUALIFICATION.md
├── STATE_SNAPSHOT.md             # Research state machine (hypothesis lifecycle)
├── SELF_ASSESSMENT.md            # TMLR four-dimension self-assessment (O2)
└── PREREG_R*.md                  # Pre-registration documents (R18/R26/R28-R32)
```

## Quick start

```bash
pip install -r requirements.txt     # numpy==2.5.2, scipy==1.18.1 (torch NOT required)

# 1. Verify the claim ledger: every claim's number is traceable to an evidence file
python3 scripts/verify_claim_ledger.py .

# 2. Reconcile the evidence manifest (hash-locked provenance)
python3 scripts/build_evidence_manifest.py . --verify evidence_manifest.json

# 3. Full acceptance gate suite (config-driven, 10 gates)
python3 scripts/run_acceptance_gates.py gates_config.json
```

## Reproduce every reported number

Every number in the manuscript and README is registered in `CLAIM_LEDGER.md` with its
evidence file + field and its "how to verify" recipe. The canonical recompute path:

```bash
# The ledger verifier is the single gate — it re-derives each claim's value from the
# evidence file and fails on any mismatch (0 FAIL required):
python3 scripts/verify_claim_ledger.py . --out reports/ledger.md

# A dedicated recompute script reproduces the abstract's headline arithmetic
# byte-for-byte (0.40 = 24/60, 43.3% = flip_rate, 0.25/0.65/0.6425/0.2425):
python3 scripts/recompute_r18_arithmetic_20261013.py
```

Most aggregate results are produced by a named `scripts/*.py` (each `verify_claim_ledger.py`
entry names the single script that recomputes it — e.g. `scripts/analyze_new60.py`,
`scripts/analyze_powrep.py`, `scripts/seal_theorems.py`). The `--seal` flag on these
scripts writes the result JSON; re-running it reproduces the file.

> **Provenance discipline.** No number in the paper is written from memory. Each one
> is either (a) a sealed JSON value in `results/` or `evidence/`, or (b) recomputed by
> a named script. The manuscript build (main.pdf) is not part of the recompute gate —
> the gate verifies the *numbers*, not the typesetting.

## Tests

The repo's "tests" are the acceptance gates and the self-contained audit scripts (there
is no pytest suite — the study's artifacts are sealed JSON + verifier scripts). Run:

```bash
python3 scripts/run_acceptance_gates.py gates_config.json   # 10 gates
python3 scripts/verify_claim_ledger.py .                     # claim-ledger 0 FAIL gate
```

> **Known working-tree state (honest):** the acceptance gates report **7/10 PASS** on
> the current working tree. The 3 FAILs are pre-existing conditions from later
> working-tree edits, not regressions introduced here:
> - **manifest hash reconciliation** — hash mismatches on files edited after the
>   manifest was sealed (CLAIM_LEDGER.md, paper/main.tex, LITERATURE_REVIEW.md, etc.)
>   plus one missing `data_r26/triviaqa-rc.tar.gz`;
> - **taint scan** — claim C85 references `results/merged_1062.json` which is present,
>   but the taint source `evidence/tainted.json` is absent so no taint is detected;
> - **R25 recount seal** — `scripts/seal_R25_numbers.py` asserts against adjudication
>   records whose working-tree state differs from the sealed baseline.
> These are **not** re-sealed or papered over: re-sealing the manifest would alter
> research evidence. They are reported as-is. The claim-ledger gate (`verify_claim_ledger.py`)
> passes (0 FAIL).

## Citation

Not yet publicly released (anonymous review). Cite the manuscript draft:
Liu, Z. (2026). *Label Matcher Choice Moves Measured Accuracy in Short-Answer QA: A
Stratified Descriptive Study with Adjudication and a Guard Patch.* Manuscript draft, TMLR.
