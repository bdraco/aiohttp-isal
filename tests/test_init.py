import zlib as zlib_original
from unittest.mock import patch

import aiohttp.http_websocket
from isal import isal_zlib as expected_zlib

from aiohttp_isal import disable_isal, enable_isal


def test_enable_disable():
    """Test enable/disable."""
    assert aiohttp.http_websocket.zlib is zlib_original
    enable_isal()
    assert aiohttp.http_websocket.zlib is expected_zlib
    disable_isal()
    assert aiohttp.http_websocket.zlib is zlib_original
    enable_isal()
    assert aiohttp.http_websocket.zlib is expected_zlib
    disable_isal()


def test_isal_not_available():
    """Test isal not available."""
    with patch("aiohttp_isal.ISAL_AVAILABLE", False):
        enable_isal()
        assert aiohttp.http_websocket.zlib is zlib_original
        disable_isal()
        assert aiohttp.http_websocket.zlib is zlib_original
