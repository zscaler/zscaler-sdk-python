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


class SecurityPolicyAPI:
    def __init__(self, client: ZIAClient):
        self.rest = client

    def get_whitelist(self) -> BoxList:
        """
        Returns a list of whitelisted URLs.

        Returns:
            :obj:`BoxList`: A list of whitelisted URLs

        Examples:
            >>> for url in zia.security.get_whitelist():
            ...    pprint(url)

        """
        response = self.rest.get("security")

        # ZIA removes the whitelistUrls key from the JSON response when it's empty.
        if "whitelist_urls" in self.rest.get("security"):
            return response.whitelist_urls
        else:
            return BoxList()  # Return empty list so other methods in this class don't break

    def get_blacklist(self) -> BoxList:
        """
        Returns a list of blacklisted URLs.

        Returns:
            :obj:`BoxList`: A list of blacklisted URLs

        Examples:
            >>> for url in zia.security.get_blacklist():
            ...    pprint(url)

        """

        return self.rest.get("security/advanced").blacklist_urls

    def erase_whitelist(self) -> int:
        """
        Erases all URLs in the whitelist.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.security.erase_whitelist()

        """
        payload = {"whitelistUrls": []}

        return self.rest.put("security", json=payload).status_code

    def replace_whitelist(self, url_list: list) -> BoxList:
        """
        Replaces the existing whitelist with the URLs provided.

        Args:
            url_list (:obj:`list` of :obj:`str`):
                The list of URLs for the new whitelist.

        Returns:
            :obj:`BoxList`: The complete and updated whitelist.

        Examples:
            >>> zia.security.replace_whitelist(['example.com'])

        """

        payload = {"whitelistUrls": url_list}

        return self.rest.put("security", json=payload).whitelist_urls

    def add_urls_to_whitelist(self, url_list: list) -> BoxList:
        """
        Adds the provided URLs to the whitelist.

        Args:
            url_list (:obj:`list` of :obj:`str`):
                The list of URLs to be added.

        Returns:
            :obj:`BoxList`: The complete and updated whitelist.

        Examples:
            >>> zia.security.add_urls_to_whitelist(['example.com', 'web.example.com'])

        """

        # Get the current whitelist
        whitelist = self.get_whitelist()

        # Add existing URLs to whitelist
        whitelist.extend(url for url in url_list if url not in whitelist)

        payload = {"whitelistUrls": whitelist}

        return self.rest.put("security", json=payload).whitelist_urls

    def delete_urls_from_whitelist(self, url_list: list) -> BoxList:
        """
        Deletes the provided URLs from the whitelist.

        Args:
            url_list (:obj:`list` of :obj:`str`):
                The list of URLs to be deleted.

        Returns:
            :obj:`BoxList`: The complete and updated whitelist.

        Examples:
            >>> zia.security.delete_urls_from_whitelist(['example.com', 'web.example.com'])

        """
        # Get the current whitelist
        whitelist = self.get_whitelist()

        # If URLs provided, create new whitelist without them
        whitelist = [url for url in whitelist if url not in url_list]

        payload = {"whitelistUrls": whitelist}

        return self.rest.put("security", json=payload).whitelist_urls

    def add_urls_to_blacklist(self, url_list: list) -> BoxList:
        """
        Adds the provided URLs to the blacklist.

        Args:
            url_list (:obj:`list` of :obj:`str`):
                The list of URLs to be added.

        Returns:
            :obj:`BoxList`: The complete and updated blacklist.

        Examples:
            >>> zia.security.add_urls_to_blacklist(['example.com', 'web.example.com'])

        """

        payload = {"blacklistUrls": url_list}

        resp = self.rest.post("security/advanced/blacklistUrls?action=ADD_TO_LIST", json=payload).status_code

        # Return the object if it was updated successfully
        if resp == 204:
            return self.get_blacklist()

    def replace_blacklist(self, url_list: list) -> BoxList:
        """
        Replaces the existing blacklist with the URLs provided.

        Args:
            url_list (:obj:`list` of :obj:`str`):
                The list of URLs for the new blacklist.

        Returns:
            :obj:`BoxList`: The complete and updated blacklist.

        Examples:
            >>> zia.security.replace_blacklist(['example.com'])

        """

        payload = {"blacklistUrls": url_list}

        return self.rest.put("security/advanced", json=payload).blacklist_urls

    def erase_blacklist(self) -> int:
        """
        Erases all URLs in the blacklist.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.security.erase_blacklist()

        """

        payload = {"blacklistUrls": []}
        try:
            self.rest.put("security/advanced", json=payload)
            return "Blacklist successfully erased."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def delete_urls_from_blacklist(self, url_list: list) -> int:
        """
        Deletes the provided URLs from the blacklist.

        Args:
            url_list (:obj:`list` of :obj:`str`):
                The list of URLs to be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.security.delete_urls_from_blacklist(['example.com', 'web.example.com'])

        """

        payload = {"blacklistUrls": url_list}

        return self.rest.post(
            "security/advanced/blacklistUrls?action=REMOVE_FROM_LIST",
            json=payload,
        ).status_code
