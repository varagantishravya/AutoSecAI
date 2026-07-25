from app.llm.client import client
import time


class DocumentationAgent:

    def analyze(self, patch: str):

        prompt = f"""
You are an experienced Technical Documentation Reviewer.

Analyze the following GitHub Pull Request.

Focus ONLY on documentation.

Check for:

- Missing docstrings
- Missing inline comments
- Outdated comments
- README updates required
- API documentation updates
- Missing usage examples
- Missing changelog updates
- Documentation quality

Return your answer in the following format:

Documentation Issues:
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

        print(f"Documentation Agent took {time.time() - start:.2f} seconds")

        return {
            "agent": "Documentation Agent",
            "status": "Analysis Completed",
            "analysis": response["message"]["content"]
        }