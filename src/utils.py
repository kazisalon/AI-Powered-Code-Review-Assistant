import os
from typing import Dict, List, Any
from colorama import init, Fore, Style
from dotenv import load_dotenv

init(autoreset=True)


def load_env_vars() -> Dict[str, str]:
    """Load and validate environment variables."""
    load_dotenv()
    required_vars = ["GITHUB_TOKEN", "ORGANIZATION", "REPOSITORY"]
    env_vars = {}

    for var in required_vars:
        value = os.getenv(var)
        if not value:
            raise ValueError(f"Missing required environment variable: {var}")
        env_vars[var] = value

    return env_vars


def format_review_comment(comment: str, severity: str = "info") -> str:
    """Format review comments with color coding."""
    colors = {
        "error": Fore.RED,
        "warning": Fore.YELLOW,
        "info": Fore.GREEN,
    }
    color = colors.get(severity.lower(), Fore.WHITE)
    return f"{color}{comment}{Style.RESET_ALL}"


# Test the functions
if __name__ == "__main__":
    try:
        # Test environment variables
        env_vars = load_env_vars()
        print("Environment variables loaded successfully:")
        for key, value in env_vars.items():
            print(f"{key}: {'*' * len(value)}")  # Hide actual values

        # Test comment formatting
        print("\nTesting comment formatting:")
        print(format_review_comment("This is an error", "error"))
        print(format_review_comment("This is a warning", "warning"))
        print(format_review_comment("This is info", "info"))

    except Exception as e:
        print(f"Error: {str(e)}")
