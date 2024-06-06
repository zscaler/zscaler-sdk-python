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


class AuthDomainsAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def get_auth_domains(self) -> Box:
        """
        Returns information on authentication domains.

        Args:
            group_id (str):
                The unique identifier for the authentication domains.

        Returns:
            :obj:`Box`: The resource record for the authentication domains.

        Examples:
            >>> pprint(zpa.authdomains.get_auth_domains())

        """
        return self.rest.get("authDomains")
