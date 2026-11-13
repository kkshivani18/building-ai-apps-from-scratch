from exercise_utils import LONG_DOCUMENTS, LONG_QUERIES, chunked_index


def evaluate(sentence_based):
    embedder, index = chunked_index(
        LONG_DOCUMENTS,
        chunk_size=40,
        sentence_based=sentence_based,
    )
    scores = []
    hits = 0
    for query, expected_id in LONG_QUERIES:
        result = index.search(embedder.embed(query), top_k=1)[0]
        scores.append(result["score"])
        hits += result["metadata"]["document_id"] == expected_id
    return sum(scores) / len(scores), hits / len(LONG_QUERIES)


def main():
    for name, sentence_based in (("fixed", False), ("sentence", True)):
        score, recall = evaluate(sentence_based)
        print(f"{name}: mean_top1_score={score:.4f} recall@1={recall:.2%}")
    print("Compare both metrics; sentence boundaries are not guaranteed to win on every corpus.")


if __name__ == "__main__":
    main()
