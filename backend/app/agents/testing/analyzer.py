from app.llm.client import client
import time


class TestingAgent:

    def analyze(self, patch: str):

        prompt = f"""
You are an experienced Software Test Engineer.

Analyze the following GitHub Pull Request.

Focus ONLY on testing.

Check for:

- Missing unit tests
- Missing integration tests
- Missing edge cases
- Missing exception handling
- Missing input validation
- Test coverage improvements

Return your answer in the following format:

Testing Issues:
- ...

Severity:
- Low / Medium / High

Recommendations:
- ...

Patch:
{patch}
"""

        start = time.time()

        response = client.chat(
            model="llama3.2:1b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        print(f"Testing Agent took {time.time() - start:.2f} seconds")

        return {
            "agent": "Testing Agent",
            "status": "Analysis Completed",
            "analysis": response["message"]["content"]
        }