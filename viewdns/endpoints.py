"""Declarative registry of every ViewDNS.info API endpoint.

Each :class:`Endpoint` maps a friendly CLI/library name to the real API path
and the query parameters it accepts, so the client and the CLI can be driven
from a single source of truth.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Endpoint:
    """A single ViewDNS API endpoint.

    ``accepts_output`` is ``False`` for endpoints that do not accept the
    ``output`` query parameter and return a raw payload (a downloadable file)
    instead of parsed JSON.
    """

    name: str
    path: str
    required: tuple[str, ...]
    optional: tuple[str, ...] = ()
    accepts_output: bool = True


ENDPOINTS: tuple[Endpoint, ...] = (
    Endpoint("abuse-contact", "abuselookup", ("domain",)),
    Endpoint("account", "account", ("action",)),
    Endpoint("chinese-firewall", "chinesefirewall", ("domain",)),
    Endpoint("dns-propagation", "propagation", ("domain",)),
    Endpoint("dns-record", "dnsrecord", ("domain",), ("recordtype",)),
    Endpoint("free-email", "freeemail", ("domain",)),
    Endpoint("http-headers", "httpheaders", ("domain",)),
    Endpoint("ip-history", "iphistory", ("domain",)),
    Endpoint("ip-location", "iplocation", ("ip",)),
    Endpoint("iran-firewall", "iranfirewall", ("siteurl",)),
    Endpoint("mac-lookup", "maclookup", ("mac",)),
    Endpoint("newly-registered", "nrd", ("date",), ("type",), accepts_output=False),
    Endpoint("ping", "ping/v2", ("host",)),
    Endpoint("port-scan", "portscan", ("host",)),
    Endpoint("reverse-dns", "reversedns", ("ip",)),
    Endpoint("reverse-ip", "reverseip", ("host",), ("page",)),
    Endpoint("reverse-mx", "reversemx", ("mx",), ("page",)),
    Endpoint("reverse-ns", "reversens", ("ns",), ("page",)),
    Endpoint("reverse-whois", "reversewhois", ("q",), ("page",)),
    Endpoint("spam-db", "spamdblookup", ("ip",)),
    Endpoint("subdomains", "subdomains", ("domain",)),
    Endpoint("traceroute", "traceroute", ("domain",)),
    Endpoint("whois", "whois/v2", ("domain",)),
)

ENDPOINTS_BY_NAME: dict[str, Endpoint] = {endpoint.name: endpoint for endpoint in ENDPOINTS}
