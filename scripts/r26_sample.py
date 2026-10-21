"""R26 external sampling (PREREG_R26_EXTERNAL R2, seed 20260908 frozen).

EntityQuestions test: round-robin across relations -> 200 rows.
TriviaQA-RC wikipedia dev: shuffle -> first 200 rows.
Writes evidence/r26_trivia_sample.jsonl / evidence/r26_entity_sample.jsonl.
"""
import json
import random
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "data_r26"
EV = HERE / "evidence"
SEED = 20260908
N = 200


def sample_entity():
    z = zipfile.ZipFile(DATA / "entityquestions-dataset.zip")
    rels = sorted(n for n in z.namelist()
                  if n.startswith("dataset/test/P") and n.endswith(".test.json"))
    assert len(rels) >= 24, len(rels)
    per_rel = {}
    for n in rels:
        rel = n.split("/")[-1].split(".")[0]
        rows = json.loads(z.read(n).decode())
        assert all("question" in r and "answers" in r for r in rows), n
        per_rel[rel] = rows
    rng = random.Random(SEED)
    for rows in per_rel.values():
        rng.shuffle(rows)
    out, i = [], 0
    rels_sorted = sorted(per_rel)
    while len(out) < N:
        for rel in rels_sorted:
            if len(out) >= N:
                break
            rows = per_rel[rel]
            if i < len(rows):
                r = rows[i]
                out.append({"id": "entity-%s-%d" % (rel, i),
                            "relation": rel,
                            "question": r["question"],
                            "aliases": sorted(set(r["answers"]))})
        i += 1
    assert len(out) == N, len(out)
    return out


def sample_trivia():
    import tarfile
    t = tarfile.open(DATA / "triviaqa-rc.tar.gz")
    member = [m for m in t.getmembers()
              if m.name.endswith("qa/wikipedia-dev.json")]
    assert len(member) == 1, [m.name for m in t.getmembers()
                              if "wikipedia-dev" in m.name][:5]
    d = json.load(t.extractfile(member[0]))
    rows = d["Data"]
    rng = random.Random(SEED)
    rng.shuffle(rows)
    out = []
    for r in rows[:N]:
        aliases = sorted(set(r["Answer"].get("Aliases", []) +
                             r["Answer"].get("NormalizedAliases", [])))
        assert aliases, r.get("QuestionId")
        out.append({"id": "trivia-%s" % r["QuestionId"],
                    "question": r["Question"],
                    "aliases": aliases})
    assert len(out) == N, len(out)
    return out


def main():
    EV.mkdir(exist_ok=True)
    ent = sample_entity()
    (EV / "r26_entity_sample.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in ent) + "\n")
    print("entity: %d rows, %d relations" %
          (len(ent), len(set(r["relation"] for r in ent))))
    try:
        tri = sample_trivia()
    except (FileNotFoundError, EOFError, Exception) as e:
        print("trivia skipped (tarball not ready): %r" % e)
        return
    (EV / "r26_trivia_sample.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in tri) + "\n")
    print("trivia: %d rows" % len(tri))


if __name__ == "__main__":
    main()
