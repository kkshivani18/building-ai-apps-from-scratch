# Use It: Context Budget Comparison

## Goal

Compare the **Build It** heuristic token counter with a real tokenizer used by
libraries in practice. Run the sample for the same system prompt, selected
tools, retrieved context, history, and user query.

## Run

```powershell
cd "D:\Learning\AI\AI from scratch courses\building and deploying AI applications"
.\\ai-course\\Scripts\\python.exe "context engg\use it\context_budget_comparison.py"
```

## Result for the authentication query

| Component | Build It heuristic | tiktoken (`cl100k_base`) |
|---|---:|---:|
| System prompt | 41 | 39 |
| Selected tools | 6 | 20 |
| Retrieved context | 36 | 36 |
| Conversation history | 31 | 35 |
| User query | 16 | 13 |
| **Total** | **130** | **143** |

The Build It counter estimates tokens as `words * 1.3`. The library result is
13 tokens larger for this exact context. The difference is a reminder that
punctuation, JSON syntax, tool names, and word boundaries are not approximated
consistently by a whitespace counter.

The Build It dynamic selector's registry metadata estimates 710 tokens for five
selected tools, while tiktoken counts the serialized tool-name list as 20
tokens. The registry number represents estimated tool-definition cost; the
20-token number counts only names, not full tool schemas. In a real application,
measure the serialized tool schema that is sent to the model.

## What changed from Build It

The Build It implementation uses a whitespace-based token approximation.
The Use It implementation uses tiktoken to encode the text exactly for the
selected encoding and compares that count with the Build It approximation.

## Verification

Change one line in `component_report()`, predict whether the total will increase
or decrease, and rerun the script. Then compare one selected-tool JSON value and
one sentence of retrieved context.
