import os
import re
import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are {role}. Respond in {format}. Do not use bullets, markdown, or metadata."),
    ("user", "{question}"),
])

model = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
)
# Model 'gemini-3.5-flash-lite' uses fixed sampling defaults; the sampling parameter(s) temperature will be ignored. Hence, removed

chain = prompt | model

variables = {
    "role": "a database expert",
    "format": "one plain-text line for each recommendation",
    "question": "When should I use Redis versus Memcached?",
}

for attempt in range(3):
    try:
        response = chain.invoke(variables)
        break
    except Exception as error:
        message = str(error)
        is_transient = "503" in message or "UNAVAILABLE" in message
        if not is_transient or attempt == 2:
            raise
        time.sleep(2 ** attempt)

content = response.content
if isinstance(content, list):
    text = "\n".join(
        block.get("text", "")
        for block in content
        if isinstance(block, dict) and block.get("type") == "text"
    )
else:
    text = str(content)

for line in text.splitlines():
    cleaned_line = re.sub(r"^\s*[-*•]\s*", "", line).strip()
    if cleaned_line:
        print(cleaned_line)

# print("Configured temperature:", model.temperature)