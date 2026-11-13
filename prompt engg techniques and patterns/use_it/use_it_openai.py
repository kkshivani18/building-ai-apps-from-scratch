from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5",
    temperature=0.0,
    messages=[
        {
            "role": "system",
            "content": "You are a senior Python developer. Respond with code only, no explanations.",
        },
        {
            "role": "user",
            "content": "Write a function that finds the longest palindromic substring.",
        },
    ],
)

print(response.choices[0].message.content)