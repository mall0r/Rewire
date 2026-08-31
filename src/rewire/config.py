"""Configuration loading and path resolution for rewire."""

import os
from configparser import ConfigParser
from pathlib import Path

GENERIC_KEY = "command"

CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))
CACHE_HOME = os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))

CONFIG_DIR = Path(CONFIG_HOME) / "rewire"
CONFIG_PATH = CONFIG_DIR / "rewire.conf"

LOG_PATH = Path(
    os.environ.get("REWIRE_LOG", str(Path(CACHE_HOME) / "rewire" / "rewire.log"))
)
LOG_LEVEL = os.environ.get("REWIRE_LOG_LEVEL", "DEBUG").upper()


def load_config(path: str | os.PathLike | None = None) -> ConfigParser:
    """Read the INI configuration from ``path`` (defaults to CONFIG_PATH)."""
    config = ConfigParser()
    config.read(path or CONFIG_PATH)
    return config
