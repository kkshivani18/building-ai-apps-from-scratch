"""Compare the Build It context budget with tiktoken's real encoding.
"""

import json
import sys
from pathlib import Path
import tiktoken

LESSON_DIR = Path(__file__).resolve().parents[1]
BUILD_DIR = LESSON_DIR / "build it"
sys.path.insert(0, str(BUILD_DIR))

from dynamic_tool_selector import classify_intent, select_tools
from token_counter import count_tokens


ENCODING = tiktoken.get_encoding("cl100k_base")


def count_real_tokens(text):
    return len(ENCODING.encode(text))


def component_report(query):
    intents = classify_intent(query)
    tools, heuristic_tool_tokens = select_tools(query, token_budget=2000)
    tool_text = json.dumps(list(tools), ensure_ascii=False)

    system_prompt = (
        "You are a helpful AI assistant. You have access to tools for "
        "code editing, file management, web search, and data analysis. "
        "Use the appropriate tools for each task. Be concise and accurate."
    )
    retrieved_context = "\n".join(
        [
            "Authentication is handled by Supabase Auth with JWT tokens.",
            "API rate limits are set to 100 requests per minute per user.",
            "The project uses PostgreSQL 16 with pgvector.",
        ]
    )
    history = (
        "[Conversation Summary]\n"
        "Previous: user: discussed authentication | assistant: suggested JWT validation\n"
        "[Recent Conversation]\n"
        "user: Check the authentication module\n"
        "assistant: Review token expiry and validation"
    )

    components = {
        "system_prompt": system_prompt,
        "tools": tool_text,
        "retrieved_context": retrieved_context,
        "conversation_history": history,
        "user_query": query,
    }

    print("=" * 68)
    print("  Build It vs tiktoken: Context Budget Comparison")
    print("=" * 68)
    print(f"\nQuery: {query}")
    print(f"Intents: {intents}")
    print(f"Selected tools: {list(tools)}")
    print(f"\n{'Component':<24}{'Build It':>12}{'tiktoken':>12}{'Difference':>12}")
    print("-" * 60)

    heuristic_total = 0
    real_total = 0
    for name, content in components.items():
        heuristic = count_tokens(content)
        real = count_real_tokens(content)
        heuristic_total += heuristic
        real_total += real
        print(f"{name:<24}{heuristic:>12}{real:>12}{real - heuristic:>12}")

    print("-" * 60)
    print(f"{'Total':<24}{heuristic_total:>12}{real_total:>12}{real_total - heuristic_total:>12}")
    print(
        f"\nBuild tool estimate: {heuristic_tool_tokens} tokens"
        f"\ntiktoken tool estimate: {count_real_tokens(tool_text)} tokens"
    )


def main():
    component_report(
        "Fix the bug in the authentication module where JWT tokens expire too early"
    )


if __name__ == "__main__":
    main()
