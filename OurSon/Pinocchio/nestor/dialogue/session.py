from dataclasses import dataclass, field

@dataclass
class SessionState:
    id: str
    chakra: str = "racine"
    history: list[dict] = field(default_factory=list)
    rating: str = "G"
