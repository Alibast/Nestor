from typing import Any, Optional, Iterable
from .lmstudio import LMStudioClient
from .openai import OpenAIClient

class LLM:
    def __init__(self, backend: str = "lmstudio", **kwargs):
        if backend == "lmstudio":
            self._client = LMStudioClient(**kwargs)
        elif backend == "openai":
            self._client = OpenAIClient(**kwargs)
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def generate(self, prompt: str, system: Optional[str] = None, tools: Optional[list] = None, **kwargs) -> str:
        return self._client.generate(prompt, system=system, tools=tools, **kwargs)

    def stream(self, prompt: str, system: Optional[str] = None, tools: Optional[list] = None, **kwargs) -> Iterable[str]:
        yield from self._client.stream(prompt, system=system, tools=tools, **kwargs)
