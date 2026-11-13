from gemini_embedder import GeminiEmbedder
all_chunks = [
    "Python is a programming language.",
    "Embeddings represent text as numerical vectors.",
    "Vector search finds semantically similar text.",
]
query = "How does vector search work?"

embedder = GeminiEmbedder()
vectors = embedder.embed_documents(all_chunks)
query_vec = embedder.embed_query(query)

print("Number of document vectors:", len(vectors))
print("Vector dimensions:", len(vectors[0]))
print("Query vector dimensions:", len(query_vec))