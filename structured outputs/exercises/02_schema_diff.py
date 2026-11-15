import json


def schema_diff(old, new):
    breaking = []
    non_breaking = []
    old_properties = old.get("properties", {})
    new_properties = new.get("properties", {})
    old_required = set(old.get("required", []))
    new_required = set(new.get("required", []))

    for field in sorted(old_required - new_required):
        non_breaking.append(f"required field made optional: {field}")
    for field in sorted(new_required - old_required):
        breaking.append(f"optional field made required: {field}")
    for field in sorted(old_properties.keys() - new_properties.keys()):
        breaking.append(f"field removed: {field}")
    for field in sorted(new_properties.keys() - old_properties.keys()):
        if field in new_required:
            breaking.append(f"required field added: {field}")
        else:
            non_breaking.append(f"optional field added: {field}")

    for field in sorted(old_properties.keys() & new_properties.keys()):
        old_type = old_properties[field].get("type")
        new_type = new_properties[field].get("type")
        if old_type != new_type:
            breaking.append(f"type changed for {field}: {old_type} -> {new_type}")
        old_enum = old_properties[field].get("enum")
        new_enum = new_properties[field].get("enum")
        if old_enum and new_enum and not set(new_enum).issuperset(old_enum):
            breaking.append(f"enum values removed for {field}")
        old_min = old_properties[field].get("minimum")
        new_min = new_properties[field].get("minimum")
        if new_min is not None and (old_min is None or new_min > old_min):
            breaking.append(f"minimum tightened for {field}")
        if old_min is not None and (new_min is None or new_min < old_min):
            non_breaking.append(f"minimum relaxed for {field}")
    return breaking, non_breaking


def main():
    old = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "price": {"type": "number", "minimum": 0}},
        "required": ["name", "price"],
    }
    new = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "price": {"type": "integer", "minimum": 10},
            "currency": {"type": "string"},
        },
        "required": ["name", "price"],
    }
    breaking, non_breaking = schema_diff(old, new)
    print("Breaking changes:")
    print(json.dumps(breaking, indent=2))
    print("Non-breaking changes:")
    print(json.dumps(non_breaking, indent=2))


if __name__ == "__main__":
    main()
