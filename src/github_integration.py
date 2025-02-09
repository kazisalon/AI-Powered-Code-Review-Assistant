import requests
from typing import List, Dict
from .utils import load_env_vars


class GitHubIntegration:
    def __init__(self):
        """Initialize GitHub integration with environment variables."""
        print("Initializing GitHub integration...")
        env_vars = load_env_vars()
        self.token = env_vars["GITHUB_TOKEN"]
        self.org = env_vars["ORGANIZATION"]
        self.repo = env_vars["REPOSITORY"]
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }
        self.base_url = f"https://api.github.com/repos/{self.org}/{self.repo}"
        print("GitHub integration initialized successfully")

    def get_pull_request(self, pr_number: int) -> Dict:
        """Get pull request details."""
        url = f"{self.base_url}/pulls/{pr_number}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_pr_files(self, pr_number: int) -> List[Dict]:
        """Get files changed in a pull request."""
        url = f"{self.base_url}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post_review_comment(
        self, pr_number: int, commit_id: str, path: str, position: int, body: str
    ) -> Dict:
        """Post a review comment on a specific line of code."""
        url = f"{self.base_url}/pulls/{pr_number}/comments"
        data = {
            "body": body,
            "commit_id": commit_id,
            "path": path,
            "position": position,
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()


# Test the GitHub integration
if __name__ == "__main__":
    try:
        github = GitHubIntegration()

        # Test getting a PR (use a real PR number)
        PR_NUMBER = 1  # Replace with an actual PR number
        print(f"\nTesting PR retrieval for PR #{PR_NUMBER}")
        pr_details = github.get_pull_request(PR_NUMBER)
        print(f"Successfully retrieved PR: {pr_details['title']}")

        # Test getting PR files
        print("\nTesting PR files retrieval")
        pr_files = github.get_pr_files(PR_NUMBER)
        print(f"Found {len(pr_files)} files in PR")

    except Exception as e:
        print(f"Error: {str(e)}")
