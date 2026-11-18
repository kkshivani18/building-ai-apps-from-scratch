"""Exercise 5: Compare truncation, summarization, and key-sentence extraction."""

import sys
from pathlib import Path

LESSON_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LESSON_DIR / "build it"))

from token_counter import count_tokens


def truncate(text, max_tokens):
    words = text.split()
    target_words = max(1, int(max_tokens / 1.3))
    return " ".join(words[:target_words])


def summarize(text):
    words = text.split()
    if len(words) <= 12:
        return text
    keywords = {
        "jwt", "authentication", "postgresql", "expiry", "token",
        "database", "vector", "cache", "deploy", "test",
    }
    selected = [word for word in words if word.lower().strip(".,") in keywords]
    if not selected:
        selected = words[:4] + words[-4:]
    return " ".join(dict.fromkeys(selected))


def extract_key_sentences(text, query, max_sentences=2):
    sentences = [sentence.strip() for sentence in text.replace("\n", " ").split(".") if sentence.strip()]
    query_words = set(query.lower().split())

    scored = []
    for sentence in sentences:
        sentence_words = set(sentence.lower().split())
        overlap = len(query_words & sentence_words)
        scored.append((overlap, sentence))

    scored.sort(reverse=True)
    return ". ".join(sentence for _, sentence in scored[:max_sentences]) + "."


def benchmark(documents, queries, max_tokens=20):
    for index, (document, query) in enumerate(zip(documents, queries)):
        original_tokens = count_tokens(document)
        strategies = {
            "truncation": truncate(document, max_tokens),
            "summarization": summarize(document),
            "key-sentence": extract_key_sentences(document, query),
        }

        print(f"\nDocument {index + 1}:")
        print(f"  Original: {original_tokens} heuristic tokens")
        for strategy, compressed in strategies.items():
            compressed_tokens = count_tokens(compressed)
            ratio = 1 - compressed_tokens / original_tokens if original_tokens else 0
            query_words = set(query.lower().split())
            answer_words = set(compressed.lower().split())
            retention = len(query_words & answer_words) / len(query_words) if query_words else 0
            print(
                f"  {strategy:<13} retained={compressed_tokens:>3} tokens "
                f"compression={ratio:.1%} query_word_overlap={retention:.1%}"
            )


def main():
    documents = [
        "JWT authentication expires tokens too early. The server clock is valid.",
        "PostgreSQL stores embeddings in a vector column. pgvector supports similarity search.",
        "The deployment pipeline runs tests before Docker image creation.",
        "Conversation history becomes large after many turns. Summarize old turns.",
    ] * 5
    queries = [
        "How does JWT authentication configure expiry?",
        "How are PostgreSQL embeddings stored?",
        "What runs before deployment?",
        "How should conversation history be compressed?",
    ] * 5
    benchmark(documents, queries)


if __name__ == "__main__":
    main()
