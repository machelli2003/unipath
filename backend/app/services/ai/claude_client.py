"""
Anthropic Claude API wrapper.
Strictly used for explanation and chat only — never for scoring.
"""
try:
    import anthropic
except Exception:  # pragma: no cover - optional dependency
    anthropic = None

from ...core.config import Config


class ClaudeClient:

    def __init__(self):
        self.client = None
        self.model = Config.CLAUDE_MODEL
        if anthropic is not None and Config.ANTHROPIC_API_KEY:
            try:
                self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
            except Exception:
                self.client = None

    def complete(self, system: str, user: str, max_tokens: int = 1024) -> str:
        if self.client is None:
            return ""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return message.content[0].text

    def stream(self, system: str, messages: list, max_tokens: int = 1024):
        if self.client is None:
            yield ""
            return

        with self.client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                yield text
