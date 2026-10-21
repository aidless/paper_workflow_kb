"""R19-REVIEW_R4 response verification: assert every reviewer number-claim before fixing text.
R22 FROZEN: R19-era audit (expects flips 58/62, hetero raw 11, etc.). v33 promotion
moves these numbers (62/62, raw 8); this script is kept as the R19 record and is
NOT a gate. Do not update its asserts; see C59/C63 for current numbers.
Exit 0 = allrone issues verified as real; any assert fail = issue needs re-triage.
Usage: python3 scripts/verify_r4_response.py (cwd=paper_workflow_kb)"""
import json, sys

ok = []
def check(name, cond, detail=""):
    assert cond, f"VERIFY-FAIL {name} {detail}"
    ok.append(name)
    print(f"ok {name} {detail}")

eu = json.load(open("results/ece_unified.json"))
strata = eu["strata"] if "strata" in eu else eu
check("eu-14-no-hetero", len(strata) == 14 and not any("hetero" in k.lower() or "gemma" in k.lower() for k in strata),
      f"keys={len(strata)}")

rh = json.load(open("results/r18_heteromodel.json"))["heteromodel"]
check("hetero-raw-ece", round(rh["ece10_exact"], 4) == 0.5143, f'{rh["ece10_exact"]}')
check("hetero-raw-flips", rh["n_flips"] == 11)
check("hetero-raw-acc", (rh["n_exact"], round(rh["acc_guarded"], 4)) == (21, 0.5333))
rh2 = json.load(open("results/r18_heteromodel_adjudication.json"))
check("hetero-adj-ece", rh2["adjudicated_ece_equalwidth"] == 0.381, f'{rh2["adjudicated_ece_equalwidth"]}')
check("hetero-adj-flips", rh2["adjudicated_flips"] == 8 and rh2["raw_flips"] == 11)

key = json.load(open("evidence/gold100_key.json"))["counts"]
check("gold100-composition", (key["n_confirmed"], key["n_excluded"], key["n_nonflip"]) == (55, 7, 38))
g = json.load(open("results/gold100_agreement.json"))
check("gold100-flips", (g["flips"]["a"], g["flips"]["n"]) == (58, 62))
vind = g.get("fp_exclusions_vindicated", [])
check("gold100-vindicated4", len(vind) == 4, f"{vind}")
agreed_excluded = key["n_excluded"] - len(vind)  # excluded items that agreed (H34/H47/H85)
confirmed_accepted = g["flips"]["a"] - agreed_excluded
check("gold100-confirmed-55", (agreed_excluded, confirmed_accepted) == (3, 55),
      "agreed_excluded=3 -> confirmed 55/55, NOT 58/58")

gg = json.load(open("results/gold_guarded_agreement.json"))
items = gg.get("per_item", [])
ids = [it.get("id") for it in items if it.get("agree_vs_guarded") is False]
check("gold25-only-G06", ids == ["G06"], f"{ids}")

r18a = json.load(open("results/r18_adjudication.json"))
reads = r18a["calls"]["lr18-46"]["reads"]
check("lr18-46-four", len(reads) == 4 and all(r == "ERROR" for r in reads), f"{reads}")

iso = json.load(open("results/isotonic.json"))
tn = json.load(open("results/tempiso_n157.json"))
cv = {
    "pilot": iso["strata"]["pilot"].get("ECE_isotonic_cv5", iso["strata"]["pilot"].get("cv5")),
    "holdout": iso["strata"]["holdout-main"]["ECE_isotonic_cv5"] if "ECE_isotonic_cv5" in iso["strata"]["holdout-main"] else None,
    "cloud": iso["strata"]["cloud-new"]["ECE_isotonic_cv5"] if "ECE_isotonic_cv5" in iso["strata"]["cloud-new"] else None,
    "powcloudnew": tn["arms"]["powcloudnew"]["isotonic"]["EW_cv5"],
    "powlocalnew": tn["arms"]["powlocalnew"]["isotonic"]["EW_cv5"],
}
print("iso-CV map:", json.dumps(cv))
raw = {"pilot": 0.0037, "holdout": 0.165, "cloud": 0.0558, "powcloudnew": 0.0268, "powlocalnew": 0.0668}
improved = [k for k in cv if cv[k] is not None and cv[k] < raw[k]]
check("five-cv-defined", set(cv) == set(raw), f"tests={sorted(cv)}")
check("five-cv-one-nontrivial-positive",
      [k for k in improved if k != "pilot"] == ["powlocalnew"],
      f"improved={improved} (pilot 0.0037->0.0 is degenerate-trivial, must be carved out in text)")

gs = json.load(open("results/guard_synth.json"))
print("R_excluded note:", gs["results"]["classes"]["R_excluded"].get("note", "(no note)"))

print(f"\nALL {len(ok)} CHECKS PASSED")
