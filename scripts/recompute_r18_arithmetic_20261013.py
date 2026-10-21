#!/usr/bin/env python3
"""Recompute C83's descriptive rates from saved counts; no model calls."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
adjudicated = json.loads((root / 'results/r18_adjudication.json').read_text())
raw = json.loads((root / 'results/r18_loose_rep.json').read_text())['loose_rep']
assert adjudicated['n'] == raw['n'] and adjudicated['n'] > 0
assert 0 <= adjudicated['adjudicated_flips'] <= raw['n_flips'] <= raw['n']
report = {
    'source_files': {},
    'n': adjudicated['n'],
    'adjudicated_flips': adjudicated['adjudicated_flips'],
    'adjudicated_flip_rate': adjudicated['adjudicated_flips'] / adjudicated['n'],
    'raw_flips': raw['n_flips'],
    'raw_flip_percent_1dp': round(100 * raw['n_flips'] / raw['n'], 1),
    'scope': 'arithmetic only; no inferential or novelty claim',
}
for name in ['results/r18_adjudication.json', 'results/r18_loose_rep.json']:
    report['source_files'][name] = hashlib.sha256((root / name).read_bytes()).hexdigest()
destination = root / 'reports/r18_arithmetic_20261013.json'
destination.parent.mkdir(exist_ok=True)
destination.write_text(json.dumps(report, ensure_ascii=False, indent=2))
print(destination)
