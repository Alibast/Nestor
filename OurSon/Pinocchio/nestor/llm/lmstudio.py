from typing import Optional, Iterable
import httpx, json

class LMStudioClient:
    def __init__(self, base_url: str = "http://localhost:1234/v1", model: str = "qwen2.5", **_):
        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str, system: Optional[str] = None, tools: Optional[list] = None, **kwargs) -> str:
        payload = {"model": self.model, "messages":[{"role":"system","content":system or ""},{"role":"user","content":prompt}]}
        with httpx.Client(timeout=60) as client:
            r = client.post(f"{self.base_url}/chat/completions", json=payload)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]

    def stream(self, prompt: str, system: Optional[str] = None, tools: Optional[list] = None, **kwargs) -> Iterable[str]:
        yield self.generate(prompt, system=system, tools=tools, **kwargs)
