from app.llm.client import client
import time


class SecurityAgent:

    def analyze(self, patch: str):

        prompt = f"""
You are a Senior Application Security Reviewer.

Your ONLY task is to review the GitHub Pull Request PATCH below.

STRICT RULES:

1. Analyze ONLY the code that appears in the patch.

2. NEVER review the whole project.

3. NEVER invent missing files.

4. NEVER assume missing code.

5. NEVER suggest features that are not part of the patch.

6. If a vulnerability is NOT directly visible inside the modified lines,
reply:

"Cannot determine from the supplied patch."

7. Never report:
- SQL Injection
- XSS
- CSRF
- Path Traversal
- Authentication
- Authorization
unless the modified code directly introduces them.

8. Do NOT make assumptions.

9. If no security issue exists, reply exactly:

"No security issues found."

For every issue include:

Severity:
File:
Line:
Explanation:
Recommendation:

Return Markdown only.



Patch:
{patch}
"""

        start = time.time()
        print("Starting chat...")
        print("Sending prompt to Ollama...")

        try:
            response = client.chat(
                model="llama3.2:1b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            analysis = response["message"]["content"]
            print("Received response from Ollama")
        except Exception as e:
            print(f"SecurityAgent ERROR: {e}")
            analysis = f"Security analysis unavailable — LLM error: {str(e)}"

        print("Chat completed")
        print(f"Security Agent took {time.time() - start:.2f} seconds")

        return {
            "agent": "Security Agent",
            "status": "Analysis Completed",
            "analysis": analysis
        }