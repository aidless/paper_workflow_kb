#!/usr/bin/env python3
"""Count CLAIM_LEDGER.md rows and check that the cited files exist.

This is a census, not a field-level verifier. It does not emit PASS counts
for scientific claims and it does not replace scripts/verify_claim_ledger.py
(that shell exits 3 on a clone when the canonical implementation is absent).

The computed line must appear exactly once in README.md, CLAIM_LEDGER.md,
and FAILURE_MODES.md:

    LEDGER_CENSUS: n=<rows> verified=<...> inconclusive=<...> superseded=<...> draft=<...> blocked=<...> other=<...>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "CLAIM_LEDGER.md"
MUST_MENTION = (ROOT / "README.md", ROOT / "CLAIM_LEDGER.md", ROOT / "FAILURE_MODES.md")
PATH_RE = re.compile(
    r"[A-Za-z0-9_./\-\u4e00-\u9fff]+\.(?:jsonl|json|md|csv|pdf|txt)"
)
ID_RE = re.compile(r"^C(\d+)$")
STALE_README = ("82-entry", "82 条", "82 entries", "80 verified")


def rows(text: str):
    out = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.startswith("| C"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 8:
            continue
        cid, evid, status = parts[1], parts[3], parts[6]
        if not ID_RE.match(cid):
            continue
        out.append((lineno, cid, evid, status))
    return out


def bucket(status: str) -> str:
    if status == "verified":
        return "verified"
    if status == "inconclusive":
        return "inconclusive"
    if status == "draft":
        return "draft"
    if status == "blocked":
        return "blocked"
    if status.startswith("superseded"):
        return "superseded"
    return "other"


def main() -> int:
    text = LEDGER.read_text(encoding="utf-8")
    parsed = rows(text)
    counts = {k: 0 for k in
              ("verified", "inconclusive", "superseded", "draft", "blocked", "other")}
    ids = []
    missing = []
    cited = 0
    bad_status = []
    for lineno, cid, evid, status in parsed:
        ids.append((int(cid[1:]), cid, lineno, status))
        kind = bucket(status)
        counts[kind] += 1
        if kind == "other":
            bad_status.append(f"{cid} line {lineno}: {status!r}")
        paths = PATH_RE.findall(evid)
        if not paths:
            missing.append(f"{cid} line {lineno}: evidence cell has no file path")
        for rel in paths:
            cited += 1
            if not (ROOT / rel).is_file():
                missing.append(f"{cid}: missing {rel}")

    dup = sorted({c for _, c, _, _ in ids if sum(1 for x in ids if x[1] == c) > 1})
    numbers = [n for n, _, _, _ in ids]
    gaps = []
    if numbers:
        for n in range(1, max(numbers) + 1):
            if n not in set(numbers):
                gaps.append(f"C{n:02d}")

    line = (
        "LEDGER_CENSUS: "
        f"n={len(parsed)} verified={counts['verified']} "
        f"inconclusive={counts['inconclusive']} superseded={counts['superseded']} "
        f"draft={counts['draft']} blocked={counts['blocked']} other={counts['other']}"
    )
    print(line)
    print(f"cited_paths={cited} missing_paths={len(missing)}")

    errors = []
    if dup:
        errors.append("duplicate ids: " + ", ".join(dup))
    if gaps:
        errors.append("id gaps: " + ", ".join(gaps))
    if bad_status:
        errors.extend(bad_status)
    if missing:
        errors.extend(missing)
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in STALE_README:
        if phrase in readme:
            errors.append(
                f"README.md still contains stale ledger shorthand {phrase!r}"
            )
    for path in MUST_MENTION:
        if not path.is_file():
            errors.append(f"missing {path.name}")
            continue
        hits = path.read_text(encoding="utf-8").count(line)
        if hits != 1:
            errors.append(
                f"{path.name} contains the computed census line {hits} times (want 1)"
            )
    if errors:
        print("CENSUS FAIL")
        for err in errors:
            print(err)
        return 1
    print("CENSUS OK (row count and cited paths only; not a field-level PASS)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
