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

from typing import Dict, List, Optional, Any, Union
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.pra_cred_pool_controller import PRACredentialPoolController
from zscaler.utils import format_url, add_id_groups


class PRACredentialPoolAPI(APIClient):
    """
    A Client object for the Privileged Remote Access Credential Pool resource.
    """

    reformat_params = [
        ("credential_ids", "credentials"),
    ]

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/waap-pra-config/v1/admin/customers/{customer_id}"

    def list_credential_pool(self, query_params: Optional[dict] = None) -> List[PRACredentialPoolController]:
        """
        Returns a list of all privileged remote access credential pool details.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.
                ``[query_params.sort_by]`` {str}: Indicates the parameter to sort by.
                ``[query_params.sort_dir]`` {str}: Specifies the sort direction. Supported Values: ASC and DESC

        Returns:

        Examples:
            >>> try:
            ...     credential_list = client.zpa.pra_credential.list_credential_pool(
            ... query_params={'search': 'pra_console01', 'page': '1', 'page_size': '100'})
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"Total pra credentials found: {len(credential_list)}")
            ... for pra in credential_list:
            ...     print(pra.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /credential-pool
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, PRACredentialPoolController)
        result = []
        for item in response.get_results():
            result.append(PRACredentialPoolController(self.form_response_body(item)))
        return result

    def get_credential_pool(self, pool_id: str, query_params: Optional[dict] = None) -> PRACredentialPoolController:
        """
        Gets information on the specified Privileged credential pool.

        Args:
            pool_id (str): The unique identifier of the Privileged credential pool.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: PRACredentialPoolController: The corresponding PRA Credential Pool object.

        Example:
            Retrieve details of a specific Privileged credential pool

            >>> try:
            ...     fetched_pool = client.zpa.pra_credential_pool.get_credential_pool('999999')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"Fetched Privileged credential pool by ID: {fetched_pool.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /credential-pool/{pool_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, PRACredentialPoolController)
        result = PRACredentialPoolController(self.form_response_body(response.get_body()))
        return result

    def get_credential_pool_info(self, pool_id: str, query_params: Optional[dict] = None) -> PRACredentialPoolController:
        """
        Given Privileged credential pool id gets mapped privileged credential info

        Args:
            pool_id (str): The unique identifier of the Privileged credential pool.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: PRACredentialPoolController: The corresponding PRA Credential Pool object.

        Example:
            Retrieve details of a specific Privileged credential pool

            >>> try:
            ...     fetched_pool = client.zpa.pra_credential_pool.get_credential_pool_info('999999')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"Fetched Privileged credential pool by ID: {fetched_pool.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /credential-pool/{pool_id}/credential
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, PRACredentialPoolController)
        result = []
        for item in response.get_results():
            result.append(PRACredentialPoolController(self.form_response_body(item)))
        return result

    def add_credential_pool(self, **kwargs) -> PRACredentialPoolController:
        """
        Adds a new Privileged Credential Pool.

        Args:
            name (str): The name of the credential.
            credential_type (str): The type of credential ('USERNAME_PASSWORD', 'SSH_KEY', 'PASSWORD').
            credentials (list): List of credential IDs

        Returns:
            :obj:`Tuple`: PRACredentialPoolController: The created Privileged Credential Pool object.

        Examples:

            >>> try:
            ...     add_pool = client.zpa.pra_credential_pool.update_credential_pool(
            ...    name='New_Credential_Pool',
            ...    credential_ids=['124545', '12545'],
            ...    credential_type='USERNAME_PASSWORD'
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"Privileged credential pool added successfully: {add_pool.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /credential-pool
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "credential_ids" in body:
            body["credentials"] = [{"id": credential_id} for credential_id in body.pop("credential_ids")]

        add_id_groups(self.reformat_params, kwargs, body)

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, PRACredentialPoolController)
        result = PRACredentialPoolController(self.form_response_body(response.get_body()))
        return result

    def update_credential_pool(self, pool_id: str, **kwargs) -> PRACredentialPoolController:
        """
        Updates a Privileged credential pool.

        Args:
            pool_id (str): The unique identifier for the Privileged credential pool.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            :obj:`Tuple`: A tuple containing PRACredential

        Examples:

            >>> try:
            ...     update_pool = client.zpa.pra_credential_pool.update_credential_pool(
            ...    pool_id="999999",
            ...    name='Update_Credential_Pool',
            ...    credential_ids=['124545', '12545'],
            ...    credential_type='USERNAME_PASSWORD'
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"Privileged credential pool added successfully: {update_pool.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /credential-pool/{pool_id}
        """
        )

        body = {}

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "credential_ids" in body:
            body["credentials"] = [{"id": credential_id} for credential_id in body.pop("credential_ids")]

        add_id_groups(self.reformat_params, kwargs, body)

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, PRACredentialPoolController)
        if response is None:
            return PRACredentialPoolController({"id": pool_id})

        result = PRACredentialPoolController(self.form_response_body(response.get_body()))
        return result

    def delete_credential_pool(self, pool_id: str, microtenant_id: str = None) -> None:
        """
        Deletes the specified privileged credential pool.

        Args:
            pool_id (str): The unique id for the privileged credential pool to be deleted.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:

        Examples:
            >>> try:
            ...     _ = client.zpa.pra_credential_pool.delete_credential_pool(
            ...     pool_id='999999'
            ... )
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"privileged credential pools with ID {'999999'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /credential-pool/{pool_id}
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        response = self._request_executor.execute(request)
        return None
