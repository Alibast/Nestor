from .base import Persona
from .middleware import apply_style
import json, importlib.resources as pkg
from typing import Dict

_cache: Dict[str, Persona] = {}

def load(name: str) -> Persona:
    if name in _cache:
        return _cache[name]
    data = json.loads(pkg.files(__package__).joinpath("chakras").joinpath(f"{name}.json").read_text(encoding="utf-8"))
    p = Persona(name=name, system_prompt=data["system"], style=data.get("style", {}))
    _cache[name] = p
    return p

def apply(name: str, ctx: dict) -> dict:
    persona = load(name)
    blocks = persona.apply(ctx)
    return apply_style(blocks)
