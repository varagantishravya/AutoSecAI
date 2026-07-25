from app.llm.client import client
import time


class SecurityAgent:

    def analyze(self, patch: str):

        prompt = f"""
You are an expert Application Security Engineer.

Review the following GitHub Pull Request.

Check ONLY for:

- SQL Injection
- XSS
- CSRF
- Hardcoded Secrets
- Authentication Issues
- Command Injection
- Path Traversal
- Insecure Coding Practices

Only report real security vulnerabilities.
If none are found, say "No security vulnerabilities found."

Patch:
{patch}
"""

        start = time.time()
        print("Starting chat...")
        print("Sending prompt to Ollama...")
        response = client.chat(
            model="llama3.2:1b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        print("Received response from Ollama")
        print("Chat completed")
        print(f"Security Agent took {time.time() - start:.2f} seconds")

        return {
            "agent": "Security Agent",
            "status": "Analysis Completed",
            "analysis": response["message"]["content"]
        }