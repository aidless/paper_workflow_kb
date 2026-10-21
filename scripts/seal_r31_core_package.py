# -*- coding: utf-8 -*-
"""Seal for the R31 CORE resubmission package (M4 review fix).

The full r31 zip (2.68GB, raw corpora) is retained on disk as build record;
the UPLOAD candidate is submission_tmlr_r31_core.zip (<200MB): raw corpora
replaced by SHASUMS + SOURCE.md + frozen samples + sampling scripts.
Asserts core-zip contents, anonymity 0 hits, keywords present in source.
No upload is performed (protected layer).

Output: results/r31_core_package_seal.json
"""
import hashlib
import json
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


EXCLUDED_HEAVY = [
    "data_r26/triviaqa-rc.tar.gz",
    "data_r26/entityquestions-dataset.zip",
    "data_boolq/BoolQ/train.jsonl",
    "data_boolq/BoolQ/test.jsonl",
    "data_boolq/BoolQ.zip",
    "paper/main_20260907.pdf.bak",
    "paper/main_review_r24.html",
]
MUST = [
    "paper/main.pdf", "paper/main.tex", "paper/main.bib",
    "data_boolq/BoolQ/val.jsonl",
    "data_boolq/SHASUMS.txt",
    "data_r26/SOURCE.md", "data_r26/SHASUMS.txt",
    "results/r30_boolq_seal.json", "results/theorems.json",
    "results/r18_heteromodel_judge2_agreement.json",
    "results/r31_package_seal.json",
    # R32 Amendment A2: second-model BoolQ arm (C82) ships with its evidence
    "results/r30_boolq_gemma_seal.json",
    "results/r30_score_boolq_gemma.json",
    "results/r30_adjudication_boolq_gemma.json",
    "results/r30_answers_boolq_gemma.jsonl",
    "scripts/r30_collect_boolq_gemma.py",
    "scripts/r30_score_boolq_gemma.py",
    "scripts/r30_adjudicate_boolq_gemma.py",
    "scripts/r30_seal_boolq_gemma.py",
    "r30_flip_pack_boolq_gemma.csv",
    "r30_miss_pack_boolq_gemma.csv",
    # R32: evidence cited by main.tex (line 110) must ship
    "evidence/hakim_song_2609.01671.pdf",
    "PREREG_R32_ENYESNO.md",
    "PREREG_R30_BOOLQ.md", "PREREG_R31_HETEROJUDGE.md",
    "PREREG_R26_EXTERNAL.md",
]


def main():
    tex = (HERE / "paper" / "main.tex").read_text(encoding="utf-8")
    assert "\\keywords{" in tex
    anon = (HERE / "submission" / "anonym_check.md").read_text(encoding="utf-8")
    assert "Hits: 0" in anon, anon.splitlines()[2]
    zpath = HERE / "submission" / "submission_tmlr_r31_core.zip"
    names = set(zipfile.ZipFile(zpath).namelist())
    for bad in EXCLUDED_HEAVY:
        assert bad not in names, bad
    for must in MUST:
        assert must in names, must
    total = sum(i.file_size for i in zipfile.ZipFile(zpath).infolist())
    assert total < 200 * 1000 * 1000, total
    manifest = json.loads((HERE / "evidence_manifest.json").read_text(
        encoding="utf-8"))["files"]

    def in_zip(entry_path):
        # the manifest is repo-root relative ("paper_workflow_kb/..."); the zip
        # stores kb-relative names. Strip the prefix before comparing, otherwise
        # every entry counts as missing.
        kb = "paper_workflow_kb/"
        rel = entry_path[len(kb):] if entry_path.startswith(kb) else entry_path
        return rel in names

    payload = {
        "zip_sha256": sha(zpath),
        "zip_n_files": len(names),
        "zip_bytes": total,
        "manifest_total": len(manifest),
        "manifest_excluded": len(manifest) - sum(
            1 for e in manifest if in_zip(e["path"])),
        "pdf_sha256": sha(HERE / "paper" / "main.pdf"),
        "anonym_hits": 0,
        "source_date_epoch": 1754000000,
        "upload_candidate": "submission_tmlr_r31_core.zip",
        "upload": "MANUAL (protected layer, not performed)",
        "self_reference_note": (
            "The package ships evidence_manifest.json, "
            "results/r31_manifest_reconciliation.md and this seal file, which "
            "describe the package itself. Their shipped copies are one "
            "generation behind the final zip hash by construction; the on-disk "
            "copies are authoritative and every number in them was recomputed "
            "from the frozen inputs, not copied."),
    }
    (HERE / "results" / "r31_core_package_seal.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()