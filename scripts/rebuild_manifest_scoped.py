"""Rebuild evidence_manifest.json scoped to paper_workflow_kb/ with repo-root prefix.

Established format (R13 seal, R16): {"root": ".", files[].path = "paper_workflow_kb/..."}.
Scope decision: manifest covers paper_workflow_kb/** only (evidence + deliverables);
workspace-level files (script_lab, movies, other paper_* dirs) are out of scope,
same as the 252-entry R16 manifest. Verify-from-root WARNs on those are expected.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_evidence_manifest import collect_files, sha256_of

ROOT = Path(".")
SCOPE = Path("paper_workflow_kb")
OUT = SCOPE / "evidence_manifest.json"

entries = []
for p in collect_files(SCOPE):
    if p.resolve() == OUT.resolve():
        continue  # never hash the manifest into itself
    st = p.stat()
    entries.append({
        "path": (SCOPE / p.relative_to(SCOPE)).as_posix(),
        "size": st.st_size,
        "sha256": sha256_of(p),
        "modified": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(timespec="seconds"),
    })

manifest = {
    "root": str(ROOT),
    "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "files": entries,
}
OUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {len(entries)} entries -> {OUT}")
