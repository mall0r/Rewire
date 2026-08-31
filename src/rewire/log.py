"""Logging setup for rewire."""

import logging
import sys

from .config import LOG_LEVEL, LOG_PATH


def setup_logging() -> logging.Logger:
    """Configure and return the ``rewire`` logger (idempotent/singleton)."""
    logger = logging.getLogger("rewire")
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.DEBUG))
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] pid=%(process)d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    except OSError as exc:
        logger.error("could not open log file %s: %s", LOG_PATH, exc)
        return logger

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(logging.Formatter("rewire: %(message)s"))
    logger.addHandler(console)

    return logger
