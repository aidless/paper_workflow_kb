# R31/R32 manifest reconciliation (R32 re-seal)

- manifest entries: 532
- core-zip files: 339 (upload candidate `submission_tmlr_r31_core.zip`, 5.5MB)
- manifest entries inside core zip: 338
- manifest entries NOT in core zip: 194, every class named below

## Out-of-zip breakdown (each class maps to a prepare_submission.py rule)

- process-docs (FM-26 excluded): 73
- rater-process (excluded): 67
- submission-dir (SKIP_DIRS): 14
- build-exhaust (suffix excluded): 11
- heavy-raw/byproduct (M4 excluded): 7
- verify-scaffolding (excluded): 7
- kb-knowledge-base (PROCESS_DIRS excluded): 5
- audit-scan-report (process, not shipped): 5
- process-files (excluded by name): 3
- blind-material (must not ship by design): 2

Unexplained: 0.
