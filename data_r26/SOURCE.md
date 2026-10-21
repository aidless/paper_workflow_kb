# data_r26 provenance (R26 external validation)

- `triviaqa-rc.tar.gz`: TriviaQA Reading Comprehension official release tarball
  (SHA-256 `ef94fac6db0541e5bb5b27020d067a8b13b1c1ffc52717e836832e02aaed87b9`).
- `entityquestions-dataset.zip`: EntityQuestions official release archive
  (SHA-256 `015eb64a12fa2f9b2f95d2c78bba69779e0d200dbbd4b0772f3ce57bc00da9c5`).
- Both archives are TOO LARGE to ship inside the upload package; the sealed
  R26 evidence is the frozen 200+200 samples (`evidence/r26_*_sample.jsonl`)
  plus model answers (`results/r26_answers_*.jsonl`), drawn by
  `scripts/r26_sample.py` / `scripts/r26_sample_trivia.py`.
- Resampling instructions: place the two archives in this directory
  (names + SHAs above) and run the sampling scripts.
- (No download URLs are stored here by G3 zero-URL policy; both are the
  well-known official releases citable from the paper bibliography.)
