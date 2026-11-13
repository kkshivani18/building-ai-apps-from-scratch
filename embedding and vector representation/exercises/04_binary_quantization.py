import numpy as np

from exercise_utils import DOCUMENTS, QUERIES, fitted_index


def hamming_distance(a, b):
    return int(np.count_nonzero(a != b))


def main():
    embedder, index = fitted_index()
    full_results = {}
    binary_vectors = [np.asarray(vector) >= 0 for vector in index.vectors]

    for query, expected_id in QUERIES:
        query_vector = embedder.embed(query)
        full = index.search(query_vector, top_k=10, metric="cosine")
        binary_order = sorted(
            range(len(index.vectors)),
            key=lambda i: hamming_distance(query_vector >= 0, binary_vectors[i]),
        )
        binary_top10 = binary_order[:10]
        full_ids = [result["metadata"]["document_id"] for result in full]
        overlap = len(set(full_ids) & set(binary_top10)) / len(full_ids)
        full_results[query] = (expected_id, overlap)
        print(
            f"query={query}\n"
            f"  expected_document={expected_id} "
            f"full_top1={full_ids[0]} "
            f"top10_overlap={overlap:.2%}"
        )

    mean_overlap = sum(value[1] for value in full_results.values()) / len(full_results)
    print(f"\nMean top-10 overlap: {mean_overlap:.2%}")


if __name__ == "__main__":
    main()
