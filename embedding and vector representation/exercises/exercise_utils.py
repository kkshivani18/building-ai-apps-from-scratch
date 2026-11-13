import sys
from pathlib import Path

BUILD_IT = Path(__file__).resolve().parents[1] / "build it"
if str(BUILD_IT) not in sys.path:
    sys.path.insert(0, str(BUILD_IT))

from embedding_from_scratch import SimpleEmbedder
from similarity_funcs import cosine_similarity, euclidean_distance
from text_chunking import chunk_by_sentences, chunk_text
from vector_index_with_brute_force_search import VectorIndex


DOCUMENTS = [
    "Python is a programming language used for building web and data applications.",
    "Embeddings represent text as numerical vectors that capture semantic meaning.",
    "Vector search retrieves documents by comparing the meaning of a query.",
    "Cosine similarity compares the angle between two embedding vectors.",
    "Chunking splits long documents into smaller pieces for better retrieval.",
    "A database stores structured records and supports reliable transactions.",
    "Caching can reduce latency by reusing results from expensive operations.",
    "Unit tests check that small pieces of code behave as expected.",
    "Monitoring collects metrics and logs so production failures are visible.",
    "Authentication verifies identity before an application grants access.",
    "Batch processing handles many records efficiently in scheduled jobs.",
    "Indexes speed up database lookups by organizing searchable fields.",
]

QUERIES = [
    ("What language is used to build applications?", 0),
    ("How do vectors represent meaning?", 1),
    ("How does semantic document retrieval work?", 2),
    ("How can I compare embedding vectors?", 3),
    ("Why split documents into smaller parts?", 4),
]

LONG_DOCUMENTS = [
    " ".join(
        [
            "Python is a programming language used for building applications.",
            "It supports web development, data analysis, automation, and testing.",
            "Developers use functions, classes, modules, and packages to organize code.",
            "Readable syntax helps teams maintain Python projects over time.",
        ]
        * 12
    ),
    " ".join(
        [
            "Embeddings represent text as numerical vectors with semantic information.",
            "A model maps related passages to nearby points in vector space.",
            "Applications use embeddings for search, recommendations, and clustering.",
            "The same embedding configuration should be used consistently.",
        ]
        * 12
    ),
    " ".join(
        [
            "Vector search compares a query vector with stored document vectors.",
            "Cosine similarity measures the angle between normalized vectors.",
            "An index ranks candidates and returns the most relevant chunks.",
            "Metadata filters can restrict results to a tenant or source.",
        ]
        * 12
    ),
]

LONG_QUERIES = [
    ("Which language is useful for automation and web development?", 0),
    ("How do vectors help applications find related passages?", 1),
    ("How does an index rank relevant chunks?", 2),
]


def fitted_index(documents=DOCUMENTS):
    embedder = SimpleEmbedder()
    embedder.fit(documents)
    index = VectorIndex()
    for i, document in enumerate(documents):
        index.add(embedder.embed(document), document, {"document_id": i})
    return embedder, index


def top_document(embedder, index, query, metric="cosine"):
    result = index.search(embedder.embed(query), top_k=1, metric=metric)[0]
    return result["metadata"]["document_id"], result["score"]


def evaluate_recall(embedder, index, queries=QUERIES, metric="cosine", top_k=1):
    hits = 0
    for query, expected_id in queries:
        results = index.search(embedder.embed(query), top_k=top_k, metric=metric)
        ids = [result["metadata"]["document_id"] for result in results]
        hits += expected_id in ids
    return hits / len(queries)


def chunked_index(documents, chunk_size, sentence_based=False):
    embedder = SimpleEmbedder()
    chunks = []
    metadata = []
    for document_id, document in enumerate(documents):
        if sentence_based:
            document_chunks = chunk_by_sentences(document, chunk_size)
        else:
            document_chunks = chunk_text(document, chunk_size, overlap=0)
        chunks.extend(document_chunks)
        metadata.extend({"document_id": document_id} for _ in document_chunks)

    embedder.fit(chunks)
    index = VectorIndex()
    for chunk, meta in zip(chunks, metadata):
        index.add(embedder.embed(chunk), chunk, meta)
    return embedder, index


def print_result(result):
    text = result["text"].replace("\n", " ")[:90]
    print(
        f"score={result['score']:.4f} "
        f"document={result['metadata'].get('document_id')} "
        f"text={text}"
    )
