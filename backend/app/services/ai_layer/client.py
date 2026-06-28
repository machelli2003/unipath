"""
ai_layer/client.py

Thin wrapper around the Anthropic API. Centralizing the API call here means
every AI invocation in the app goes through one chokepoint, which makes it
easy to enforce guardrails, swap models, add logging/rate-limiting, etc.
"""

import os
from anthropic import Anthropic

_client = None


def get_client() -> Anthropic:
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set in environment.")
        _client = Anthropic(api_key=api_key)
    return _client


def call_ai(system_prompt: str, user_message: str, max_tokens: int = 600) -> str:
    """
    Single chokepoint for all AI calls. system_prompt MUST be built via
    ai_layer.guardrails.build_system_prompt() — never pass a freeform prompt
    that bypasses the guardrails.
    """
    client = get_client()
    model = os.getenv("AI_MODEL", "claude-sonnet-4-6")

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    text_blocks = [block.text for block in response.content if block.type == "text"]
    return "\n".join(text_blocks)
