# -*- coding: utf-8 -*-
"""
CLI de test pour M3
Exemples :
  python io_utils/m3_cli.py --path standup.json --k 3 --lang fr
  python io_utils/m3_cli.py --path . --collection sitcom --q "pizza" --k 5
"""
from __future__ import annotations
import argparse
from pathlib import Path
from m3_jokes import JokeLibrary

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--path", default=".", help="Fichier (.json/.ndjson) OU dossier à charger")
    p.add_argument("--lang", default=None)
    p.add_argument("--style", default=None)
    p.add_argument("--audience", default=None)
    p.add_argument("--tag", action="append", default=None)
    p.add_argument("--char", action="append", default=None)
    p.add_argument("--q", default=None)
    p.add_argument("--safety", default=None)
    p.add_argument("--collection", default=None)
    p.add_argument("--k", type=int, default=1)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--export", default=None, help="Chemin .json pour exporter l'échantillon")
    return p.parse_args()

def main():
    a = parse_args()
    lib = JokeLibrary.from_path(Path(a.path))
    print(f"[M3/CLI] blagues chargées: {lib.size}")

    jokes = lib.sample(k=a.k, seed=a.seed,
                       lang=a.lang, style=a.style, audience=a.audience,
                       include_tags=a.tag, include_characters=a.char,
                       text_query=a.q, safety=a.safety, collection=a.collection)
    if a.export:
        lib.export_json_array(jokes, a.export)
        print(f"[M3/CLI] exporté {len(jokes)} blague(s) -> {a.export}")
        return

    if not jokes:
        print("[M3/CLI] Aucun résultat.")
        return

    for i, j in enumerate(jokes, 1):
        print(f"\n--- {i}/{len(jokes)} ---")
        print(f"[{j.lang} | {j.style} | {j.audience} | {', '.join(j.tags or [])}]")
        if j.characters:
            print(f"Characters: {', '.join(j.characters)}")
        if j.collection:
            print(f"Collection: {j.collection}")
        print(j.render())

if __name__ == "__main__":
    main()
