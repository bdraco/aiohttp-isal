__version__ = "0.3.2"

import importlib
import logging
import zlib as zlib_original

import aiohttp

try:
    from isal import isal_zlib as best_zlib

    ISAL_AVAILABLE = True
except ImportError:
    ISAL_AVAILABLE = False

_LOGGER = logging.getLogger(__name__)

TARGETS = (
    "compression_utils",
    "http_writer",
    "http_websocket",
    "http_writer",
    "http_parser",
    "multipart",
    "web_response",
)


def enable_isal() -> None:
    """Enable isal."""
    if not ISAL_AVAILABLE:
        _LOGGER.warning(
            "isal is not available, falling back to zlib, performance will be degraded."
        )
        return

    for location in TARGETS:
        try:
            importlib.import_module(f"aiohttp.{location}")
        except ImportError:
            continue
        if module := getattr(aiohttp, location, None):
            module.zlib = best_zlib


def disable_isal() -> None:
    """Disable isal and restore the original zlib."""
    for location in TARGETS:
        if module := getattr(aiohttp, location, None):
            module.zlib = zlib_original
