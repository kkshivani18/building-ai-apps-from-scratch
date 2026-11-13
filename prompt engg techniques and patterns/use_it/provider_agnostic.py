from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are {role}. Respond in {format}."),
    ("user", "{question}"),
])

chain_openai = prompt | ChatOpenAI(model="gpt-5", temperature=0)
chain_claude = prompt | ChatAnthropic(model="claude-opus-4-7", temperature=0)

variables = {"role": "a database expert", "format": "bullet points", "question": "When should I use Redis vs Memcached?"}

print("GPT-4o:", chain_openai.invoke(variables).content)
print("Claude:", chain_claude.invoke(variables).content)