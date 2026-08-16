"""HTTP client for the ViewDNS.info API."""

from __future__ import annotations

import http.client
import json
import urllib.parse
from typing import Any

from .endpoints import ENDPOINTS_BY_NAME, Endpoint

BASE_URL = "https://api.viewdns.info"
USER_AGENT = "viewdns-python"


class ViewDNSError(Exception):
    """Raised on transport failures or when a JSON response cannot be parsed.

    Application-level errors reported by the API itself (an invalid key, an
    exhausted quota, a rejected parameter) arrive as a structured ``error``
    body and are returned to the caller as data, not raised.
    """


class ViewDNSClient:
    """Thin client exposing every ViewDNS.info API endpoint through :meth:`request`."""

    def __init__(
        self,
        apikey: str,
        *,
        base_url: str = BASE_URL,
        timeout: float = 30.0,
    ) -> None:
        if not apikey:
            raise ValueError("An API key is required")
        self._apikey = apikey
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def request(
        self, name: str, *, output: str = "json", **params: str
    ) -> dict[str, Any] | str | bytes:
        """Call the endpoint registered under ``name`` and return its response.

        Returns the parsed object for JSON output, the decoded text body for XML
        output, and the raw ``bytes`` for endpoints that serve a downloadable
        file (which may be binary, e.g. the gzip-compressed ``newly-registered``
        feed).
        """
        endpoint = ENDPOINTS_BY_NAME.get(name)
        if endpoint is None:
            raise ValueError(f"Unknown endpoint: {name!r}")
        query = self._build_query(endpoint, params, output)
        path = f"/{endpoint.path}/?{urllib.parse.urlencode(query)}"
        body = self._fetch(path)
        if not endpoint.accepts_output:
            return body
        if output == "json":
            try:
                parsed: dict[str, Any] = json.loads(body)
            except json.JSONDecodeError as exc:
                raise ViewDNSError(f"Unexpected non-JSON response from ViewDNS: {exc}") from exc
            return parsed
        return body.decode("utf-8", errors="replace")

    def _build_query(
        self,
        endpoint: Endpoint,
        params: dict[str, str],
        output: str,
    ) -> dict[str, str]:
        allowed = set(endpoint.required) | set(endpoint.optional)
        for missing in endpoint.required:
            if missing not in params:
                raise ValueError(f"Missing required parameter: {missing!r}")
        for unknown in params:
            if unknown not in allowed:
                raise ValueError(f"Unknown parameter for {endpoint.name!r}: {unknown!r}")
        query = dict(params)
        query["apikey"] = self._apikey
        if endpoint.accepts_output:
            query["output"] = output
        return query

    def _fetch(self, path: str) -> bytes:
        parts = urllib.parse.urlsplit(self._base_url)
        if parts.scheme == "https":
            conn: http.client.HTTPConnection = http.client.HTTPSConnection(
                parts.netloc, timeout=self._timeout
            )
        else:
            conn = http.client.HTTPConnection(parts.netloc, timeout=self._timeout)
        try:
            conn.request("GET", path, headers={"User-Agent": USER_AGENT})
            response = conn.getresponse()
            return response.read()
        except OSError as exc:
            raise ViewDNSError(f"Network error contacting ViewDNS: {exc}") from exc
        finally:
            conn.close()
