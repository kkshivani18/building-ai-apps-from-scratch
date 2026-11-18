---
name: skill-context-engineering
description: Design and validate context assembly pipelines for LLM applications
---

# Context Engineering

Apply this framework when an application assembles system instructions, tools,
retrieved documents, memory, and a user query.

## Principles

- Context is a scarce resource; allocate it by component.
- Measure tokens with the target model's tokenizer.
- Include dynamic context only when it is relevant to the current query.
- Put critical instructions and the current query near the context boundaries.
- Summarize old history and keep only recent turns verbatim.
- Reserve enough tokens for the expected response.

## Budget

1. Reserve generation output first.
2. Allocate a tight system prompt.
3. Prune tools by classified intent.
4. Retrieve, rerank, deduplicate, and threshold documents.
5. Summarize history older than the last few turns.
6. Place the user query near the end.

## Validation

Before accepting a context layout, test:

- A query with one clear intent
- A query with two valid intents
- An ambiguous query
- A long conversation that triggers history compression
- A query for which the correct document is in the middle
- A budget near the context-window limit

Report token counts, selected tools, retained history, document ordering, and
remaining generation budget. If the layout is rebuilt for a new query, it is
dynamic; if components remain fixed for every query, inspect them for waste.
