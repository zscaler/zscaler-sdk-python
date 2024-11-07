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

from zscaler.zia import ZIAClient


class AppTotalAPI:
    def __init__(self, client: ZIAClient):
        self.rest = client

    def get_app(self, app_id: str, verbose: bool = False) -> Box:
        """
        Searches the AppTotal App Catalog by app ID. If the app exists in the catalog, the app's information is
        returned. If not, the app is submitted for analysis. After analysis is complete, a subsequent GET request is
        required to fetch the app's information.

        Args:
            app_id (str): The app ID to search for.
            verbose (bool, optional): Defaults to False.

        Returns:
            :obj:`Box`: The response object.

        Examples:
            Return verbose information on an app with ID 12345::

                zia.apptotal.get_app(app_id="12345", verbose=True)

        """
        params = {
            "app_id": app_id,
            "verbose": verbose,
        }
        return self.rest.get("apps/app", params=params)

    def scan_app(self, app_id: str) -> Box:
        """
        Submits an app for analysis in the AppTotal Sandbox. After analysis is complete, a subsequent GET request is
        required to fetch the app's information.

        Args:
            app_id (str): The app ID to scan.

        Returns:
            :obj:`Box`: The response object.

        Examples:
            Scan an app with ID 12345::

                zia.apptotal.scan_app(app_id="12345")

        """
        payload = {
            "appId": app_id,
        }
        return self.rest.post("apps/app", json=payload)
