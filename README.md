<p align="center">
  <img src="https://img.shields.io/badge/viewdns-ViewDNS.info%20API%20client-blue?style=for-the-badge" alt="viewdns">
</p>

<h1 align="center">viewdns</h1>

<p align="center">
  <strong>CLI and Python library for every ViewDNS.info API endpoint</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/viewdns/"><img src="https://img.shields.io/pypi/v/viewdns?style=flat-square&logo=pypi&logoColor=white" alt="PyPI Version"></a>
  <a href="https://pypi.org/project/viewdns/"><img src="https://img.shields.io/pypi/pyversions/viewdns?style=flat-square&logo=python&logoColor=white" alt="Python Versions"></a>
  <a href="https://github.com/seifreed/viewdns/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License"></a>
  <a href="https://github.com/seifreed/viewdns/actions"><img src="https://img.shields.io/github/actions/workflow/status/seifreed/viewdns/ci.yml?style=flat-square&logo=github&label=CI" alt="CI Status"></a>
  <a href="#"><img src="https://img.shields.io/badge/coverage-100%25-brightgreen?style=flat-square" alt="Coverage"></a>
</p>

<p align="center">
  <a href="https://github.com/seifreed/viewdns/stargazers"><img src="https://img.shields.io/github/stars/seifreed/viewdns?style=flat-square" alt="GitHub Stars"></a>
  <a href="https://github.com/seifreed/viewdns/issues"><img src="https://img.shields.io/github/issues/seifreed/viewdns?style=flat-square" alt="GitHub Issues"></a>
  <a href="https://buymeacoffee.com/seifreed"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-yellow?style=flat-square&logo=buy-me-a-coffee&logoColor=white" alt="Buy Me a Coffee"></a>
</p>

---

## Overview

**viewdns** is a Python toolkit that covers **every** endpoint of the
[ViewDNS.info API](https://viewdns.info/api/documentation/) — reverse IP, WHOIS,
DNS records, port scanning, IP geolocation, spam-database lookups, and more. It
works both as a command-line tool and as an importable library, prints readable
tables by default, and also speaks JSON, TOON, and raw XML. The HTTP layer uses
only the Python standard library.

### Key Features

| Feature | Description |
|---------|-------------|
| **All 23 endpoints** | Complete coverage of the ViewDNS.info API from a single interface |
| **Table by default** | Human-readable output rendered with [prettytable](https://pypi.org/project/prettytable/) |
| **Multi-format** | `table`, `json`, `toon` (Token-Oriented Object Notation), and raw `xml` |
| **CLI + Library** | Use as a command-line tool or a typed Python package |
| **File downloads** | Streams the gzip-compressed Newly Registered Domains feed as raw bytes |
| **Typed & tested** | Fully type-checked (`mypy --strict`), 100% test coverage, no mocks |
| **Zero-dependency HTTP** | Transport built on `http.client` from the standard library |

### Supported Outputs

```text
Structured data   table (prettytable), json, toon
Passthrough       xml (raw API payload)
File feeds        newly-registered -> gzip bytes (redirect to a file)
Errors            API errors rendered as a key/value table
```

---

## Installation

### From PyPI (Recommended)

```bash
pip install viewdns
```

Set your API key once (get one from your ViewDNS.info account):

```bash
export VIEWDNS=your_api_key
```

### From Source

```bash
git clone https://github.com/seifreed/viewdns.git
cd viewdns
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

---

## Quick Start

```bash
# Reverse IP lookup (table by default)
viewdns reverse-ip --host google.com

# WHOIS for a domain
viewdns whois --domain example.com

# DNS records of a given type
viewdns dns-record --domain example.com --recordtype MX

# Your account balance
viewdns account --action balance
```

---

## Usage

### Command Line Interface

```bash
# JSON output
viewdns ip-location --ip 8.8.8.8 --format json

# TOON output
viewdns dns-record --domain google.com --recordtype A --format toon

# Raw XML from the API
viewdns whois --domain example.com --format xml

# Download the gzip Newly Registered Domains feed
viewdns newly-registered --date 2026-08-14 > nrd.txt.gz
```

`--format` selects the output (`table` default, `json`, `toon`, `xml`);
`--apikey` overrides `$VIEWDNS`; `--timeout` sets the request timeout in
seconds. Global options work before or after the subcommand. Run
`viewdns --help` for the full command list.

### Endpoints

| Command | API path | Required | Optional |
|---|---|---|---|
| `abuse-contact` | `abuselookup` | `domain` | |
| `account` | `account` | `action` | |
| `chinese-firewall` | `chinesefirewall` | `domain` | |
| `dns-propagation` | `propagation` | `domain` | |
| `dns-record` | `dnsrecord` | `domain` | `recordtype` |
| `free-email` | `freeemail` | `domain` | |
| `http-headers` | `httpheaders` | `domain` | |
| `ip-history` | `iphistory` | `domain` | |
| `ip-location` | `iplocation` | `ip` | |
| `iran-firewall` | `iranfirewall` | `siteurl` | |
| `mac-lookup` | `maclookup` | `mac` | |
| `newly-registered` | `nrd` | `date` | `type` |
| `ping` | `ping/v2` | `host` | |
| `port-scan` | `portscan` | `host` | |
| `reverse-dns` | `reversedns` | `ip` | |
| `reverse-ip` | `reverseip` | `host` | `page` |
| `reverse-mx` | `reversemx` | `mx` | `page` |
| `reverse-ns` | `reversens` | `ns` | `page` |
| `reverse-whois` | `reversewhois` | `q` | `page` |
| `spam-db` | `spamdblookup` | `ip` | |
| `subdomains` | `subdomains` | `domain` | |
| `traceroute` | `traceroute` | `domain` | |
| `whois` | `whois/v2` | `domain` | |

### Format Flags

| Option | Description |
|--------|-------------|
| `--format table` | Human-readable tables (default) |
| `--format json` | Pretty-printed JSON |
| `--format toon` | Token-Oriented Object Notation |
| `--format xml` | Raw XML payload from the API |
| `--apikey <key>` | API key (defaults to `$VIEWDNS`) |
| `--timeout <seconds>` | Request timeout |

---

## Python Library

### Basic Usage

```python
from viewdns import ViewDNSClient

client = ViewDNSClient("your_api_key")
data = client.request("reverse-ip", host="google.com")
whois = client.request("whois", domain="example.com")
xml = client.request("ip-location", ip="9.9.9.9", output="xml")
```

`request` returns parsed JSON (a `dict`) by default, the decoded text for
`output="xml"`, and raw `bytes` for endpoints that serve a downloadable file.
Transport failures and unparseable responses raise `ViewDNSError`; invalid
arguments raise `ValueError`. API-level problems (bad key, exhausted quota,
missing subscription) come back inside the response payload.

### Downloading a File Feed

```python
gz = client.request("newly-registered", date="2026-08-14")  # bytes
with open("nrd.txt.gz", "wb") as f:
    f.write(gz)
```

### Rendering Responses

```python
from viewdns import render

print(render(data, "table"))  # or "json" / "toon"
```

---

## Requirements

- Python 3.14+
- Runtime dependencies: `prettytable`, `python-toon`
- See [pyproject.toml](pyproject.toml) for the full list and dev extras

---

## Development

```bash
pip install -e ".[dev]"
black --check . && ruff check . && mypy .
bandit -r viewdns && pip-audit
pytest
```

Tests run real code against the live API (no mocks) and require `$VIEWDNS`.

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Support the Project

If this project is useful in your workflows, you can support development:

<a href="https://buymeacoffee.com/seifreed" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50">
</a>

---

## License

This project is licensed under the MIT license. See [LICENSE](LICENSE).

**Attribution**
- Author: **Marc Rivero López** | [@seifreed](https://github.com/seifreed)
- Repository: [github.com/seifreed/viewdns](https://github.com/seifreed/viewdns)

---

<p align="center">
  <sub>Built for practical DNS/OSINT research and security automation</sub>
</p>
