import csv
from pathlib import Path

from exercise_utils import LONG_DOCUMENTS, LONG_QUERIES, chunked_index


def main():
    rows = []
    for chunk_size in (50, 100, 200, 500):
        embedder, index = chunked_index(LONG_DOCUMENTS, chunk_size)
        scores = []
        hits = 0
        for query, expected_id in LONG_QUERIES:
            result = index.search(embedder.embed(query), top_k=1)[0]
            scores.append(result["score"])
            hits += result["metadata"]["document_id"] == expected_id
        rows.append(
            {
                "chunk_size": chunk_size,
                "mean_top1_score": sum(scores) / len(scores),
                "recall_at_1": hits / len(LONG_QUERIES),
            }
        )

    output = Path(__file__).with_name("chunk_size_results.csv")
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)

    for row in rows:
        print(
            f"chunk_size={row['chunk_size']} "
            f"mean_top1_score={row['mean_top1_score']:.4f} "
            f"recall@1={row['recall_at_1']:.2%}"
        )
    print(f"\nSaved results to {output}")
    print("Plot chunk_size against mean_top1_score and recall_at_1 from the CSV.")


if __name__ == "__main__":
    main()
