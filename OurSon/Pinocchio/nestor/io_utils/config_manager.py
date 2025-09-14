"""
Module M2 — Config Manager
Objectif : centraliser les réglages (chemins, paramètres) dans un seul fichier config.json
"""

from pathlib import Path
from typing import Any, Dict, Optional, Union
import os
import re

# On réutilise ton M1
from io_utils.json_loader import load_json

_ENV_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)\}")

class ConfigManager:
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        self._config: Dict[str, Any] = {}
        self._path: Optional[Path] = None
        if config_path:
            self.load(config_path)

    def load(self, config_path: Union[str, Path]) -> Dict[str, Any]:
        """Charge le config.json et applique la résolution des variables d'environnement."""
        path = Path(config_path)
        self._path = path
        data = load_json(str(path))
        self._config = self._resolve_envs(data)
        return self._config

    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Récupère une valeur du config via une clé en notation pointée.
        Ex: "paths.data_dir" ou "llm.temperature"
        """
        node: Any = self._config
        for part in key.split("."):
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                return default
        return node

    # --- Helpers -------------------------------------------------------------

    def _resolve_envs(self, value: Any) -> Any:
        """
        Remplace les variables ${ENV_VAR} dans les chaînes par la valeur d'env.
        Applique récursivement sur dict / list.
        """
        if isinstance(value, dict):
            return {k: self._resolve_envs(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._resolve_envs(v) for v in value]
        if isinstance(value, str):
            def repl(m):
                var = m.group(1)
                return os.environ.get(var, "")
            return _ENV_PATTERN.sub(repl, value)
        return value


# Singleton pratique pour usage direct
_config_singleton: Optional[ConfigManager] = None

def init_config(config_path: Union[str, Path]) -> None:
    global _config_singleton
    _config_singleton = ConfigManager(config_path)

def get_config(key: str, default: Any = None) -> Any:
    if _config_singleton is None:
        raise RuntimeError("Config non initialisé. Appelle init_config(<chemin_config.json>) d'abord.")
    return _config_singleton.get_config(key, default)


if __name__ == "__main__":
    from pathlib import Path
    CONFIG_JSON = Path(__file__).parent / "tests" / "config.json"
    try:
        init_config(CONFIG_JSON)
        print("__file__     =", __file__)
        print("CONFIG_JSON  =", CONFIG_JSON.resolve())
        print("✔ persona.name          :", get_config("persona.name"))
        print("✔ llm.model             :", get_config("llm.model"))
        print("✔ paths.data_dir        :", get_config("paths.data_dir"))
        print("✔ inconnu (default=42)  :", get_config("does.not.exist", 42))
    except Exception as e:
        print(f"❌ Erreur ConfigManager: {e}")
import os
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

class ConfigManager:
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        self._config: Dict[str, Any] = {}
        self._path: Optional[Path] = None
        if config_path:
            self.load(config_path)

    def load(self, config_path: Union[str, Path]):
        """Charge un fichier JSON de configuration."""
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Fichier introuvable: {path}")
        with open(path, "r", encoding="utf-8") as f:
            self._config = json.load(f)
        self._path = path

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Récupère une valeur de config.
        - Si la clé est 'openai.api_key' et absente du JSON → va chercher dans l'environnement.
        - Sinon retourne la valeur du JSON ou la valeur par défaut.
        """
        if key == "openai.api_key":
            return self._config.get(key, os.environ.get("OPENAI_API_KEY", default))
        return self._config.get(key, default)


