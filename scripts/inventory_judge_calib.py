"""R21-P0: judge-calibration pair inventory (read-only, no new runs).

For every model judge verdict row in evidence/*judge*.json, resolve the
human gold counterpart from the sealed adjudication records and emit the
pair list with (judge, prompt-family, trace_id, judge_says_correct,
human_says_correct). Multi-pass structures contribute FINAL verdicts only
(pass intermediates recorded separately, never mixed in).

Human-gold sources (all sealed, none fabricated):
  cloud_judge_16 / confirm2  -> in-session 16/16 ruling (paper L119)
  cloud_judge_new60 (5)      -> 4/5 (cloud-new-42 incorrect)
  xdomain (21+pass2 5)       -> xdomain_adjudication 21/21 on content
  powrep 10 + loose 7        -> 10/10, 7/7 in-session
  r18 (27, pass1/2/2b/2c)    -> r18_adjudication final (24 confirmed; excluded
                                lr18-42/54/55 human-incorrect)
  hetero (11)                -> r18_heteromodel_adjudication final (8 confirmed;
                                excluded gr18-41/42/45 human-incorrect)

Writes results/judge_calib_inventory.json. Exit nonzero on unresolved row.
"""

import json
import os
import sys


def load(kb, *parts):
    with open(os.path.join(kb, *parts), encoding="utf-8") as f:
        return json.load(f)


def rows_of(doc):
    if isinstance(doc, list):
        return doc
    for k in ("rows", "calls", "verdicts"):
        if isinstance(doc.get(k), list):
            return doc[k]
    raise KeyError("no row list")


def verdict_of(r):
    for k in ("judge_verdict", "cloud_verdict"):
        if k in r:
            return r[k]
    raise KeyError(str(list(r.keys())))


def norm(v):
    v = str(v).strip().upper()
    if v in ("CORRECT", "对", "1", "TRUE", "YES"):
        return 1
    if v in ("INCORRECT", "错", "0", "FALSE", "NO"):
        return 0
    if "ERROR" in v:
        return None
    raise ValueError(v)


def main(kb):
    pairs = []
    notes = []

    def add(judge, fam, tid, jsays, hsays):
        if jsays is None:
            notes.append(f"judge-ERROR dropped (never evidence): {judge} {tid}")
            return
        pairs.append({"judge": judge, "family": fam, "trace_id": tid,
                      "judge_says_correct": jsays,
                      "human_says_correct": hsays})

    # 16 prior flips: human 16/16 correct
    d = load(kb, "evidence", "cloud_judge_16.json")
    for r in rows_of(d):
        add(d["model"] + "@cloud", "prior16", r["trace_id"],
            norm(verdict_of(r)), 1)

    # cloud-new 5: human 4/5 (cloud-new-42 incorrect)
    d = load(kb, "evidence", "cloud_judge_new60.json")
    for r in rows_of(d):
        add(d["model"] + "@cloud", "cloudnew5", r["trace_id"],
            norm(verdict_of(r)), 0 if r["trace_id"] == "cloud-new-42" else 1)

    # xdomain 21 + pass2 finals
    d = load(kb, "evidence", "xdomain_judge.json")
    adj = load(kb, "results", "xdomain_adjudication.json")
    assert adj.get("content_correct") == 21, adj
    confirmed = {r["trace_id"] for r in rows_of(d)}  # 21/21 on content
    p2 = {}
    try:
        for r in rows_of(load(kb, "evidence", "xdomain_judge_pass2.json")):
            raw = r["second_pass"] if "second_pass" in r else verdict_of(r)
            v = norm(raw)
            if v is not None:
                p2[r["trace_id"]] = v
    except OSError:
        pass
    for r in rows_of(d):
        tid = r["trace_id"]
        v = p2.get(tid, norm(verdict_of(r)))
        add(d["model"] + "@local", "xdomain", tid, v,
            1 if tid in confirmed else 0)

    # powrep tight 10 + loose 7: human all correct
    for fn, fam in (("powrep_judge.json", "powrep10"),
                    ("powrep_loose_judge.json", "powrep7")):
        d = load(kb, "evidence", fn)
        for r in rows_of(d):
            add(d["model"] + "@local", fam, r["trace_id"],
                norm(verdict_of(r)), 1)

    # R18 27 finals from adjudication
    r18 = load(kb, "evidence", "r18_judge.json")
    assert isinstance(r18, list) and len(r18) == 27, len(r18)
    adj18 = load(kb, "results", "r18_adjudication.json")
    calls18 = adj18["calls"]
    ok18 = {t for t, c in calls18.items()
            if c.get("call") in ("confirmed", "confirmed-author")}
    exc18 = set(adj18.get("excluded", []))
    # R22: v33 drops lr18-42 from the flip set (guard now rejects it);
    # its judge-rejected content ruling stands as human=0 below.
    assert exc18 == {"lr18-54", "lr18-55"}, exc18
    assert len(ok18) == 24, len(ok18)
    finals = {}
    for fn in ("r18_judge_pass2.json", "r18_judge_pass2b.json",
               "r18_judge_pass2c.json"):
        try:
            doc = load(kb, "evidence", fn)
        except OSError:
            continue
        for r in rows_of(doc):
            v = norm(verdict_of(r))
            if v is not None:
                finals[r["trace_id"]] = v
    for r in r18:
        tid = r["trace_id"]
        v = finals.get(tid, norm(verdict_of(r)))
        if tid == "lr18-46":
            human = 1  # author-ruled correct (disclosed, paper L230)
        elif tid == "lr18-42":
            human = 0  # R22: non-flip under v33; judge-rejected content stands
        elif tid in exc18:
            human = 0
        else:
            assert tid in ok18, tid
            human = 1
        add("deepseek-r1:7b@local", "r18", tid, v, human)

    # hetero 11 finals
    dh = load(kb, "evidence", "r18_heteromodel_judge.json")
    ah = load(kb, "results", "r18_heteromodel_adjudication.json")
    callsh = ah.get("calls", {})
    okh = {t for t, c in callsh.items()
           if isinstance(c, dict) and c.get("call") == "confirmed"}
    if not okh:
        okh = set(ah.get("confirmed", [])) | set(ah.get("correct", []))
    exche = set(ah.get("excluded", []))
    assert exche == {"gr18-41", "gr18-42", "gr18-45"}, exche
    assert len(okh) == 8, len(okh)
    for r in rows_of(dh):
        tid = r["trace_id"]
        add(dh["model"] + "@local", "hetero11", tid, norm(verdict_of(r)),
            0 if tid in exche else (1 if tid in okh else "UNRESOLVED"))

    bad = [p for p in pairs if p["human_says_correct"] == "UNRESOLVED"]
    if bad:
        raise SystemExit(f"UNRESOLVED gold: {bad}")

    by_judge = {}
    for p in pairs:
        by_judge.setdefault(p["judge"], [0, 0])[0] += 1
        by_judge[p["judge"]][1] += int(p["human_says_correct"] == 0)
    out = {"n_pairs": len(pairs),
           "n_human_incorrect": sum(1 for p in pairs
                                    if p["human_says_correct"] == 0),
           "by_judge": {k: {"n": v[0], "human_incorrect": v[1]}
                        for k, v in sorted(by_judge.items())},
           "dropped_notes": notes,
           "pairs": pairs}
    json.dump(out, open(os.path.join(
        kb, "results", "judge_calib_inventory.json"), "w",
        encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"n_pairs={len(pairs)} "
          f"human_incorrect={out['n_human_incorrect']}")
    print("by_judge=" + json.dumps(out["by_judge"], ensure_ascii=False))
    for n in notes:
        print("NOTE:", n)


if __name__ == "__main__":
    main(sys.argv[1])
