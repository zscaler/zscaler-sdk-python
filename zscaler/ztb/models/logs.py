# flake8: noqa
"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from typing import Any, Dict, List, Optional

from pydash.strings import camel_case

from zscaler.oneapi_object import ZscalerObject


def _get(config: dict, snake_key: str, default=None):
    """Get from config with camelCase or snake_case fallback."""
    if not config:
        return default
    v = config.get(snake_key)
    if v is not None:
        return v
    return config.get(camel_case(snake_key), default)


# ---------------------------------------------------------------------------
# GET /api/logs - visibility chart: node "d" object
# ---------------------------------------------------------------------------


class VisibilityChartNodeData(ZscalerObject):
    """Node data (d) for type=node in visibility chart."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.cid = _get(config, "cid")
            self.created = _get(config, "created")
            self.display_name = _get(config, "display_name")
            self.name = _get(config, "name")
            self.siteid = _get(config, "siteid")
            self.type = _get(config, "type")
        else:
            self.cid = None
            self.created = None
            self.display_name = None
            self.name = None
            self.siteid = None
            self.type = None


# ---------------------------------------------------------------------------
# Visibility chart item: node or link (union)
# ---------------------------------------------------------------------------


class VisibilityChartItem(ZscalerObject):
    """
    Single item in visibility chart data array (node or link).
    For type=node: has d (node data), id.
    For type=link: has d (flows), id, id1, id2.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.type = _get(config, "type")
            self.id = _get(config, "id")
            self.id1 = _get(config, "id1")
            self.id2 = _get(config, "id2")
            self.d = config.get("d")
        else:
            self.type = None
            self.id = None
            self.id1 = None
            self.id2 = None
            self.d = None


# ---------------------------------------------------------------------------
# GET /api/logs - result wrapper
# ---------------------------------------------------------------------------


class VisibilityChartData(ZscalerObject):
    """Result from GET /api/logs (visibility chart data)."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            inner = config.get("result") or config
            if isinstance(inner, dict):
                raw_data = inner.get("data") or []
                self.data = [VisibilityChartItem(item) for item in raw_data]
                self.data_type = _get(inner, "data_type")
            else:
                self.data = []
                self.data_type = None
        else:
            self.data = []
            self.data_type = None
