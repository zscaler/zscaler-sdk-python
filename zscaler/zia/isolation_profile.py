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
        Returns list of all the profiles in the Isolation Profile field for URL Filtering rules and Cloud App Control rules.

        Args:
            **kwargs: Optional keyword args.

        Keyword Args:

        Returns:
            :obj:`BoxList`: A list of isolation profile resource records.

        Examples:
            Get a list of all configured browser isolation profiles:
            >>> location = zia.isolation_profile.list_isolation_profiles()
        """
        payload = {snake_to_camel(key): value for key, value in kwargs.items()}
        return self.rest.get("browserIsolation/profiles", json=payload)

    # Search Cloud Browser Isolation By Name
    def get_profiles_by_name(self, name):
        profiles = self.list_isolation_profiles()
        for profile in profiles:
            if profile.get("name") == name:
                return profile
        return None

    # Search Cloud Browser Isolation By ID
    def get_profiles_by_id(self, profile_id):
        profiles = self.list_isolation_profiles()
        for profile in profiles:
            if profile.get("id") == profile_id:
                return profile
        return None
