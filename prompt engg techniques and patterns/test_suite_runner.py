from prompt_builder import build_prompt
from prompt_comparison_and_score import compare_models
from multi_model_testing_harness import run_prompt_test

TEST_SUITE = [
    {
        "name": "Persona: Technical Writer",
        "pattern": "persona",
        "variables": {
            "role": "a senior technical writer at Stripe",
            "experience": "10 years of API documentation experience",
            "style": "precise, concise, and example-driven",
            "priority": "clarity over comprehensiveness",
            "task": "Explain what an API rate limit is and why it exists.",
        },
        "criteria": {
            "max_words": 200,
            "required_keywords": ["rate limit", "API", "requests"],
            "forbidden_phrases": ["in conclusion", "it is important to note"],
        },
    },
    {
        "name": "Few-Shot: Sentiment Analysis",
        "pattern": "few_shot",
        "variables": {
            "examples": (
                'Input: "The food was amazing but service was slow"\n'
                'Output: {"sentiment": "mixed", "food": "positive", "service": "negative"}\n\n'
                'Input: "Terrible experience, never coming back"\n'
                'Output: {"sentiment": "negative", "food": null, "service": "negative"}'
            ),
            "input": "Great ambiance and the pasta was perfect, though a bit pricey",
        },
        "criteria": {
            "expected_format": "json",
            "required_keywords": ["sentiment"],
        },
    },
    {
        "name": "Chain-of-Thought: Math Problem",
        "pattern": "chain_of_thought",
        "variables": {
            "problem": "A store offers 20% off all items. An item originally costs $85. There is also a $10 coupon. Which saves more: applying the discount first then the coupon, or the coupon first then the discount?",
        },
        "criteria": {
            "required_keywords": ["discount", "coupon", "$"],
            "max_words": 300,
        },
    },
    {
        "name": "Template Fill: Resume Extraction",
        "pattern": "template_fill",
        "variables": {
            "text": "John Smith is a software engineer at Google with 5 years of experience. He graduated from MIT with a BS in Computer Science in 2019. He specializes in distributed systems and Go programming.",
            "template_structure": "Name: [full name]\nCompany: [current employer]\nYears of Experience: [number]\nEducation: [degree, school, year]\nSpecialties: [comma-separated list]",
        },
        "criteria": {
            "required_keywords": ["John Smith", "Google", "MIT"],
        },
    },
    {
        "name": "Guardrail: Scoped Assistant",
        "pattern": "guardrail",
        "variables": {
            "role": "Python programming tutor",
            "domain": "Python programming",
            "additional_rules": "Do not write complete solutions. Guide the student with hints.",
            "question": "How do I sort a list of dictionaries by a specific key?",
        },
        "criteria": {
            "required_keywords": ["sorted", "key", "lambda"],
            "forbidden_phrases": ["here is the complete solution"],
        },
    },
    {
        "name": "Meta-Prompt: Support Classifier",
        "pattern": "meta_prompt",
        "variables": {
            "objective": "classify customer support requests by urgency",
            "metric": "consistent JSON output",
            "model": "Gemini",
        },
        "criteria": {
            "required_keywords": ["role", "constraints", "output format"],
            "max_words": 250,
        },
    },
    {
        "name": "Decomposition: Project Plan",
        "pattern": "decomposition",
        "variables": {
            "problem": "Plan the steps for building a small Python web API with automated tests.",
        },
        "criteria": {
            "required_keywords": ["sub-problem", "verify", "tests"],
            "max_words": 300,
        },
    },
    {
        "name": "Critique: Technical Explanation",
        "pattern": "critique",
        "variables": {
            "task": "Explain database indexing to a junior Python developer.",
        },
        "criteria": {
            "required_keywords": ["accuracy", "clarity", "index"],
            "max_words": 350,
        },
    },
    {
        "name": "Audience Adaptation: Caching",
        "pattern": "audience_adapt",
        "variables": {
            "concept": "database caching",
            "audience": "a beginner programmer",
            "length": "exactly 3 sentences",
            "include": "one everyday analogy",
            "exclude": "advanced implementation details",
        },
        "criteria": {
            "required_keywords": ["cache", "database"],
            "max_words": 120,
        },
    },
    {
        "name": "Boundary: Python Assistant",
        "pattern": "boundary",
        "variables": {
            "scope": "Python programming",
            "refusal_message": "This is outside my scope.",
            "user_input": "What is the capital of France?",
        },
        "criteria": {
            "required_keywords": ["outside my scope"],
            "max_words": 30,
        },
    },
]


def run_test_suite():
    print("=" * 70)
    print("  PROMPT ENGINEERING TEST SUITE")
    print("=" * 70)

    all_results = []

    for test in TEST_SUITE:
        print(f"\n{'=' * 60}")
        print(f"  Test: {test['name']}")
        print(f"  Pattern: {test['pattern']}")
        print(f"{'=' * 60}")

        prompt = build_prompt(test["pattern"], test["variables"])
        print(f"\n  System: {prompt['system'][:80]}...")
        print(f"  User prompt: {prompt['user'][:120]}...")
        print(f"  Temperature: {prompt['temperature']}")

        results = run_prompt_test(prompt, models=["gemini", "groq"])
        comparison, ranked = compare_models(results, test["criteria"])

        print(f"\n  {'Model':<12} {'Score':>8} {'Words':>8} {'Format':>8} {'Keywords':>10} {'Latency':>10}")
        print(f"  {'-'*70}")
        for model_name, data in ranked:
            score = data["scores"]["composite_score"]
            scores = data["scores"]
            word_count = scores.get("word_count", 0)
            format_valid = scores.get("format_valid", "n/a")
            keyword_coverage = scores.get("keyword_coverage", "n/a")
            latency = data["latency_ms"]
            print(
                f"  {model_name:<12} {score:>8.3f} {word_count:>8} "
                f"{str(format_valid):>8} {str(keyword_coverage):>10} {latency:>8.1f}ms"
            )

        all_results.append({
            "test": test["name"],
            "pattern": test["pattern"],
            "scores": {
                name: data["scores"]["composite_score"]
                for name, data in comparison.items()
            },
        })

    print(f"\n\n{'=' * 70}")
    print("  SUMMARY: MODEL RANKINGS ACROSS ALL TESTS")
    print(f"{'=' * 70}")

    model_wins = {}
    model_scores = {}
    for result in all_results:
        if result["scores"]:
            winner = max(result["scores"], key=result["scores"].get)
            model_wins[winner] = model_wins.get(winner, 0) + 1
            for model, score in result["scores"].items():
                model_scores.setdefault(model, []).append(score)

    for model, wins in sorted(model_wins.items(), key=lambda x: x[1], reverse=True):
        print(f"  {model}: {wins} wins out of {len(all_results)} tests")

    print("\n  Average instruction-following score:")
    for model, scores in sorted(model_scores.items(), key=lambda x: sum(x[1]) / len(x[1]), reverse=True):
        average = sum(scores) / len(scores)
        print(f"  {model}: {average:.3f}")

    return all_results