from app.llm.client import client


class CodeQualityAgent:

    def analyze(self, patch: str):

        prompt = f"""
You are an experienced Senior Software Engineer.

Review the following GitHub Pull Request.

Focus ONLY on code quality.

Check for:
- Clean Code
- Readability
- Naming conventions
- Code duplication
- Large functions
- Maintainability
- PEP8 violations
- Bad coding practices

Return your answer in this format:

Code Quality Issues:
- ...

Severity:
- Low / Medium / High

Recommendations:
- ...

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
            "agent": "Code Quality Agent",
            "status": "Analysis Completed",
            "analysis": response["message"]["content"]
        }