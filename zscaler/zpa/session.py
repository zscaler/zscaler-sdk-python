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


from restfly import APISession
from restfly.endpoint import APIEndpoint


class AuthenticatedSessionAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)

        self.url_base = api.url_base

    def create_token(self, client_id: str, client_secret: str):
        """
        Creates a ZPA authentication token.

        Args:
            client_id (str): The ZPA API Client ID.
            client_secret (str): The ZPA API Client Secret Key.

        Returns:
            :obj:`dict`: The authenticated session information.

        Examples:
            >>> zpa.session.create(client_id='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx==',
            ...    client_secret='yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')

        """

        payload = {"client_id": client_id, "client_secret": client_secret}

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        return self._post(f"{self.url_base}/signin", headers=headers, data=payload).access_token
