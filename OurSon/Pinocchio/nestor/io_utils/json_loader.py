"""
Module M1 — JSON Loader
Objectif: Charger un fichier .json et le transformer en dictionnaire Python.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

def load_json(file_path: str) -> Dict[str, Any]:
    """
    Charge un fichier JSON et le retourne sous forme de dictionnaire.

    Args:
        file_path: Chemin vers le fichier JSON.

    Returns:
        dict: Contenu du JSON.

    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
        json.JSONDecodeError: Si le JSON est invalide.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {file_path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    # ✅ Version avec chemin ABSOLU (raw string) – remplace par le tien si besoin
    TEST_JSON = r"C:\Users\athan\OneDrive\Nestor\Our Son\Pinocchio\nestor\io\tests\exemple.json"
    try:
        data = load_json(TEST_JSON)
        print(f"✅ JSON chargé avec succès: {data}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
