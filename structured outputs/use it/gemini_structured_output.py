"""Extract product data with Gemini's schema-constrained JSON output.
"""

import os
import sys

from google import genai
from google.genai import types
from pydantic import BaseModel, Field


class Product(BaseModel):
    product: str
    price: float = Field(ge=0)
    in_stock: bool
    categories: list[str]


def extract_product(text: str) -> Product:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        contents=(
            "Extract the product information from the text. "
            "Do not infer a price or availability that is not stated.\n\n"
            f"Text: {text}"
        ),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Product,
            temperature=0,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")
    return Product.model_validate_json(response.text)


def main() -> None:
    text = "Sony WH-1000XM5 headphones are priced at $348 and currently available."
    product = extract_product(sys.argv[1] if len(sys.argv) > 1 else text)
    print(product.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
