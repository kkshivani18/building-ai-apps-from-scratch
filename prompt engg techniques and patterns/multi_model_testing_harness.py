import os
import time

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

MODEL_CONFIGS = {
    "gemini": {
        "provider": "google",
        "model": os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
    },
    "groq": {
        "provider": "groq",
        "model": os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
    },
}


def _extract_text(content):
    if isinstance(content, list):
        return "\n".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return str(content)


def _create_model(model_name, prompt):
    config = MODEL_CONFIGS[model_name]
    if config["provider"] == "google":
        return ChatGoogleGenerativeAI(model=config["model"])
    return ChatGroq(model=config["model"], temperature=prompt["temperature"])


def _call_real_llm(model_name, prompt):
    model = _create_model(model_name, prompt)
    messages = [
        ("system", prompt["system"]),
        ("user", prompt["user"]),
    ]

    for attempt in range(3):
        try:
            start = time.perf_counter()
            response = model.invoke(messages)
            latency_ms = round((time.perf_counter() - start) * 1000, 1)
            usage = response.response_metadata.get("token_usage", {})
            return {
                "response": _extract_text(response.content),
                "tokens_used": {
                    "prompt": usage.get("prompt_tokens", 0),
                    "completion": usage.get("completion_tokens", 0),
                    "total": usage.get("total_tokens", 0),
                },
                "latency_ms": latency_ms,
                "finish_reason": response.response_metadata.get("finish_reason"),
            }
        except Exception as error:
            message = str(error)
            is_transient = any(code in message for code in ("429", "500", "503", "UNAVAILABLE"))
            if not is_transient or attempt == 2:
                raise
            time.sleep(2 ** attempt)


def run_prompt_test(prompt, models=None):
    if models is None:
        models = list(MODEL_CONFIGS.keys())

    results = {}
    for model_name in models:
        response = _call_real_llm(model_name, prompt)

        results[model_name] = {
            "response": response["response"],
            "tokens": response["tokens_used"],
            "api_latency_ms": response["latency_ms"],
            "wall_time_ms": response["latency_ms"],
            "finish_reason": response.get("finish_reason"),
        }

    return results