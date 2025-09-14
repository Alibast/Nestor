from typing import List, Dict
from ..storage.vector import VectorStore

class SemanticMemory:
    def __init__(self, vec: VectorStore):
        self.vec = vec

    def recall(self, query: str, k: int = 5, namespace: str = "texts") -> List[Dict]:
        hits = self.vec.search(query, k=k, namespace=namespace)
        return [{"id": i, "score": s, "meta": m} for (i,s,m) in hits]
