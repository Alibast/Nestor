from typing import List, Dict, Any, Tuple
import chromadb

class VectorStore:
    def __init__(self, name: str = "nestor"):
        self.client = chromadb.Client()
        self.col = self.client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})

    def add(self, items: List[Dict[str, Any]], namespace: str = "default"):
        ids = [f"{namespace}:{i.get('id')}" for i in items]
        texts = [i.get("text") or i.get("content") for i in items]
        metas = [{"namespace":namespace, **{k:v for k,v in i.items() if k not in ("id","text","content")}} for i in items]
        self.col.add(ids=ids, documents=texts, metadatas=metas)

    def search(self, query: str, k: int = 5, namespace: str = "default") -> List[Tuple[str,float,Dict[str,Any]]]:
        res = self.col.query(query_texts=[query], n_results=k, where={"namespace":namespace})
        out = []
        for i in range(len(res["ids"][0])):
            out.append((res["ids"][0][i], res["distances"][0][i], res["metadatas"][0][i]))
        return out
