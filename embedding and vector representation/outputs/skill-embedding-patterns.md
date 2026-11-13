# Skill: Production Embedding Patterns

## Purpose

Help an agent design, implement, evaluate, and operate embedding-based
retrieval systems without mixing incompatible vectors or hiding retrieval
failures.

## When to use

Use this skill for semantic search, retrieval-augmented generation,
recommendations, document similarity, clustering, or vector-index design.

## Required inputs

Collect or infer:

- Document and query examples
- Languages and domain
- Corpus size and growth
- Latency, freshness, and cost targets
- Privacy and provider constraints
- Vector-store or database choice
- Required metadata filters

If a choice materially affects quality, cost, or privacy, ask for the missing
requirement instead of silently assuming it.

## Core workflow

1. **Define the retrieval task**
   - Separate search, recommendation, clustering, and classification.
   - Create representative queries and label relevant documents.

2. **Choose an embedding model**
   - Compare hosted and local models against the requirements.
   - Verify current model names, dimensions, limits, pricing, and availability.
   - Use one model consistently for the indexed documents and queries.

3. **Prepare documents**
   - Preserve useful metadata such as source, title, section, tenant, and
     timestamp.
   - Start with sentence-aware or recursive chunks.
   - Begin around 256-512 tokens with modest overlap, then measure quality.

4. **Embed correctly**
   - Use the provider's document task for stored chunks.
   - Use the provider's query task for user queries when supported.
   - Batch document requests, handle rate limits explicitly, and record the
     model, dimension, and preprocessing version with each index.
   - Never mix vectors from different models or incompatible dimensions.

5. **Retrieve**
   - Use cosine similarity for normalized embeddings unless the model
     documentation recommends another metric.
   - Use brute force only for small prototypes.
   - Use an ANN index such as HNSW or a vector database as the corpus grows.
   - Apply metadata filters before or during vector search where possible.

6. **Evaluate**
   - Test semantic paraphrases, exact matches, long queries, no-result cases,
     multilingual input, and adversarial or irrelevant queries.
   - Measure recall@k, precision@k, MRR, latency, and embedding/API failure
     rates.
   - Compare against a keyword baseline before changing models.
   - Tune chunking, `top_k`, filters, and reranking independently.

7. **Rerank and answer**
   - Retrieve a wider candidate set with a bi-encoder.
   - Rerank only the candidates with a cross-encoder or LLM when improved
     relevance justifies the latency and cost.
   - Keep retrieval separate from answer generation so each stage can be
     evaluated independently.

8. **Operate safely**
   - Keep API keys in environment variables or a secret manager, never in
     source code or terminal screenshots.
   - Add timeouts, bounded retries, rate-limit handling, and explicit error
     reporting.
   - Log model/version, dimension, query latency, candidate counts, and
     retrieval scores without logging sensitive document content by default.
   - Version the index and support rebuilding and rollback.

## Provider adapter contract

Implement a provider adapter with these separate operations:

```python
class Embedder:
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        ...

    def embed_query(self, text: str) -> list[float]:
        ...
```

The search engine should call `embed_documents` while indexing and
`embed_query` while searching. Do not use a single generic method when the
provider has different document and query task types.

## Gemini example

With the Google GenAI SDK, configure the document and query task types
separately:

```python
document_vectors = client.models.embed_content(
    model="gemini-embedding-001",
    contents=chunks,
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT",
        output_dimensionality=768,
    ),
)

query_vector = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query,
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_QUERY",
        output_dimensionality=768,
    ),
)
```

Do not hard-code credentials. Read `GEMINI_API_KEY` from the environment and
rotate any key that has been exposed.

## Definition of done

- Document and query embeddings are generated with compatible configuration.
- Search returns relevant chunks with source metadata and scores.
- Similarity metric and dimensions are documented.
- A small relevance evaluation exists.
- API failures are visible and bounded.
- Secrets are externalized.
- The index can be rebuilt after a model, chunking, or dimension change.
