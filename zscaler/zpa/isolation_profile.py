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

from zscaler.zpa.client import ZPAClient


class IsolationProfileAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_profiles(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured isolation profiles.

        Keyword Args:
            max_items (int): The maximum number of items to request before stopping iteration.
            max_pages (int): The maximum number of pages to request before stopping iteration.
            pagesize (int): Specifies the page size. The default size is 20, but the maximum size is 500.
            search (str, optional): The search string used to match against features and fields.

        Returns:
            BoxList: A list of all configured isolation profiles.

        Examples:
            >>> for isolation_profile in zpa.isolation_profiles.list_profiles():
            ...     pprint(isolation_profile)
        """
        list, _ = self.rest.get_paginated_data(path="/isolation/profiles", **kwargs)
        return list

    def get_profile_by_name(self, name: str):
        """
        Retrieves a specific isolation profile by its name.

        Args:
            name (str): The name of the isolation profile to search for.

        Returns:
            dict or None: The isolation profile with the specified name if found, otherwise None.

        Examples:
            >>> profile = zpa.isolation_profiles.get_profile_by_name('DefaultProfile')
            >>> print(profile)
        """
        profiles = self.list_profiles()
        for profile in profiles:
            if profile.get("name") == name:
                return profile
        return None

    def get_profile_by_id(self, profile_id: str):
        """
        Retrieves a specific isolation profile by its unique identifier (ID).

        Args:
            profile_id (str): The ID of the isolation profile to retrieve.

        Returns:
            dict or None: The isolation profile with the specified ID if found, otherwise None.

        Examples:
            >>> profile = zpa.isolation_profiles.get_profile_by_id('12345')
            >>> print(profile)
        """
        profiles = self.list_profiles()
        for profile in profiles:
            if str(profile.get("id")) == str(profile_id):  # Ensuring ID comparison as strings
                return profile
        return None
