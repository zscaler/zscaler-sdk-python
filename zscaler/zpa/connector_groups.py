# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


from warnings import warn

from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from zscaler.utils import Iterator


class ConnectorGroupsAPI(APIEndpoint):
    def list_groups(self, **kwargs) -> BoxList:
        """
        Returns a list of all connector groups.

        Warnings:
            .. deprecated:: 0.13.0
                Use :func:`zpa.connectors.list_connector_groups` instead.

        Returns:
            :obj:`BoxList`: List of all configured connector groups.

        Examples:
            >>> connector_groups = zpa.connector_groups.list_groups()

        """
        warn(
            "This endpoint is deprecated and will eventually be removed. "
            "Use zpa.connectors.list_connector_groups() instead."
        )

        return BoxList(Iterator(self._api, "appConnectorGroup", **kwargs))

    def get_group(self, group_id: str) -> Box:
        """
        Get information for a specified connector group.

        Warnings:
            .. deprecated:: 0.13.0
                Use :func:`zpa.connectors.get_connector_group` instead.

        Args:
            group_id (str):
                The unique identifier for the connector group.

        Returns:
            :obj:`Box`:
                The connector group resource record.

        Examples:
            >>> connector_group = zpa.connector_groups.get_group('2342342354545455')

        """
        warn(
            "This endpoint is deprecated and will eventually be removed. " "Use zpa.connectors.get_connector_group() instead."
        )

        return self._get(f"appConnectorGroup/{group_id}")
