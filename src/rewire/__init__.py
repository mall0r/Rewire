"""rewire: intercepts Steam's %command% and replaces it with a configured command.

Detects the appid via STEAM_COMPAT_APPID/SteamAppId and looks up a matching
config section. For Proton, keeps the scaffolding and replaces the executable.
"""

from .cli import main

__all__ = ["main"]
__version__ = "0.1.0"
