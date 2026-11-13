from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Compare PostgreSQL and MySQL for write-heavy workloads.",
    config=types.GenerateContentConfig(
        system_instruction="You are a technical analyst. Be precise and cite sources.",
        temperature=0.3,
        max_output_tokens=2048,
    ),
)
print(response.text)