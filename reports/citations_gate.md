# Citation-gate record (Phase 5, R25)

- `gate_citations.py --fail-on-suspicious`: infra exit — wraps
  `.\research-kit\citation-verifier\verify_citations.py`, which does
  not exist on this machine (no research-kit checkout; Windows-path project).
  Per skill spec this degrades to a documented pass, never a silent block.
- Substitute (local, deterministic): `scan_hallucination.py --fail-on-error`
  → reports/hallucination.md — 0 cite errors (no \cite key without .bib entry,
  no bib entry missing title/author), 0 missing method files, 0 arithmetic
  warnings. The 326 uncovered numeric literals are class-(I) surface for the
  LLM judge, not errors (ledger holds 68 claim values; the scan counts every
  literal including CIs, thresholds, and dates).
- Full 4-layer external verification (title/author/result validity per FM-27)
  remains a human pre-upload item; venue is TMLR (no new external citations
  added since R19, bibliography unchanged by R20–R25 text-only rounds).
