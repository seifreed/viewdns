"""Real-code tests for the ViewDNS client and CLI.

Network tests hit the live ViewDNS.info API using the key in the ``VIEWDNS``
environment variable. They assert on response shape only, so they pass whether
the account has quota left or the API answers with an in-band error payload.
"""

from __future__ import annotations

import os
import runpy
import sys

import pytest

from viewdns import ViewDNSClient, ViewDNSError, render
from viewdns.cli import main

APIKEY = os.environ["VIEWDNS"]


def test_init_requires_apikey() -> None:
    with pytest.raises(ValueError, match="API key is required"):
        ViewDNSClient("")


def test_request_unknown_endpoint() -> None:
    with pytest.raises(ValueError, match="Unknown endpoint"):
        ViewDNSClient("dummy").request("does-not-exist")


def test_missing_required_parameter() -> None:
    with pytest.raises(ValueError, match="Missing required parameter"):
        ViewDNSClient("dummy").request("reverse-ip")


def test_unknown_parameter() -> None:
    with pytest.raises(ValueError, match="Unknown parameter"):
        ViewDNSClient("dummy").request("reverse-dns", ip="9.9.9.9", bogus="x")


def test_network_error_is_wrapped() -> None:
    client = ViewDNSClient("dummy", base_url="http://127.0.0.1:1", timeout=1.0)
    with pytest.raises(ViewDNSError, match="Network error"):
        client.request("reverse-dns", ip="9.9.9.9")


def test_json_endpoint_returns_object() -> None:
    result = ViewDNSClient(APIKEY).request("account", action="balance")
    assert isinstance(result, dict)


def test_xml_output_returns_text() -> None:
    result = ViewDNSClient(APIKEY).request("reverse-dns", output="xml", ip="9.9.9.9")
    assert isinstance(result, str)


def test_endpoint_without_output_returns_bytes() -> None:
    result = ViewDNSClient(APIKEY).request("newly-registered", date="not-a-date")
    assert isinstance(result, bytes)


def test_non_json_response_raises() -> None:
    client = ViewDNSClient(APIKEY, base_url="https://example.com")
    with pytest.raises(ViewDNSError, match="non-JSON"):
        client.request("reverse-dns", ip="9.9.9.9")


def test_cli_requires_apikey() -> None:
    with pytest.raises(SystemExit):
        main(["--apikey", "", "account", "--action", "balance"])


@pytest.mark.parametrize(
    ("extra_args", "marker"),
    [
        ([], "+"),  # table border
        (["--format", "json"], "{"),
        (["--format", "toon"], "monthly:"),
    ],
    ids=["table", "json", "toon"],
)
def test_cli_account_format(
    extra_args: list[str], marker: str, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = main(["--apikey", APIKEY, "account", "--action", "balance", *extra_args])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert marker in captured.out


def test_cli_xml_passthrough(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["--apikey", APIKEY, "whois", "--domain", "example.com", "--format", "xml"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.lstrip().startswith("<?xml")


def test_cli_writes_bytes(capsysbinary: pytest.CaptureFixture[bytes]) -> None:
    exit_code = main(["--apikey", APIKEY, "newly-registered", "--date", "not-a-date"])
    captured = capsysbinary.readouterr()
    assert exit_code == 0
    assert isinstance(captured.out, bytes)
    assert captured.out


def test_cli_reports_transport_error(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(
        ["--apikey", APIKEY, "--timeout", "0.000001", "account", "--action", "balance"]
    )
    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.err.startswith("error:")


def test_module_entrypoint() -> None:
    saved = sys.argv
    sys.argv = ["viewdns"]
    try:
        with pytest.raises(SystemExit):
            runpy.run_module("viewdns", run_name="__main__")
    finally:
        sys.argv = saved


# ---- render (offline, real data literals, no mocks) ----


def test_render_json() -> None:
    assert render({"a": 1}, "json").strip().startswith("{")


def test_render_toon() -> None:
    out = render({"records": [{"name": "g.com", "ttl": "1"}]}, "toon")
    assert "records[" in out


def test_render_table_error() -> None:
    out = render({"success": False, "error": {"code": 401, "message": "Invalid API key."}}, "table")
    assert "error" in out and "Invalid API key." in out


def test_render_table_dict_all_branches() -> None:
    data = {
        "response": {
            "count": "2",
            "items": [{"x": "1", "y": "2"}, {"x": "3"}],
            "tags": ["a", "b"],
            "info": {"k": "v"},
        }
    }
    out = render(data, "table")
    assert "count" in out  # meta scalar
    assert "items" in out and "x" in out  # list-of-dicts table
    assert "tags" in out  # scalar list table
    assert "info" in out and "k" in out  # nested dict table


def test_render_table_empty_list() -> None:
    out = render({"response": {"headers": []}}, "table")
    assert "headers" in out


def test_render_table_payload_is_list() -> None:
    out = render({"response": [{"domain": "a.com"}, {"domain": "b.com"}]}, "table")
    assert "domain" in out and "a.com" in out


def test_render_table_payload_is_scalar() -> None:
    assert render({"response": "ok"}, "table") == "ok"


def test_render_unknown_format_raises() -> None:
    with pytest.raises(ValueError, match="Unknown format"):
        render({"a": 1}, "yaml")


def test_render_table_nested_cell_compacted() -> None:
    out = render({"response": [{"ips": ["1.1.1.1", "2.2.2.2"]}]}, "table")
    assert '["1.1.1.1","2.2.2.2"]' in out
