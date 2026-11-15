# Skill: Production Structured Outputs

## Purpose

Design reliable pipelines that turn unstructured text into validated,
versioned, schema-conforming data.

## Decision framework

1. **Use provider-native structured output** when the provider supports the
   required schema features and reliability matters.
2. **Use JSON mode plus application validation** when JSON syntax is guaranteed
   but the provider cannot enforce the full schema.
3. **Use unconstrained generation plus parse, validate, and bounded retry** only
   when native structured output is unavailable.
4. **Use constrained decoding** when token-level validity is required and the
   runtime supports a grammar or schema constraint.

Provider support, schema limits, model names, and pricing must be verified
against current provider documentation before production use.

## Production workflow

1. Define a minimal schema with explicit types, required fields, bounds, enums,
   and `additionalProperties: false` where supported.
2. Version schemas. Classify changes as breaking or non-breaking before
   deploying them.
3. Give the model the schema and extraction rules, while treating source text
   as untrusted data.
4. Prefer provider-native schema enforcement.
5. Parse the response and validate it in application code anyway.
6. Retry only bounded, retryable failures. Preserve the validation error in
   telemetry and do not silently return a success-shaped fallback.
7. Route persistent failures to review or a dead-letter queue.
8. Measure exact match, field accuracy, type compliance, validation failures,
   retry rate, latency, and cost.
9. Attach confidence and provenance to extracted fields when human review is
   possible.

## Schema design

- Keep field names stable and descriptive.
- Use `oneOf` for genuinely polymorphic values and require a discriminator
  when possible.
- Use enums for controlled vocabularies.
- Use numeric bounds and array limits to prevent unreasonable outputs.
- Decide explicitly how missing or unknown values are represented.
- Avoid accepting arbitrary additional properties unless they are needed.

## Security and operations

- Keep API keys in environment variables or a secret manager.
- Treat extracted data and source text as untrusted input.
- Redact sensitive source content from logs.
- Set request timeouts and bounded retries.
- Log schema version, model, validation status, retry count, and latency.
- Store raw responses only under an approved retention policy.

## Definition of done

- Valid outputs parse and validate.
- Invalid types, missing required fields, bounds, enums, and polymorphic
  alternatives are rejected.
- Breaking schema changes are identified before release.
- Extraction quality is measured on a labeled evaluation set.
- Low-confidence or inconsistent fields are flagged for review.
- Provider failures are explicit and bounded.
