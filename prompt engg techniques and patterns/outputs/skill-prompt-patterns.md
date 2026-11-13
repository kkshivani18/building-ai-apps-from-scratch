# Prompt Pattern Decision Guide

| Task | Pattern |
|---|---|
| Need domain-specific expertise | Persona |
| Need consistent examples | Few-Shot |
| Need fixed fields extracted | Template Fill |
| Need scope restrictions | Guardrail or Boundary |
| Need a complex task broken down | Decomposition |
| Need self-review and improvement | Critique |
| Need different explanations for different readers | Audience Adaptation |
| Need another prompt written | Meta-Prompt |
| Need a fixed response structure | Template |

Use low temperature or fixed sampling for extraction, classification, and structured output. Use higher temperature for brainstorming and creative work.

For this project, use Gemini with LangChain to test the selected pattern.