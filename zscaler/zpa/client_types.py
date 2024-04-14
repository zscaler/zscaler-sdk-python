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

from box import Box

from zscaler.zpa.client import ZPAClient


class ClientTypesAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_client_types(self) -> Box:
        """
        Returns a list of ZPA Access Policy supported Client Types.

        Returns:
            :obj:`BoxList`: A list containing the ZPA Access Policy supported Client Types.

        Examples:
            Iterate over the ZPA Access Policy supported Client Types and print each one:

            .. code-block:: python

                for client_type in zpa.client_types.list_client_types():
                    print(client_type)

        """
        list, _ = self.rest.get_paginated_data(
            path="/clientTypes",
        )
        return list
