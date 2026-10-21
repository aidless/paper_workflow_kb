# -*- coding: utf-8 -*-
"""Manifest-vs-core-zip reconciliation for the R32 core package.

Recomputes the reconciliation from the CURRENT evidence_manifest.json and the
CURRENT submission_tmlr_r31_core.zip, using the shipping rules in
scripts/prepare_submission.py (imported, not duplicated) so the record cannot
drift from the packer.

Class priority mirrors the R31 record so counts stay comparable.

Output: results/r31_manifest_reconciliation.md
"""
import json
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))

import prepare_submission as ps  # noqa: E402

CORE = HERE / "submission" / "submission_tmlr_r31_core.zip"
MAN = HERE / "evidence_manifest.json"
OUT = HERE / "results" / "r31_manifest_reconciliation.md"
# the packer runs from the repo root; manifest paths carry the kb/ prefix
KB_PREFIX = "paper_workflow_kb/"


def classify(rel_posix):
    p = Path(rel_posix)
    parts = p.parts
    # excluded by design, not by a packer rule: the R29 blind key must never be
    # distributed (it would void the blindness) and the volunteer pack is an
    # outbound artifact, not manuscript evidence.
    if p.name in {"r29_blind_key.json", "r29_blind_pack_volunteer.csv"}:
        return "blind-material (must not ship by design)"
    # four-scan outputs are acceptance-gate records; the scanners ship, the
    # per-round reports stay local (same as every earlier round).
    if p.name.startswith("scan_") and p.suffix.lower() == ".md":
        return "audit-scan-report (process, not shipped)"
    if parts and parts[0] == "submission":
        return "submission-dir (SKIP_DIRS)"
    if any(sub in p.name for sub in ps.RATER_SUBSTRINGS):
        return "rater-process (excluded)"
    if p.name in ps.PROCESS_FILES:
        return "process-files (excluded by name)"
    if p.suffix.lower() in {".aux", ".log", ".out", ".fls",
                            ".fdb_latexmk", ".xdv", ".blg"}:
        return "build-exhaust (suffix excluded)"
    if rel_posix in ps.HEAVY_RAW_EXCLUDE:
        return "heavy-raw/byproduct (M4 excluded)"
    for part in parts:
        if any(part.startswith(x) for x in ps.VERIFY_PREFIX) or \
                any(part.endswith(x) for x in ps.VERIFY_SUFFIX):
            return "verify-scaffolding (excluded)"
    if any("/".join(parts[:i + 1]) in ps.PROCESS_DIRS
           for i in range(len(parts))) or parts[0] in ps.PROCESS_DIRS:
        return "kb-knowledge-base (PROCESS_DIRS excluded)"
    if p.name.startswith(ps.PROCESS_PREFIXES) or \
            p.name.endswith(ps.PROCESS_SUFFIXES):
        return "process-docs (FM-26 excluded)"
    if parts and parts[0] == "paper" and p.suffix.lower() == ".txt":
        return "paper-text-extraction (excluded)"
    return None


def main():
    man = json.loads(MAN.read_text(encoding="utf-8"))["files"]
    paths = [e["path"] for e in man]
    with zipfile.ZipFile(CORE) as z:
        names = set(z.namelist())
        total_bytes = sum(i.file_size for i in z.infolist())
    # manifest paths are repo-root relative; zip names are kb-relative
    inside = [p for p in paths
              if p.startswith(KB_PREFIX) and p[len(KB_PREFIX):] in names]
    outside = [p for p in paths if p not in inside]

    classes = {}
    unexplained = []
    for p in outside:
        rel = p[len(KB_PREFIX):] if p.startswith(KB_PREFIX) else p
        c = classify(rel)
        if c is None:
            unexplained.append(p)
        else:
            classes[c] = classes.get(c, 0) + 1

    lines = [
        "# R31/R32 manifest reconciliation (R32 re-seal)",
        "",
        "- manifest entries: %d" % len(paths),
        "- core-zip files: %d (upload candidate `submission_tmlr_r31_core.zip`, "
        "%.1fMB)" % (len(names), total_bytes / 1e6),
        "- manifest entries inside core zip: %d" % len(inside),
        "- manifest entries NOT in core zip: %d, every class named below"
        % len(outside),
        "",
        "## Out-of-zip breakdown (each class maps to a prepare_submission.py rule)",
        "",
    ]
    for k in sorted(classes, key=lambda x: -classes[x]):
        lines.append("- %s: %d" % (k, classes[k]))
    lines.append("")
    lines.append("Unexplained: %d." % len(unexplained))
    if unexplained:
        lines.append("")
        for u in unexplained:
            lines.append("- %s" % u)
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    assert not unexplained, unexplained[:5]


if __name__ == "__main__":
    main()
