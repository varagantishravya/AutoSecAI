from app.llm.client import client
import time


class TestingAgent:

    def analyze(self, patch: str):

        prompt = f"""
You are a Senior QA Engineer conducting a Test Coverage Review.

Your ONLY task is to review the GitHub Pull Request PATCH below.

STRICT RULES:
1. Suggest ONLY tests that directly correspond to the modified code.
2. Do NOT invent unrelated test cases.
3. Do NOT suggest testing code that was not changed.
4. If the patch needs no additional tests, reply exactly: "No additional tests required."

For every missing test, include:

Test Case:
Type: (Unit / Integration / E2E)
What to test:
Expected behaviour:

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
            print(f"TestingAgent ERROR: {e}")
            analysis = f"Testing analysis unavailable — LLM error: {str(e)}"

        print(f"Testing Agent took {time.time() - start:.2f} seconds")

        return {
            "agent": "Testing Agent",
            "status": "Analysis Completed",
            "analysis": analysis
        }