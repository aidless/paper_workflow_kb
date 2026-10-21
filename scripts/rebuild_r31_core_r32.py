# -*- coding: utf-8 -*-
"""Rebuild the R31/R32 CORE upload package with the final compile (R32).

Why: the previous core zip shipped a stale main.pdf (built before the TikZ /
keywords / layout fixes) and predated the R32 Amendment A2 second-model BoolQ
arm. This rebuild:

- replaces the built paper artifacts (main.pdf/tex/bib/bbl) with the current,
  three-pass XeTeX output;
- refreshes CLAIM_LEDGER.md (now carrying C82);
- adds the second-model arm's evidence and scripts so every number cited by
  the new paragraph ships with the package.

Everything else is copied byte-for-byte from the previous core zip, so the
package's file set changes only by the intended additions.

Inputs: submission/submission_tmlr_r31_core.zip (previous core package)
Output: submission/submission_tmlr_r31_core.zip (overwritten; previous kept
  beside it as submission_tmlr_r31_core_pre_r32.zip.bak)
"""
import shutil
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
CORE = HERE / "submission" / "submission_tmlr_r31_core.zip"
BAK = HERE / "submission" / "submission_tmlr_r31_core_pre_r32.zip.bak"
SOURCE_DATE_EPOCH = 1754000000

# refreshed in place from disk
REPLACE = [
    "paper/main.pdf", "paper/main.tex", "paper/main.bib", "paper/main.bbl",
    "CLAIM_LEDGER.md", "scripts/seal_r31_core_package.py",
    "evidence_manifest.json",
]
# added by R32
ADD = [
    "results/r30_boolq_gemma_seal.json",
    "results/r30_score_boolq_gemma.json",
    "results/r30_adjudication_boolq_gemma.json",
    "results/r30_answers_boolq_gemma.jsonl",
    "results/r30_collect_boolq_gemma.log",
    "scripts/r30_collect_boolq_gemma.py",
    "scripts/r30_score_boolq_gemma.py",
    "scripts/r30_adjudicate_boolq_gemma.py",
    "scripts/r30_seal_boolq_gemma.py",
    "scripts/rebuild_r31_core_r32.py",
    "r30_flip_pack_boolq_gemma.csv",
    "r30_miss_pack_boolq_gemma.csv",
    # cited by main.tex line 110 as the provenance for the external comparison
    # numbers but previously missing from the upload package (R32 catch)
    "evidence/hakim_song_2609.01671.pdf",
    # completeness: all 8 pre-registrations ship, this one included
    "PREREG_R32_ENYESNO.md",
    "scripts/reconcile_r31_core_r32.py",
]

# Heavy raw corpora the core package must NOT ship (same rule the seal asserts).
# Discovered on the R32 rebuild: the previous core zip still carried
# data_boolq/BoolQ.zip (4.1MB), contradicting EXCLUDED_HEAVY in
# scripts/seal_r31_core_package.py. Dropped here so rule and artifact agree.
# data_boolq/BoolQ/val.jsonl (the frozen scored sample) stays: it is in MUST.
DROP = [
    "data_r26/triviaqa-rc.tar.gz",
    "data_r26/entityquestions-dataset.zip",
    "data_boolq/BoolQ/train.jsonl",
    "data_boolq/BoolQ/test.jsonl",
    "data_boolq/BoolQ.zip",
    "paper/main_20260907.pdf.bak",
    "paper/main_review_r24.html",
]


def fixed_date_time(epoch):
    import datetime
    d = datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc)
    return (d.year, d.month, d.day, d.hour, d.minute, d.second)


def main():
    assert CORE.exists(), CORE
    if not BAK.exists():
        shutil.copy2(CORE, BAK)
    old = zipfile.ZipFile(CORE)
    old_names = old.namelist()
    written = set()

    tmp = CORE.with_suffix(".zip.tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        # 1) copy everything not being replaced, dropped, or re-added
        for info in old.infolist():
            if info.filename in REPLACE or info.filename in DROP \
                    or info.filename in ADD:
                continue
            data = old.read(info.filename)
            ni = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            ni.compress_type = zipfile.ZIP_DEFLATED
            ni.external_attr = info.external_attr
            out.writestr(ni, data)
            written.add(info.filename)
        # 2) refreshed + added files from disk
        for rel in REPLACE + ADD:
            p = HERE / rel
            assert p.exists(), "missing source: %s" % rel
            ni = zipfile.ZipInfo(rel, date_time=fixed_date_time(SOURCE_DATE_EPOCH))
            ni.compress_type = zipfile.ZIP_DEFLATED
            out.writestr(ni, p.read_bytes())
            written.add(rel)
    old.close()
    tmp.replace(CORE)

    with zipfile.ZipFile(CORE) as z:
        names = z.namelist()
        dupes = len(names) - len(set(names))
        print("files=%d dupes=%d bytes=%d"
              % (len(names), dupes,
                 sum(i.file_size for i in z.infolist())))
        for must in REPLACE + ADD:
            assert must in names, must
        for bad in DROP:
            assert bad not in names, "excluded-heavy present: %s" % bad


if __name__ == "__main__":
    main()
