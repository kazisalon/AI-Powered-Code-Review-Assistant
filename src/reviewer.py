from typing import Dict, List, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from .utils import format_review_comment


class CodeReviewer:
    def __init__(self, model_name: str = "microsoft/codebert-base"):
        """Initialize the code reviewer with a pre-trained model."""
        print("Initializing CodeReviewer...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        # Review categories and their prompts
        self.review_categories = {
            "quality": (
                "Review this code for quality issues:\n"
                "- Check variable naming\n"
                "- Look for code organization\n"
                "- Identify potential bugs\n"
            ),
            "security": (
                "Review this code for security issues:\n"
                "- Check for input validation\n"
                "- Look for potential vulnerabilities\n"
                "- Identify unsafe operations\n"
            ),
            "performance": (
                "Review this code for performance issues:\n"
                "- Check for inefficient operations\n"
                "- Look for potential bottlenecks\n"
                "- Identify memory issues\n"
            ),
        }
        print("CodeReviewer initialized successfully")

    def analyze_code(self, code: str) -> Dict[str, List[str]]:
        """Analyze code and return review comments."""
        results = {}

        for category, prompt in self.review_categories.items():
            # Combine prompt and code
            input_text = f"{prompt}\n\nCode to review:\n{code}"

            # Tokenize input
            inputs = self.tokenizer(
                input_text, return_tensors="pt", truncation=True, max_length=512
            )

            # Generate review
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs["input_ids"],
                    max_length=150,
                    num_return_sequences=1,
                    temperature=0.7,
                )

            # Decode and parse response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            results[category] = self._parse_response(response)

        return results

    def _parse_response(self, response: str) -> List[str]:
        """Parse model response into list of review comments."""
        comments = []
        for line in response.split("\n"):
            line = line.strip()
            if line and not line.startswith("Code to review:"):
                comments.append(line)
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


# Test the reviewer
if __name__ == "__main__":
    # Sample code to review
    test_code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
    """

    try:
        reviewer = CodeReviewer()
        results = reviewer.analyze_code(test_code)
        formatted_review = reviewer.format_review(results)
        print("\nReview Results:")
        print(formatted_review)

    except Exception as e:
        print(f"Error during review: {str(e)}")
