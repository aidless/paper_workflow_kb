"""R18 P1-2b evidence-pointers + ledger-range edits."""
P = "paper_workflow_kb/paper/main.tex"
s = open(P, encoding="utf-8").read()

EDITS = [
("claim ledger CLAIM\\_LEDGER.md (C09--C48 verified);",
 "claim ledger CLAIM\\_LEDGER.md (C09--C54 verified, C52--C53 unified-binning convention);"),
("Unified-binning recomputation scripts/recompute\\_ece\\_unified.py with results/ece\\_unified.json "
 "(all fourteen strata under one equal-width convention,",
 "Unified-binning recomputation scripts/recompute\\_ece\\_unified.py with results/ece\\_unified.json "
 "(all fifteen strata under one equal-width convention,"),
("seal scripts/seal\\_r18\\_update.py with results/r18\\_seal.json (16 files).",
 "seal scripts/seal\\_r18\\_update.py with results/r18\\_seal.json (16 files). Hetero-family records: "
 "mini-pre-registration PREREG\\_R18\\_HETEROMODEL.md (with Amendment A1 model substitution), "
 "collection scripts/r18\\_heteromodel60.py with raw evidence/r18\\_heteromodel\\_gemma60\\_raw.json "
 "(60/60, zero errors) plus the 54-row failed-attempt record evidence/r18\\_heteromodel60\\_raw.json "
 "(thinking-mode rows, never analyzed), analysis scripts/analyze\\_r18\\_heteromodel.py with "
 "results/r18\\_heteromodel.json (raw 11/60, descriptive), judge scripts/local\\_judge\\_heteromodel.py "
 "with evidence/r18\\_heteromodel\\_judge.json (8/11), rollup scripts/r18\\_heteromodel\\_adjudicate.py "
 "with results/r18\\_heteromodel\\_adjudication.json (8 of 11 confirmed; excluded gr18-41/42/45), "
 "merged sums scripts/seal\\_merged\\_hetero.py with results/merged\\_1062.json (830/922/92 of 1062)."),
]

for old, new in EDITS:
    assert s.count(old) == 1, ("ANCHOR", old[:70], s.count(old))
    s = s.replace(old, new)

open(P, "w", encoding="utf-8").write(s)
print(len(EDITS), "edits ok")
