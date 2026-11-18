"""Exercise 3: Replay a conversation and visualize context allocations."""

import json
import sys
from pathlib import Path

LESSON_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LESSON_DIR / "build it"))

from context_budget_manager import ContextBudget
from conversation_history_compressor import ConversationManager
from dynamic_tool_selector import select_tools
from lost_in_the_middle_reorder import score_relevance
from token_counter import count_tokens


TRANSCRIPT = [
    ("user", "Where is JWT validation implemented?"),
    ("assistant", "The authentication module contains JWT validation."),
    ("user", "Why are tokens expiring early?"),
    ("assistant", "Check token timestamps and the server clock."),
    ("user", "Fix the expiry configuration."),
    ("assistant", "Update the JWT expiry setting and its tests."),
]


def replay(transcript):
    manager = ConversationManager(max_history_tokens=150)
    budget = ContextBudget(max_tokens=1000, generation_reserve=200)
    system_prompt = "You are an AI coding assistant."
    knowledge = [
        "Authentication uses Supabase Auth with JWT tokens.",
        "JWT expiry is configured in the authentication module.",
        "The project uses PostgreSQL 16.",
    ]

    print("Turn | component allocations")
    print("-" * 60)

    for index, (role, content) in enumerate(transcript):
        manager.add_turn(role, content)
        query = content if role == "user" else "continue"

        replay_budget = ContextBudget(max_tokens=1000, generation_reserve=200)
        replay_budget.allocate("system_prompt", system_prompt, max_tokens=200)

        tools, _ = select_tools(query, token_budget=300)
        replay_budget.allocate("tools", json.dumps(list(tools)), max_tokens=300)

        relevance = score_relevance(query, knowledge)
        relevant = [doc for doc, score in zip(knowledge, relevance) if score > 0]
        if relevant:
            replay_budget.allocate(
                "retrieved_context",
                "\n".join(relevant),
                max_tokens=300,
            )

        replay_budget.allocate(
            "conversation_history",
            manager.get_context(),
            max_tokens=400,
        )
        replay_budget.allocate("user_query", content, max_tokens=200)

        print(
            f"{index + 1:>4} | "
            + ", ".join(
                f"{name}={tokens}"
                for name, tokens in replay_budget.allocations.items()
            )
            + f" | history_live={len(manager.turns)} "
            f"history_summaries={len(manager.summaries)} "
            f"history_tokens={count_tokens(manager.get_context())}"
        )

        if manager.summaries:
            print("     | history compression started")


def main():
    replay(TRANSCRIPT)


if __name__ == "__main__":
    main()
