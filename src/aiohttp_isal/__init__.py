__version__ = "0.1.0"

import importlib
import zlib as zlib_original

import aiohttp
from isal import isal_zlib as best_zlib

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
