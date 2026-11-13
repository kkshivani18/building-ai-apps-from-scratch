import difflib
import re

from multi_model_testing_harness import run_prompt_test
from prompt_comparison_and_score import score_response


OLD_PROMPT = """Explain Redis and Memcached."""

NEW_PROMPT = """You are a database caching expert.

Compare Redis and Memcached for a beginner programmer.

Use exactly 4 numbered points. Cover data structures, persistence, performance,
and a practical recommendation. Keep the answer under 120 words. Avoid marketing
language and define technical terms briefly."""

CRITERIA = {
    "max_words": 120,
    "required_keywords": ["Redis", "Memcached", "persistence", "performance"],
    "forbidden_phrases": ["in conclusion", "it depends"],
    "expected_format": "numbered_list",
}


def changed_lines(old_prompt, new_prompt):
    return list(difflib.unified_diff(
        old_prompt.splitlines(),
        new_prompt.splitlines(),
        fromfile="old_prompt",
        tofile="new_prompt",
        lineterm="",
    ))


def classify_changes(old_prompt, new_prompt):
    old_lower = old_prompt.lower()
    new_lower = new_prompt.lower()
    changes = {}

    role_patterns = ("you are", "role", "expert", "specialist")
    constraint_patterns = (
        "must", "exactly", "under ", "do not", "avoid", "only", "include",
    )
    example_patterns = ("example", "input:", "output:", "for instance")
    format_patterns = (
        "numbered", "bullet", "json", "table", "paragraph", "sentences",
    )

    def count_matches(text, patterns):
        return sum(text.count(pattern) for pattern in patterns)

    old_role = count_matches(old_lower, role_patterns)
    new_role = count_matches(new_lower, role_patterns)
    if old_role != new_role or ("you are" in old_lower) != ("you are" in new_lower):
        changes["role"] = "added or made more specific" if new_role > old_role else "removed or made less specific"

    old_constraints = count_matches(old_lower, constraint_patterns)
    new_constraints = count_matches(new_lower, constraint_patterns)
    if old_constraints != new_constraints:
        changes["constraints"] = "added" if new_constraints > old_constraints else "removed"

    old_examples = count_matches(old_lower, example_patterns)
    new_examples = count_matches(new_lower, example_patterns)
    if old_examples != new_examples:
        changes["examples"] = "added" if new_examples > old_examples else "removed"

    old_formats = count_matches(old_lower, format_patterns)
    new_formats = count_matches(new_lower, format_patterns)
    if old_formats != new_formats:
        changes["format"] = "added or made more specific" if new_formats > old_formats else "removed"

    if not changes:
        changes["content"] = "wording changed without a detected structural change"
    return changes


def predict_quality(changes):
    reasons = []
    points = 0

    if changes.get("role") == "added or made more specific":
        points += 1
        reasons.append("a more specific role should focus the response")
    if changes.get("constraints") == "added":
        points += 1
        reasons.append("explicit constraints reduce ambiguity")
    if changes.get("format") == "added or made more specific":
        points += 1
        reasons.append("a specified format makes compliance measurable")
    if changes.get("examples") == "added":
        points += 1
        reasons.append("examples can anchor the expected behavior")
    if changes.get("examples") == "removed":
        points -= 1
        reasons.append("removing examples may reduce consistency")
    if changes.get("constraints") == "removed":
        points -= 1
        reasons.append("removing constraints increases ambiguity")

    prediction = "improve" if points > 0 else "degrade" if points < 0 else "remain similar"
    return prediction, reasons


def make_model_prompt(prompt_text):
    return {
        "system": "Follow the user's instructions exactly. Return only the requested answer.",
        "user": prompt_text,
        "temperature": 0.7,
    }


def run_prompt_diff():
    changes = classify_changes(OLD_PROMPT, NEW_PROMPT)
    prediction, reasons = predict_quality(changes)

    print("PROMPT DIFF")
    for line in changed_lines(OLD_PROMPT, NEW_PROMPT):
        print(line)

    print("\nCHANGES DETECTED")
    for category, description in changes.items():
        print(f"- {category}: {description}")

    print(f"\nPREDICTION: quality will {prediction}")
    for reason in reasons:
        print(f"- {reason}")

    results = run_prompt_test(
        make_model_prompt(OLD_PROMPT),
        models=["gemini"],
    )
    old_response = results["gemini"]["response"]
    old_score = score_response(old_response, CRITERIA)

    results = run_prompt_test(
        make_model_prompt(NEW_PROMPT),
        models=["gemini"],
    )
    new_response = results["gemini"]["response"]
    new_score = score_response(new_response, CRITERIA)

    print("\nACTUAL GEMINI OUTPUTS")
    print("\nOld prompt response:\n" + old_response)
    print("\nNew prompt response:\n" + new_response)

    print("\nMEASURED RESULTS")
    print(f"Old score: {old_score['composite_score']:.3f}")
    print(f"New score: {new_score['composite_score']:.3f}")
    print(f"Old words: {old_score['word_count']}")
    print(f"New words: {new_score['word_count']}")
    print(f"Old keyword coverage: {old_score.get('keyword_coverage', 0):.3f}")
    print(f"New keyword coverage: {new_score.get('keyword_coverage', 0):.3f}")
    print(f"Old format valid: {old_score.get('format_valid', 'n/a')}")
    print(f"New format valid: {new_score.get('format_valid', 'n/a')}")

    actual_change = new_score["composite_score"] - old_score["composite_score"]
    actual_result = "improved" if actual_change > 0 else "degraded" if actual_change < 0 else "did not change"
    print(f"Actual result: quality {actual_result} ({actual_change:+.3f})")
    print(f"Prediction matched: {prediction == ('improve' if actual_change > 0 else 'degrade' if actual_change < 0 else 'remain similar')}")


if __name__ == "__main__":
    run_prompt_diff()
