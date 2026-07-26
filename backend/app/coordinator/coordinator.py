from concurrent.futures import ThreadPoolExecutor
from app.github.changed_files import get_changed_files
from app.agents.security.analyzer import SecurityAgent
from app.agents.code_quality.analyzer import CodeQualityAgent
from app.agents.performance.analyzer import PerformanceAgent
from app.agents.testing.analyzer import TestingAgent
from app.agents.documentation.analyzer import DocumentationAgent
from app.reports.report_generator import generate_report




class CoordinatorAgent:

    def __init__(self):
        self.security_agent = SecurityAgent()
        self.code_quality_agent = CodeQualityAgent()
        self.performance_agent = PerformanceAgent()
        self.testing_agent = TestingAgent()
        self.documentation_agent = DocumentationAgent()
    def calculate_summary(self, results):

        critical = 0
        high = 0
        medium = 0
        low = 0

        for result in results:

            text = result["analysis"].lower()

            if "critical" in text:
                critical += 1

            elif "high" in text:
                high += 1

            elif "medium" in text:
                medium += 1

            elif "low" in text:
                low += 1

        score = 10

        score -= critical * 3
        score -= high * 2
        score -= medium * 1
        score -= low * 0.5

        if score < 0:
            score = 0

        if critical > 0 or high >= 2:
            recommendation = "Request Changes"

        elif medium > 2:
            recommendation = "Approve with Minor Changes"

        else:
            recommendation = "Approve"

        return {
            "overall_score": f"{score:.1f}/10",
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low,
            "recommendation": recommendation,
            "agents_reviewed": len(results)
        }
        

    def review_pull_request(self, owner, repo, pull_request):

        files = get_changed_files(owner, repo, pull_request)
        patch = ""

        for file in files:
            if file.get("patch"):
                patch += file["patch"] + "\n"
        MAX_PATCH_LINES = 300

        lines = patch.splitlines()

        if len(lines) > MAX_PATCH_LINES:
            patch = "\n".join(lines[:MAX_PATCH_LINES])

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

        summary = self.calculate_summary([
            security_result,
            quality_result,
            performance_result,
            testing_result,
            documentation_result
        ])
        report_path = generate_report(
            owner,
            repo,
            pull_request,
            summary,
            [
                security_result,
                quality_result,
                performance_result,
                testing_result,
                documentation_result
            ]
        )

        return {
            "status": "Review Completed",
            "summary": summary,
            "report": report_path,
            "results": [
                security_result,
                quality_result,
                performance_result,
                testing_result,
                documentation_result
            ]
        }