import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    temperature=0.0,
    system="You are a data extraction engine. Output valid JSON only.",
    messages=[
        {
            "role": "user",
            "content": "Extract: John Smith, age 34, works at Google as a senior engineer since 2019.",
        },
        {
            "role": "assistant",
            "content": "{",
        },
    ],
)

result = "{" + response.content[0].text
print(result)