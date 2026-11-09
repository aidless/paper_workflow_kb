#!/usr/bin/env python3
"""Compare key ledger cells and the README SEAL_DRIFT block to results JSON.

No new measurements. Values are read from the sealed JSON already in the tree
and from the claim rows that point at those fields. A mismatch is drift.
This script does not recompute matchers; the offline gate runs the seal
scripts for that. It also does not turn a match into an acceptance or a PASS
of the external ledger verifier.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "CLAIM_LEDGER.md"
README = ROOT / "README.md"

# Rows whose evidence cell is `file -> field / field` and whose value cell is
# the same number of slash-separated tokens. Chosen because they are the
# public yes/no arms, the disclosed external over-fire counts, and the
# isotonic negative (CV ECE did not improve).
HEADLINES = ("C21", "C69", "C70", "C71", "C78", "C82", "C84")
ID_RE = re.compile(r"^C(\d+)$")
BLOCK_RE = re.compile(r"<!-- SEAL_DRIFT\n(.*?)-->", re.S)
PATH_TOK = re.compile(r"[^.\[\]]+|\[\d+\]")


def close(got, token: str) -> bool:
    token = token.strip()
    if isinstance(got, bool):
        return token.lower() == ("true" if got else "false")
    if isinstance(got, str):
        return got == token
    if isinstance(got, int) and "." not in token:
        return got == int(token)
    expected = float(token)
    gotf = float(got)
    if "." in token:
        nd = len(token.split(".", 1)[1])
        return round(gotf, nd) == round(expected, nd)
    return gotf == expected


def get_path(obj, path: str):
    cur = obj
    for tok in PATH_TOK.findall(path):
        if tok.startswith("["):
            cur = cur[int(tok[1:-1])]
        else:
            cur = cur[tok]
    return cur


def ledger_rows(text: str):
    found = {}
    for line in text.splitlines():
        if not line.startswith("| C"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 8 or not ID_RE.match(parts[1]):
            continue
        found[parts[1]] = {"evidence": parts[3], "values": parts[4], "status": parts[6]}
    return found


def check_row(cid: str, row: dict, errors: list[str]) -> None:
    evid = row["evidence"]
    if ";" in evid or "->" not in evid:
        errors.append(f"{cid}: evidence cell is not a single file->fields pointer")
        return
    file_part, field_part = (p.strip() for p in evid.split("->", 1))
    fields = [f.strip() for f in field_part.split("/")]
    values = [v.strip() for v in row["values"].split("/")]
    if len(fields) != len(values):
        errors.append(
            f"{cid}: {len(fields)} fields vs {len(values)} values"
        )
        return
    path = ROOT / file_part
    if not path.is_file():
        errors.append(f"{cid}: missing {file_part}")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    for field, token in zip(fields, values):
        try:
            got = get_path(data, field)
        except (KeyError, IndexError, TypeError) as exc:
            errors.append(f"{cid}: {file_part} {field}: {exc}")
            continue
        if not close(got, token):
            errors.append(
                f"{cid}: {file_part} {field} json={got!r} ledger={token!r}"
            )
    print(f"ledger {cid} {row['status']} {file_part} fields={len(fields)}")


def check_readme_block(errors: list[str]) -> None:
    text = README.read_text(encoding="utf-8")
    m = BLOCK_RE.search(text)
    if not m:
        errors.append("README.md has no SEAL_DRIFT block")
        return
    n = 0
    for raw in m.group(1).splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        bits = line.split()
        file_part, assigns = bits[0], bits[1:]
        if not assigns:
            errors.append(f"SEAL_DRIFT empty assignments: {line}")
            continue
        path = ROOT / file_part
        if not path.is_file():
            errors.append(f"SEAL_DRIFT missing {file_part}")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for assign in assigns:
            if "=" not in assign:
                errors.append(f"SEAL_DRIFT bad token {assign}")
                continue
            field, token = assign.split("=", 1)
            try:
                got = get_path(data, field)
            except (KeyError, IndexError, TypeError) as exc:
                errors.append(f"SEAL_DRIFT {file_part} {field}: {exc}")
                continue
            if not close(got, token):
                errors.append(
                    f"SEAL_DRIFT {file_part} {field} json={got!r} readme={token!r}"
                )
        n += 1
        print(f"readme {file_part} fields={len(assigns)}")
    if n == 0:
        errors.append("SEAL_DRIFT block is empty")


def check_merged_in_c54(rows: dict, errors: list[str]) -> None:
    """C54's value cell is not a clean field list. Require the four merged
    totals, as stored in results/merged_1062.json, to appear in that cell in
    the same order. The integers come from the JSON, not from this script."""
    path = ROOT / "results" / "merged_1062.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    want = [str(data[k]) for k in
            ("n", "n_exact", "n_guarded_adjudicated", "n_flips")]
    tokens = [t.strip() for t in rows["C54"]["values"].split("/")]
    found = any(tokens[i:i + 4] == want for i in range(len(tokens) - 3))
    if not found:
        errors.append(
            "C54 value cell does not contain merged_1062.json totals "
            + " / ".join(want)
        )
    else:
        print("ledger C54 merged_1062 totals " + " ".join(want))


def selftest() -> None:
    assert close(0.6889, "0.6889")
    assert close(0.0009765624999999999, "0.0009765625")
    assert close(0.03333333333333333, "0.03333")
    assert not close(0.69, "0.6889")
    assert close(55, "55")
    assert not close(56, "55")
    assert close(False, "false")
    assert close(True, "true")
    assert not close(False, "true")
    assert get_path({"a": {"b-c": [1, 2]}}, "a.b-c[1]") == 2


def main() -> int:
    selftest()
    rows = ledger_rows(LEDGER.read_text(encoding="utf-8"))
    errors: list[str] = []
    for cid in HEADLINES:
        if cid not in rows:
            errors.append(f"missing ledger row {cid}")
            continue
        check_row(cid, rows[cid], errors)
    if "C54" not in rows:
        errors.append("missing ledger row C54")
    else:
        check_merged_in_c54(rows, errors)
    check_readme_block(errors)
    if errors:
        print("DRIFT FAIL")
        for err in errors:
            print(err)
        return 1
    print("DRIFT OK (ledger and README match the sealed JSON; not a new measurement)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
