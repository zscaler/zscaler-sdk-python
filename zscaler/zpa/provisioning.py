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

from typing import List, Optional
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.provisioning_keys import ProvisioningKey
from zscaler.utils import format_url


def simplify_key_type(key_type):
    """
    Simplifies the key type for the user.

    Args:
        key_type (str): The key type ('connector' or 'service_edge').

    Returns:
        str: The simplified key type.
    """
    if key_type == "connector":
        return "CONNECTOR_GRP"
    elif key_type == "service_edge":
        return "SERVICE_EDGE_GRP"
    else:
        raise ValueError("Unexpected key type.")


class ProvisioningKeyAPI(APIClient):
    """
    A client object for the Provisioning Keys resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_provisioning_keys(self, key_type: str, query_params: Optional[dict] = None) -> List[ProvisioningKey]:
        """
        Returns a list of all configured provisioning keys.

        Args:
            key_type (str): The type of provisioning key ('connector' or 'service_edge').
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[ProvisioningKey]: A list of ProvisioningKey instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     keys = client.zpa.provisioning.list_provisioning_keys('connector')
            ...     for key in keys:
            ...         print(key.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/associationType/{simplify_key_type(key_type)}/provisioningKey")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, ProvisioningKey)

        return [ProvisioningKey(self.form_response_body(item)) for item in response.get_results()]

    def get_provisioning_key(self, key_id: str, key_type: str, query_params: Optional[dict] = None) -> ProvisioningKey:
        """
        Returns information on the specified provisioning key.

        Args:
            key_id (str): The unique id of the provisioning key.
            key_type (str): The type ('connector' or 'service_edge').
            query_params (dict, optional): Map of query parameters.

        Returns:
            ProvisioningKey: The provisioning key object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     key = client.zpa.provisioning.get_provisioning_key('9999', 'connector')
            ...     print(key.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/associationType/{simplify_key_type(key_type)}/provisioningKey/{key_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, ProvisioningKey)

        return ProvisioningKey(self.form_response_body(response.get_body()))

    def get_provisioning_key_by_zcomponent(
        self, zcomponent_id: str, key_type: str, query_params: Optional[dict] = None
    ) -> ProvisioningKey:
        """
        Returns provisioning key by App Connector or Service Edge ID.

        Args:
            zcomponent_id (str): The unique id of the component.
            key_type (str): The type ('connector' or 'service_edge').
            query_params (dict, optional): Map of query parameters.

        Returns:
            ProvisioningKey: The provisioning key object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     key = client.zpa.provisioning.get_provisioning_key_by_zcomponent('9999', 'connector')
            ...     print(key.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(
            f"{self._zpa_base_endpoint}/associationType/{simplify_key_type(key_type)}zcomponent/{zcomponent_id}/provisioningKey"
        )

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, ProvisioningKey)

        return ProvisioningKey(self.form_response_body(response.get_body()))

    def add_provisioning_key(self, key_type: str, **kwargs) -> ProvisioningKey:
        """
        Adds a new provisioning key to ZPA.

        Args:
            key_type (str): The type ('connector' or 'service_edge').
            name (str): The name of the provisioning key.
            max_usage (int): The maximum usage count.
            enrollment_cert_id (str): The enrollment certificate ID.
            component_id (str): The component ID.

        Returns:
            ProvisioningKey: The newly created provisioning key.

        Raises:
            ZscalerAPIException: If the API request fails.
            ValueError: If key_type is not provided.

        Examples:
            >>> try:
            ...     key = client.zpa.provisioning.add_provisioning_key(
            ...         key_type='connector',
            ...         name="NewKey",
            ...         max_usage="10",
            ...         enrollment_cert_id="2519",
            ...         component_id="72058304855047746"
            ...     )
            ...     print(key.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        if not key_type:
            raise ValueError("key_type must be provided.")

        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/associationType/{simplify_key_type(key_type)}/provisioningKey")

        body = kwargs
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        name = body.pop("name", None)
        max_usage = body.pop("max_usage", None)
        enrollment_cert_id = body.get("enrollment_cert_id")
        component_id = body.get("component_id")

        body.update({
            "name": name,
            "maxUsage": max_usage,
            "enrollmentCertId": enrollment_cert_id,
            "zcomponentId": component_id
        })

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, ProvisioningKey)

        return ProvisioningKey(self.form_response_body(response.get_body()))

    def update_provisioning_key(self, key_id: str, key_type: str, **kwargs) -> ProvisioningKey:
        """
        Updates the specified provisioning key.

        Args:
            key_id (str): The unique id of the key.
            key_type (str): The type ('connector' or 'service_edge').
            **kwargs: Fields to update.

        Returns:
            ProvisioningKey: The updated provisioning key.

        Raises:
            ZscalerAPIException: If the API request fails.
            ValueError: If key_type is not provided.

        Examples:
            >>> try:
            ...     key = client.zpa.provisioning.update_provisioning_key(
            ...         '999999',
            ...         'connector',
            ...         max_usage="20"
            ...     )
            ...     print(key.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        if not key_type:
            raise ValueError("key_type must be provided.")

        http_method = "PUT"
        api_url = format_url(
            f"{self._zpa_base_endpoint}/associationType/{simplify_key_type(key_type)}/provisioningKey/{key_id}"
        )

        body = kwargs
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body, params, {})
        response = self._request_executor.execute(request, ProvisioningKey)

        if response is None:
            return ProvisioningKey({"id": key_id})

        return ProvisioningKey(self.form_response_body(response.get_body()))

    def delete_provisioning_key(self, key_id: str, key_type: str, microtenant_id: str = None) -> None:
        """
        Deletes the specified provisioning key.

        Args:
            key_id (str): The unique id of the provisioning key.
            key_type (str): The type ('connector' or 'service_edge').
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.provisioning.delete_provisioning_key('9999', 'connector')
            ...     print("Key deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(
            f"{self._zpa_base_endpoint}/associationType/{simplify_key_type(key_type)}/provisioningKey/{key_id}"
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)
