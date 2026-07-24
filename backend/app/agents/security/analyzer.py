from app.llm.client import client


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

        response = client.chat(
            model="llama3.1",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return {
            "agent": "Security Agent",
            "status": "Analysis Completed",
            "analysis": response["message"]["content"]
        }