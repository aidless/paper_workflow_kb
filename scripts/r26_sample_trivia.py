"""R26 TriviaQA sample: n=200 from rc.wikipedia validation, frozen seed. No context columns."""
import json, random
import pyarrow.parquet as pq

SEED = 20260908
N = 200

rows = pq.read_table('/tmp/trivia_wiki_val.parquet',
                     columns=['question_id', 'question', 'answer']).to_pylist()
rng = random.Random(SEED)
idx = rng.sample(range(len(rows)), N)
out = []
for i in idx:
    r = rows[i]
    a = r['answer'] or {}
    aliases = list(dict.fromkeys([a.get('value', '')] + list(a.get('aliases') or [])))
    aliases = [x for x in aliases if x]
    out.append({'id': f"trivia-{r['question_id']}", 'question': r['question'], 'aliases': aliases})
with open('evidence/r26_trivia_sample.jsonl', 'w', encoding='utf-8') as f:
    for o in out:
        f.write(json.dumps(o, ensure_ascii=False) + '\n')
print(f'wrote {len(out)} rows, seed={SEED}, source=mandarjoshi/trivia_qa rc.wikipedia/validation (7993 rows)')
print('median aliases:', sorted(len(o['aliases']) for o in out)[len(out)//2])
