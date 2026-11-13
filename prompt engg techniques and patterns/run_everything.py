import os
import re
import time

from langchain_google_genai import ChatGoogleGenerativeAI
from prompt_template_lib import PROMPT_PATTERNS
from prompt_builder import build_prompt
import json
from test_suite_runner import run_test_suite

def run_pattern_catalog_demo():
    print("=" * 70)
    print("  PROMPT PATTERN CATALOG")
    print("=" * 70)

    for name, pattern in PROMPT_PATTERNS.items():
        print(f"\n  [{name}] {pattern['name']}")
        print(f"    {pattern['description']}")
        print(f"    Variables: {', '.join(pattern['variables'])}")
        print(f"    Recommended temp: {pattern['temperature']}")


def run_single_prompt_demo():
    print(f"\n{'=' * 70}")
    print("  SINGLE PROMPT BUILD + TEST")
    print("=" * 70)

    prompt = build_prompt("persona", {
        "role": "a database expert",
        "experience": "deep experience designing caching systems",
        "style": "concise and practical",
        "priority": "clear tradeoffs over generalities",
        "task": "When should I use Redis versus Memcached?",
    })

    print(f"\n  System message:\n    {prompt['system']}")
    print(f"\n  User message:\n    {prompt['user'][:200]}...")
    print(f"\n  Temperature: {prompt['temperature']}")
    print(f"\n  Pattern metadata: {json.dumps(prompt['metadata'], indent=4)}")

    model = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
    )

    for attempt in range(3):
        try:
            response = model.invoke(
                [
                    ("system", prompt["system"] + " Respond in plain-text lines without bullets or metadata."),
                    ("user", prompt["user"]),
                ]
            )
            break
        except Exception as error:
            message = str(error)
            is_transient = "503" in message or "UNAVAILABLE" in message
            if not is_transient or attempt == 2:
                raise
            time.sleep(2 ** attempt)

    print("\n  [Gemini real response]")
    content = response.content
    if isinstance(content, list):
        text = "\n".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    else:
        text = str(content)

    for line in text.splitlines():
        cleaned_line = re.sub(r"^\s*[-*•]\s*", "", line).strip()
        if cleaned_line:
            print(f"    {cleaned_line}")


if __name__ == "__main__":
    run_pattern_catalog_demo()
    run_single_prompt_demo()
    run_test_suite()