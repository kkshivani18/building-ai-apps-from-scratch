"""Exercise 1: Detect context components that consume more than 30%."""

import sys
from pathlib import Path

LESSON_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LESSON_DIR / "build it"))

from context_budget_manager import ContextBudget


def detect_waste(budget):
    threshold = budget.max_tokens * 0.30
    findings = []

    for component, tokens in budget.allocations.items():
        if tokens <= threshold:
            continue

        if component in {"conversation_history", "history"}:
            strategy = "summarize old turns and keep only the most recent turns"
        elif component in {"tools", "tool_definitions"}:
            strategy = "prune tools by query intent"
        elif component in {"retrieved_context", "retrieved_documents"}:
            strategy = "rerank, filter, and deduplicate retrieved documents"
        elif component in {"system_prompt", "few_shot_examples"}:
            strategy = "move optional instructions or examples to dynamic context"
        else:
            strategy = "truncate low-value content or split it across requests"

        findings.append(
            {
                "component": component,
                "tokens": tokens,
                "percentage": round(tokens / budget.max_tokens * 100, 1),
                "strategy": strategy,
            }
        )

    return findings


def main():
    budget = ContextBudget(max_tokens=10000, generation_reserve=2000)
    budget.allocate("system_prompt", "You are an assistant. " * 60)
    budget.allocate("tools", "tool schema " * 100)
    budget.allocate("retrieved_context", "useful retrieved text " * 25)
    budget.allocate("conversation_history", "old conversation turn " * 20)
    budget.allocate("user_query", "Fix the authentication bug")

    print(budget.report())
    print("\nWaste detector findings:")
    findings = detect_waste(budget)
    if not findings:
        print("  No component exceeds 30% of the context window.")
        return

    for finding in findings:
        print(
            f"  {finding['component']}: {finding['tokens']} tokens "
            f"({finding['percentage']}%). Strategy: {finding['strategy']}"
        )


if __name__ == "__main__":
    main()
