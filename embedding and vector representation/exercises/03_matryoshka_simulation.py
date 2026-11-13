import numpy as np

from exercise_utils import evaluate_recall
from embedding_from_scratch import SimpleEmbedder
from vector_index_with_brute_force_search import VectorIndex


class FixedDimensionSimpleEmbedder(SimpleEmbedder):
    def __init__(self, dimensions=500):
        super().__init__()
        self.dimensions = dimensions
        self.dimension_order = None

    def fit(self, documents):
        super().fit(documents)
        order = np.arange(len(self.vocab))
        np.random.default_rng(42).shuffle(order)
        self.dimension_order = order[: self.dimensions]

    def embed(self, text):
        vector = super().embed(text)
        if self.dimension_order is not None:
            vector = vector[self.dimension_order]
        if len(vector) < self.dimensions:
            return np.pad(vector, (0, self.dimensions - len(vector)))
        return vector[: self.dimensions]


def evaluate_dimension(dimension):
    documents = [
        " ".join([f"topic_{i:02d}", *(f"token_{i:03d}_{j:03d}" for j in range(60))])
        for i in range(10)
    ]
    queries = [(f"topic_{i:02d}", i) for i in range(10)]
    embedder = FixedDimensionSimpleEmbedder()
    embedder.fit(documents)
    index = VectorIndex()
    for document_id, document in enumerate(documents):
        index.add(embedder.embed(document), document, {"document_id": document_id})

    full_vectors = [embedder.embed(document) for document in documents]
    truncated = FixedDimensionSimpleEmbedder()
    truncated.fit(documents)
    truncated.dimensions = dimension
    truncated.dimension_order = embedder.dimension_order
    index = VectorIndex()
    for document_id, vector in enumerate(full_vectors):
        index.add(vector[:dimension], documents[document_id], {"document_id": document_id})
    return evaluate_recall(truncated, index, queries=queries, top_k=1)


def main():
    for dimension in (50, 100, 200, 500):
        print(f"dimensions={dimension} recall@1={evaluate_dimension(dimension):.2%}")


if __name__ == "__main__":
    main()
