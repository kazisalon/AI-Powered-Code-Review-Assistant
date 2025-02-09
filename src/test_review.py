from src.reviewer import CodeReviewer
from src.github_integration import GitHubIntegration
from dotenv import load_dotenv


def main():
    print("Starting code review test...")

    # Initialize components
    reviewer = CodeReviewer()
    github = GitHubIntegration()

    # Test PR number (replace with actual PR number)
    PR_NUMBER = 1

    try:
        # Get PR files
        print(f"\nFetching files from PR #{PR_NUMBER}")
        pr_files = github.get_pr_files(PR_NUMBER)

        for file in pr_files:
            if file["filename"].endswith(".py"):
                print(f"\nReviewing file: {file['filename']}")

                # Analyze code
                review_results = reviewer.analyze_code(file["patch"])

                # Format and post review
                formatted_review = reviewer.format_review(review_results)
                print("\nReview results:")
                print(formatted_review)

                # Post review comment
                print("\nPosting review comment...")
                github.post_review_comment(
                    pr_number=PR_NUMBER,
                    commit_id=file["sha"],
                    path=file["filename"],
                    position=1,
                    body=formatted_review,
                )

        print("\nCode review completed successfully!")

    except Exception as e:
        print(f"\nError during code review: {str(e)}")


if __name__ == "__main__":
    load_dotenv()
    main()
