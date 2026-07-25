from app.llm.client import client
import time


class SummaryAgent:

    def analyze(self, security, quality, performance, testing, documentation):

        prompt = f"""
You are an experienced Senior Software Architect.

You have received reviews from five AI agents.

Security Review:
{security}

Code Quality Review:
{quality}

Performance Review:
{performance}

Testing Review:
{testing}

Documentation Review:
{documentation}

Create a FINAL Pull Request Review.

Your response should contain:

1. Overall Summary
2. Key Strengths
3. Major Issues
4. Recommendation:
   - Approve
   - Approve with Minor Changes
   - Request Changes
5. Overall PR Score (out of 10)

Keep the report professional and concise.
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

        print(f"Summary Agent took {time.time() - start:.2f} seconds")

        return {
            "agent": "Summary Agent",
            "status": "Analysis Completed",
            "analysis": response["message"]["content"]
        }