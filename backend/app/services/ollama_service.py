from ollama import Client

# Shared Ollama client — consistent with llm/client.py
client = Client(host="http://localhost:11434")


def ask_llama(prompt: str, model: str = "llama3.2:1b") -> str:
    """
    Send a prompt to the local Ollama LLM and return the response text.

    Args:
        prompt: The prompt string to send to the model.
        model:  The Ollama model name to use (default: llama3.2:1b).

    Returns:
        The model's text response, or an error message string.
    """
    try:
        response = client.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        # Correct dict-style access (not dot notation)
        return response["message"]["content"]
    except Exception as e:
        return f"LLM error: {str(e)}"


if __name__ == "__main__":
    result = ask_llama("Explain SQL Injection in one sentence.")
    print(result)