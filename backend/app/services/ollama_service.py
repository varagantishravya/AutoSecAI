from ollama import chat


def ask_llama(prompt: str):
    response = chat(
        model="llama3.1",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content
if __name__ == "__main__":
    result = ask_llama("Explain SQL Injection in one sentence.")
    print(result)