import json

from exercise_utils import validation_errors


PRODUCT_OR_SERVICE_SCHEMA = {
    "oneOf": [
        {
            "type": "object",
            "properties": {
                "kind": {"type": "string", "enum": ["product"]},
                "name": {"type": "string"},
                "price": {"type": "number", "minimum": 0},
            },
            "required": ["kind", "name", "price"],
            "additionalProperties": False,
        },
        {
            "type": "object",
            "properties": {
                "kind": {"type": "string", "enum": ["service"]},
                "name": {"type": "string"},
                "hourly_rate": {"type": "number", "minimum": 0},
            },
            "required": ["kind", "name", "hourly_rate"],
            "additionalProperties": False,
        },
    ]
}


def validate_one_of(data, schema):
    alternatives = schema.get("oneOf", [])
    matches = []
    for alternative in alternatives:
        errors = validation_errors(data, alternative)
        properties = set(alternative.get("properties", {}))
        extra = set(data) - properties if isinstance(data, dict) else set()
        if alternative.get("additionalProperties") is False and extra:
            errors.append(f"$: additional properties are not allowed: {sorted(extra)}")
        if not errors:
            matches.append(alternative)
    if len(matches) != 1:
        return [f"$: expected exactly one matching schema, found {len(matches)}"]
    return []


def main():
    cases = [
        {"kind": "product", "name": "Keyboard", "price": 99},
        {"kind": "service", "name": "Consulting", "hourly_rate": 120},
        {"kind": "product", "name": "Broken"},
        {"kind": "service", "name": "Ambiguous", "price": 10, "hourly_rate": 20},
    ]
    for case in cases:
        errors = validate_one_of(case, PRODUCT_OR_SERVICE_SCHEMA)
        print(json.dumps(case), "PASS" if not errors else f"FAIL: {errors}")


if __name__ == "__main__":
    main()
