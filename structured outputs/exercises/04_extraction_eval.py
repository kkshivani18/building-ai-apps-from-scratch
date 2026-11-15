from exercise_utils import PRODUCTS, exact_match, extract_product, field_accuracy, validation_errors


def main():
    exact = 0
    fields = 0.0
    valid = 0
    for text, expected in PRODUCTS:
        actual = extract_product(text)
        errors = validation_errors(actual)
        valid += not errors
        exact += exact_match(actual, expected)
        fields += field_accuracy(actual, expected)
        print(f"\n{text}\nactual={actual}\nexpected={expected}")
        print(f"valid={not errors} field_accuracy={field_accuracy(actual, expected):.0%}")

    total = len(PRODUCTS)
    print(f"\nExamples: {total}")
    print(f"Exact match: {exact / total:.0%}")
    print(f"Field-level accuracy: {fields / total:.0%}")
    print(f"Type/schema compliance: {valid / total:.0%}")
    print("Hardest fields: product naming and availability wording should be reviewed on larger data.")


if __name__ == "__main__":
    main()
