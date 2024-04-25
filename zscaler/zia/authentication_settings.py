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


from box import BoxList

from zscaler.zia import ZIAClient


class AuthenticationSettingsAPI:
    def __init__(self, client: ZIAClient):
        self.rest = client

    def get_exempted_urls(self) -> BoxList:
        """
        Returns a list of exempted URLs.

        Returns:
            :obj:`BoxList`: A list of exempted URLs

        Examples:
            >>> for url in zia.authentication_settings.get_exempted_urls():
            ...    pprint(url)
        """
        response = self.rest.get("authSettings/exemptedUrls")

        # Ensure the correct attribute key is used in the response check.
        if "urls" in response:
            return response.urls
        else:
            return BoxList()

    def add_urls_to_exempt_list(self, url_list: list) -> BoxList:
        """
        Adds the provided URLs to the exempt list.

        Args:
            url_list (:obj:`list` of :obj:`str`):
                The list of URLs to be added.

        Returns:
            :obj:`BoxList`: The complete and updated exempt list.

        """

        payload = {"urls": url_list}

        resp = self.rest.post("authSettings/exemptedUrls?action=ADD_TO_LIST", json=payload)

        # Check if the response object has a 'status_code' attribute before accessing it
        if hasattr(resp, "status_code"):
            if resp.status_code == 204:
                return self.get_exempted_urls()
        else:
            # Handle case where resp is a Box object
            if "urls" in resp:
                return resp.urls
            else:
                return BoxList()  # Return empty list if no URLs are present

    def delete_urls_from_exempt_list(self, url_list: list) -> BoxList:
        """
        Deletes the provided URLs from the exemption list.

        Args:
            url_list (:obj:`list` of :obj:`str`):
                The list of URLs to be removed.

        Returns:
            :obj:`BoxList`: The updated exemption list.

        Examples:
            >>> zia.authentication_settings.delete_urls_from_exempt_list(['example.com'])

        """
        payload = {"urls": url_list}
        resp = self.rest.post("authSettings/exemptedUrls?action=REMOVE_FROM_LIST", json=payload)

        # Return the updated exemption list if the removal was successful.
        if resp == 200:
            return self.get_exempted_urls()
