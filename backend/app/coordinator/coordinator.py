import re
from concurrent.futures import ThreadPoolExecutor
from app.github.changed_files import get_changed_files
from app.agents.security.analyzer import SecurityAgent
from app.agents.code_quality.analyzer import CodeQualityAgent
from app.agents.performance.analyzer import PerformanceAgent
from app.agents.testing.analyzer import TestingAgent
from app.agents.documentation.analyzer import DocumentationAgent
from app.agents.summary.analyzer import SummaryAgent
from app.reports.report_generator import generate_report
from app.database.database import save_review


class CoordinatorAgent:

    def __init__(self):
        self.security_agent = SecurityAgent()
        self.code_quality_agent = CodeQualityAgent()
        self.performance_agent = PerformanceAgent()
        self.testing_agent = TestingAgent()
        self.documentation_agent = DocumentationAgent()
        self.summary_agent = SummaryAgent()

    def parse_summary_output(self, summary_text: str) -> dict:
        """
        Parse the SummaryAgent's structured output to extract severity counts,
        overall score, and recommendation using regex.

        The SummaryAgent is instructed to output:
            Critical : <number>
            High     : <number>
            Medium   : <number>
            Low      : <number>
        and an overall score like "8/10" and a recommendation phrase.

        Falls back to safe defaults if parsing fails.
        """
        text = summary_text

        # --- Severity counts ---
        def extract_count(label: str) -> int:
            match = re.search(rf'{label}\s*:\s*(\d+)', text, re.IGNORECASE)
            return int(match.group(1)) if match else 0

        critical = extract_count("critical")
        high = extract_count("high")
        medium = extract_count("medium")
        low = extract_count("low")

        # --- Score: look for patterns like "8/10" or "7.5/10" ---
        score_match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*10', text, re.IGNORECASE)
        if score_match:
            score = float(score_match.group(1))
            score = max(0.0, min(10.0, score))   # clamp to [0, 10]
        else:
            # Derive score from counts if LLM didn't output it
            score = 10.0 - (critical * 3) - (high * 2) - (medium * 1) - (low * 0.5)
            score = max(0.0, score)

        # --- Recommendation (exact phrase matching) ---
        text_lower = text.lower()
        if "request changes" in text_lower:
            recommendation = "Request Changes"
        elif "approve with minor" in text_lower:
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
            "agents_reviewed": 6,   # 5 specialist agents + 1 summary agent
        }

    def limit_patch(self, patch: str, max_lines: int = 120) -> str:
        """Truncate patch to max_lines to avoid overflowing the LLM context window."""
        lines = patch.splitlines()
        if len(lines) > max_lines:
            return "\n".join(lines[:max_lines])
        return patch

    def review_pull_request(self, owner: str, repo: str, pull_request: int) -> dict:

        files = get_changed_files(owner, repo, pull_request)
        security_patch = ""
        performance_patch = ""
        testing_patch = ""
        documentation_patch = ""
        quality_patch = ""

        print(f"Changed files: {len(files)}")

        for file in files:
            if not file.get("patch"):
                continue

            filename = file["filename"]
            patch = file["patch"]
            patch_lower = patch.lower()

            # ---------------- Security ----------------
            if (
                filename.endswith((".py", ".js", ".ts", ".sql"))
                or "password" in patch_lower
                or "secret" in patch_lower
                or "token" in patch_lower
                or "api_key" in patch_lower
                or "select " in patch_lower
                or "insert " in patch_lower
                or "delete " in patch_lower
            ):
                security_patch += patch + "\n"

            # ---------------- Performance ----------------
            if (
                filename.endswith((".py", ".js", ".ts"))
                or "for " in patch_lower
                or "while " in patch_lower
                or ".sort(" in patch_lower
                or ".append(" in patch_lower
                or "range(" in patch_lower
            ):
                performance_patch += patch + "\n"

            # ---------------- Testing ----------------
            if (
                filename.endswith((".py", ".js", ".ts"))
                or "try:" in patch_lower
                or "except" in patch_lower
                or "@app.get" in patch_lower
                or "@app.post" in patch_lower
                or "assert" in patch_lower
            ):
                testing_patch += patch + "\n"

            # ---------------- Documentation ----------------
            if filename.endswith((".md", ".txt", ".rst")):
                documentation_patch += patch + "\n"

            # ---------------- Code Quality ----------------
            if filename.endswith((".py", ".js", ".ts", ".sql")):
                quality_patch += patch + "\n"

        security_patch      = self.limit_patch(security_patch)
        performance_patch   = self.limit_patch(performance_patch)
        testing_patch       = self.limit_patch(testing_patch)
        documentation_patch = self.limit_patch(documentation_patch)
        quality_patch       = self.limit_patch(quality_patch)

        print("=" * 60)
        print("Security Patch:",      len(security_patch.splitlines()),      "lines")
        print("Performance Patch:",   len(performance_patch.splitlines()),   "lines")
        print("Testing Patch:",       len(testing_patch.splitlines()),       "lines")
        print("Documentation Patch:", len(documentation_patch.splitlines()), "lines")
        print("Quality Patch:",       len(quality_patch.splitlines()),       "lines")
        print("=" * 60)

        # ── Step 1: Run all 5 specialist agents sequentially to avoid Groq rate limits ──────────────────
        with ThreadPoolExecutor(max_workers=1) as executor:

            security_future      = executor.submit(self.security_agent.analyze,      security_patch)
            quality_future       = executor.submit(self.code_quality_agent.analyze,  quality_patch)
            performance_future   = executor.submit(self.performance_agent.analyze,   performance_patch)
            testing_future       = executor.submit(self.testing_agent.analyze,       testing_patch)
            documentation_future = executor.submit(self.documentation_agent.analyze, documentation_patch)

            print("Waiting for Security Agent...")
            security_result = security_future.result()
            print("Security Agent finished.")

            print("Waiting for Code Quality Agent...")
            quality_result = quality_future.result()
            print("Code Quality Agent finished.")

            print("Waiting for Performance Agent...")
            performance_result = performance_future.result()
            print("Performance Agent finished.")

            print("Waiting for Testing Agent...")
            testing_result = testing_future.result()
            print("Testing Agent finished.")

            print("Waiting for Documentation Agent...")
            documentation_result = documentation_future.result()
            print("Documentation Agent finished.")

        # ── Step 2: Run SummaryAgent with all 5 specialist results ───────────
        print("Waiting for Summary Agent...")
        summary_result = self.summary_agent.analyze(
            security      = security_result["analysis"],
            quality       = quality_result["analysis"],
            performance   = performance_result["analysis"],
            testing       = testing_result["analysis"],
            documentation = documentation_result["analysis"],
        )
        print("Summary Agent finished.")

        # ── Step 3: Parse SummaryAgent output for structured metrics ─────────
        summary = self.parse_summary_output(summary_result["analysis"])

        # ── Step 4: Generate Markdown report (includes all 6 agent results) ──
        all_results = [
            security_result,
            quality_result,
            performance_result,
            testing_result,
            documentation_result,
            summary_result,
        ]

        report_path = generate_report(owner, repo, pull_request, summary, all_results)

        # ── Step 5: Persist the review in the database ───────────────────
        review_id = save_review(owner, repo, pull_request, summary, all_results, report_path)

        return {
            "status":  "Review Completed",
            "review_id": review_id,
            "summary": summary,
            "report":  report_path,
            "results": all_results,
        }


