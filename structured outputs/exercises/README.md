# Structured outputs exercises

These exercises use the local schema validator and deterministic extraction
examples. They do not require Gemini, Groq, or an API key. Run them from this
directory:

```powershell
python 01_oneof_validator.py
python 02_schema_diff.py
python 03_constrained_decoding.py
python 04_extraction_eval.py
python 05_confidence_consistency.py
```

## Exercise 1: `oneOf` validation

Extend validation for polymorphic `Product` or `Service` objects. An object
passes only when exactly one alternative schema matches. Record which cases
pass, fail, or match zero/multiple alternatives.

## Exercise 2: schema diff

Compare two schema versions. Record breaking changes such as removed fields,
new required fields, changed types, removed enum values, and tightened
constraints. Also record non-breaking changes such as added optional fields,
relaxed constraints, and fields made optional.

## Exercise 3: constrained decoding

Walk through a small JSON generation and count valid token classes at each
step. Compare the valid count with the vocabulary size. This is intentionally
a teaching simulation; it is not a tokenizer or production grammar.

## Exercise 4: extraction evaluation

Run extraction against the 50 labeled product examples. Record exact-match,
field-level accuracy, and schema/type compliance. Identify which fields are
hardest to extract correctly.

## Exercise 5: confidence and consistency

Run extraction three times, estimate each field's confidence as the proportion
of identical values, and flag fields below 67% for human review. In production,
prefer provider token probabilities or calibrated confidence data when
available.

## Results log

Fill in the table after running the scripts. Record the date, Python version,
schema version, and any changes to the examples.

| Exercise | Completed | Main result | Observation |
|---|---:|---|---|
| 1. `oneOf` validator | [x] | 2 valid and 2 invalid cases | Missing required fields and extra fields were rejected. |
| 2. Schema diff | [x] | 2 breaking and 1 non-breaking change | Type/minimum changes break compatibility; optional fields do not. |
| 3. Constrained decoding | [x] | Vocabulary 45; average allowed classes 6.38 | Schema constraints reduce the valid generation space. |
| 4. Extraction evaluation | [x] | Exact match 100%; field accuracy 100%; compliance 100% | The deterministic 50-case baseline is correct; broader real-world text is still needed. |
| 5. Confidence consistency | [x] | Repeated outputs were compared field by field | Deliberate inconsistent runs flagged `product` or `in_stock` for review. |

### Environment

- Date: 2026-11-15
- Python version: 3.12.10
- Schema version: local `PRODUCT_SCHEMA` baseline
- Provider/API model: none; deterministic local simulation
- Dataset size: 50 labeled product descriptions

### Conclusions

1. Polymorphic validation: `oneOf` requires exactly one matching alternative and rejects missing or extra fields.
2. Breaking schema changes: changing a numeric type or tightening a minimum is breaking; adding an optional field is non-breaking.
3. Constrained-token behavior: the valid token space is much smaller than the full vocabulary at structured positions.
4. Extraction quality: the controlled 50-example baseline reached 100% on all measured metrics.
5. Low-confidence fields: consistency below 67% should trigger human review; confidence is not correctness.
