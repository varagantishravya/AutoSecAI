from app.services.github_service import get_pull_request_files


files = get_pull_request_files(
    owner="tiangolo",
    repo="fastapi",
    pr_number=11000
)

for file in files:

    filename = file["filename"]

    # Analyze only code files
    if filename.endswith((".py", ".js", ".java", ".cpp", ".go", ".rs")):

        print("=" * 50)
        print("File:", filename)
        print("Status:", file["status"])
        print("Changes:", file["changes"])
        print("Patch:")
        print(file.get("patch"))