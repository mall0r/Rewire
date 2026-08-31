"""Core logic for rewire: appid detection, command resolution and rebuilding."""

import os
from configparser import ConfigParser

from .config import GENERIC_KEY

PROTON_MARKER = "waitforexitandrun"


def detect_appid(environ: dict[str, str] | None = None) -> str | None:
    """Return the game appid from the Steam env vars, or ``None`` if absent."""
    env = os.environ if environ is None else environ
    for var in ("STEAM_COMPAT_APPID", "SteamAppId"):
        value = env.get(var, "").strip()
        if value.isdigit():
            return value
    return None


def resolve_replacement(
    appid: str | None, config: ConfigParser
) -> tuple[str | None, list[str]]:
    """Resolve the active section and its replacement args.

    Returns a ``(section, replacement_args)`` tuple. ``section`` is ``None``
    when no appid-specific section matches, meaning the original command is
    kept unchanged.
    """
    if appid and config.has_section(appid):
        return appid, _split_command(config.get(appid, GENERIC_KEY))
    return None, []


def _split_command(command: str) -> list[str]:
    import shlex

    return shlex.split(command.strip())


def build_final_args(
    original: list[str], replacement_args: list[str]
) -> tuple[list[str], list[str]]:
    """Rebuild the final command, preserving the Proton scaffolding when applicable.

    Returns ``(final_args, replaced_target)`` where ``replaced_target`` is the
    slice of the original command that was replaced.
    """
    if not replacement_args:
        return list(original), []

    w_indexes = [i for i, t in enumerate(original) if t == PROTON_MARKER]
    if not w_indexes:
        return list(replacement_args), list(original)

    w_idx = w_indexes[-1]
    target = original[w_idx + 1 :]

    reaper_idx = next(
        (i for i, t in enumerate(original) if os.path.basename(t) == "reaper"),
        None,
    )

    if (
        reaper_idx is not None
        and os.path.basename(original[0]) == "steam-launch-wrapper"
    ):
        post_reaper = original[reaper_idx:]
        dash = next((i for i, t in enumerate(post_reaper) if t == "--"), None)
        if dash is not None:
            head = post_reaper[: dash + 1]  # reaper ... -- (first "--")
            launcher = original[0:2]  # steam-launch-wrapper -- (pattern at start)
            middle = original[reaper_idx + dash + 1 : w_idx + 1]
            return head + launcher + middle + replacement_args, target

    prefix = original[: w_idx + 1]
    return prefix + replacement_args, target
