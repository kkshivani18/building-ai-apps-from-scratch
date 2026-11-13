from vector_index_with_brute_force_search import VectorIndex
# from embedding_from_scratch import SimpleEmbedder
from gemini_embedder import GeminiEmbedder
from text_chunking import chunk_text

class SemanticSearchEngine:
    def __init__(self, chunk_size=200, overlap=50):
        self.embedder = GeminiEmbedder()
        self.index = VectorIndex()
        self.chunk_size = chunk_size
        self.overlap = overlap

    def index_documents(self, documents, source_names=None):
        all_chunks = []
        all_sources = []
        for i, doc in enumerate(documents):
            chunks = chunk_text(doc, self.chunk_size, self.overlap)
            all_chunks.extend(chunks)
            name = source_names[i] if source_names else f"doc_{i}"
            all_sources.extend([name] * len(chunks))
        # self.embedder.fit(all_chunks)
        
        for chunk, source in zip(all_chunks, all_sources):
            vec = self.embedder.embed(chunk)
            self.index.add(vec, chunk, {"source": source})
        return len(all_chunks)

    def search(self, query, top_k=5, metric="cosine"):
        query_vec = self.embedder.embed(query)
        return self.index.search(query_vec, top_k, metric)

    def search_with_scores(self, query, top_k=5):
        results = self.search(query, top_k)
        return [
            {
                "text": r["text"][:200],
                "source": r["metadata"].get("source", "unknown"),
                "score": round(r["score"], 4)
            }
            for r in results
        ]

    def index_documents(self, documents, source_names=None):
        all_chunks = []
        all_sources = []

        for i, doc in enumerate(documents):
            chunks = chunk_text(doc, self.chunk_size, self.overlap)
            all_chunks.extend(chunks)

            name = source_names[i] if source_names else f"doc_{i}"
            all_sources.extend([name] * len(chunks))

        vectors = self.embedder.embed_documents(all_chunks)

        for vector, chunk, source in zip(vectors, all_chunks, all_sources):
            self.index.add(vector, chunk, {"source": source})

        return len(all_chunks)


    def search(self, query, top_k=5, metric="cosine"):
        query_vector = self.embedder.embed_query(query)
        return self.index.search(query_vector, top_k, metric)