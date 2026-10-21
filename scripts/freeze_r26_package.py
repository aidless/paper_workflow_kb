#!/usr/bin/env python3
"""freeze_r26_package.py — build submission_tmlr_r26.zip (R26 package freeze).

Difference from prepare_submission.py: also excludes data_r26/ (2.5 GB external
benchmark downloads — triviaqa-rc.tar.gz + entityquestions zip), which are
size-recorded in PHASE5_SEAL (not hashed, not project-generated) and must NOT
ship inside the TMLR package (100 MB limit + not reproducible project evidence).

Reuses prepare_submission.excluded() so the FM-26 process-doc/rater/verify
exclusions stay identical. Writes a NEW zip; does NOT touch the r25 zip, so the
"r25 invariant" recorded by the R26-external seal stays valid.
"""
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]  # paper_workflow_kb
sys.path.insert(0, str(HERE / "scripts"))

from prepare_submission import excluded  # reuse FM-26 exclusion logic

EXTRA_EXCLUDE_DIRS = {"data_r26"}


def excluded_r26(p: Path, root: Path) -> bool:
    if excluded(p, root):
        return True
    try:
        rel = p.relative_to(root)
    except ValueError:
        return True
    return rel.parts[0] in EXTRA_EXCLUDE_DIRS


def main() -> int:
    root = HERE
    out = root / "submission" / "submission_tmlr_r26.zip"
    included = []
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(root.rglob("*")):
            if not p.is_file() or excluded_r26(p, root):
                continue
            rel = p.relative_to(root).as_posix()
            zf.write(p, arcname=rel)
            included.append(rel)
    size_mb = out.stat().st_size / 1e6
    leaked = [f for f in included if f.startswith("data_r26/")]
    has_pdf = any(f == "paper/main.pdf" for f in included)
    has_tex = any(f == "paper/main.tex" for f in included)
    print(f"r26 zip: {out} ({size_mb:.2f} MB, {len(included)} files)")
    print(f"  data_r26 leaked: {len(leaked)}")
    print(f"  paper/main.pdf: {'YES' if has_pdf else 'NO'}; paper/main.tex: {'YES' if has_tex else 'NO'}")
    assert not leaked, f"data_r26 leaked into package: {leaked[:5]}"
    assert has_pdf and has_tex, "package must include main.pdf + main.tex"
    assert size_mb <= 100, f"package over 100 MB limit: {size_mb:.1f}"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())