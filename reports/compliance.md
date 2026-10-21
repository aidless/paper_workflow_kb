# TMLR compliance scan report

Target: `paper`  |  findings: 10  |  failures: 3
- [G1] PASS :: anonymous tmlr usage '\\usepackage{tmlr}' @ paper/main.tex
- [G4] INFO :: url https://github.com/goodfeli/dlbook_notation. @ paper/main.tex:9 (allowed / acceptance-policy)
- [G4] INFO :: url https://openreview.net/forum?id=XXXX @ paper/main.tex:35 (allowed / acceptance-policy)
- [G6] PASS :: bibliography mechanism present
- [EXTRA] FAIL :: placeholder 'TODO' @ STATE_SNAPSHOT.md:7
- [EXTRA] FAIL :: placeholder 'TODO' @ STATE_SNAPSHOT.md:14
- [EXTRA] FAIL :: placeholder 'TODO' @ STATE_SNAPSHOT.md:23
- [G7] PASS :: Broader Impact section @ paper/main.tex:127 (65 words, 3 keywords)
- [G9] PASS :: dataset license/source declaration in protocol.md
- [G9] WARN :: no compute-resource declaration in protocol.md (FM-29: add 'hardware: <GPU model xN>, runtime: <hours>')