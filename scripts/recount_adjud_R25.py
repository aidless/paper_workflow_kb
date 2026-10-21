"""R25 N1 recount v2: correct schema handling."""
import json, os
EV = "evidence"

def verdict(r):
    for k in ("judge_verdict", "cloud_verdict", "confirm_verdict",
              "ruling", "verdict", "second_pass"):
        if r.get(k) is not None:
            return r[k]
    return None

def load_rows(f):
    d = json.load(open(os.path.join(EV, f), encoding="utf-8"))
    if isinstance(d, list):
        return d
    for k in ("rows", "flips"):
        if isinstance(d.get(k), list):
            return d[k]
    return [d]

def show(f):
    rs = load_rows(f)
    vs = [verdict(r) for r in rs]
    n_ok = sum(1 for v in vs if v == "correct")
    n_no = sum(1 for v in vs if v == "incorrect")
    n_other = len(vs) - n_ok - n_no
    print(f"{f}: n={len(rs)} correct={n_ok} incorrect={n_no} other={n_other}")
    if n_other:
        for r, v in zip(rs, vs):
            if v not in ("correct", "incorrect"):
                print("   ", r.get("trace_id"), repr(v))

for f in ["cloud_judge_16.json", "cloud_judge_confirm2.json",
          "holdout_adjudication.json", "cloud_judge_new60.json",
          "local_adjudication.json", "big_adjudication.json",
          "xdomain_judge.json", "xdomain_judge_pass2.json",
          "powrep_judge.json", "powrep_loose_judge.json",
          "r18_judge.json", "r18_judge_pass2.json",
          "r18_judge_pass2b.json", "r18_judge_pass2c.json",
          "r18_heteromodel_judge.json"]:
    show(f)
