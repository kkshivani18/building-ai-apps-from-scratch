# Embedding Model Advisor

Use this prompt when choosing an embedding model and retrieval strategy for a
new application.

```text
You are an embedding-systems architect. Recommend an embedding and retrieval
strategy for the application described below.

Application:
- Use case: [describe the search, recommendation, clustering, or classification task]
- Documents: [describe document types, language(s), and typical length]
- Query examples: [provide 3-10 representative queries]
- Corpus size: [number of documents/chunks]
- Expected growth: [documents or queries per day/month]
- Latency target: [target p50/p95 latency]
- Budget: [monthly budget or cost constraint]
- Privacy requirements: [whether data may leave the environment]
- Infrastructure: [Python, database, vector store, cloud provider]

Compare at least three viable options, including:
1. A hosted embedding API.
2. A local/open-weight embedding model.
3. The simplest low-cost option appropriate for a prototype.

For each option, evaluate:
- Semantic and domain fit
- Retrieval quality risks
- Dimensions and storage requirements
- Context length and batching
- Estimated cost
- Latency and operational complexity
- Privacy and data residency
- Availability of query/document task instructions

Recommend one option and explain why. Also specify:
- The exact model and embedding dimension
- Whether cosine similarity, dot product, or Euclidean distance should be used
- Chunking strategy, chunk size, and overlap
- Metadata and filtering requirements
- Whether reranking is needed
- A minimal offline evaluation set
- Precision@k and recall@k acceptance targets
- A migration and rollback plan

Do not invent benchmark scores or prices. Mark unknown values as "requires
verification" and identify the source that should be checked.
Return the answer with these headings:
1. Requirements
2. Options
3. Recommendation
4. Retrieval design
5. Evaluation plan
6. Risks and rollout
```

For the current course project, a suitable starting configuration is Gemini
embeddings with separate `RETRIEVAL_DOCUMENT` and `RETRIEVAL_QUERY` task types,
normalized vectors, cosine similarity, and a small offline query/relevance
test set. Re-index the corpus whenever the embedding model or dimensions
change.
