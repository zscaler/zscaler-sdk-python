"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zia.models.vzen_nodes import VZenNodes
from zscaler.utils import format_url


class VZENNodesAPI(APIClient):
    """
    A Client object for the VZen Nodes resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_zen_nodes(self, query_params=None) -> tuple:
        """
        Retrieves the ZIA Virtual Service Edge for an organization

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of VZenNodes instances, Response, error)

        Examples:
            List Zen Nodes using default settings:

            >>> zen_node_list, _, error = client.zia.vzen_nodes.list_zen_nodes(
                query_params={'search': updated_zen_node.name})
            >>> if error:
            ...     print(f"Error listing Zen Nodes: {error}")
            ...     return
            ... print(f"Total Zen Nodes found: {len(zen_node_list)}")
            ... for zen_node in zen_node_list:
            ...     print(zen_node.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /virtualZenNodes
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(VZenNodes(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_zen_node(self, node_id: int) -> tuple:
        """
        Fetches a specific Zen Node by ID.

        Args:
            node_id (int): The unique identifier for the Zen Node.

        Returns:
            tuple: A tuple containing (Zen Node instance, Response, error).

        Examples:
            Print a specific Zen Node by ID:

            >>> fetched_zen_node, _, error = client.zia.vzen_nodes.get_zen_node(
                '1254654')
            >>> if error:
            ...     print(f"Error fetching Zen Node by ID: {error}")
            ...     return
            ... print(f"Fetched Zen Node by ID: {fetched_zen_node.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /virtualZenNodes/{node_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, VZenNodes)
        if error:
            return (None, response, error)

        try:
            result = VZenNodes(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_zen_node(self, **kwargs) -> tuple:
        """
        Creates a new ZIA Virtual Zen Node.

        Args:
            name (str): The name of the Virtual Zen Node.
            **kwargs: Optional keyword args.

        Keyword Args:
            enabled (bool): Whether the Virtual Zen Node is enabled or disabled.
            status (str): The status of the Virtual Zen Node (e.g., "ENABLED", "DISABLED").
            in_production (bool): Whether the Virtual Zen Node is in production mode.
            ip_address (str): The IP address of the Virtual Zen Node.
            subnet_mask (str): The subnet mask for the Virtual Zen Node.
            default_gateway (str): The default gateway IP address for the Virtual Zen Node.
            type (str): The type of Virtual Zen Node (e.g., "SMLB").
            ip_sec_enabled (bool): Whether IPsec is enabled for the Virtual Zen Node.
            on_demand_support_tunnel_enabled (bool): Whether on-demand support tunnel is enabled.
            establish_support_tunnel_enabled (bool): Whether support tunnel establishment is enabled.
            load_balancer_ip_address (str): The IP address of the load balancer.
            deployment_mode (str): The deployment mode for the Virtual Zen Node (e.g., "CLUSTER").
            vzen_sku_type (str): The SKU type for the Virtual Zen Node (e.g., "LARGE").
            description (str): Additional notes or information about the Virtual Zen Node.

        Returns:
            tuple: A tuple containing the newly added Virtual Zen Node, response, and error.

        Examples:
            Add a new Virtual Zen Node with basic configuration:

            >>> added_node, _, error = client.zia.vzen_nodes.add_zen_node(
            ...     name="NewVZEN1234",
            ...     enabled=True,
            ...     status="ENABLED",
            ...     in_production=True,
            ...     ip_address="10.0.0.100",
            ...     subnet_mask="255.255.255.0",
            ...     default_gateway="10.0.0.3",
            ...     type="SMLB",
            ...     load_balancer_ip_address="10.0.0.50",
            ...     deployment_mode="CLUSTER",
            ...     vzen_sku_type="LARGE"
            ... )
            >>> if error:
            ...     print(f"Error adding vzen node: {error}")
            ...     return
            ... print(f"vzen node added successfully: {added_node.as_dict()}")

            Add a new Virtual Zen Node with advanced configuration:

            >>> added_node, _, error = client.zia.vzen_nodes.add_zen_node(
            ...     name="NewVZEN5678",
            ...     enabled=True,
            ...     status="ENABLED",
            ...     in_production=True,
            ...     ip_address="10.0.0.100",
            ...     subnet_mask="255.255.255.0",
            ...     default_gateway="10.0.0.3",
            ...     type="SMLB",
            ...     ip_sec_enabled=True,
            ...     on_demand_support_tunnel_enabled=True,
            ...     establish_support_tunnel_enabled=True,
            ...     load_balancer_ip_address="10.0.0.50",
            ...     deployment_mode="CLUSTER",
            ...     vzen_sku_type="LARGE",
            ...     description="Production Virtual Zen Node"
            ... )
            >>> if error:
            ...     print(f"Error adding vzen node: {error}")
            ...     return
            ... print(f"vzen node added successfully: {added_node.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /virtualZenNodes
        """
        )

        body = kwargs

        if "enabled" in kwargs:
            kwargs["status"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, VZenNodes)
        if error:
            return (None, response, error)

        try:
            result = VZenNodes(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_zen_node(self, node_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA Virtual Zen Node.

        Args:
            node_id (int): The unique ID for the Virtual Zen Node.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the Virtual Zen Node.
            enabled (bool): Whether the Virtual Zen Node is enabled or disabled.
            status (str): The status of the Virtual Zen Node (e.g., "ENABLED", "DISABLED").
            in_production (bool): Whether the Virtual Zen Node is in production mode.
            ip_address (str): The IP address of the Virtual Zen Node.
            subnet_mask (str): The subnet mask for the Virtual Zen Node.
            default_gateway (str): The default gateway IP address for the Virtual Zen Node.
            type (str): The type of Virtual Zen Node (e.g., "SMLB").
            ip_sec_enabled (bool): Whether IPsec is enabled for the Virtual Zen Node.
            on_demand_support_tunnel_enabled (bool): Whether on-demand support tunnel is enabled.
            establish_support_tunnel_enabled (bool): Whether support tunnel establishment is enabled.
            load_balancer_ip_address (str): The IP address of the load balancer.
            deployment_mode (str): The deployment mode for the Virtual Zen Node (e.g., "CLUSTER").
            vzen_sku_type (str): The SKU type for the Virtual Zen Node (e.g., "LARGE").
            description (str): Additional notes or information about the Virtual Zen Node.

        Returns:
            tuple: A tuple containing the updated Virtual Zen Node, response, and error.

        Examples:
            Update an existing Virtual Zen Node with basic configuration:

            >>> updated_node, _, error = client.zia.vzen_nodes.update_zen_node(
            ...     node_id=1524566,
            ...     name="UpdateVZEN1234",
            ...     enabled=True,
            ...     status="ENABLED",
            ...     in_production=True,
            ...     ip_address="10.0.0.100",
            ...     subnet_mask="255.255.255.0",
            ...     default_gateway="10.0.0.3",
            ...     type="SMLB",
            ...     load_balancer_ip_address="10.0.0.50",
            ...     deployment_mode="CLUSTER",
            ...     vzen_sku_type="LARGE"
            ... )
            >>> if error:
            ...     print(f"Error updating vzen node: {error}")
            ...     return
            ... print(f"vzen node updated successfully: {updated_node.as_dict()}")

            Update an existing Virtual Zen Node with advanced configuration:

            >>> updated_node, _, error = client.zia.vzen_nodes.update_zen_node(
            ...     node_id=1524566,
            ...     name="UpdateVZEN5678",
            ...     enabled=True,
            ...     status="ENABLED",
            ...     in_production=True,
            ...     ip_address="10.0.0.100",
            ...     subnet_mask="255.255.255.0",
            ...     default_gateway="10.0.0.3",
            ...     type="SMLB",
            ...     ip_sec_enabled=True,
            ...     on_demand_support_tunnel_enabled=True,
            ...     establish_support_tunnel_enabled=True,
            ...     load_balancer_ip_address="10.0.0.50",
            ...     deployment_mode="CLUSTER",
            ...     vzen_sku_type="LARGE",
            ...     description="Updated Production Virtual Zen Node"
            ... )
            >>> if error:
            ...     print(f"Error updating vzen node: {error}")
            ...     return
            ... print(f"vzen node updated successfully: {updated_node.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /virtualZenNodes/{node_id}
        """
        )
        body = kwargs

        if "enabled" in kwargs:
            kwargs["status"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, VZenNodes)
        if error:
            return (None, response, error)

        try:
            result = VZenNodes(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_zen_node(self, node_id: int) -> tuple:
        """
        Deletes the specified Zen Node.

        Args:
            node_id (str): The unique identifier of the Zen Node.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a Zen Node:

            >>> _, _, error = client.zia.vzen_nodes.delete_zen_node('73459')
            >>> if error:
            ...     print(f"Error deleting Zen Node: {error}")
            ...     return
            ... print(f"Zen Node with ID {'73459'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /virtualZenNodes/{node_id}
        """
        )

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
