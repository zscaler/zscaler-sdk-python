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

from zscaler.utils import snake_to_camel
from zscaler.zia.client import ZIAClient


class IsolationProfileAPI:
    def __init__(self, client: ZIAClient):
        self.rest = client

    def list_isolation_profiles(self, **kwargs) -> BoxList:
        """
        Returns a list of all profiles in the Isolation Profile field for URL Filtering rules and Cloud App Control rules.

        Args:
            **kwargs: Optional keyword arguments to refine the search query.

        Returns:
            :obj:`BoxList`: A list of isolation profile resource records.

        Examples:
            >>> isolation_profiles = zia.isolation_profiles.list_isolation_profiles()

        """
        payload = {snake_to_camel(key): value for key, value in kwargs.items()}
        return self.rest.get("browserIsolation/profiles", json=payload)

    def get_profiles_by_name(self, name: str):
        """
        Retrieves a specific isolation profile by its name.

        Args:
            name (str): The name of the isolation profile to retrieve.

        Returns:
            :obj:`Box`: The isolation profile if found, otherwise None.

        Examples:
            >>> profile = zia.isolation_profiles.get_profiles_by_name('Default Isolation')
            ...    print(profile)
        """
        profiles = self.list_isolation_profiles()
        for profile in profiles:
            if profile.get("name") == name:
                return profile
        return None

    def get_profiles_by_id(self, profile_id: str):
        """
        Retrieves a specific isolation profile by its unique identifier.

        Args:
            profile_id (str): The ID of the isolation profile to retrieve.

        Returns:
            :obj:`Box`: The isolation profile if found, otherwise None.

        Examples:
            >>> profile = zia.isolation_profiles.get_profiles_by_id('12345')
            ...    print(profile)
        """
        profiles = self.list_isolation_profiles()
        for profile in profiles:
            if profile.get("id") == profile_id:
                return profile
        return None
