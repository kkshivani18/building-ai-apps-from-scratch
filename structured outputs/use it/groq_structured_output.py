"""Extract product data with Groq's JSON Schema structured output.
"""

import os
import sys

from groq import Groq
from pydantic import BaseModel, Field


class Product(BaseModel):
    product: str
    price: float = Field(ge=0)
    in_stock: bool
    categories: list[str]


def groq_json_schema() -> dict:
    schema = Product.model_json_schema()

    def add_strict_objects(value: object) -> None:
        if isinstance(value, dict):
            if value.get("type") == "object":
                value["additionalProperties"] = False
            for child in value.values():
                add_strict_objects(child)
        elif isinstance(value, list):
            for child in value:
                add_strict_objects(child)

    add_strict_objects(schema)
    return schema


def extract_product(text: str) -> Product:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set.")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract product information from the user's text. "
                    "Do not infer a price or availability that is not stated."
                ),
            },
            {"role": "user", "content": text},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "product",
                "strict": True,
                "schema": groq_json_schema(),
            },
        },
        temperature=0,
    )

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Groq returned an empty response.")
    return Product.model_validate_json(content)


def main() -> None:
    text = "Sony WH-1000XM5 headphones are priced at $348 and currently available."
    product = extract_product(sys.argv[1] if len(sys.argv) > 1 else text)
    print(product.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
