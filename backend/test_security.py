from app.agents.security.security_agent import SecurityAgent


sample_patch = """
diff --git a/app.py b/app.py

- query = "SELECT * FROM users WHERE id=" + user_id
+ query = "SELECT * FROM users WHERE id=?"
"""


agent = SecurityAgent()

report = agent.analyze_patch(sample_patch)

print(report)