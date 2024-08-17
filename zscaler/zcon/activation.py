# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from box import Box
from zscaler.zcon.client import ZCONClient


class ActivationAPI:
    def __init__(self, client: ZCONClient):
        self.rest = client

    def activate(self, force: bool = False) -> Box:
        """
        Activate the configuration.

        Args:
            force (bool): If set to True, forces the activation. Default is False.

        Returns:
            :obj:`Box`: The status code of the operation.

        Examples:
            Activate the configuration without forcing::

                zcon.config.activate()

            Forcefully activate the configuration::

                zcon.config.activate(force=True)

        """
        if force:
            return self.rest.put("ecAdminActivateStatus/forcedActivate")
        else:
            return self.rest.put("ecAdminActivateStatus/activate")

    def get_status(self):
        """
        Get the status of the configuration.

        Returns:
            :obj:`Box`: The status of the configuration.

        Examples:
            Get the status of the configuration::

                print(zcon.config.get_status())

        """
        return self.rest.get("ecAdminActivateStatus")
