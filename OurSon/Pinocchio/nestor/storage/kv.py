import sqlite3, json
from typing import Any, Optional

class KV:
    def __init__(self, path: str = "nestor.db"):
        self.conn = sqlite3.connect(path)
        self.conn.execute("CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT)")
        self.conn.commit()

    def get(self, k: str) -> Optional[Any]:
        cur = self.conn.execute("SELECT v FROM kv WHERE k=?", (k,))
        row = cur.fetchone()
        return json.loads(row[0]) if row else None

    def set(self, k: str, v: Any) -> None:
        self.conn.execute("REPLACE INTO kv (k, v) VALUES (?,?)", (k, json.dumps(v)))
        self.conn.commit()

    def delete(self, k: str) -> None:
        self.conn.execute("DELETE FROM kv WHERE k=?", (k,))
        self.conn.commit()
