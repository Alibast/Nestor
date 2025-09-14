from typing import List, Dict
from ..storage.kv import KV

class EpisodicMemory:
    def __init__(self, kv: KV):
        self.kv = kv

    def remember(self, event: Dict):
        timeline = self.kv.get("episodic") or []
        timeline.append(event)
        self.kv.set("episodic", timeline)

    def recent(self, n: int = 10) -> List[Dict]:
        return (self.kv.get("episodic") or [])[-n:]
