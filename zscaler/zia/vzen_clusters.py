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
from zscaler.zia.models.vzen_clusters import VZENClusters
from zscaler.utils import format_url, transform_common_id_fields, reformat_params


class VZENClustersAPI(APIClient):
    """
    A Client object for the VZEN Clusters resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_vzen_clusters(self, query_params=None) -> tuple:
        """
        Retrieves a list of ZIA Virtual Service Edge clusters

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search for a configured Virtual Service Edge cluster

        Returns:
            tuple: A tuple containing (list of Service Edges instances, Response, error)

        Examples:
            List Service Edges using default settings:

            >>> vzen_list, _, error = client.zia.vzen_clusters.list_vzen_clusters(
                query_params={'search':'VZEN01'})
            >>> if error:
            ...     print(f"Error listing vzens: {error}")
            ...     return
            ... print(f"Total vzens found: {len(vzen_list)}")
            ... for vzen in vzen_list:
            ...     print(vzen.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /virtualZenClusters
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
                result.append(VZENClusters(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_vzen_cluster(self, cluster_id: int) -> tuple:
        """
        Retrieves the Virtual Service Edge cluster based on the specified ID

        Args:
            cluster_id (int): The unique identifier for the vzen cluster.

        Returns:
            tuple: A tuple containing (VZEN Cluster instance, Response, error).

        Examples:
            Print a specific VZEN Cluster

            >>> fetched_vzen, _, error = client.zia.vzen_clusters.get_vzen_cluster(
                '1254654')
            >>> if error:
            ...     print(f"Error fetching VZEN Cluster by ID: {error}")
            ...     return
            ... print(f"Fetched VZEN Cluster by ID: {fetched_vzen.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /virtualZenClusters/{cluster_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, VZENClusters)
        if error:
            return (None, response, error)

        try:
            result = VZENClusters(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_vzen_cluster(self, **kwargs) -> tuple:
        """
        Adds a new Virtual Service Edge cluster.

        Args:
            name (str): Name of the Virtual Service Edge cluster
            **kwargs: Optional keyword args.

        Keyword Args:
            status (str): Specifies the status of the Virtual Service Edge cluster.
                The status is set to ENABLED by default.
                Supported Values: ENABLED, DISABLED, DISABLED_BY_SERVICE_PROVIDER, NOT_PROVISIONED_IN_SERVICE_PROVIDER
            ip_address (str): The Virtual Service Edge cluster IP address
            subnet_mask (str): The Virtual Service Edge cluster subnet mask
            default_gateway (str): The IP address of the default gateway to the internet
            ip_sec_enabled (bool): The IP address of the default gateway to the internet
            virtual_zen_node_ids (list): The Virtual Service Edge instances you want to include in the cluster.

            type (str): The Virtual Service Edge cluster type
                See the
                `available list of VZEN Types:
                <https://help.zscaler.com/zia/service-edges#/virtualZenClusters/{virtualZenClusterId}-get>`_
                for further detail on optional keyword parameter structures.

        Returns:
            tuple: A tuple containing the newly added Virtual ZENS, response, and error.

        Examples:
            Add a new Virtual ZEN :

            >>> added_vzen, _, error = client.zia.vzen_clusters.add_vzen_cluster(
            ...     name=f"NewVZEN_{random.randint(1000, 10000)}",
            ...     status=True,
            ...     ip_address='192.168.100.100',
            ...     subnet_mask='255.255.255.0',
            ...     default_gateway='192.168.100.1',
            ...     ip_sec_enabled=True,
            ...     virtual_zen_node_ids=[],
            ... )
            >>> if error:
            ...     print(f"Error adding vzen cluster: {error}")
            ...     return
            ... print(f"VZEN Cluster added successfully: {added_vzen.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /virtualZenClusters
        """
        )

        body = kwargs

        if "enabled" in kwargs:
            kwargs["status"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, VZENClusters)
        if error:
            return (None, response, error)

        try:
            result = VZENClusters(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_vzen_cluster(self, cluster_id: int, **kwargs) -> tuple:
        """
        Updates the Virtual Service Edge cluster based on the specified ID

        Args:
            cluster_id (int): The unique ID for the VZEN Cluster.

        Returns:
            tuple: A tuple containing the updated VZEN Cluster, response, and error.

        Examples:
            Update a new VZEN Cluster :

            >>> updated_vzen, _, error = client.zia.vzen_clusters.update_vzen_cluster(
            ...     cluster_id='1524566'
            ...     name=f"NewVZEN_{random.randint(1000, 10000)}",
            ...     status=True,
            ...     ip_address='192.168.100.100',
            ...     subnet_mask='255.255.255.0',
            ...     default_gateway='192.168.100.1',
            ...     ip_sec_enabled=True,
            ...     virtual_zen_node_ids=[],
            ... )
            >>> if error:
            ...     print(f"Error adding VZEN Cluster: {error}")
            ...     return
            ... print(f"VZEN Cluster added successfully: {added_vzen.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /virtualZenClusters/{cluster_id}
        """
        )
        body = kwargs

        if "enabled" in kwargs:
            kwargs["status"] = "ENABLED" if kwargs.pop("enabled") else "DISABLED"

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, VZENClusters)
        if error:
            return (None, response, error)

        try:
            result = VZENClusters(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_vzen_cluster(self, cluster_id: int) -> tuple:
        """
        Deletes the Virtual Service Edge cluster based on the specified ID

        Args:
            cluster_id (str): The unique identifier of the VZEN Cluster.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a VZEN Cluster:

            >>> _, _, error = client.zia.vzen_clusters.delete_vzen_cluster('73459')
            >>> if error:
            ...     print(f"Error deleting VZEN Cluster: {error}")
            ...     return
            ... print(f"VZEN Cluster with ID {'73459' deleted successfully.")
        """
        # Step 1: Fetch the cluster
        cluster, _, error = self.get_vzen_cluster(cluster_id)
        if error:
            return (None, None, error)

        # Step 2: Build minimal update payload
        payload = {
            "id": cluster.id,
            "name": cluster.name,
            "status": cluster.status,
            "type": cluster.type,
            "ipAddress": cluster.ip_address,
            "subnetMask": cluster.subnet_mask,
            "defaultGateway": cluster.default_gateway,
            "ipSecEnabled": cluster.ip_sec_enabled,
            "virtualZenNodes": [],  # detach
        }

        # Step 3: PUT to update the cluster (detach nodes)
        api_url = format_url(f"{self._zia_base_endpoint}/virtualZenClusters/{cluster_id}")
        request, error = self._request_executor.create_request(
            method="PUT",
            endpoint=api_url,
            body=payload,
        )
        if error:
            return (None, None, error)

        _, error = self._request_executor.execute(request)
        if error:
            return (None, None, error)

        # Step 4: DELETE the cluster
        request, error = self._request_executor.create_request(
            method="DELETE",
            endpoint=api_url,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
