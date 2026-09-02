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
            # Matches: "Medium : 1", "**Medium**: 1", "* Medium: 1", etc. at the start of a line
            match = re.search(rf'(?m)^[*#\s]*{label}[*#\s]*:\s*(\d+)', text, re.IGNORECASE)
            return int(match.group(1)) if match else 0

        critical = extract_count("critical")
        high = extract_count("high")
        medium = extract_count("medium")
        low = extract_count("low")

        # --- Score: look for patterns like "8/10" or "7.5/10" ---
        score_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:/|out of)\s*10', text, re.IGNORECASE)
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

    def limit_patch(self, patch: str, max_lines: int = 250, max_chars: int = 4000) -> str:
        """Truncate patch to max_lines / max_chars to prevent LLM context and rate limit overflows."""
        lines = patch.splitlines()
        if len(lines) > max_lines:
            patch = "\n".join(lines[:max_lines])
        if len(patch) > max_chars:
            patch = patch[:max_chars] + "\n... [Truncated for rate-limit optimization] ..."
        return patch

    def review_pull_request(self, owner: str, repo: str, pull_request: int, token: str | None = None, user_id: int | None = None) -> dict:
        import time

        files = get_changed_files(owner, repo, pull_request, token=token)

        security_patch = ""
        performance_patch = ""
        testing_patch = ""
        documentation_patch = ""
        quality_patch = ""

        print(f"Changed files: {len(files)}")

        ignored_extensions = (".lock", "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "cargo.lock", "go.sum", ".min.js", ".min.css", ".map")

        for file in files:
            if not file.get("patch"):
                continue

            filename = file["filename"].lower()
            
            # Skip lock & compiled minified assets that clog up context
            if any(filename.endswith(ext) or ext in filename for ext in ignored_extensions):
                continue
                
            patch = file["patch"]
            patch_lower = patch.lower()

            # ---------------- Security ----------------
            if (
                filename.endswith((".py", ".js", ".ts", ".sql", ".jsx", ".tsx"))
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
                filename.endswith((".py", ".js", ".ts", ".jsx", ".tsx"))
                or "for " in patch_lower
                or "while " in patch_lower
                or ".sort(" in patch_lower
                or ".append(" in patch_lower
                or "range(" in patch_lower
            ):
                performance_patch += patch + "\n"

            # ---------------- Testing ----------------
            if (
                filename.endswith((".py", ".js", ".ts", ".jsx", ".tsx"))
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
            if filename.endswith((".py", ".js", ".ts", ".sql", ".jsx", ".tsx")):
                quality_patch += patch + "\n"

        security_patch      = self.limit_patch(security_patch)
        performance_patch   = self.limit_patch(performance_patch)
        testing_patch       = self.limit_patch(testing_patch)
        documentation_patch = self.limit_patch(documentation_patch)
        quality_patch       = self.limit_patch(quality_patch)

        # ── RAG Integration ──────────────────────────────────────────────────
        try:
            from app.rag.knowledge_base import KnowledgeBase
            kb = KnowledgeBase()
            # Use the security patch as a query for relevant knowledge
            query_text = security_patch[:300]
            if query_text.strip():
                docs = kb.search(query_text, top_k=2)
                if docs:
                    rag_context = "=== Context from Knowledge Base ===\n"
                    for doc in docs:
                        rag_context += doc['text'] + "\n"
                    rag_context += "===================================\n\n"
                    security_patch = rag_context + security_patch
        except Exception as e:
            print(f"RAG Integration skipped or failed: {e}")

        print("=" * 60)
        print("Security Patch:",      len(security_patch.splitlines()),      "lines")
        print("Performance Patch:",   len(performance_patch.splitlines()),   "lines")
        print("Testing Patch:",       len(testing_patch.splitlines()),       "lines")
        print("Documentation Patch:", len(documentation_patch.splitlines()), "lines")
        print("Quality Patch:",       len(quality_patch.splitlines()),       "lines")
        print("=" * 60)

        # ── Step 1: Run 5 specialist agents sequentially with small delay to respect rate limits ──
        print("Executing Security Agent...")
        security_result = self.security_agent.analyze(security_patch)
        time.sleep(1.0)

        print("Executing Code Quality Agent...")
        quality_result = self.code_quality_agent.analyze(quality_patch)
        time.sleep(1.0)

        print("Executing Performance Agent...")
        performance_result = self.performance_agent.analyze(performance_patch)
        time.sleep(1.0)

        print("Executing Testing Agent...")
        testing_result = self.testing_agent.analyze(testing_patch)
        time.sleep(1.0)

        print("Executing Documentation Agent...")
        documentation_result = self.documentation_agent.analyze(documentation_patch)
        time.sleep(1.0)


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
        review_id = save_review(owner, repo, pull_request, summary, all_results, report_path, user_id=user_id)


        return {
            "status":  "Review Completed",
            "review_id": review_id,
            "summary": summary,
            "report":  report_path,
            "results": all_results,
        }


