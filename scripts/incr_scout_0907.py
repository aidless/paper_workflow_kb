# -*- coding: utf-8 -*-
"""One-off arXiv increment scout (2026-08-08 -> 2026-09-07) for C07/C08.
Queries target: (a) same-batch three-matcher flip-rate reporting (C07
counterexample hunt); (b) standard binned-ECE-under-degradation procedure
(C08). Prints machine-readable summary; full hit list to stdout.
"""
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

SINCE = "2026-08-08"
QUERIES = [
    "all:llm AND all:calibration AND all:confidence",
    "all:\"exact match\" AND all:question AND all:answering AND all:tolerance",
    "all:calibration AND all:\"expected calibration error\" AND all:judge",
]
NS = {"a": "http://www.w3.org/2005/Atom"}


def fetch(q):
    url = ("https://export.arxiv.org/api/query?search_query="
           + urllib.parse.quote(q)
           + "&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending")
    with urllib.request.urlopen(url, timeout=60) as r:
        return ET.fromstring(r.read())


seen = {}
for qi, q in enumerate(QUERIES):
    feed = fetch(q)
    for e in feed.findall("a:entry", NS):
        aid = e.find("a:id", NS).text.strip()
        pub = e.find("a:published", NS).text[:10]
        if pub < SINCE or aid in seen:
            continue
        title = " ".join(e.find("a:title", NS).text.split())
        summ = " ".join(e.find("a:summary", NS).text.split())
        seen[aid] = (pub, title, summ, qi)

print(f"HITS_TOTAL={len(seen)} since={SINCE}")
kw_flip = re.compile(r"flip.?rate|three.?matcher|exact.match.*toleran|toleran.*exact.match", re.I)
kw_ece = re.compile(r"standard.*procedur|benchmark.*degrad|binned.*ECE.*degrad|ECE.*under.*shift", re.I)
for aid, (pub, title, summ, qi) in sorted(seen.items()):
    f1 = bool(kw_flip.search(title + " " + summ))
    f2 = bool(kw_ece.search(title + " " + summ))
    print(f"- {pub} q{qi+1} fliplikely={int(f1)} eceproc={int(f2)} {aid} :: {title[:120]}")
