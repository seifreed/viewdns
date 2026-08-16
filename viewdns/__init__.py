"""ViewDNS.info API client and CLI."""

from __future__ import annotations

from .client import BASE_URL, ViewDNSClient, ViewDNSError
from .endpoints import ENDPOINTS, ENDPOINTS_BY_NAME, Endpoint
from .render import render

__all__ = [
    "BASE_URL",
    "ENDPOINTS",
    "ENDPOINTS_BY_NAME",
    "Endpoint",
    "ViewDNSClient",
    "ViewDNSError",
    "render",
]

__version__ = "1.0.0"
