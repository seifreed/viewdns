"""Command-line interface for the ViewDNS.info API."""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence

from .client import ViewDNSClient, ViewDNSError
from .endpoints import ENDPOINTS, ENDPOINTS_BY_NAME
from .render import render


def _add_global_options(parser: argparse.ArgumentParser, *, with_defaults: bool) -> None:
    """Add the shared options.

    ``with_defaults`` is True on the top-level parser (real defaults) and False
    on each subparser, where the defaults are suppressed so options placed after
    the subcommand override the top-level ones instead of resetting them.
    """
    apikey_default = os.environ.get("VIEWDNS") if with_defaults else argparse.SUPPRESS
    format_default = "table" if with_defaults else argparse.SUPPRESS
    timeout_default = 30.0 if with_defaults else argparse.SUPPRESS
    parser.add_argument(
        "--apikey",
        default=apikey_default,
        help="API key (defaults to the VIEWDNS environment variable)",
    )
    parser.add_argument(
        "--format",
        dest="format",
        choices=("table", "json", "toon", "xml"),
        default=format_default,
        help="output format (default: table)",
    )
    parser.add_argument(
        "--timeout", type=float, default=timeout_default, help="request timeout in seconds"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="viewdns", description="ViewDNS.info API client")
    _add_global_options(parser, with_defaults=True)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for endpoint in ENDPOINTS:
        command = subparsers.add_parser(endpoint.name, help=f"/{endpoint.path}/ endpoint")
        _add_global_options(command, with_defaults=False)
        for name in endpoint.required:
            command.add_argument(f"--{name}", required=True)
        for name in endpoint.optional:
            command.add_argument(f"--{name}")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.apikey:
        parser.error("no API key: pass --apikey or set the VIEWDNS environment variable")
    endpoint = ENDPOINTS_BY_NAME[args.command]
    params = {
        name: getattr(args, name)
        for name in (*endpoint.required, *endpoint.optional)
        if getattr(args, name) is not None
    }
    api_output = "xml" if args.format == "xml" else "json"
    client = ViewDNSClient(args.apikey, timeout=args.timeout)
    try:
        result = client.request(args.command, output=api_output, **params)
    except (ViewDNSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if isinstance(result, bytes):
        sys.stdout.buffer.write(result)
    elif isinstance(result, str):
        print(result)
    else:
        print(render(result, args.format))
    return 0
