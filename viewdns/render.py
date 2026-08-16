"""Presentation helpers that turn a parsed ViewDNS response into text.

Kept separate from the client: the library core returns raw data, and callers
(the CLI, or library users who want it) choose how to display it.
"""

from __future__ import annotations

import json
from typing import Any

import toon
from prettytable import PrettyTable


def render(data: dict[str, Any], fmt: str) -> str:
    """Render a parsed JSON response as ``table``, ``json`` or ``toon`` text."""
    if fmt == "table":
        return _render_table(data)
    if fmt == "json":
        return json.dumps(data, indent=2)
    if fmt == "toon":
        encoded: str = toon.encode(data)
        return encoded
    raise ValueError(f"Unknown format: {fmt!r}")


def _cell(value: Any) -> str:
    """Stringify a cell, compacting nested structures so they stay on one line."""
    if isinstance(value, (dict, list)):
        return json.dumps(value, separators=(",", ":"))
    return str(value)


def _build_table(field_names: list[str], rows: list[list[str]], *, title: str | None = None) -> str:
    table = PrettyTable(field_names=field_names)
    if title is not None:
        table.title = title
    table.align = "l"
    for row in rows:
        table.add_row(row)
    return table.get_string()


def _kv_table(title: str, mapping: dict[str, Any]) -> str:
    rows = [[key, _cell(value)] for key, value in mapping.items()]
    return _build_table(["Field", "Value"], rows, title=title)


def _list_table(title: str, rows: list[dict[str, Any]]) -> str:
    columns = list(rows[0].keys())
    cells = [[_cell(row.get(column, "")) for column in columns] for row in rows]
    return _build_table(columns, cells, title=title)


def _scalar_list_table(title: str, items: list[Any]) -> str:
    return _build_table([title], [[_cell(item)] for item in items])


def _render_table(data: dict[str, Any]) -> str:
    error = data.get("error")
    if isinstance(error, dict):
        return _kv_table("error", error)

    payload = data.get("response", data)
    if isinstance(payload, dict):
        return _render_dict(payload)
    if _is_row_list(payload):
        return _list_table("response", payload)
    return _cell(payload)


def _render_dict(payload: dict[str, Any]) -> str:
    tables: list[str] = []
    meta: dict[str, Any] = {}
    for key, value in payload.items():
        if _is_row_list(value):
            tables.append(_list_table(key, value))
        elif isinstance(value, list):
            tables.append(_scalar_list_table(key, value))
        elif isinstance(value, dict):
            tables.append(_kv_table(key, value))
        else:
            meta[key] = value
    if meta:
        tables.insert(0, _kv_table("response", meta))
    return "\n\n".join(tables)


def _is_row_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict)
