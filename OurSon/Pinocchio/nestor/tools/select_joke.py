import random
from ..storage.schemas import Joke

def pick(jokes: list[Joke], rating: str = "G", theme: str | None = None) -> Joke | None:
    pool = [j for j in jokes if j.rating == rating or rating in ("PG","16+","18+") and j.rating in ("G","PG","16+","18+")]
    if theme:
        pool = [j for j in pool if theme in j.tags]
    return random.choice(pool) if pool else None
