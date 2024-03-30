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
from zscaler.utils import convert_keys, snake_to_camel
from zscaler.zia import ZIAClient


class ZPAGatewayAPI:
    def __init__(self, client: ZIAClient):
        self.rest = client

    def list_gateways(self, **kwargs) -> BoxList:
        """
        Returns the list of ZPA Gateways.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.

        Returns:
            :obj:`BoxList`: The list of ZPA Gateways configured in ZIA.

        Examples:
            List ZPA Gateways using default settings:

            >>> for gateway in zia.zpa_gateway.list_gateways():
            ...   print(gateway)

            List labels, limiting to a maximum of 10 items:

            >>> for gateway in zia.zpa_gateway.list_gateways(max_items=10):
            ...    print(gateway)

            List labels, returning 200 items per page for a maximum of 2 pages:

            >>> for gateway in zia.zpa_gateway.list_gateways(page_size=200, max_pages=2):
            ...    print(label)

        """
        list = self.rest.get(path="/zpaGateways", **kwargs)
        if isinstance(list, Response):
            return None
        return list

    def get_gateway(self, gateway_id: str) -> Box:
        """
        Returns the zpa gateway details for a given ZPA Gateway.

        Args:
            gatewayId (str): The unique identifier for the ZPA Gateway.

        Returns:
            :obj:`Box`: The ZPA Gateway resource record.

        Examples:
            >>> label = zia.zpa_gateway.get_gateway('99999')

        """
        response = self.rest.get("/zpaGateways/%s" % (gateway_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response

    def add_gateway(
        self,
        name: str,
        zpa_server_group: dict = None,
        zpa_app_segments: list = None,
        **kwargs,
    ) -> Box:
        """
        Creates a new ZPA Gateway.

        Args:
            name (str): The name of the ZPA Gateway.
            zpa_server_group (dict, required): The ZPA Server Group that is
                configured for Source IP Anchoring.
            zpa_app_segments (list, optional): All the Application Segments that are
                associated with the selected ZPA Server Group for which Source IP
                Anchoring is enabled.

        Keyword Args:
            description (str): Additional details about the ZPA gateway.
            type (str): Indicates whether the ZPA gateway is configured for Zscaler
                Internet Access (using option ZPA) or Zscaler Cloud Connector (using
                option ECZPA). Accepted values are 'ZPA' or 'ECZPA'.
            zpa_tenant_id (int): The ID of the ZPA tenant where Source IP Anchoring
                is configured

        Returns:
            :obj:`Box`: The newly added ZPA Gateway resource record.
        """
        payload = {"name": name, "type": "ZPA"}

        if zpa_server_group:
            payload["zpaServerGroup"] = {
                "externalId": zpa_server_group.get("external_id"),
                "name": zpa_server_group.get("name"),
            }

        if zpa_app_segments:
            payload["zpaAppSegments"] = [
                {"externalId": segment.get("external_id"), "name": segment.get("name")}
                for segment in zpa_app_segments
            ]

        # Add other optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("zpaGateways", json=payload)
        if isinstance(response, Response):
            # Handle error response
            status_code = response.status_code
            raise Exception(
                f"API call failed with status {status_code}: {response.json()}"
            )
        return response

    def update_gateway(self, gateway_id: str, **kwargs):
        """
        Updates information for the specified ZPA Gateway.

        Args:
            gateway_id (str): The unique id for the ZPA Gateway to be updated.

        Keyword Args:
            name (str): The name of the ZPA gateway.
            description (str): Additional details about the ZPA gateway.
            type (str): Indicates whether the ZPA gateway is configured for
                Zscaler Internet Access (using option ZPA) or Zscaler Cloud
                Connector (using option ECZPA). Accepted values are 'ZPA' or 'ECZPA'.
            zpa_server_group (dict, optional): The ZPA Server Group configured for
                Source IP Anchoring.
            zpa_app_segments (list, optional): All the Application Segments associated
                with the selected ZPA Server Group for which Source IP Anchoring is
                enabled.
            zpa_tenant_id (int): The ID of the ZPA tenant where Source IP Anchoring
                is configured

        Returns:
            :obj:`Box`: The updated ZPA Gateway resource record.
        """
        payload = convert_keys(self.get_gateway(gateway_id))

        # Update payload with provided arguments
        for key, value in kwargs.items():
            if key == "zpa_server_group" and isinstance(value, dict):
                # Convert nested keys in zpa_server_group to camelCase
                value = {snake_to_camel(k): v for k, v in value.items()}
            elif key == "zpa_app_segments" and isinstance(value, list):
                # Convert nested keys in zpa_app_segments to camelCase
                value = [
                    {snake_to_camel(k): v for k, v in item.items()} for item in value
                ]

            payload[snake_to_camel(key)] = value

        response = self.rest.put(f"zpaGateways/{gateway_id}", json=payload)
        if isinstance(response, Response) and not response.ok:
            # Handle error response
            raise Exception(
                f"API call failed with status {response.status_code}: "
                f"{response.json()}"
            )

        # Return the updated object
        return self.get_gateway(gateway_id)

    def delete_gateway(self, gateway_id):
        """
        Deletes the specified ZPA Gateway.

        Args:
            gateway_id (str): The unique identifier of the ZPA Gateway that will be deleted.

        Returns:
            :obj:`int`: The response code for the request.

        Examples
            >>> gateway = zia.zpa_gateway.delete_gateway('99999')

        """
        return self.rest.delete(f"zpaGateways/{gateway_id}").status_code
