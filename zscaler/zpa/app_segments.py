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
    transform_clientless_apps,
)
from zscaler.zpa.client import ZPAClient


class ApplicationSegmentAPI:
    reformat_params = [
        ("clientless_app_ids", "clientlessApps"),
        ("server_group_ids", "serverGroups"),
    ]

    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_segments(self, **kwargs) -> BoxList:
        """
        Retrieve all configured application segments.

        Keyword Args:
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **page (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: List of application segments.

        Examples:
            >>> app_segments = zpa.app_segments.list_segments()

        """
        list, _ = self.rest.get_paginated_data(path="/application", **kwargs, api_version="v1")
        return list

    def get_segment(self, segment_id: str) -> Box:
        """
        Get information for an application segment.

        Args:
            segment_id (str):
                The unique identifier for the application segment.

        Returns:
            :obj:`Box`: The application segment resource record.

        Examples:
            >>> app_segment = zpa.app_segments.details('99999')

        """
        response = self.rest.get("/application/%s" % (segment_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response

    def get_segment_by_name(self, name):
        apps = self.list_segments()
        for app in apps:
            if app.get("name") == name:
                return app
        return None

    def delete_segment(self, segment_id: str, force_delete: bool = False) -> int:
        """
        Delete an application segment.

        Args:
            force_delete (bool):
                Setting this field to true deletes the mapping between Application Segment and Segment Group.
            segment_id (str):
                The unique identifier for the application segment.

        Returns:
            :obj:`int`: The operation response code.

        Examples:
            Delete an Application Segment with an id of 99999.

            >>> zpa.app_segments.delete('99999')

            Force deletion of an Application Segment with an id of 88888.

            >>> zpa.app_segments.delete('88888', force_delete=True)

        """
        query = ""
        if force_delete:
            query = "forceDelete=true"
        response = self.rest.delete("/application/%s?%s" % (segment_id, query))
        return response.status_code

    def add_segment(
        self,
        name: str,
        domain_names: list,
        segment_group_id: str,
        server_group_ids: list,
        tcp_port_ranges: list = None,
        udp_port_ranges: list = None,
        **kwargs,
    ) -> Box:
        """
        Create an application segment.

        Args:
            name (str): Name of the application segment.
            domain_names (list of str): Domain names or IP addresses for the segment.
            segment_group_id (str): Unique identifier for the segment group.
            server_group_ids (list of str): Server group IDs for this segment.
            tcp_port_ranges (list of str, optional): TCP port range pairs (e.g., ['22', '22']).
            udp_port_ranges (list of str, optional): UDP port range pairs (e.g., ['35000', '35000']).

        Keyword Args:
            bypass_type (str): Bypass type for the segment. Values: `ALWAYS`, `NEVER`, `ON_NET`.
            clientless_app_ids (list): IDs for associated clientless apps.
            config_space (str): Config space for the segment. Values: `DEFAULT`, `SIEM`.
            default_idle_timeout (int): Default Idle Timeout for the segment.
            default_max_age (int): Default Max Age for the segment.
            description (str): Additional information about the segment.
            double_encrypt (bool): If true, enables double encryption.
            enabled (bool): If true, enables the application segment.
            health_check_type (str): Health Check Type. Values: `DEFAULT`, `NONE`.
            health_reporting (str): Health Reporting mode. Values: `NONE`, `ON_ACCESS`, `CONTINUOUS`.
            ip_anchored (bool): If true, enables IP Anchoring.
            is_cname_enabled (bool): If true, enables CNAMEs for the segment.
            passive_health_enabled (bool): If true, enables Passive Health Checks.
            icmp_access_type (str): Sets ICMP access type for ZPA clients.

        Returns:
            :obj:`Box`: The newly created application segment.

        Examples:
            Add a new application segment for example.com on ports 8080-8085:

            >>> zpa.app_segments.add_segment('new_app_segment',
            ...    domain_names=['example.com'],
            ...    segment_group_id='99999',
            ...    tcp_port_ranges=['8080', '8085'],
            ...    server_group_ids=['99999', '88888'])
        """
        # Initialise payload
        payload = {
            "name": name,
            "domainNames": domain_names,
            "tcpPortRanges": tcp_port_ranges,
            "udpPortRanges": udp_port_ranges,
            "segmentGroupId": segment_group_id,
            "serverGroups": [{"id": group_id} for group_id in server_group_ids],
        }

        # Handle clientless_app_ids separately
        if "clientless_app_ids" in kwargs:
            clientless_apps = kwargs.pop("clientless_app_ids")
            payload["clientlessApps"] = transform_clientless_apps(clientless_apps)

        # add_id_groups(self.reformat_params, kwargs, payload)

        # # Add optional parameters to payload
        # for key, value in kwargs.items():
        #     payload[snake_to_camel(key)] = value
        add_id_groups(self.reformat_params, kwargs, payload)
        for key, value in kwargs.items():
            if value is not None:
                payload[snake_to_camel(key)] = value

        # Convert the entire payload's keys to camelCase before sending
        camel_payload = recursive_snake_to_camel(payload)
        for key, value in kwargs.items():
            if value is not None:
                camel_payload[snake_to_camel(key)] = value

        response = self.rest.post("application", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_segment(self, segment_id: str, **kwargs) -> Box:
        """
        Update an application segment.

        Args:
            segment_id (str):
                The unique identifier for the application segment.
            **kwargs:
                Optional params.

        Keyword Args:
            bypass_type (str):
                The type of bypass for the Application Segment. Accepted values are `ALWAYS`, `NEVER` and `ON_NET`.
            clientless_app_ids (:obj:`list`):
                List of unique IDs for clientless apps to associate with this Application Segment.
            config_space (str):
                The config space for this Application Segment. Accepted values are `DEFAULT` and `SIEM`.
            default_idle_timeout (int):
                The Default Idle Timeout for the Application Segment.
            default_max_age (int):
                The Default Max Age for the Application Segment.
            description (str):
                Additional information about this Application Segment.
            domain_names (:obj:`list` of :obj:`str`):
                List of domain names or IP addresses for the application segment.
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
            name (str):
                The name of the application segment.
            passive_health_enabled (bool):
                Enable Passive Health Checks for this Application Segment.
            segment_group_id (str):
                The unique identifer for the segment group this application segment belongs to.
            server_group_ids (:obj:`list` of :obj:`str`):
                The list of server group IDs that belong to this application segment.
            tcp_port_ranges (:obj:`list` of :obj:`tuple`):
                List of TCP port ranges specified as a tuple pair, e.g. for ports 21-23, 8080-8085 and 443:
                     [(21, 23), (8080, 8085), (443, 443)]
            udp_port_ranges (:obj:`list` of :obj:`tuple`):
                List of UDP port ranges specified as a tuple pair, e.g. for ports 34000-35000 and 36000:
                     [(34000, 35000), (36000, 36000)]
            icmp_access_type (str): Sets ICMP access type for ZPA clients.

        Returns:
            :obj:`Box`: The updated application segment resource record.

        Examples:
            Rename the application segment for example.com.

            >>> zpa.app_segments.update('99999',
            ...    name='new_app_name',

        """
        # Set payload to value of existing record and convert nested dict keys.
        payload = convert_keys(self.get_segment(segment_id))

        if kwargs.get("tcp_port_ranges"):
            payload["tcpPortRange"] = [{"from": ports[0], "to": ports[1]} for ports in kwargs.pop("tcp_port_ranges")]

        if kwargs.get("udp_port_ranges"):
            payload["udpPortRange"] = [{"from": ports[0], "to": ports[1]} for ports in kwargs.pop("udp_port_ranges")]

        # Handle the clientless_app_ids directly within this function without a separate helper
        if kwargs.get("clientless_app_ids"):
            # Here you would implement any necessary formatting directly
            formatted_clientless_apps = [{"id": app.get("id")} for app in kwargs.pop("clientless_app_ids")]
            payload["clientlessApps"] = formatted_clientless_apps  # use the correct key expected by your API

        # Convert other keys in payload
        add_id_groups(self.reformat_params, kwargs, payload)

        # Add remaining optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"application/{segment_id}", json=payload).status_code

        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_segment(segment_id)

    def detach_from_segment_group(self, app_id, seg_group_id):
        seg_group = self.rest.get("/segmentGroup/%s" % (seg_group_id))
        if isinstance(seg_group, Response):
            status_code = seg_group.status_code
            if status_code > 299:
                return None
        apps = seg_group.get("applications", [])
        addaptedApps = []
        for app in apps:
            if app.get("id") != app_id:
                addaptedApps.append(app)
        seg_group["applications"] = addaptedApps
        self.rest.put(
            "/segmentGroup/%s" % (seg_group_id),
            json=seg_group,
        )
