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
from restfly.endpoint import APIEndpoint

from zscaler.utils import obfuscate_api_key


class AuthenticatedSessionAPI(APIEndpoint):
    def status(self) -> Box:
        """
        Returns the status of the authentication session if it exists.

        Returns:
            :obj:`Box`: Session authentication information.

        Examples:
            >>> print(zia.session.status())

        """
        return self._get("authenticatedSession")

    def create(self, api_key: str, username: str, password: str) -> Box:
        """
        Creates a ZIA authentication session.

        Args:
            api_key (str): The ZIA API Key.
            username (str): Username of admin user for the authentication session.
            password (str): Password of the admin user for the authentication session.

        Returns:
            :obj:`Box`: The authenticated session information.

        # THIS IS A FAKE (EXAMPLE) USERNAME AND PASSWORD AND NOT USED IN PRODUCTION
        Examples:
            >>> zia.session.create(api_key='12khsdfh3289',
            ...    username='admin@example.com',
            ...    password='MyInsecurePassword')


        """
        api_obf = obfuscate_api_key(api_key)

        payload = {
            "apiKey": api_obf["key"],
            "username": username,
            "password": password,
            "timestamp": api_obf["timestamp"],
        }

        return self._post("authenticatedSession", json=payload)

    def delete(self) -> int:
        """
        Ends an authentication session.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            >>> zia.session.delete()

        """
        return self._delete("authenticatedSession", box=False).status_code
