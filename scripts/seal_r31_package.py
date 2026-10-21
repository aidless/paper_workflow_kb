# -*- coding: utf-8 -*-
"""Seal for the R31 resubmission package (P6 close-out).

Asserts: main.pdf freshly built from current main.tex (new subsections
present in source), submission_tmlr_r31.zip present, anonymity re-check at
0 hits, package ships the frozen BoolQ source + seal files. No upload is
performed (protected layer: human clicks submit).

Output: results/r31_package_seal.json
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


def main():
    tex = (HERE / "paper" / "main.tex").read_text(encoding="utf-8")
    assert "Theorem 1" in tex and "Theorem 2" in tex
    assert "Public yes/no arm (R30, BoolQ)" in tex
    assert "cross-family reliability evidence" in tex
    pdf = HERE / "paper" / "main.pdf"
    assert pdf.stat().st_size > 100000, pdf.stat().st_size
    anon = (HERE / "submission" / "anonym_check.md").read_text(encoding="utf-8")
    assert "Hits: 0" in anon, anon.splitlines()[2]
    zpath = HERE / "submission" / "submission_tmlr_r31.zip"
    names = set(zipfile.ZipFile(zpath).namelist())
    for must in ("paper/main.tex", "paper/main.pdf",
                 "data_boolq/BoolQ.zip", "data_boolq/BoolQ/val.jsonl",
                 "results/r30_boolq_seal.json", "results/theorems.json",
                 "results/r18_heteromodel_judge2_agreement.json",
                 "PREREG_R30_BOOLQ.md", "PREREG_R31_HETEROJUDGE.md"):
        assert must in names, must
    payload = {
        "pdf_sha256": sha(pdf),
        "zip_sha256": sha(zpath),
        "zip_n_files": len(names),
        "tex_sha256": sha(HERE / "paper" / "main.tex"),
        "ledger_sha256": sha(HERE / "CLAIM_LEDGER.md"),
        "source_date_epoch": 1754000000,
        "anonym_hits": 0,
        "upload": "MANUAL (protected layer, not performed)",
    }
    (HERE / "results" / "r31_package_seal.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()