from app.github.changed_files import get_changed_files
from app.agents.security.analyzer import SecurityAgent
from app.agents.code_quality.analyzer import CodeQualityAgent

class CoordinatorAgent:

    def __init__(self):
        self.security_agent = SecurityAgent()
        self.code_quality_agent = CodeQualityAgent()

    def review_pull_request(self, owner, repo, pull_request):

        files = get_changed_files(owner, repo, pull_request)
        patch = ""

        for file in files:
            if file.get("patch"):
                patch += file["patch"] + "\n"

        security_result = self.security_agent.analyze(patch)
        quality_result = self.code_quality_agent.analyze(patch)

        return {
            "status": "Review Completed",
            "results": [
                security_result,
                quality_result
            ]
        }