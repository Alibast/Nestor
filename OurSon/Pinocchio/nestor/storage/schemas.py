from pydantic import BaseModel
from typing import Literal, List, Optional

class Joke(BaseModel):
    id: str
    text: str
    rating: Literal["G","PG","16+","18+"]
    tags: List[str] = []

class Memory(BaseModel):
    id: str
    kind: Literal["episodic","semantic"]
    content: str
    score: Optional[float] = None
