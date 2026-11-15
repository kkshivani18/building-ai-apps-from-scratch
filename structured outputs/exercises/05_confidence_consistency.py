from collections import Counter
from exercise_utils import PRODUCTS, extract_product


def confidence(values):
    counts = Counter(values)
    return counts.most_common(1)[0][1] / len(values)


def noisy_extract(text, run):
    result = extract_product(text)
    if run == 2 and "MacBook" in result["product"]:
        result["product"] = "MacBook Pro 16-inch"
    if run == 3 and result["in_stock"]:
        result["in_stock"] = False
    return result


def main():
    for text, _ in PRODUCTS:
        runs = [noisy_extract(text, run) for run in (1, 2, 3)]
        field_confidence = {
            field: confidence([run[field] for run in runs])
            for field in runs[0]
        }
        low_confidence = [
            field for field, score in field_confidence.items() if score < 0.67
        ]
        print(f"\n{text}")
        print(f"runs={runs}")
        print(f"confidence={field_confidence}")
        print(f"human_review={low_confidence or 'no'}")


if __name__ == "__main__":
    main()
