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

from __future__ import annotations

from typing import TYPE_CHECKING

from zscaler.ztb.alarms import AlarmsAPI

if TYPE_CHECKING:
    from zscaler.oneapi_client import Client


class ZTBService:
    """
    ZTB Service client, exposing Zero Trust Branch API resources.

    This service is used via the OneAPI authentication path
    (``ZscalerClient`` / ``Client``).  For standalone / legacy token-based
    access, use ``LegacyZTBClient`` or ``LegacyZTBClientHelper`` directly.
    """

    def __init__(self, client: "Client") -> None:
        self._request_executor = client.get_request_executor()

    @property
    def alarms(self) -> AlarmsAPI:
        """Interface for the ZTB Alarms API."""
        return AlarmsAPI(self._request_executor)
