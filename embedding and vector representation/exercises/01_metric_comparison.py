from exercise_utils import DOCUMENTS, QUERIES, fitted_index, print_result


def main():
    embedder, index = fitted_index()
    for query, _ in QUERIES:
        print(f"\nQUERY: {query}")
        for metric in ("cosine", "dot", "euclidean"):
            print(f"  {metric}:")
            for result in index.search(embedder.embed(query), top_k=3, metric=metric):
                print("   ", end="")
                print_result(result)


if __name__ == "__main__":
    main()
