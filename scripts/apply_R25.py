"""R25: apply reviewer round-2 (N1-N5, C3/C4 cont., P2). Text edits only.
Fails loudly if any anchor is missing or ambiguous. Prints abstract word count."""
import re

TEX = "paper/main.tex"
src = open(TEX, encoding="utf-8").read()

def rep(old, new):
    global src
    assert src.count(old) == 1, f"anchor x{src.count(old)}: {old[:80]!r}"
    src = src.replace(old, new)

def words(s):
    return len(re.findall(r"[A-Za-z0-9']+", s))

abs_m = re.search(r"\\begin\{abstract\}\n(.*)\n\\end\{abstract\}", src, re.S)
before_wc = words(abs_m.group(1))
print("abstract words before:", before_wc)

# ---------- E1 N1: abstract counting convention ----------
rep("Discordant rows were adjudicated (99 of 106 confirmed on content).",
    "Discordant rows were adjudicated (99 of 106 rows put to judges confirmed "
    "on content: 102 flip rows plus 4 non-flip probe rows, Methods).")

# ---------- E2 N1+N4: contributions framing + (ii) full breakdown ----------
rep("Contributions: (i)",
    "Descriptive contributions (no inferential claim attaches to any of them): (i)")
rep("(ii) row-by-row adjudication of every row put to judges, 67 of the 68 judged rows confirmed correct on content (20 of 21 prior by a heterogeneous judge including one documented false positive excluded from the guarded basis, 9 of 9 extension in-session under the same standard with the failed second-judge attempt disclosed, 21 of 21 cross-domain on content by a second heterogeneous judge family with both passes on record, 10 of 10 power-replication plus 7 of 7 loose-regime by the same second family, 8 of 8 hetero-family gemma replication by local qwen2.5:7b (three single-character fragments judge-rejected but non-flips under the v3.3 guard);",
    "(ii) row-by-row adjudication of 106 rows put to judges, 99 confirmed correct on content (20 of 21 prior by a heterogeneous judge including one documented false positive excluded from the guarded basis, 9 of 9 extension in-session under the same standard with the failed second-judge attempt disclosed, 21 of 21 cross-domain on content by a second heterogeneous judge family with both passes on record, 10 of 10 power-replication plus 7 of 7 loose-regime by the same second family, 24 of 26 R18 loose-replication flips with 2 echo-containment exclusions, 8 of 8 hetero-family gemma replication by local qwen2.5:7b; the 106 count includes 4 non-flip probe rows carried as controls (R18 lr18-42 plus three hetero-family single-character fragments, all guard-rejected under v3.3); results/adjudication\\_recount\\_R25.json);")

# ---------- E3 N1: R18 pass-1 27 explained ----------
rep("pass 1 confirms 17 of 27;",
    "pass 1 confirms 17 of 27 rows put to the judge "
    "(26 raw flips plus the lr18-42 non-flip control);")

# ---------- E4 N1: hetero 11 rows ----------
rep("evidence/r18\\_heteromodel\\_judge.json; rollup results/r18\\_heteromodel\\_adjudication.json): 8 of 8 confirmed on content;",
    "evidence/r18\\_heteromodel\\_judge.json; rollup results/r18\\_heteromodel\\_adjudication.json): 8 of 8 flips confirmed on content (11 rows put to the judge);")

# ---------- E5 N1: canonical convention in Methods ----------
rep("see the GOLD-100 paragraph below for the decoded numbers.",
    "see the GOLD-100 paragraph below for the decoded numbers. Adjudication accounting convention (used identically in the Abstract, Contributions, and every stratum paragraph): judged counts every row submitted to any judge pass, including 4 non-flip probe rows carried as controls (R18 lr18-42 plus hetero-family gr18-41/42/45, all judge-rejected and guard-rejected under v3.3); confirmed counts rows accepted correct on content in the final ruling. Canonical rollup: 106 judged (102 flip rows plus 4 probes), 99 confirmed (scripts/seal\\_R25\\_numbers.py, results/adjudication\\_recount\\_R25.json).")

# ---------- E6 N2: accuracy-regime distinction (append to asymmetry para) ----------
rep("the loose-regime non-replication of the prompt-regime contrast bounds the regime-contrast claim to question styles with a paraphrase surface.",
    "the loose-regime non-replication of the prompt-regime contrast bounds the regime-contrast claim to question styles with a paraphrase surface.\n\nAccuracy-regime distinction. The flip phenomenon reads differently across accuracy regimes. On the high-accuracy strata (exact accuracy 0.6333 pilot and holdout-main, 0.80 cloud-new and local-new, 0.925 local-big) at most 8 rows per stratum remain wrong after adjudicated tolerant matching (pilot 0, holdout-main 6, cloud-new 8, local-new 7, local-big 8), so flips there are matcher strictness on otherwise-correct output. On the R18 loose-replication (exact 0.25) and hetero-family (exact 0.35) strata, 21 of 60 and 31 of 60 rows remain wrong even after adjudicated tolerant matching, so the high flip counts there (24 and 8 adjudicated) partly reflect model output failure, not matcher strictness alone; the cross-domain loose layer sits between (exact 0.4167, 15 of 60 still wrong after guarded adjudication). Guarded-accuracy claims are therefore reported per stratum, and no pooled flip rate is interpreted as a pure matcher effect.")

# ---------- E7 N3+C4: Limitations FN quantification + reliability hedge ----------
rep("but author grades carry measured reliability (second-rater $\\kappa=0.91$ on 30 items));",
    "but author grades carry measured reliability, not validity (second-rater $\\kappa=0.91$ on 30 items; independent external-human grading beyond the 30-item overlap is future work)); guard false negatives quantified: the guard rejects 140 of 1062 rows on the adjudicated basis (all exact-reject by nesting), and on the 38 GOLD-100 non-flip rows 9 are guard false negatives (conditional rate 9 of 38; the GOLD-100 set is stratified, so no population rate is claimed); the misses make reported guarded accuracy conservative (a lower bound on semantic accuracy); no new guard version is cut here, and the 9 rows stay on record in the GOLD-100 grade files as regression targets (scripts/seal\\_R25\\_numbers.py, results/guard\\_fn\\_R25.json);")

# ---------- E8 C4: second-rater identity ----------
rep("with a blinded second rater agreeing 29 of 30, Cohen $\\kappa=0.91$",
    "with a blinded second rater (an external human volunteer, not an author) agreeing 29 of 30, Cohen $\\kappa=0.91$")
rep("scripts/decode\\_gold100.py, results/gold100\\_agreement.json). Agreement against guarded outcomes is 90 of 100",
    "scripts/decode\\_gold100.py, results/gold100\\_agreement.json; second-rater overlap grades\\_rater2\\_user2.csv with results/rater2\\_kappa.json ($\\kappa=0.91$ on 30 items; the second rater is an external human volunteer, not an author)). Agreement against guarded outcomes is 90 of 100")
rep("no human participants (the only human grading is the author's own blinded grading disclosed in Results).",
    "no human participants (human grading is the author's own blinded grading plus a 30-item blinded overlap by an external volunteer, disclosed in Results).")

# ---------- E9 C3: scale scope bound ----------
rep("(ii) cross-model or cross-type generalization beyond the studied strata (five models counting the authoring model, four question sets; all but the pool are post-registration extensions);",
    "(ii) cross-model, cross-type, or cross-scale generalization beyond the studied strata (five small open-source-grade models, four question sets; no 70B-plus or closed model tested; all but the pool are post-registration extensions);")
rep("a paraphrase-regime replication on a second question family to test the prompt-regime contrast further.",
    "a paraphrase-regime replication on a second question family to test the prompt-regime contrast further; no frontier-scale (70B-plus or closed) model was tested, so the conclusions are bounded to the tested small-model class and cross-scale generalization is future work.")

# ---------- E10 N5: Holm to appendix (move paragraph programmatically) ----------
paras = src.split("\n\n")
idx = next(i for i, p in enumerate(paras)
           if p.startswith("Multiplicity accounting."))
holm_para = paras[idx]
assert "Eighteen paired comparisons are sealed" in holm_para, holm_para[:100]
paras[idx] = ("Multiplicity accounting (audit only). The Holm-Bonferroni ordering "
    "over the sealed comparison family is retained as an audit artifact with no "
    "inferential license (nested construction, $c=0$ by construction); the full "
    "sealed ordering and sensitivity checks stay in the appendix (Holm accounting).")
src = "\n\n".join(paras)
rep("\\section{Equal-frequency ECE values (audit appendix)}",
    "\\section{Holm accounting (audit appendix)}\n" + holm_para
    + "\n\n\\section{Equal-frequency ECE values (audit appendix)}")

# ---------- E10b: L131 seventeen->eighteen + pointer ----------
rep("A Holm-Bonferroni accounting over the seventeen paired comparisons is sealed (results/holm.json) and reported for completeness; under the nested construction it carries no inferential license (see Multiplicity accounting).",
    "A Holm-Bonferroni accounting over the eighteen paired comparisons is sealed (results/holm.json) and reported for completeness; under the nested construction it carries no inferential license (see the Holm accounting appendix).")

# ---------- E11 P2: abstract compression ----------
rep("Programmatic label matchers decide which model answers count as correct, and calibration metrics inherit those decisions. We report 1062 paired comparisons in fifteen strata (plus 412 regime-contrast rows excluded from N): exact string-normalized matching versus a semantic-tolerant matcher and its guarded revision v3.3 (v3.1 formula guard plus v3.2 raw-fallback plus the R22 single-CJK-character substring guard). This is a descriptive measurement study: the guarded matcher nests the exact matcher, so reverse flips are zero by construction on non-degenerate rows and no paired significance is claimed.",
    "Label matchers decide which answers count as correct, and calibration metrics inherit those calls. We report 1062 paired comparisons in fifteen strata (plus 412 regime-contrast rows excluded from N): exact matching versus a semantic-tolerant matcher and its guarded revision v3.3. This is a descriptive study: the guarded matcher nests the exact one, so reverse flips are zero by construction and no paired significance is claimed.")
rep("Observed flip counts (exact-wrong/guarded-right versus reverse) are:",
    "Flip counts (exact-wrong/guarded-right versus reverse):")
rep("(n=30 of pre-specified 50; retained as descriptive pilot data, no top-up);",
    "(descriptive pilot data, no top-up);")
rep("A blinded 25-item gold set grades 24 of 25 against guarded outcomes (95\\% CI 0.805 to 0.993; divergence G06, the documented false positive (the R18-layer second exemplar lr18-42 postdates the 25-item set and is covered by the 100-item extension); grader: the author, blinded to outcomes).",
    "A blinded 25-item gold set grades 24 of 25 against guarded outcomes (divergence G06, the documented false positive; grader: the author, blinded to outcomes).")
rep("(the former second false-positive exemplar lr18-42 fragment over-match is now caught by the v3.3 guard);",
    "(lr18-42 now guard-caught);")
rep("(the three single-character-fragment exclusions now rejected by the guard itself).",
    "(three fragment exclusions now guard-rejected).")
rep("(88 of 100 against sealed adjudicated outcomes; 55 of 55 confirmed flips accepted --- all 62 flip rows agree, the 7 further agreements being excluded rows decided on the exact basis; 9 guard false negatives on non-flip rows disclosed as a limitation plus one author grading slip (H64) adjudicated against the author).",
    "(88 of 100 against sealed adjudicated outcomes; all 62 flip rows agree; 9 guard false negatives on non-flip rows plus one author slip (H64) disclosed as limitations).")
rep("Temperature scaling and isotonic regression show no consistent ECE repair on adjudicated labels (negatives with one n=157 isotonic-CV positive excepted).",
    "Temperature scaling and isotonic regression show no consistent ECE repair.")

# ---------- E12 P2: split Methods snapshot mega-paragraph ----------
rep("The cloud-new stratum is a disclosed new layer, not a same-distribution backfill of missing rows.\nThe fourth stratum",
    "The cloud-new stratum is a disclosed new layer, not a same-distribution backfill of missing rows.\n\nThe fourth stratum")
rep("extending the total to N=942. The R18 loose-replication adds",
    "extending the total to N=942.\n\nThe R18 loose-replication adds")

open(TEX, "w", encoding="utf-8").write(src)

abs_m = re.search(r"\\begin\{abstract\}\n(.*)\n\\end\{abstract\}", src, re.S)
after_wc = words(abs_m.group(1))
print("abstract words after:", after_wc)
assert after_wc < before_wc, "no compression achieved"
assert after_wc <= 310, f"abstract still too long: {after_wc}"

# ---------- standing-number sentinels (N1 gate) ----------
for s in ["99 of 106 rows put to judges confirmed",
          "106 judged (102 flip rows plus 4 probes), 99 confirmed",
          "24 of 26 R18 loose-replication flips",
          "11 rows put to the judge",
          "26 raw flips plus the lr18-42 non-flip control",
          "conditional rate 9 of 38",
          "Holm accounting (audit appendix)",
          "external human volunteer, not an author"]:
    assert s in src, f"sentinel missing: {s}"
print("ALL R25 EDITS APPLIED + SENTINELS OK")
