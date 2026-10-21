"""R25-P2b: second abstract compression pass. Fails loudly if anchors miss."""
import re
TEX = "paper/main.tex"
src = open(TEX, encoding="utf-8").read()

def rep(old, new):
    global src
    assert src.count(old) == 1, f"anchor x{src.count(old)}: {old[:80]!r}"
    src = src.replace(old, new)

rep("This is a descriptive study: the guarded matcher nests the exact one, so reverse flips are zero by construction and no paired significance is claimed.",
    "Descriptive study: the guarded matcher nests the exact one, so reverse flips are zero by construction; no significance claimed.")
rep("one single-arm replication 7 versus 0 of 157; rollups holdout 7 versus 0 of 108 and local-new 12 versus 0 of 217.",
    "rollups holdout 7 versus 0 of 108 and local-new 12 versus 0 of 217.")
rep("A loose-regime rerun (2, 1, and 4 flips) shows the prompt-regime contrast is question-type-dependent.",
    "A loose-regime rerun shows the prompt-regime contrast is question-type-dependent.")
rep("ECE moves track the accuracy shift under near-degenerate confidences and carry no independent calibration-improvement claim.",
    "ECE moves track the accuracy shift; no independent calibration claim.")
rep("Discordant rows were adjudicated (99 of 106 rows put to judges confirmed on content: 102 flip rows plus 4 non-flip probe rows, Methods).",
    "Adjudication confirms 99 of 106 rows put to judges (102 flips plus 4 probes; Methods).")
rep("(formula recall 12 of 12, precision 12 of 12, accept specificity 12 of 12; CJK-fragment catch 8 of 8 under the v3.3 patch, 8 of 8 missed before it);",
    "(formula 12/12, CJK 8/8);")
rep("a pre-registered fourteenth loose-replication stratum contributes 24 adjudicated flips of 26 raw flips (lr18-42 now guard-caught);",
    "a pre-registered loose-replication stratum contributes 24 of 26 flips;")
rep("a mini-pre-registered fifteenth hetero-family stratum (gemma3:4b, same 60 questions, loose prompt) contributes 8 adjudicated flips of 8 raw flips (three fragment exclusions now guard-rejected).",
    "a hetero-family stratum (gemma3:4b) contributes 8 of 8.")
rep("A blinded 25-item gold set grades 24 of 25 against guarded outcomes (divergence G06, the documented false positive; grader: the author, blinded to outcomes).",
    "A blinded 25-item gold set grades 24 of 25 (divergence G06).")
rep("A 100-item stratified extension (graded blindly by the author, with a blinded second rater (an external human volunteer, not an author) agreeing 29 of 30, Cohen $\\kappa=0.91$) grades 90 of 100 against guarded outcomes (88 of 100 against sealed adjudicated outcomes; all 62 flip rows agree; 9 guard false negatives on non-flip rows plus one author slip (H64) disclosed as limitations).",
    "A 100-item stratified extension (author-graded blindly; external-volunteer second rater agrees 29 of 30, $\\kappa=0.91$) grades 90 of 100 (88 of 100 adjudicated; all 62 flip rows agree; 9 guard false negatives plus one author slip (H64)).")
rep("A same-question retest reproduces the flip set exactly (guarded agreement 1.0).",
    "A retest reproduces the flip set exactly.")
rep("Adjudicated guarded accuracy is 922 of 1062. Strata are reported separately with registration-status labels.",
    "Adjudicated guarded accuracy is 922 of 1062, reported per stratum.")

open(TEX, "w", encoding="utf-8").write(src)
abs_m = re.search(r"\\begin\{abstract\}\n(.*)\n\\end\{abstract\}", src, re.S)
wc = len(re.findall(r"[A-Za-z0-9']+", abs_m.group(1)))
print("abstract words now:", wc)
assert wc <= 310, f"still too long: {wc}"
print("ABSTRACT COMPRESSION OK")
