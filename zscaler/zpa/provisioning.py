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
from zscaler.zpa.models.provisioning_keys import ProvisioningKey
from zscaler.utils import format_url


def simplify_key_type(key_type):
    """
    Simplifies the key type for the user. Accepted values are 'connector' and 'service_edge'.

    Args:
        key_type (str): The key type provided by the user.

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

    def list_provisioning_keys(self, key_type: str, query_params=None) -> tuple:
        """
        Returns a list of all configured provisioning keys that match the specified ``key_type``.

        Args:
            key_type (str): The type of provisioning key. Accepted values are:
                ``connector`` and ``service_edge``.

            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            tuple: A tuple containing (list of ProvisioningKey instances, Response, error)

        Examples:
            List all App Connector Groups provisioning keys:

            >>> key_list, _, err = client.zpa.provisioning.list_provisioning_keys(
            ... key_type=connector
            ... query_params={'search': 'Connector_ProvKey01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing provisioning key: {err}")
            ...     return
            ... print(f"Total provisioning key found: {len(key_list)}")
            ... for key in key_list:
            ...     print(keys.as_dict())

            List all Service Edge Groups provisioning keys:

            >>> key_list, _, err = client.zpa.provisioning.list_provisioning_keys(
            ... key_type=service_edge
            ... query_params={'search': 'ServiceEdge_ProvKey01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing provisioning key: {err}")
            ...     return
            ... print(f"Total provisioning key found: {len(key_list)}")
            ... for key in key_list:
            ...     print(keys.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /associationType/{simplify_key_type(key_type)}/provisioningKey
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ProvisioningKey)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ProvisioningKey(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_provisioning_key(self, key_id: str, key_type: str, query_params=None) -> tuple:
        """
        Returns information on the specified provisioning key.

        Args:
            key_id (str): The unique id of the provisioning key.
            key_type (str): The type of provisioning key, accepted values are:
                ``connector`` and ``service_edge``.

            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: The requested provisioning key resource record.

        Examples:
            Get the specified App Connector key.

        Examples:
            >>> fetched_key, _, err = client.zpa.provisioning.get_provisioning_key(
                key_id='9999', key_type=connector
            ... if err:
            ...     print(f"Error fetching provisioning key by ID: {err}")
            ...     return
            ... print(f"Fetched provisioning key by ID: {fetched_key.as_dict()}")

            Get the specified Service Edge key.

            >>> fetched_key, _, err = client.zpa.provisioning.get_provisioning_key(
                key_id='9999', key_type=service_edge
            ... if err:
            ...     print(f"Error fetching provisioning key by ID: {err}")
            ...     return
            ... print(f"Fetched provisioning key by ID: {fetched_key.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /associationType/{simplify_key_type(key_type)}/provisioningKey/{key_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ProvisioningKey)
        if error:
            return (None, response, error)

        try:
            result = ProvisioningKey(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_provisioning_key(self, key_type: str, **kwargs) -> tuple:
        """
        Adds a new provisioning key to ZPA.

        Args:
            key_type (str): The type of provisioning key, accepted values are:
                ``connector`` and ``service_edge``.
            name (str): The name of the provisioning key.
            max_usage (int): The maximum amount of times this key can be used.
            enrollment_cert_id (str): The unique id of the enrollment certificate for this provisioning key.
            component_id (str): The unique id of the component linked to this provisioning key.
            microtenant_id (str, optional): The microtenant ID if applicable.

            **kwargs: Additional optional attributes.

        Returns:
            :obj:`Tuple`: The newly created Provisioning Key resource record.

        Examples:
            >>> new_prov_key, _, err = zpa.provisioning.add_provisioning_key(
            ...     key_type=key_type,
            ...     name=f"NewProvisioningKey_{random.randint(1000, 10000)}",
            ...     description=f"NewProvisioningKey_{random.randint(1000, 10000)}",
            ...     max_usage="10",
            ...     enrollment_cert_id="2519",
            ...     component_id="72058304855047746",
            ... )
            ... if err:
            ...     print(f"Error creating provisioning key: {err}")
            ...     return
            ... print(f"provisioning key created successfully: {new_prov_key.as_dict()}")
        """
        if not key_type:
            raise ValueError("key_type must be provided.")

        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /associationType/{simplify_key_type(key_type)}/provisioningKey
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        name = body.pop("name", None)
        max_usage = body.pop("max_usage", None)
        enrollment_cert_id = body.get("enrollment_cert_id")
        component_id = body.get("component_id")

        body.update(
            {"name": name, "maxUsage": max_usage, "enrollmentCertId": enrollment_cert_id, "zcomponentId": component_id}
        )

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ProvisioningKey)
        if error:
            return (None, response, error)

        try:
            result = ProvisioningKey(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def update_provisioning_key(self, key_id: str, key_type: str, **kwargs) -> tuple:
        """
        Updates the specified provisioning key.

        Args:
            key_id (str): The unique id of the Provisioning Key being updated.
            key_type (str): The type of provisioning key, accepted values are:
                ``connector`` and ``service_edge``.

        Keyword Args:
            name (str, optional): The new name for the provisioning key.
            max_usage (int, optional): The new maximum usage count.
            enrollment_cert_id (str, optional): The enrollment certificate ID to associate.
            component_id (str, optional): The component ID to associate (mapped to zcomponentId).
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            :obj:`Tuple`: The updated Provisioning Key resource record.

        Examples:

            Updated Provisioning Key `max_usage` to `20`
            >>> update_prov_key, _, err = zpa.provisioning.add_provisioning_key(
            ...     key_type=key_type,
            ...     name=f"NewProvisioningKey_{random.randint(1000, 10000)}",
            ...     description=f"NewProvisioningKey_{random.randint(1000, 10000)}",
            ...     max_usage="20",
            ...     enrollment_cert_id="2519",
            ...     component_id="72058304855047746",
            ... )
            ... if err:
            ...     print(f"Error creating provisioning key: {err}")
            ...     return
            ... print(f"provisioning key created successfully: {new_prov_key.as_dict()}")
        """
        if not key_type:
            raise ValueError("key_type must be provided.")

        http_method = "PUT"
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /associationType/{simplify_key_type(key_type)}/provisioningKey/{key_id}
            """
        )

        body = kwargs
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body, params, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ProvisioningKey)
        if error:
            return (None, response, error)

        if response is None:
            return (ProvisioningKey({"id": key_id}), None, None)

        try:
            result = ProvisioningKey(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def delete_provisioning_key(self, key_id: str, key_type: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified provisioning key from ZPA.

        Args:
            key_id (str): The unique id of the provisioning key that will be deleted.
            key_type (str): The type of provisioning key, accepted values are:

                ``connector`` and ``service_edge``.
            **kwargs: Optional keyword args.

        Keyword Args:
            microtenant_id (str): The microtenant ID to be used for this request.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            Delete a Service Edge provisioning key:

            >>> _, _, err = client.zpa.provisioning.delete_provisioning_key(
            ... key_id='9999', key_type='connector')
            ... if err:
            ...     print(f"Error deleting provisioning key: {err}")
            ...     return
            ... print(f"provisioning key with ID {updated_key.id} deleted successfully.")

        Examples:

            Delete a Service Edge provisioning key:

            >>> _, _, err = client.zpa.provisioning.delete_provisioning_key(
            ... key_id='9999', key_type='service_edge')
            ... if err:
            ...     print(f"Error deleting provisioning key: {err}")
            ...     return
            ... print(f"provisioning key with ID {updated_key.id} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /associationType/{simplify_key_type(key_type)}/provisioningKey/{key_id}
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
