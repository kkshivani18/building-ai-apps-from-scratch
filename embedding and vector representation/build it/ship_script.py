from semantic_search_engine import SemanticSearchEngine

documents = [
    "Python is a programming language used for building applications.",
    "Embeddings represent text as numerical vectors.",
    "Vector search finds semantically similar documents.",
]

engine = SemanticSearchEngine()
engine.index_documents(documents, ["python.txt", "embeddings.txt", "search.txt"])

results = engine.search_with_scores(
    "How does semantic vector search work?",
    top_k=2,
)

for result in results:
    print(result)