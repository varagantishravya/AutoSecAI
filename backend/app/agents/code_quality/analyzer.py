from app.llm.client import client
import time


class CodeQualityAgent:

    def analyze(self, patch: str):

        prompt = f"""
You are a Senior Software Engineer conducting a Code Quality Review.

Your ONLY task is to review the GitHub Pull Request PATCH below.

STRICT RULES:
1. Analyze ONLY the modified lines in the patch.
2. Do NOT rewrite the code.
3. Do NOT invent functions or suggest unrelated improvements.
4. Only comment on issues that are directly visible in the patch.
5. If no code quality issues exist, reply exactly: "No code quality issues found."

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
            print(f"CodeQualityAgent ERROR: {e}")
            analysis = f"Code quality analysis unavailable — LLM error: {str(e)}"

        print(f"Code Quality Agent took {time.time() - start:.2f} seconds")

        return {
            "agent": "Code Quality Agent",
            "status": "Analysis Completed",
            "analysis": analysis
        }