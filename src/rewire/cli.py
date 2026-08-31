"""Command-line entry point for rewire."""

import os
import shlex
import sys

from .config import load_config
from .core import build_final_args, detect_appid, resolve_replacement
from .log import setup_logging


def exec_command(args: list[str]) -> int:
    """Replace the current process with ``args``. Returns an exit code on error."""
    logger = setup_logging()
    if not args:
        logger.error("no command to run")
        return 1
    os.execvp(args[0], args)


def main(argv: list[str] | None = None) -> int:
    logger = setup_logging()
    raw = list(sys.argv[1:] if argv is None else argv)
    intercepted = shlex.join(raw) if raw else ""

    logger.info("intercepted command: %s", intercepted or "(empty)")

    if not raw:
        logger.error("no arguments received (expected Steam %%command%%)")
        return 1

    appid = detect_appid()
    config = load_config()

    section, replacement_args = resolve_replacement(appid, config)

    final_args = raw
    replaced_target: list[str] = []
    if section is None:
        logger.info("appid=%s no substitution; running default", appid)
    else:
        if not replacement_args:
            logger.error("section %s: empty replacement command", section)
            return 1
        final_args, replaced_target = build_final_args(raw, replacement_args)
        logger.info("substitution [%s]: %s", section, shlex.join(replacement_args))
        logger.info(
            "EXEC: appid=%s intercepted=%r | sent=%r | replaced_target=%r",
            appid,
            intercepted,
            shlex.join(final_args),
            shlex.join(replaced_target),
        )

    return exec_command(final_args)


if __name__ == "__main__":
    sys.exit(main())
