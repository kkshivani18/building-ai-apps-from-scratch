# Embedding and vector representation exercises

Each exercise is a separate, runnable Python file. Run commands from this
directory:

```powershell
python 01_metric_comparison.py
python 02_chunk_size_experiment.py
python 03_matryoshka_simulation.py
python 04_binary_quantization.py
python 05_sentence_chunking.py
```

The exercises intentionally use the local `SimpleEmbedder` and brute-force
`VectorIndex`. This makes the experiments reproducible and avoids unnecessary
Gemini API calls. The experiments test retrieval behavior; the production
adapter remains in the `use it` section.

## Exercise 1: metric comparison

Run the same five queries using cosine similarity, dot product, and Euclidean
distance. Record the top three document IDs and scores. Note where rankings
disagree and whether vector normalization explains the difference.

## Exercise 2: chunk size experiment

The script tests chunk sizes 50, 100, 200, and 500 words and writes
`chunk_size_results.csv`. Record the mean top-1 score and recall@1. If desired,
plot both columns against `chunk_size` using your preferred plotting tool.

## Exercise 3: Matryoshka simulation

The script creates 500-dimensional padded vectors and evaluates truncation to
50, 100, 200, and 500 dimensions. Record recall@1 and explain why this is only
a simulation: truncating ordinary TF-IDF dimensions is not the same as a model
trained for Matryoshka representations.

## Exercise 4: binary quantization

Vectors are converted to binary signs and ranked with Hamming distance. Record
the top-10 overlap with full-precision cosine search. Discuss the memory
savings and retrieval-quality trade-off.

## Exercise 5: sentence-based chunking

The script compares fixed-size chunks with `chunk_by_sentences`. Record mean
top-1 score and recall@1. Explain whether sentence boundaries improved this
small corpus; do not generalize from five queries alone.

## Results log

Fill in the table after running the scripts. Scores depend on the exact Python,
NumPy, and source-code versions, so record the date and environment.

| Exercise | Command completed | Main result | Observation |
|---|---|---|---|
| 1. Metrics | [x] | Cosine and dot product agreed on the top result; Euclidean disagreed on some lower-ranked results. | Normalized vectors make cosine and dot product equivalent for ranking. |
| 2. Chunk size | [x] | Mean top-1 score: 0.3823 (50), 0.3481 (100), 0.3391 (200), 0.3132 (500). | Recall@1 was 100% for this small dataset, but larger chunks reduced the score. |
| 3. Matryoshka | [x] | Recall@1: 10% (50), 30% (100), 40% (200), 80% (500). | More dimensions preserved more retrieval signal in this simulation. |
| 4. Binary quantization | [x] | Mean top-10 overlap: 100%. | This small dataset did not expose a ranking change; use a larger corpus for a meaningful trade-off. |
| 5. Sentence chunking | [x] | Fixed score 0.3993; sentence score 0.3124. Both recall@1 values were 100%. | Sentence boundaries did not improve this synthetic corpus. |

### Environment

- Date: 2026-11-13
- Python version: 3.12.10
- NumPy version: 2.4.4
- Dataset: five sample documents in `exercise_utils.py`
- Embedding model: local `SimpleEmbedder` (TF-IDF-style baseline)
- Vector metric:

### Conclusions

1. Metric comparison: cosine and dot product produced the same ranking because the baseline vectors are normalized; Euclidean can rank zero-overlap vectors differently.
2. Best chunk size: 50 words produced the highest mean top-1 score in this experiment, while all tested sizes achieved 100% recall@1.
3. Matryoshka truncation behavior: recall improved as dimensions increased, but this is only a controlled simulation and not a trained Matryoshka model.
4. Binary top-10 overlap: 100% on this small corpus; the result should not be generalized to larger datasets.
5. Sentence-based chunking: it did not improve this synthetic corpus, showing why chunking choices should be measured on task-specific data.
