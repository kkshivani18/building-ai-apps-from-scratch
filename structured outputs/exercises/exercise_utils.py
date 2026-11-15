import json
import re
import sys
from pathlib import Path

STRUCTURED_OUTPUTS = Path(__file__).resolve().parents[1]
if str(STRUCTURED_OUTPUTS) not in sys.path:
    sys.path.insert(0, str(STRUCTURED_OUTPUTS))

from json_schema_validator import validate_schema


PRODUCT_SCHEMA = {
    "type": "object",
    "properties": {
        "product": {"type": "string"},
        "price": {"type": "number", "minimum": 0},
        "in_stock": {"type": "boolean"},
        "categories": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["product", "price", "in_stock"],
}


_PRODUCT_CATALOG = [
    ("Sony WH-1000XM5", 348),
    ("MacBook Pro 16", 2499),
    ("Kindle Paperwhite", 149),
    ("Logitech MX Keys", 99),
    ("Anker USB-C charger", 29),
    ("Samsung T7 SSD", 119),
    ("Nintendo Switch", 299),
    ("Bose SoundLink", 199),
    ("Raspberry Pi 5", 80),
    ("Canon EOS R50", 679),
]

PRODUCTS = []
for product, price in _PRODUCT_CATALOG:
    for in_stock, status in (
        (True, "is in stock"),
        (False, "is sold out"),
        (True, "is currently available"),
        (False, "is unavailable"),
        (True, "is ready to ship"),
    ):
        text = f"The {product} costs ${price} and {status}."
        PRODUCTS.append(
            (text, {"product": product, "price": float(price), "in_stock": in_stock})
        )


def validation_errors(value, schema=PRODUCT_SCHEMA):
    return validate_schema(value, schema)


def extract_product(text):
    lower = text.lower()
    product = text
    for marker in (" costs ", " is ", " are ", " sells "):
        if marker in product.lower():
            product = product[: product.lower().index(marker)]
            break
    product = product.strip()
    if product.startswith("The "):
        product = product[4:]
    product = product.rstrip(" ,.")
    price_match = re.search(r"\$(\d+(?:,\d{3})*(?:\.\d+)?)", text)
    price = float(price_match.group(1).replace(",", "")) if price_match else 0.0
    in_stock = not any(word in lower for word in ("sold out", "unavailable"))
    return {"product": product, "price": price, "in_stock": in_stock}


def exact_match(actual, expected):
    return actual == expected


def field_accuracy(actual, expected):
    return sum(actual.get(key) == value for key, value in expected.items()) / len(expected)
