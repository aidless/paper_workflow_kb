# Hallucination scan report (MLR-Bench four types)

Target: `paper`

## (E) Nonexistent Citations / incomplete bib entries
- none

## (E) Hallucinated Methodology: named method files missing
- scripts/ablation.py@main.tex
- scripts/isotonic.py@main.tex
- scripts/tempscale.py@main.tex

## (W) Mathematical Errors: inline arithmetic contradictions
- none

## (I) Faked Results surface: strong-claim count for LLM judge
- 0 strong-assertion phrases found; LLM judge must verify each against evidence

## (I) Numbers without ledger coverage
- 319 numeric literals not covered by CLAIM_LEDGER.md values (no CLAIM_LEDGER.md found)
+0.04, +0.62, -0.0043, -0.015, -0.04, -0.0602, -0.1136, -0.12, -0.55, -0.62, -0.6706, -0.70, 0, 0.0, 0.0005, 0.0008, 0.0037, 0.005, 0.0064, 0.0078, 0.0092, 0.0107, 0.0167, 0.0204, 0.0241, 0.025, 0.0256, 0.0261, 0.0268, 0.0277, 0.0349, 0.0351, 0.0367, 0.0409, 0.0413, 0.0425, 0.0446, 0.05, 0.0517, 0.0533, 0.0542, 0.0558, 0.0667, 0.0668, 0.07, 0.0782, 0.08, 0.0833, 0.0866, 0.0907, 0.095, 0.1035, 0.1067, 0.1075, 0.1127, 0.1147, 0.1172, 0.1215, 0.1255, 0.13, 0.1333, 0.1363, 0.1384, 0.1407, 0.1427, 0.1433, 0.144, 0.155, 0.1567, 0.16, 0.165, 0.1667, 0.1692, 0.1733, 0.1934, 0.2, 0.2025, 0.2036, 0.205, 0.207

## Summary: 0 cite errors, 5 missing method files, 0 arithmetic warnings, 0 strong claims