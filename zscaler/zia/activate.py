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


from zscaler.zia import ZIAClient


class ActivationAPI:
    def __init__(self, client: ZIAClient):
        self.rest = client

    def status(self) -> str:
        """
        Returns the activation status for a configuration change.

        Returns:
            :obj:`str`
                Configuration status.

        Examples:
            >>> config_status = zia.config.status()

        """
        return self.rest.get("status").status

    def activate(self) -> str:
        """
        Activates configuration changes.

        Returns:
            :obj:`str`
                Configuration status.

        Examples:
            >>> config_activate = zia.config.activate()

        """
        return self.rest.post("status/activate").status
