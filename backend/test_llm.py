from app.llm.client import client

response = client.chat(
    model="llama3.1",
    messages=[
        {
            "role": "user",
            "content": "What is SQL Injection? Reply in one sentence."
        }
    ]
)

print(response["message"]["content"])