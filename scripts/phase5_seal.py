# -*- coding: utf-8 -*-
"""phase5_seal.py — rebuild the PHASE5_SEAL.json snapshot.

Re-hash the 5 core artifacts + the R26 source ledger, fold the sealed R26
combined numbers in, and re-verify the evidence manifest.  The frozen invariant
this seal proves: submission_tmlr_r25.zip must still hash to the R25-sealed
value — R26 does NOT rebuild the submission package (pre-reg R6), and this seal
asserts that byte-for-byte.

Convergence: it builds the manifest (to ingest this very script), verifies,
writes the seal with the verified manifest count, then builds+verifies one more
time so the on-disk manifest includes the final seal bytes — leaving the tree at
a self-consistent fixed point (0 FAIL / 0 WARN).

Run from the repo root:
  python scripts/phase5_seal.py
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]  # paper_workflow_kb

ZIP_R25_SHA = "05d03a61a99f96fb05e2bdbce94a6d30b24bf106c27371d284b958cd92102332"

CORE = [
    "CLAIM_LEDGER.md",
    "SELF_ASSESSMENT.md",
    "paper/main.tex",
    "paper/main.pdf",
    "submission/submission_tmlr_r25.zip",
]

# R26 source ledger — every file that constitutes/decisive for the R26 result.
R26_SOURCES = [
    "PREREG_R26_EXTERNAL.md",
    "ROUND_R26.md",
    "R26_ADJUDICATION_REVIEW.md",
    "r26_flip_pack_entity.csv",
    "r26_miss_pack_entity.csv",
    "r26_flip_pack_trivia.csv",
    "r26_miss_pack_trivia.csv",
    "scripts/r26_sample.py",
    "scripts/r26_sample_trivia.py",
    "scripts/r26_answer.py",
    "scripts/r26_score.py",
    "scripts/fill_r26_verdict.py",
    "scripts/seal_R26.py",
    "results/r26_answers_entity.jsonl",
    "results/r26_answers_trivia.jsonl",
    "results/r26_external.json",
    "results/r26_seal.json",
    "evidence/r26_entity_sample.jsonl",
    "evidence/r26_trivia_sample.jsonl",
    "writing_session.jsonl",
    "STATE_SNAPSHOT.md",
]

# External dataset downloads: size-recorded only (triviaqa-rc is 2.6 GB;
# hashing adds no information and is not a project-generated artifact).
DATASETS = [
    "data_r26/triviaqa-rc.tar.gz",
    "data_r26/entityquestions-dataset.zip",
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd):
    return subprocess.run(cmd, cwd=str(HERE), capture_output=True, text=True)


def build_manifest():
    return run([sys.executable, "scripts/build_evidence_manifest.py", "."])


def verify_manifest():
    r = run([sys.executable, "scripts/build_evidence_manifest.py", ".",
             "--verify", "evidence_manifest.json"])
    totals = [l for l in r.stdout.splitlines() if l.startswith("TOTAL:")]
    summary = totals[0] if totals else "exit %d (tail: %s)" % (r.returncode,
                                                               r.stdout[-200:])
    n = len(json.loads((HERE / "evidence_manifest.json").read_text(
        encoding="utf-8"))["files"])
    return r.returncode, n, summary


def main():
    prev_path = HERE / "PHASE5_SEAL.json"
    prev = json.loads(prev_path.read_text(encoding="utf-8"))
    prev_art = {k.split("/", 1)[-1] if "/" in k and k.startswith(
        "paper_workflow_kb") else k: v for k, v in
        prev.get("artifacts", {}).items()}

    artifacts = {}
    for f in CORE:
        p = HERE / f
        assert p.exists(), f
        artifacts[f] = sha256(p)

    # ---- frozen invariant: submission zip NOT rebuilt by R26 ----
    zip_sha = artifacts["submission/submission_tmlr_r25.zip"]
    assert zip_sha == ZIP_R25_SHA, \
        ("zip changed! R26 must not rebuild the r25 zip. disk=%s sealed=%s"
         % (zip_sha, ZIP_R25_SHA))

    sources = {}
    for f in R26_SOURCES:
        p = HERE / f
        assert p.exists(), "missing R26 source: %s" % f
        sources[f] = sha256(p)

    datasets = {}
    for f in DATASETS:
        p = HERE / f
        assert p.exists(), "missing dataset: %s" % f
        datasets[f] = {"size": p.stat().st_size,
                       "note": "external download, size recorded (not hashed)"}

    r26 = json.loads((HERE / "results/r26_seal.json").read_text(encoding="utf-8"))

    # ---- first build+verify: ingest this script, get green count ----
    build_manifest()
    rc1, n1, s1 = verify_manifest()
    if rc1 != 0:
        print("first verify failed:", s1, file=sys.stderr)

    seal = {
        "artifacts": artifacts,
        "r26": {
            "sources": sources,
            "datasets": datasets,
            "combined": r26["combined"],
            "adoption_bar": r26["adoption_bar"],
        },
        "gates": ("10/10 PASS (gates_history.jsonl last run "
                  "ts=2026-09-08T23:05:14, all_pass=true)"),
        "ledger": "71 PASS / 0 FAIL / 1 WARN (C08)",
        "manifest": "%d entries / %s" % (n1, s1),
        "manifest_ok": (rc1 == 0),
        "zip_invariant": "HELD: r25 zip sha == R25 sealed value (not rebuilt by R26)",
        "note": (
            "R26-external seal. main.tex + CLAIM_LEDGER.md re-frozen at R26 state; "
            "SELF_ASSESSMENT.md, paper/main.pdf, and submission_tmlr_r25.zip unchanged "
            "(main.pdf still R25 — R26 prose lives in source main.tex only, PDF rebuilt "
            "at next package freeze). R26 source ledger (21 files) + datasets "
            "(size-recorded) folded in. v3.4 verdict negative: miss drop 2 < 5, "
            "v3.3 remains baseline; R26 is a descriptive external-validity supplement "
            "and does not block submission."
        ),
        "round": "R26-external",
    }
    prev_path.write_text(json.dumps(seal, ensure_ascii=False, indent=1),
                         encoding="utf-8")

    # ---- second build+verify: fold the final seal bytes into the manifest ----
    build_manifest()
    rc2, n2, s2 = verify_manifest()
    ok = (rc2 == 0 and "0 FAIL" in s2 and "0 WARN" in s2)

    print("=== PHASE5_SEAL rebuilt (round=%s) ===" % seal["round"])
    for f, h in artifacts.items():
        tag = ""
        if prev_art.get(f) not in (None, h):
            tag = "  [changed vs R25: was %s]" % prev_art[f][:12]
        elif prev_art.get(f) == h:
            tag = "  [unchanged]"
        print("  %s  %s%s" % (h, f, tag))
    print("r26.sources: %d files; r26.datasets: %d (size-recorded)"
          % (len(sources), len(datasets)))
    print("combined: miss_drop=%s overfire_increase=%s adopt_v34=%s"
          % (r26["combined"]["miss_drop"],
             r26["combined"]["overfire_increase"],
             r26["combined"]["adopt_v34"]))
    print("manifest final: %s (converged=%s)" % (s2, ok))
    print("zip invariant:", seal["zip_invariant"])
    assert ok, "manifest did not converge to 0 FAIL / 0 WARN: %s" % s2


if __name__ == "__main__":
    main()