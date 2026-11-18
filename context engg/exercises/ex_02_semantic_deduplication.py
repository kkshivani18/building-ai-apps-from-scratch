"""Exercise 2: Remove highly overlapping retrieved documents."""

import sys
from pathlib import Path

LESSON_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LESSON_DIR / "build it"))

from token_counter import count_tokens


def word_overlap(left, right):
    left_words = set(left.lower().split())
    right_words = set(right.lower().split())
    if not left_words or not right_words:
        return 0.0
    return len(left_words & right_words) / len(left_words | right_words)


def deduplicate(documents, scores, threshold=0.80):
    ranked = sorted(
        zip(scores, documents),
        key=lambda pair: pair[0],
        reverse=True,
    )
    kept = []

    for score, document in ranked:
        if any(word_overlap(document, existing["document"]) >= threshold for existing in kept):
            continue
        kept.append({"document": document, "score": score})

    return kept


def main():
    documents = [
        "Authentication uses Supabase Auth with JWT tokens.",
        "The application authenticates users using Supabase Auth and JWT.",
        "PostgreSQL 16 stores vector embeddings with pgvector.",
        "The frontend uses Next.js 15 and the App Router.",
    ]
    scores = [0.95, 0.90, 0.82, 0.60]

    before = sum(count_tokens(document) for document in documents)
    kept = deduplicate(documents, scores)
    after = sum(count_tokens(item["document"]) for item in kept)

    print("Deduplicated retrieved context:")
    for item in kept:
        print(f"  [{item['score']:.2f}] {item['document']}")
    print(f"\nBefore: {before} heuristic tokens")
    print(f"After:  {after} heuristic tokens")
    print(f"Recovered: {before - after} heuristic tokens")


if __name__ == "__main__":
    main()
