from typing import Dict, Any
from ..config import load_settings
from ..logging import get_logger
from ..llm.client import LLM
from ..persona import registry as personas
from ..memory.episodic import EpisodicMemory
from ..memory.semantic import SemanticMemory
from ..storage.kv import KV
from ..storage.vector import VectorStore
from .session import SessionState

log = get_logger(__name__)

class DialogueManager:
    def __init__(self):
        self.settings = load_settings()
        self.llm = LLM(backend=self.settings.llm_backend, base_url=self.settings.lmstudio_base_url, api_key=self.settings.openai_api_key)
        self.kv = KV()
        self.vec = VectorStore()
        self.epi = EpisodicMemory(self.kv)
        self.sem = SemanticMemory(self.vec)

    def respond(self, user_msg: str, meta: Dict[str, Any] | None = None, state: SessionState | None = None) -> str:
        state = state or SessionState(id="default")
        ctx = {"user": user_msg, "history": state.history}
        blocks = personas.apply(state.chakra, ctx)
        system = blocks.get("system", "")
        retrieval = self.sem.recall(user_msg, k=3, namespace="texts")
        prompt = f"Context: {retrieval}\nUser: {user_msg}"
        reply = self.llm.generate(prompt, system=system)
        state.history.append({"user": user_msg, "assistant": reply})
        self.epi.remember({"u": user_msg, "a": reply})
        return reply
