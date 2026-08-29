from app.llm.client import client
import time


class DocumentationAgent:

    def analyze(self, patch: str):

        prompt = f"""
You are a Senior Technical Writer conducting a Documentation Review.

Your ONLY task is to review the GitHub Pull Request PATCH below.

STRICT RULES:
1. Report ONLY missing or incorrect documentation for the modified code.
2. Do NOT assume README changes are needed unless the patch shows README changes.
3. Do NOT invent API endpoints.
4. Check for missing: docstrings, inline comments for complex logic, type hints.
5. If no documentation issues exist, reply exactly: "No documentation issues found."

For every issue found, include:

Issue:
Severity: (High / Medium / Low)
File:
What is missing:
Recommendation:

Return Markdown only.

Patch:
{patch}
"""

        start = time.time()

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
        except Exception as e:
            print(f"DocumentationAgent ERROR: {e}")
            analysis = f"Documentation analysis unavailable — LLM error: {str(e)}"

        print(f"Documentation Agent took {time.time() - start:.2f} seconds")

        return {
            "agent": "Documentation Agent",
            "status": "Analysis Completed",
            "analysis": analysis
        }