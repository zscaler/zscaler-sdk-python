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
from zscaler.ztw.models.provisioning_url import ProvisioningURL
from zscaler.utils import format_url
from zscaler.types import APIResult


class ProvisioningURLAPI(APIClient):
    """
    A Client object for the ProvisioningURLAPI resource.
    """

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_provisioning_url(self, query_params: Optional[dict] = None) -> APIResult[List[ProvisioningURL]]:
        """
        List all provisioning URLs.

        Keyword Args:
            query_params {dict}: Optional query parameters.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size. The default size is 250.

        Returns:
            :obj:`Tuple`: The list of provisioning URLs.

        Examples:
            Print all provisioning URLs::

                roles = ztw.provisioning.list_provisioning_url()
                for role in roles:
                    print(role)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /provUrl
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
                result.append(ProvisioningURL(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_provisioning_url(self, provision_id: str) -> APIResult[dict]:
        """
        Get details for a provisioning template by ID.

        Args:
            provision_id (str): ID of Cloud & Branch Connector provisioning template.

        Returns:
            :obj:`Tuple`: The provisiong template url details.

        Examples:
            Print the details of a provisioning template url:

                print(ztw.provisioning.get_provisioning_url("123456789")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /provUrl/{provision_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ProvisioningURL)
        if error:
            return (None, response, error)

        try:
            result = ProvisioningURL(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_provisioning_url(self, **kwargs) -> APIResult[dict]:
        """
        Adds a new Provisioning URL.

        Args:
            name (str): The name of the provisioning URL.
            desc (str): Additional information for the provisioning URL.
            prov_url_type (str): The type of provisioning URL. Supported values: ``CLOUD``, ``BRANCH``.
            prov_url_data (dict): The provisioning URL data containing:
                - location_template (dict): Location template with ``id``.
                - cloud_provider_type (str): Cloud provider type (e.g., ``AWS``, ``AZURE``, ``GCP``).
                - form_factor (str): Form factor (e.g., ``SMALL``, ``MEDIUM``, ``LARGE``).
                - release_channel (str): Release channel (e.g., ``LATEST``, ``STABLE``).

        Returns:
            tuple: The new provisioning URL resource record.

        Examples:
            Add a new provisioning URL:

            >>> added_prov_url, _, error = client.ztw.provisioning_url.add_provisioning_url(
            ...     name="AWS_CAN02",
            ...     desc="AWS_CAN02_Description",
            ...     prov_url_type="CLOUD",
            ...     prov_url_data={
            ...         "location_template": {
            ...             "id": 82521
            ...         },
            ...         "cloud_provider_type": "AWS",
            ...         "form_factor": "SMALL",
            ...         "release_channel": "LATEST"
            ...     }
            ... )
            >>> if error:
            ...     print(f"Error adding provisioning URL: {error}")
            ...     return
            ... print(f"Provisioning URL added successfully: {added_prov_url.as_dict()}")

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /provUrl
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, ProvisioningURL)
        if error:
            return (None, response, error)

        try:
            result = ProvisioningURL(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_provisioning_url(self, provision_id: int, **kwargs) -> APIResult[dict]:
        """
        Updates information for the specified Provisioning URL.

        Args:
            provision_id (int): The unique ID for the Provisioning URL.
            name (str): The name of the provisioning URL.
            desc (str): Additional information for the provisioning URL.
            prov_url_type (str): The type of provisioning URL. Supported values: ``CLOUD``, ``BRANCH``.
            prov_url_data (dict): The provisioning URL data containing:
                - location_template (dict): Location template with ``id``.
                - cloud_provider_type (str): Cloud provider type (e.g., ``AWS``, ``AZURE``, ``GCP``).
                - form_factor (str): Form factor (e.g., ``SMALL``, ``MEDIUM``, ``LARGE``).
                - release_channel (str): Release channel (e.g., ``LATEST``, ``STABLE``).

        Returns:
            tuple: A tuple containing the updated Provisioning URL, response, and error.

        Examples:
            Update an existing Provisioning URL:

            >>> updated_prov_url, _, error = client.ztw.provisioning_url.update_provisioning_url(
            ...     provision_id=added_prov_url.id,
            ...     name="AWS_CAN02",
            ...     desc="AWS_CAN02_Updated_Description",
            ...     prov_url_type="CLOUD",
            ...     prov_url_data={
            ...         "location_template": {
            ...             "id": 82521
            ...         },
            ...         "cloud_provider_type": "AWS",
            ...         "form_factor": "SMALL",
            ...         "release_channel": "LATEST"
            ...     }
            ... )
            >>> if error:
            ...     print(f"Error updating provisioning URL: {error}")
            ...     return
            ... print(f"Provisioning URL updated successfully: {updated_prov_url.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /provUrl/{provision_id}
        """
        )
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ProvisioningURL)
        if error:
            return (None, response, error)

        try:
            result = ProvisioningURL(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_provisioning_url(self, provision_id: int) -> APIResult[dict]:
        """
        Deletes a provisioning URL.

        Args:
            provision_id (str): The unique ID of the provisioning URL to be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, response, error = client.ztw.provisioning.delete_provisioning_url('545845')
            ... if error:
            ...     print(f"Error deleting provisioning URL: {error}")
            ... return

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /provUrl/{provision_id}
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
