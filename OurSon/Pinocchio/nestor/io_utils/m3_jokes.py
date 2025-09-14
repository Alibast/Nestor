# -*- coding: utf-8 -*-
"""
M3 — Bibliothèque de blagues (JSON-array ou NDJSON)
- Charge 1 fichier (.json / .ndjson) OU un dossier (récursif)
- Détecte auto JSON-array vs NDJSON
- Recherche, random, export
"""

from __future__ import annotations
import json, random, re, sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional, Dict, Any, Tuple

# ---------- Modèle ----------

@dataclass
class Joke:
    id: str
    lang: str                 # "fr" | "en"
    style: str                # sitcom | standup | dad | wordplay | roast | clean | grivois | etc.
    audience: str             # "all-ages" | "PG-13" | "18+"
    tags: List[str] = field(default_factory=list)
    characters: List[str] = field(default_factory=list)
    beats: Optional[Dict[str, str]] = None  # {"setup","turn","punchline"}
    text: Optional[str] = None
    delivery: Optional[str] = None
    safety: Optional[str] = None            # "safe" | "borderline" | "risky"
    source: Optional[str] = None            # "original" | "domaine-public" | "adaptation"
    attribution: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    notes: Optional[str] = None
    collection: Optional[str] = None        # ex: "standup", "sitcom", "poemes"

    def render(self) -> str:
        if self.beats and any(self.beats.get(k) for k in ("setup","turn","punchline")):
            parts = []
            if self.beats.get("setup"):     parts.append(self.beats["setup"])
            if self.beats.get("turn"):      parts.append(self.beats["turn"])
            if self.beats.get("punchline"): parts.append(self.beats["punchline"])
            out = " / ".join(parts)
        else:
            out = (self.text or "").strip()
        if self.delivery:
            out += f"  (delivery: {self.delivery})"
        return out

# ---------- Validation légère ----------

REQUIRED = ("id", "lang", "style", "audience")

def _basic_validate(j: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    for k in REQUIRED:
        if k not in j or j[k] in (None, ""):
            return False, f"champ requis manquant: {k}"
    has_beats = isinstance(j.get("beats"), dict) and any(j["beats"].get(k) for k in ("setup","turn","punchline"))
    has_text  = bool(j.get("text"))
    if not has_beats and not has_text:
        return False, "fournir 'beats' (setup/turn/punchline) ou 'text'"
    if j["lang"] not in {"fr","en"}:
        return False, f"lang invalide: {j['lang']}"
    if j["audience"] not in {"all-ages","PG-13","18+"}:
        return False, f"audience invalide: {j['audience']}"
    return True, None

# ---------- Bibliothèque ----------

class JokeLibrary:
    def __init__(self):
        self._jokes: List[Joke] = []
        self._by_lang: Dict[str, List[int]] = {}
        self._by_style: Dict[str, List[int]] = {}
        self._by_audience: Dict[str, List[int]] = {}
        self._by_tag: Dict[str, List[int]] = {}
        self._by_character: Dict[str, List[int]] = {}

    # -- Construction --

    @classmethod
    def from_path(cls, path: Path | str) -> "JokeLibrary":
        """
        path: fichier unique (.json/.ndjson) OU dossier (chargement récursif)
        """
        lib = cls()
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Chemin introuvable: {p}")

        if p.is_file():
            lib._load_file(p)
        else:
            # dossier → charge tous les .json/.ndjson récursivement
            for f in p.rglob("*"):
                if f.suffix.lower() in {".json", ".ndjson"}:
                    lib._load_file(f)

        lib._build_indexes()
        return lib

    # -- Lecture de fichier --

    def _load_file(self, fpath: Path):
        try:
            text = fpath.read_text(encoding="utf-8")
        except Exception as e:
            _warn(f"{fpath}: lecture impossible: {e}")
            return

        # Déduction collection d'après le nom de fichier (standup/sitcom/poemes)
        collection_guess = fpath.stem.lower()

        # Détection JSON-array vs NDJSON
        first_non_ws = next((ch for ch in text.lstrip()[:1]), "")
        if first_non_ws == "[":  # JSON-array
            try:
                items = json.loads(text)
                if not isinstance(items, list):
                    _warn(f"{fpath}: JSON non-array")
                    return
            except Exception as e:
                _warn(f"{fpath}: JSON invalide ({e})")
                return

            for idx, raw in enumerate(items, start=1):
                self._ingest_obj(raw, f"{fpath}[{idx}]", collection_guess)

        else:  # NDJSON
            for line_no, line in enumerate(text.splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    raw = json.loads(line)
                except Exception as e:
                    _warn(f"{fpath}:{line_no} JSON invalide: {e}")
                    continue
                self._ingest_obj(raw, f"{fpath}:{line_no}", collection_guess)

    def _ingest_obj(self, raw: Dict[str, Any], origin: str, collection_guess: str):
        ok, err = _basic_validate(raw)
        if not ok:
            _warn(f"{origin} invalide: {err}")
            return
        raw.setdefault("collection", raw.get("collection") or collection_guess)
        self._jokes.append(Joke(**raw))

    def _build_indexes(self):
        for idx, j in enumerate(self._jokes):
            self._by_lang.setdefault(j.lang, []).append(idx)
            self._by_style.setdefault(j.style, []).append(idx)
            self._by_audience.setdefault(j.audience, []).append(idx)
            for t in (j.tags or []):
                self._by_tag.setdefault(t.lower(), []).append(idx)
            for c in (j.characters or []):
                self._by_character.setdefault(c.lower(), []).append(idx)

    # -- Accès --

    @property
    def size(self) -> int:
        return len(self._jokes)

    def all(self) -> List[Joke]:
        return list(self._jokes)

    # -- Recherche --

    def search(self,
               lang: Optional[str] = None,
               style: Optional[str] = None,
               audience: Optional[str] = None,
               include_tags: Optional[Iterable[str]] = None,
               include_characters: Optional[Iterable[str]] = None,
               text_query: Optional[str] = None,
               safety: Optional[str] = None,
               collection: Optional[str] = None,
               limit: Optional[int] = None) -> List[Joke]:
        candidates = set(range(self.size))
        def narrow(index_map: Dict[str, List[int]], key: Optional[str]):
            nonlocal candidates
            if key:
                candidates &= set(index_map.get(key, []))

        narrow(self._by_lang, lang)
        narrow(self._by_style, style)
        narrow(self._by_audience, audience)

        if include_tags:
            for tag in include_tags:
                candidates &= set(self._by_tag.get(str(tag).lower().strip(), []))

        if include_characters:
            for ch in include_characters:
                candidates &= set(self._by_character.get(str(ch).lower().strip(), []))

        out: List[Joke] = []
        pattern = re.compile(re.escape(text_query), re.IGNORECASE) if text_query else None
        for i in candidates:
            j = self._jokes[i]
            if safety and j.safety != safety:
                continue
            if collection and (j.collection or "").lower() != collection.lower():
                continue
            if pattern:
                pool = [
                    j.text or "",
                    *(j.tags or []),
                    *(j.characters or []),
                    *( [j.beats.get("setup",""), j.beats.get("turn",""), j.beats.get("punchline","")] if j.beats else [] )
                ]
                if not any(pattern.search(x or "") for x in pool):
                    continue
            out.append(j)
        if limit is not None:
            out = out[:max(0, int(limit))]
        return out

    # -- Sélection --

    def random(self, seed: Optional[int] = None, **kwargs) -> Optional[Joke]:
        items = self.search(**kwargs)
        if not items:
            return None
        rng = random.Random(seed)
        return rng.choice(items)

    def sample(self, k: int, seed: Optional[int] = None, **kwargs) -> List[Joke]:
        items = self.search(**kwargs)
        if not items:
            return []
        k = max(0, min(k, len(items)))
        rng = random.Random(seed)
        return rng.sample(items, k)

    # -- Export --

    def export_json_array(self, jokes: Iterable[Joke], out_path: Path | str):
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        data = [asdict(j) for j in jokes]
        out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def _warn(msg: str):
    print(f"[M3:WARN] {msg}", file=sys.stderr)

if __name__ == "__main__":
    # Debug rapide : python io_utils/m3_jokes.py path/to/standup.json
    p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("standup.json")
    lib = JokeLibrary.from_path(p)
    print(f"Blagues chargées: {lib.size}")
    ex = lib.random(lang="fr")
    if ex:
        print("Exemple:", ex.render())
