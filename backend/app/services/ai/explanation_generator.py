"""
Generates AI narrative for recommendation results.
Called AFTER the deterministic engine has run.
"""
from .claude_client import ClaudeClient
from .prompt_builder import build_summary_prompt, build_course_explanation_prompt


class ExplanationGenerator:

    def __init__(self):
        self.client = ClaudeClient()

    def generate_summary(self, result: dict) -> str:
        try:
            system, user = build_summary_prompt(result)
            return self.client.complete(system, user, max_tokens=300)
        except Exception as e:
            print(f"[AI] Summary generation failed: {e}")
            return ""

    def generate_course_explanation(self, course_result: dict, profile: dict) -> str:
        try:
            system, user = build_course_explanation_prompt(course_result, profile)
            return self.client.complete(system, user, max_tokens=500)
        except Exception as e:
            print(f"[AI] Course explanation failed: {e}")
            return ""
