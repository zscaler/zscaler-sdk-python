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

    def get_group(self, group_id: str) -> Box:
        """
        Returns information on the specified segment group.

        Args:
            group_id (str):
                The unique identifier for the segment group.

        Returns:
            :obj:`Box`: The resource record for the segment group.

        Examples:
            >>> pprint(zpa.segment_groups.get_group('99999'))

        """
        return self.rest.get(f"segmentGroup/{group_id}")

    def get_segment_group_by_name(self, name):
        apps = self.list_groups()
        for app in apps:
            if app.get("name") == name:
                return app
        return None

    def add_group(self, name: str, enabled: bool = True, **kwargs) -> Box:
        """
        Adds a new segment group.

        Args:
            name (str):
                The name of the new segment group.
            enabled (bool):
                Enable the segment group. Defaults to True.
            **kwargs:

        Keyword Args:
            application_ids (:obj:`list` of :obj:`dict`):
                Unique application IDs to associate with the segment group.
            config_space (str):
                The config space for the segment group. Can either be DEFAULT or SIEM.
            description (str):
                A description for the segment group.
            policy_migrated (bool):

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

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("segmentGroup", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_group(self, group_id: str, **kwargs) -> Box:
        """
        Updates an existing segment group.

        Args:
            group_id (str):
                The unique identifier for the segment group to be updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str):
                The name of the new segment group.
            enabled (bool):
                Enable the segment group.
            application_ids (:obj:`list` of :obj:`dict`):
                Unique application IDs to associate with the segment group.
            config_space (str):
                The config space for the segment group. Can either be DEFAULT or SIEM.
            description (str):
                A description for the segment group.
            policy_migrated (bool):

        Returns:
            :obj:`Box`: The resource record for the updated segment group.

        Examples:
            Updating the name of a segment group:

            >>> zpa.segment_groups.update_group('99999',
            ...    name='updated_name')

        """
        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_group(group_id).items()}

        if kwargs.get("application_ids"):
            payload["applications"] = [{"id": app_id} for app_id in kwargs.pop("application_ids")]

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"segmentGroup/{group_id}", json=payload).status_code

        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_group(group_id)

    def delete_group(self, group_id: str) -> int:
        """
        Deletes the specified segment group.

        Args:
            group_id (str):
                The unique identifier for the segment group to be deleted.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.segment_groups.delete_group('99999')

        """
        return self.rest.delete(f"segmentGroup/{group_id}").status_code
