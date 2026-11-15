import string

VOCABULARY = list(string.ascii_lowercase + string.digits + '{}[]":,. ')

def valid_tokens(partial, required_keys):
    stripped = partial.strip()
    if not stripped:
        return ["{"]
    if stripped.endswith("{") or stripped.endswith(","):
        return ['"', "}"]
    if stripped.endswith(":"):
        return list('0123456789" tf')
    if stripped.endswith('"'):
        return ['"', ",", "}"]
    if stripped.endswith("}"):
        return ["<EOS>"]
    return [token for token in VOCABULARY if token not in "{}[]"]


def simulate_generation(required_keys):
    states = ['{']
    for key in required_keys:
        states.append(states[-1] + f'"{key}":')
        states.append(states[-1] + '"value",')
    states.append(states[-1].rstrip(",") + "}")
    return states


def main():
    required_keys = ["product", "price", "in_stock"]
    allowed_counts = []
    for state in simulate_generation(required_keys):
        allowed = valid_tokens(state, required_keys)
        allowed_counts.append(len(allowed))
        print(f"{state!r}: {len(allowed)} valid token classes")
    average = sum(allowed_counts) / len(allowed_counts)
    print(f"\nVocabulary size: {len(VOCABULARY)}")
    print(f"Average valid token classes: {average:.2f}")
    print("This is a teaching simulator, not a tokenizer or production grammar.")


if __name__ == "__main__":
    main()
