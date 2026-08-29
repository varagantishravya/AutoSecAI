from app.llm.client import client
import time


class PerformanceAgent:

    def analyze(self, patch: str):

        prompt = f"""
You are a Senior Performance Engineer conducting a Performance Review.

Your ONLY task is to review the GitHub Pull Request PATCH below.

STRICT RULES:
1. Analyze ONLY the modified lines in the patch.
2. Report only performance issues that are directly visible (e.g., inefficient loops, unnecessary DB calls, blocking I/O).
3. Do NOT invent unrelated improvements.
4. If no performance issues exist, reply exactly: "No performance issues found."

For every issue found, include:

Issue:
Severity: (High / Medium / Low)
File:
Line:
Explanation:
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
            print(f"PerformanceAgent ERROR: {e}")
            analysis = f"Performance analysis unavailable — LLM error: {str(e)}"

        print(f"Performance Agent took {time.time() - start:.2f} seconds")

        return {
            "agent": "Performance Agent",
            "status": "Analysis Completed",
            "analysis": analysis
        }