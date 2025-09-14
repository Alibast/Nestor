from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Persona:
    name: str
    system_prompt: str
    style: Dict[str, Any]

    def apply(self, message_ctx: Dict[str, Any]) -> Dict[str, Any]:
        return {"system": self.system_prompt, "style": self.style, "ctx": message_ctx}
