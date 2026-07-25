from app.llm.client import client
import time


class PerformanceAgent:

    def analyze(self, patch: str):

        prompt = f"""
You are a Senior Performance Engineer.

Analyze the following GitHub Pull Request.

Focus ONLY on performance.

Check for:

- Time complexity
- Space complexity
- Inefficient loops
- Unnecessary database/API calls
- Memory issues
- Expensive operations
- Performance bottlenecks

Return your answer in the following format:

Performance Issues:
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

        print(f"Performance Agent took {time.time() - start:.2f} seconds")

        return {
            "agent": "Performance Agent",
            "status": "Analysis Completed",
            "analysis": response["message"]["content"]
        }