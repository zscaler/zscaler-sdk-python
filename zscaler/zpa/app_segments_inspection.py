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

from zscaler.utils import (
    add_id_groups,
    convert_keys,
    recursive_snake_to_camel,
    snake_to_camel,
)
from zscaler.zpa.client import ZPAClient


class AppSegmentsInspectionAPI:
    # Params that need reformatting
    reformat_params = [
        ("server_group_ids", "serverGroups"),
    ]

    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_segment_inspection(self, **kwargs) -> BoxList:
        """
        Retrieve all configured AppProtection application segments.

        Returns:
            :obj:`BoxList`: List of AppProtection application segments.

        Examples:
            >>> app_segments = zpa.app_segments_inspection.list_segments_inspection()

        """
        list, _ = self.rest.get_paginated_data(path="/application", **kwargs)
        return list

    def get_segment_inspection(self, segment_id: str) -> Box:
        """
        Get information for an AppProtection application segment.

        Args:
            segment_id (str):
                The unique identifier for the AppProtection application segment.

        Returns:
            :obj:`Box`: The AppProtection application segment resource record.

        Examples:
            >>> app_segment = zpa.app_segments_inspection.details('99999')

        """
        return self.rest.get(f"application/{segment_id}")

    def get_segment_inspection_by_name(self, name):
        apps = self.list_segment_inspection()
        for app in apps:
            if app.get("name") == name:
                return app
        return None

    def delete_segment_inspection(self, segment_id: str, force_delete: bool = False) -> int:
        """
        Delete an AppProtection application segment.

        Args:
            force_delete (bool):
                Setting this field to true deletes the mapping between AppProtection Application Segment and Segment Group.
            segment_id (str):
                The unique identifier for the AppProtection application segment.

        Returns:
            :obj:`int`: The operation response code.

        Examples:
            Delete an AppProtection Application Segment with an id of 99999.

            >>> zpa.app_segments.delete('99999')

            Force deletion of an AppProtection Application Segment with an id of 88888.

            >>> zpa.app_segments_inspection.delete('88888', force_delete=True)

        """
        query = ""
        if force_delete:
            query = "forceDelete=true"
        response = self.rest.delete("/application/%s?%s" % (segment_id, query))
        return response.status_code

    def add_segment_inspection(
        self,
        name: str,
        domain_names: list,
        segment_group_id: str,
        server_group_ids: list,
        tcp_port_ranges: list = None,
        udp_port_ranges: list = None,
        common_apps_dto: dict = None,
        **kwargs,
    ) -> Box:
        """
        Create an AppProtection application segment.

        Args:
            segment_group_id (str):
                The unique identifer for the segment group this application segment belongs to.
            udp_ports (:obj:`list` of :obj:`str`):
                List of udp port range pairs, e.g. ['35000', '35000'] for port 35000.
            tcp_ports (:obj:`list` of :obj:`str`):
                List of tcp port range pairs, e.g. ['22', '22'] for port 22-22, ['80', '100'] for 80-100.
            domain_names (:obj:`list` of :obj:`str`):
                List of domain names or IP addresses for the application segment.
            name (str):
                The name of the application segment.
            server_group_ids (:obj:`list` of :obj:`str`):
                The list of server group IDs that belong to this application segment.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            bypass_type (str):
                The type of bypass for the Application Segment. Accepted values are `ALWAYS`, `NEVER` and `ON_NET`.
            config_space (str):
                The config space for this Application Segment. Accepted values are `DEFAULT` and `SIEM`.
            default_idle_timeout (int):
                The Default Idle Timeout for the Application Segment.
            default_max_age (int):
                The Default Max Age for the Application Segment.
            description (str):
                Additional information about this Application Segment.
            double_encrypt (bool):
                Double Encrypt the Application Segment micro-tunnel.
            enabled (bool):
                Enable the Application Segment.
            health_check_type (str):
                Set the Health Check Type. Accepted values are `DEFAULT` and `NONE`.
            health_reporting (str):
                Set the Health Reporting. Accepted values are `NONE`, `ON_ACCESS` and `CONTINUOUS`.
            ip_anchored (bool):
                Enable IP Anchoring for this Application Segment.
            is_cname_enabled (bool):
                Enable CNAMEs for this Application Segment.
            passive_health_enabled (bool):
                Enable Passive Health Checks for this Application Segment.
            icmp_access_type (str): Sets ICMP access type for ZPA clients.

        Returns:
            :obj:`Box`: The newly created application segment resource record.

        Examples:
            Add a new AppProtection application segment for example.com, ports 8080-8085.

            >>> zpa.app_segments_inspection.add_segment_inspection('new_app_segment',
            ...    domain_names=['example.com'],
            ...    segment_group_id='99999',
            ...    tcp_ports=['8080', '8085'],
            ...    server_group_ids=['99999', '88888'])

        """

        # Initialise payload
        payload = {
            "name": name,
            "domainNames": domain_names,
            "tcpPortRanges": tcp_port_ranges,
            "udpPortRanges": udp_port_ranges,
            "segmentGroupId": segment_group_id,
            "commonAppsDto": common_apps_dto if common_apps_dto else None,
            "serverGroups": [{"id": group_id} for group_id in server_group_ids],
        }

        # Process common_apps_dto if it's provided
        if common_apps_dto:
            camel_common_apps_dto = recursive_snake_to_camel(common_apps_dto)
            payload["commonAppsDto"] = camel_common_apps_dto

        add_id_groups(self.reformat_params, kwargs, payload)
        for key, value in kwargs.items():
            if value is not None:
                payload[snake_to_camel(key)] = value

        # Convert the entire payload's keys to camelCase before sending
        camel_payload = recursive_snake_to_camel(payload)
        for key, value in kwargs.items():
            if value is not None:
                camel_payload[snake_to_camel(key)] = value

        response = self.rest.post("application", json=camel_payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_segment_inspection(self, segment_id: str, common_apps_dto=None, **kwargs) -> Box:
        """
        Update an AppProtection application segment.

        Args:
            segment_id (str):
                The unique identifier for the AppProtection application segment.
            **kwargs:
                Optional params.

        Keyword Args:
            bypass_type (str): Bypass type for the segment. Values: `ALWAYS`, `NEVER`, `ON_NET`.
            config_space (str): Config space for the segment. Values: `DEFAULT`, `SIEM`.
            default_idle_timeout (int):
                The Default Idle Timeout for the AppProtection Application Segment.
            default_max_age (int):
                The Default Max Age for the AppProtection Application Segment.
            description (str):
                Additional information about this AppProtection Application Segment.
            domain_names (:obj:`list` of :obj:`str`):
                List of domain names or IP addresses for the AppProtection application segment.
            double_encrypt (bool):
                Double Encrypt the AppProtection Application Segment micro-tunnel.
            enabled (bool):
                Enable the AppProtection Application Segment.
            health_check_type (str):
                Set the Health Check Type. Accepted values are `DEFAULT` and `NONE`.
            health_reporting (str):
                Set the Health Reporting. Accepted values are `NONE`, `ON_ACCESS` and `CONTINUOUS`.
            ip_anchored (bool):
                Enable IP Anchoring for this AppProtection Application Segment.
            is_cname_enabled (bool):
                Enable CNAMEs for this AppProtection Application Segment.
            name (str):
                The name of the AppProtection Application Segment.
            passive_health_enabled (bool):
                Enable Passive Health Checks for this AppProtection Application Segment.
            segment_group_id (str):
                The unique identifer for the segment group this AppProtection application segment belongs to.
            server_group_ids (:obj:`list` of :obj:`str`):
                The list of server group IDs that belong to this AppProtection application segment.
            tcp_ports (:obj:`list` of :obj:`tuple`):
                List of TCP port ranges specified as a tuple pair, e.g. for ports 21-23, 8080-8085 and 443:
                     [(21, 23), (8080, 8085), (443, 443)]
            udp_ports (:obj:`list` of :obj:`tuple`):
                List of UDP port ranges specified as a tuple pair, e.g. for ports 34000-35000 and 36000:
                     [(34000, 35000), (36000, 36000)]
            icmp_access_type (str): Sets ICMP access type for ZPA clients.

        Returns:
            :obj:`Box`: The updated AppProtection application segment resource record.

        Examples:
            Rename the application segment for example.com.

            >>> zpa.app_segments_inspection.update('99999',
            ...    name='new_app_name',

        """
        # Set payload to value of existing record and recursively convert nested dict keys from snake_case to camelCase.
        payload = convert_keys(self.get_segment_inspection(segment_id))

        if kwargs.get("tcp_port_ranges"):
            payload["tcpPortRange"] = [{"from": ports[0], "to": ports[1]} for ports in kwargs.pop("tcp_port_ranges")]

        if kwargs.get("udp_port_ranges"):
            payload["udpPortRange"] = [{"from": ports[0], "to": ports[1]} for ports in kwargs.pop("udp_port_ranges")]

        if common_apps_dto:
            camel_common_apps_dto = recursive_snake_to_camel(common_apps_dto)  # use the recursive function
            payload["commonAppsDto"] = camel_common_apps_dto  # ensure commonAppsDto gets added to payload

        # Convert other keys in payload
        add_id_groups(self.reformat_params, kwargs, payload)

        # Add remaining optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"application/{segment_id}", json=payload).status_code

        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_segment_inspection(segment_id)
