from typing import Optional, Iterable
import os

class OpenAIClient:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini", **_):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        # Placeholder: wire actual SDK if desired

    def generate(self, prompt: str, system: Optional[str] = None, tools: Optional[list] = None, **kwargs) -> str:
        # Minimal stub to keep interface consistent
        return "(openai) " + (system + " " if system else "") + prompt

    def stream(self, prompt: str, system: Optional[str] = None, tools: Optional[list] = None, **kwargs) -> Iterable[str]:
        yield self.generate(prompt, system=system, tools=tools, **kwargs)
