import os
import time

from langchain_google_genai import ChatGoogleGenerativeAI

from prompt_comparison_and_score import score_response


SAMPLE_COUNT = 5
ITERATION_COUNT = 3

INITIAL_PROMPT = """Explain Redis and Memcached for a beginner programmer."""

CRITERIA = {
    "max_words": 100,
    "required_keywords": ["Redis", "Memcached", "cache"],
    "forbidden_phrases": ["it depends", "in conclusion"],
    "expected_format": "numbered_list",
}


def extract_text(content):
    if isinstance(content, list):
        return "\n".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return str(content)


def invoke_with_retry(model, messages):
    for attempt in range(3):
        try:
            return extract_text(model.invoke(messages).content)
        except Exception as error:
            message = str(error)
            is_transient = any(
                code in message for code in ("429", "500", "503", "UNAVAILABLE")
            )
            if not is_transient or attempt == 2:
                raise
            time.sleep(2 ** attempt)


def run_samples(model, prompt):
    responses = []
    scores = []

    for sample_number in range(1, SAMPLE_COUNT + 1):
        response = invoke_with_retry(
            model,
            [
                (
                    "system",
                    "Follow the user's instructions exactly. Return only the requested answer.",
                ),
                ("user", prompt),
            ],
        )
        score = score_response(response, CRITERIA)
        responses.append(response)
        scores.append(score)
        print(
            f"    Sample {sample_number}: "
            f"score={score['composite_score']:.3f}, "
            f"words={score['word_count']}"
        )

    return responses, scores


def average_scores(scores):
    metric_names = (
        "composite_score",
        "length_compliant",
        "keyword_coverage",
        "no_violations",
        "format_valid",
    )
    averages = {}
    for metric in metric_names:
        values = [score[metric] for score in scores if metric in score]
        if values:
            averages[metric] = sum(values) / len(values)
    return averages


def find_weakest_criterion(averages):
    candidates = {
        "length": averages.get("length_compliant", 1.0),
        "keywords": averages.get("keyword_coverage", 1.0),
        "forbidden phrases": averages.get("no_violations", 1.0),
        "format": averages.get("format_valid", 1.0),
    }
    return min(candidates, key=candidates.get), candidates


def rewrite_prompt(model, prompt, weakest_criterion, averages):
    rewrite_request = f"""Rewrite the prompt below to improve its weakest criterion: {weakest_criterion}.

Current measured scores:
{averages}

Requirements for the rewrite:
- Preserve the original task and meaning.
- Add only constraints that directly improve {weakest_criterion}.
- Keep the prompt concise and practical.
- Return only the rewritten prompt, with no explanation or markdown fences.

Current prompt:
{prompt}
"""
    return invoke_with_retry(
        model,
        [
            (
                "system",
                "You are a prompt engineer. Improve prompts without changing their intent.",
            ),
            ("user", rewrite_request),
        ],
    ).strip()


def run_optimizer():
    model_name = os.getenv("GEMINI_OPTIMIZER_MODEL", os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"))
    model = ChatGoogleGenerativeAI(model=model_name, temperature=0.7)
    prompt = INITIAL_PROMPT
    iteration_reports = []

    print(f"Prompt optimizer using Gemini model: {model_name}")
    print(f"Samples per iteration: {SAMPLE_COUNT}")

    for iteration in range(1, ITERATION_COUNT + 1):
        print(f"\nITERATION {iteration}")
        print(f"Prompt: {prompt}")
        _, scores = run_samples(model, prompt)
        averages = average_scores(scores)
        weakest, criterion_values = find_weakest_criterion(averages)
        print(f"Average scores: {averages}")
        print(f"Weakest criterion: {weakest} ({criterion_values[weakest]:.3f})")

        iteration_reports.append({
            "iteration": iteration,
            "prompt": prompt,
            "averages": averages,
            "weakest_criterion": weakest,
        })

        if iteration < ITERATION_COUNT:
            prompt = rewrite_prompt(model, prompt, weakest, averages)
            print(f"Rewritten prompt: {prompt}")

    print("\nIMPROVEMENT SUMMARY")
    first_score = iteration_reports[0]["averages"].get("composite_score", 0)
    last_score = iteration_reports[-1]["averages"].get("composite_score", 0)
    change = last_score - first_score
    print(f"Initial average score: {first_score:.3f}")
    print(f"Final average score:   {last_score:.3f}")
    print(f"Change after {ITERATION_COUNT} iterations: {change:+.3f}")
    if change > 0:
        print("Result: scores improved.")
    elif change < 0:
        print("Result: scores decreased; inspect the rewritten prompts.")
    else:
        print("Result: scores did not change.")

    return iteration_reports


if __name__ == "__main__":
    run_optimizer()
