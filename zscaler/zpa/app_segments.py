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

    def get_segment(self, segment_id: str, **kwargs) -> Box:
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
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.get(f"application/{segment_id}", params=params)

    def get_segment_by_name(self, name: str, **kwargs):
        """
        Returns information on the application segment with the specified name.

        Args:
            name (str): The name of the application segment.

        Returns:
            :obj:`Box` or None: The resource record for the application segment  if found, otherwise None.

        Examples:
            >>> appsegment = zpa.app_segments.get_segment_by_name('example_name')
            >>> if appsegment:
            ...     pprint(appsegment)
            ... else:
            ...     print("Application segment not found")

        """
        apps = self.list_segments(**kwargs)
        for app in apps:
            if app.get("name") == name:
                return app
        return None

    def get_segments_by_type(self, application_type: str, expand_all: bool = False, **kwargs) -> Box:
        """
        Retrieve all configured application segments of a specified type, optionally expanding all related data.

        Args:
            application_type (str): Type of application segment to retrieve.
            Must be one of "BROWSER_ACCESS", "INSPECT", "SECURE_REMOTE_ACCESS".
            expand_all (bool, optional): Whether to expand all related data. Defaults to False.

        Keyword Args:
            max_items (int, optional): The maximum number of items to request before stopping iteration.
            max_pages (int, optional): The maximum number of pages to request before stopping iteration.
            pagesize (int, optional): Specifies the page size. The default size is 20, but the maximum size is 500.
            page (int, optional): Specifies the page number to begin fetching from.
            search (str, optional): The search string used to match against features and fields.

        Returns:
            BoxList: List of application segments.

        Examples:
            >>> app_type = 'BROWSER_ACCESS'
            >>> expand_all = True
            >>> search = "ba_server01"
            >>> app_segments = zpa.app_segments.get_segments_by_type(app_type, expand_all, search=search)
        """
        params = {"applicationType": application_type, "expandAll": "true" if expand_all else "false"}
        if "search" in kwargs:
            params["search"] = kwargs["search"]

        result, error = self.rest.get_paginated_data(path="/application/getAppsByType", params=params, **kwargs)
        if error:
            return BoxList([])
        return result

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
        payload = {
            "name": name,
            "domainNames": domain_names,
            "tcpPortRanges": tcp_port_ranges,
            "udpPortRanges": udp_port_ranges,
            "segmentGroupId": segment_group_id,
            "serverGroups": [{"id": group_id} for group_id in server_group_ids],
        }
        if "clientless_app_ids" in kwargs:
            clientless_apps = kwargs.pop("clientless_app_ids")
            payload["clientlessApps"] = transform_clientless_apps(clientless_apps)

        add_id_groups(self.reformat_params, kwargs, payload)
        for key, value in kwargs.items():
            if value is not None:
                payload[snake_to_camel(key)] = value

        camel_payload = recursive_snake_to_camel(payload)
        for key, value in kwargs.items():
            if value is not None:
                camel_payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post("application", json=payload, params=params)
        if isinstance(response, Response):
            status_code = response.status_code
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
        payload = convert_keys(self.get_segment(segment_id))

        if kwargs.get("tcp_port_ranges"):
            payload["tcpPortRange"] = [{"from": ports[0], "to": ports[1]} for ports in kwargs.pop("tcp_port_ranges")]

        if kwargs.get("udp_port_ranges"):
            payload["udpPortRange"] = [{"from": ports[0], "to": ports[1]} for ports in kwargs.pop("udp_port_ranges")]

        if kwargs.get("clientless_app_ids"):
            formatted_clientless_apps = [{"id": app.get("id")} for app in kwargs.pop("clientless_app_ids")]
            payload["clientlessApps"] = formatted_clientless_apps

        add_id_groups(self.reformat_params, kwargs, payload)

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        resp = self.rest.put(f"application/{segment_id}", json=payload, params=params).status_code
        if not isinstance(resp, Response):
            return self.get_segment(segment_id)

    def delete_segment(self, segment_id: str, force_delete: bool = False, **kwargs) -> int:
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

            >>> zpa.app_segments.delete_segment('88888', force_delete=True)

        """
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        query = "forceDelete=true" if force_delete else ""
        response = self.rest.delete(f"/application/{segment_id}?{query}", params=params)
        return response.status_code

    def app_segment_move(self, application_id: str, **kwargs) -> Box:
        """
        Moves application segments from one microtenant to another
        Note: Application segments can only be moved from a Default Microtenant microtenant_id as 0 to a child tenant

        Args:
            application_id (str):
                The unique identifier of the Application Segment.
            target_segment_group_id (str):
                The unique identifier of the target segment group that the application segment is being moved to.
            target_server_group_id (str):
                The unique identifier of the target server group that the application segment is being moved to.
            target_microtenant_id (str):
                The unique identifier of the Microtenant that the application segment is being moved to.

        Keyword Args:
            ...

        Returns:
            :obj:`Box`: The resource record for the moved application segment.

        Examples:
            Moving an application segment to another microtenant:

            >>> zpa.app_segments.app_segment_move(
            ...    application_id='216199618143373016',
            ...    target_segment_group_id='216199618143373010',
            ...    target_server_group_id='216199618143373012',
            ...    target_microtenant_id='216199618143372994'
            ... )

        """
        payload = {
            "targetSegmentGroupId": kwargs.pop("target_segment_group_id", None),
            "targetMicrotenantId": kwargs.pop("target_microtenant_id", None),
            "targetServerGroupId": kwargs.pop("target_server_group_id", None),
        }
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post(f"application/{application_id}/move", json=payload, params=params)
        if response.status_code == 204:
            return Box({})
        elif isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def app_segment_share(self, application_id: str, **kwargs) -> Box:
        """
        Moves application segments from one microtenant to another
        Note: Application segments can only be shared between child tenants.

        Args:
            application_id (str):
                The unique identifier of the Application Segment.
            share_to_microtenants (:obj:`list` of :obj:`str`):
                The unique identifier of the Microtenant that the application segment is being shared to.
                This field is required if you want to share an application segment.
                To remove the share send the attribute as an empty list.
        Keyword Args:
            ...

        Returns:
            :obj:`Box`: An empty Box object if the operation is successful.

        Examples:
            Moving an application segment to another microtenant:

            >>> zpa.app_segments.app_segment_share(
            ...    application_id='216199618143373016',
            ...    share_to_microtenants=['216199618143373010']
            ... )

        """
        payload = {
            "shareToMicrotenants": kwargs.pop("share_to_microtenants", None),
        }
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.put(f"application/{application_id}/share", json=payload, params=params)
        if response.status_code == 204:
            return Box({})
        elif isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response
