from app.github.client import github_client

def test_connection():
    user = github_client.get_user()

    print("✅ Connected Successfully!")
    print("Username:", user.login)
    print("Name:", user.name)

if __name__ == "__main__":
    test_connection()