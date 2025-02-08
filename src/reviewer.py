from typing import Dict, List, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from .utils import format_review_comment


class CodeReviewer:
    def __init__(self):
        """Initialize the code reviewer with a pre-trained model."""
        # Using CodeBERT as an example - you can replace with your preferred model
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/codebert-base")

        # Review categories and their prompts
        self.review_categories = {
            "quality": "Analyze code quality, including readability and maintainability:",
            "security": "Check for security vulnerabilities:",
            "performance": "Identify performance issues:",
        }

    def analyze_code(self, code: str) -> Dict[str, List[str]]:
        """
        Analyze code and return review comments.

        Args:
            code (str): Source code to analyze

        Returns:
            Dict[str, List[str]]: Review comments by category
        """
        results = {}

        for category, prompt in self.review_categories.items():
            input_text = f"{prompt}\n\n{code}"
            inputs = self.tokenizer(
                input_text, return_tensors="pt", truncation=True, max_length=512
            )

            with torch.no_grad():
                outputs = self.model.generate(
                    inputs["input_ids"],
                    max_length=150,
                    num_return_sequences=1,
                    temperature=0.7,
                )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            results[category] = self._parse_response(response)

        return results

    def _parse_response(self, response: str) -> List[str]:
        """Parse model response into list of review comments."""
        # Split response into individual comments
        comments = [line.strip() for line in response.split("\n") if line.strip()]
        return comments

    def format_review(self, review_results: Dict[str, List[str]]) -> str:
        """Format review results into a readable string."""
        formatted_review = []

        for category, comments in review_results.items():
            formatted_review.append(f"\n## {category.title()} Review")
            for comment in comments:
                severity = (
                    "error"
                    if "error" in comment.lower()
                    else "warning" if "warning" in comment.lower() else "info"
                )
                formatted_review.append(format_review_comment(f"- {comment}", severity))

        return "\n".join(formatted_review)
