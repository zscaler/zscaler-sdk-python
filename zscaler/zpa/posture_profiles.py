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


from box import Box, BoxList
from requests import Response

from zscaler.utils import remove_cloud_suffix

from . import ZPAClient


class PostureProfilesAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_profiles(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured posture profiles.

        Keyword Args:
            max_items (int):
                The maximum number of items to request before stopping iteration.
            max_pages (int):
                The maximum number of pages to request before stopping iteration.
            pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            search (str, optional):
                The search string used to match against features and fields.

        Returns:
            BoxList: A list of all configured posture profiles.

        Examples:
            >>> for posture_profile in zpa.posture_profiles.list_profiles():
            ...    pprint(posture_profile)
        """
        list, _ = self.rest.get_paginated_data(path="/posture", **kwargs, api_version="v2")
        return list

    def get_profile_by_name(self, name):
        """
        Searches for and returns a posture profile based on its name.

        This method performs a case-sensitive search through all posture profiles,
        returning the first profile that matches the specified name exactly.

        Args:
            name (str): The name of the posture profile to search for.

        Returns:
            Box: The posture profile that matches the given name, or None if no match is found.

        Examples:
            >>> profile = zpa.posture_profiles.get_profile_by_name("Example Profile Name")
            >>> if profile:
            ...     print("Profile ID:", profile.id)
            ... else:
            ...     print("Profile not found.")
        """
        profiles = self.list_profiles()
        for profile in profiles:
            if profile.get("name") == name:
                return profile
        return None

    def get_profile(self, profile_id: str) -> Box:
        """
        Returns information on the specified posture profiles.

        Args:
            profile_id (str):
                The unique identifier for the posture profiles.

        Returns:
            :obj:`Box`: The resource record for the posture profiles.

        Examples:
            >>> pprint(zpa.posture_profiles.get_profile('99999'))

        """
        response = self.rest.get("/posture/%s" % (profile_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response

    def get_udid_by_profile_name(self, search_name: str, **kwargs) -> str:
        """
        Searches for a posture profile by name and returns its posture_udid.

        This function searches through all configured posture profiles, comparing the
        provided search_name against each profile's name, both exactly and with any cloud suffix removed.
        It returns the 'posture_udid' of the first matching profile found.

        Args:
            search_name (str): The name of the posture profile to search for.

        Keyword Args:
            **kwargs: Additional keyword arguments to pass to the list_profiles method, such as
                    'max_items', 'max_pages', 'pagesize', and 'search'.

        Returns:
            str: The posture_udid of the found posture profile, or None if not found.

        Examples:
            >>> udid = zpa.posture_profiles.get_udid_by_profile_name("Example Profile")
            >>> if udid:
            ...     print(f"Found Profile UDID: {udid}")
            ... else:
            ...     print("Profile not found.")
        """
        profiles = self.list_profiles(**kwargs)
        for profile in profiles:
            clean_profile_name = remove_cloud_suffix(profile.get("name"))
            if clean_profile_name == search_name or profile.get("name") == search_name:
                return profile.get("posture_udid")
        return None

    def get_name_by_posture_udid(self, search_udid: str, **kwargs) -> str:
        """
        Searches for a posture profile by posture_udid and returns its name.

        Args:
            search_udid (str): The posture_udid of the posture profile to search for.

        Keyword Args:
            **kwargs: Additional keyword arguments to pass to the list_profiles method.

        Returns:
            str: The name of the found posture profile, or None if not found.
        """
        profiles = self.list_profiles(**kwargs)
        for profile in profiles:
            if profile.get("posture_udid") == search_udid:
                return profile.get("name")
        return None
