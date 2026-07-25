from concurrent.futures import ThreadPoolExecutor
from app.github.changed_files import get_changed_files
from app.agents.security.analyzer import SecurityAgent
from app.agents.code_quality.analyzer import CodeQualityAgent
from app.agents.performance.analyzer import PerformanceAgent
from app.agents.testing.analyzer import TestingAgent
from app.agents.documentation.analyzer import DocumentationAgent
from app.agents.summary.analyzer import SummaryAgent



class CoordinatorAgent:

    def __init__(self):
        self.security_agent = SecurityAgent()
        self.code_quality_agent = CodeQualityAgent()
        self.performance_agent = PerformanceAgent()
        self.testing_agent = TestingAgent()
        self.documentation_agent = DocumentationAgent()
        self.summary_agent = SummaryAgent()

    def review_pull_request(self, owner, repo, pull_request):

        files = get_changed_files(owner, repo, pull_request)
        patch = ""

        for file in files:
            if file.get("patch"):
                patch += file["patch"] + "\n"

    # ADD THESE LINES HERE
        with ThreadPoolExecutor(max_workers=5) as executor:

            security_future = executor.submit(self.security_agent.analyze, patch)
            quality_future = executor.submit(self.code_quality_agent.analyze, patch)
            performance_future = executor.submit(self.performance_agent.analyze, patch)
            testing_future = executor.submit(self.testing_agent.analyze, patch)
            documentation_future = executor.submit(
                self.documentation_agent.analyze,
                patch
            )

            security_result = security_future.result()
            quality_result = quality_future.result()
            performance_result = performance_future.result()
            testing_result = testing_future.result()
            documentation_result = documentation_future.result()
            summary_result = self.summary_agent.analyze(
                security_result["analysis"],
                quality_result["analysis"],
                performance_result["analysis"],
                testing_result["analysis"],
                documentation_result["analysis"]
            )

        return {
            "status": "Review Completed",
            "results": [
                security_result,
                quality_result,
                performance_result,
                testing_result,
                documentation_result,
                summary_result
            ]
        }