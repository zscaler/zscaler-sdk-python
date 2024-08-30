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

from zscaler.utils import snake_to_camel

from . import ZPAClient


class SegmentGroupsAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_groups(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured segment groups.

        Returns:
            :obj:`BoxList`: A list of all configured segment groups.

        Examples:
            >>> for segment_group in zpa.segment_groups.list_groups():
            ...    pprint(segment_group)

        """
        list, _ = self.rest.get_paginated_data(path="/segmentGroup", **kwargs, api_version="v1")
        return list

    def get_group(self, group_id: str, **kwargs) -> Box:
        """
        Returns information on the specified segment group.

        Args:
            group_id (str): The unique identifier for the segment group.

        Returns:
            :obj:`Box`: The resource record for the segment group.

        Examples:
            >>> pprint(zpa.segment_groups.get_group('99999'))

        """
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.get(f"segmentGroup/{group_id}", params=params)

    def get_segment_group_by_name(self, name: str, **kwargs) -> Box:
        """
        Returns information on the segment group with the specified name.

        Args:
            name (str): The name of the segment group.

        Returns:
            :obj:`Box` or None: The resource record for the segment group if found, otherwise None.

        Examples:
            >>> segment_group = zpa.segment_groups.get_segment_group_by_name('example_name')
            >>> if segment_group:
            ...     pprint(segment_group)
            ... else:
            ...     print("Segment group not found")
        """
        groups = self.list_groups(**kwargs)
        for group in groups:
            if group.get("name") == name:
                return group
        return None

    def add_group(self, name: str, enabled: bool = True, **kwargs) -> Box:
        """
        Adds a new segment group.

        Args:
            name (str): The name of the new segment group.
            enabled (bool): Enable the segment group. Defaults to True.
            **kwargs:

        Keyword Args:
            application_ids (:obj:`list` of :obj:`dict`):
                Unique application IDs to associate with the segment group.
            description (str):
                A description for the segment group.
            microtenant_id (str):
                The microtenant ID to be used for this request.

        Returns:
            :obj:`Box`: The resource record for the newly created segment group.

        Examples:
            Creating a segment group with the minimum required parameters:

            >>> zpa.segment_groups.add_group('new_segment_group',
            ...    True)

        """
        payload = {
            "name": name,
            "enabled": enabled,
        }

        if kwargs.get("application_ids"):
            payload["applications"] = [{"id": app_id} for app_id in kwargs.pop("application_ids")]

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post("segmentGroup", json=payload, params=params)
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_group(self, group_id: str, **kwargs) -> Box:
        """
        Updates an existing segment group.

        Args:
            group_id (str): The unique identifier for the segment group to be updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the new segment group.
            enabled (bool): Enable the segment group.
            application_ids (:obj:`list` of :obj:`dict`): Unique application IDs to associate with the segment group.
            config_space (str): The config space for the segment group. Can either be DEFAULT or SIEM.
            description (str): A description for the segment group.
            policy_migrated (bool):
            microtenant_id (str): The microtenant ID to be used for this request.

        Returns:
            :obj:`Box`: The resource record for the updated segment group.

        Examples:
            Updating the name of a segment group:

            >>> zpa.segment_groups.update_group('99999',
            ...    name='updated_name')

        """
        payload = {snake_to_camel(k): v for k, v in self.get_group(group_id).items()}

        if kwargs.get("application_ids"):
            payload["applications"] = [{"id": app_id} for app_id in kwargs.pop("application_ids")]

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        resp = self.rest.put(f"segmentGroup/{group_id}", json=payload, params=params).status_code
        if not isinstance(resp, Response):
            return self.get_group(group_id)

    # REQUIRES DEPLOYMENT OF ET-76506 IN PRODUCTION BEFORE ENABLING IT.
    def update_group_v2(self, group_id: str, **kwargs) -> Box:
        """
        Updates an existing segment group using v2 endpoint.

        Args:
            group_id (str): The unique identifier for the segment group to be updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the new segment group.
            enabled (bool): Enable the segment group.
            application_ids (:obj:`list` of :obj:`dict`): Unique application IDs to associate with the segment group.
            config_space (str): The config space for the segment group. Can either be DEFAULT or SIEM.
            description (str): A description for the segment group.
            policy_migrated (bool):
            microtenant_id (str): The microtenant ID to be used for this request.

        Returns:
            :obj:`Box`: The resource record for the updated segment group.

        Examples:
            Updating the name of a segment group:

            >>> zpa.segment_groups.update_group_v2('99999',
            ...    name='updated_name')

        """
        payload = {snake_to_camel(k): v for k, v in self.get_group(group_id).items()}

        if kwargs.get("application_ids"):
            payload["applications"] = [{"id": app_id} for app_id in kwargs.pop("application_ids")]

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        resp = self.rest.put(f"segmentGroup/{group_id}", json=payload, params=params, api_version="v2").status_code
        if not isinstance(resp, Response):
            return self.get_group(group_id)

    def delete_group(self, group_id: str, **kwargs) -> int:
        """
        Deletes the specified segment group.

        Args:
            group_id (str): The unique identifier for the segment group to be deleted.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.segment_groups.delete_group('99999')

        """
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.delete(f"segmentGroup/{group_id}", params=params).status_code
