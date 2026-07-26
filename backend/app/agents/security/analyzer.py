from app.llm.client import client
import time


class SecurityAgent:

    def analyze(self, patch: str):

        prompt = f"""
You are a Senior Application Security Engineer reviewing a GitHub Pull Request.

Analyze ONLY the provided code patch.

Look ONLY for these vulnerabilities:

- SQL Injection
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Hardcoded Secrets
- Authentication Issues
- Command Injection
- Path Traversal
- Insecure Coding Practices

Rules:

1. Report ONLY vulnerabilities directly visible in the patch.
2. Do NOT assume hidden code exists.
3. If there is not enough evidence, say:
   "No security vulnerabilities found."
4. Do NOT invent vulnerabilities.
5. Keep the response concise.

Return exactly in this format:

Security Issues:
- ...

Severity:
- Low / Medium / High

Recommendations:
- ...

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