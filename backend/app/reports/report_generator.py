import os

def generate_report(owner, repo, pull_request, summary, results):

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/{repo}_PR_{pull_request}_Report.md"

    with open(filename, "w", encoding="utf-8") as file:

        file.write("# AutoSecAI Pull Request Review Report\n\n")

        file.write(f"**Repository:** {owner}/{repo}\n\n")
        file.write(f"**Pull Request:** #{pull_request}\n\n")

        file.write("## Summary\n\n")
        file.write(f"- Overall Score: {summary['overall_score']}\n")
        file.write(f"- Recommendation: {summary['recommendation']}\n")
        file.write(f"- Critical: {summary['critical']}\n")
        file.write(f"- High: {summary['high']}\n")
        file.write(f"- Medium: {summary['medium']}\n")
        file.write(f"- Low: {summary['low']}\n\n")

        file.write("---\n\n")

        for result in results:

            file.write(f"## {result['agent']}\n\n")
            file.write(result["analysis"])
            file.write("\n\n---\n\n")

    return filename