"""Exercise 4: Rank tools by relevance and fill a tool token budget."""

import sys
from pathlib import Path

LESSON_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LESSON_DIR / "build it"))

from dynamic_tool_selector import TOOL_REGISTRY


def score_tool(query, tool):
    query_words = set(query.lower().split())
    description_words = set(tool["description"].lower().split())
    category_words = set(tool["categories"])
    overlap = len(query_words & (description_words | category_words))
    return overlap


def select_priority_tools(query, token_budget):
    ranked = sorted(
        (
            (score_tool(query, tool), name, tool)
            for name, tool in TOOL_REGISTRY.items()
        ),
        key=lambda result: (result[0], result[2]["tokens"]),
        reverse=True,
    )

    selected = {}
    used = 0
    for relevance, name, tool in ranked:
        if used + tool["tokens"] <= token_budget:
            selected[name] = {
                "relevance": relevance,
                "tokens": tool["tokens"],
            }
            used += tool["tokens"]
    return selected, used


def main():
    query = "Fix the database authentication bug and show query performance stats"

    for budget in (5, 10, 20, 50):
        print(f"\nTool count comparison: limit={budget}")
        candidates = sorted(
            TOOL_REGISTRY,
            key=lambda name: score_tool(query, TOOL_REGISTRY[name]),
            reverse=True,
        )[:budget]

        print("  Ranked candidates:", ", ".join(candidates))

        for name in candidates:
            tool = TOOL_REGISTRY[name]
            print(
                f"  {name:<24} relevance={score_tool(query, tool):>2} "
                f"tokens={tool['tokens']}"
            )

    selected, used = select_priority_tools(query, token_budget=500)
    print("\nPriority tools within a 500-token tool budget:")
    for name, details in selected.items():
        print(f"  {name}: relevance={details['relevance']}, tokens={details['tokens']}")
    print(f"  Used: {used} tokens")


if __name__ == "__main__":
    main()
