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
from zscaler.zia.models.traffic_vpn_credentials import TrafficVPNCredentials
from zscaler.utils import format_url


class TrafficVPNCredentialAPI(APIClient):
    """
    A Client object for the Traffic Forwarding VPN Credentials resources.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_vpn_credentials(self, query_params=None) -> tuple:
        """
        Returns the list of all configured VPN credentials with optional filtering.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.type]`` {str}: The type of VPN credential. Must be one of 'CN', 'IP', 'UFQDN', 'XAUTH'.

                ``[query_params.include_only_without_location]`` {bool}: Include VPN credential only
                    if not associated with any location.

                ``[query_params.location_id]`` {int}: Gets the VPN credentials for the specified location ID.
                ``[query_params.managed_by]`` {int}: Gets the VPN credentials managed by the given partner.

        Returns:
            tuple: A tuple containing (list of VPN credentials instances, Response, error)

        Examples:
            List VPN credentials of type UFQDN:

            >>> credentials_list, _, err = client.zia.traffic_vpn_credentials.list_vpn_credentials(
                query_params={"type": "UFQDN"})
            ... if err:
            ...     print(f"Error listing credentials: {err}")
            ...     return
            ... print(f"Total UFQDN credentials found: {len(credentials_list)}")
            ... for credential in credentials_list:
            ...     print(credential.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /vpnCredentials
        """
        )

        query_params = query_params or {}

        # Validate the 'type' parameter if provided
        if "type" in query_params:
            valid_types = ["CN", "IP", "UFQDN", "XAUTH"]
            if query_params["type"] not in valid_types:
                return (
                    None,
                    None,
                    ValueError(f"Invalid type '{query_params['type']}' provided. Must be one of {valid_types}."),
                )

        # Prepare request body and headers
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(TrafficVPNCredentials(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_vpn_credential(self, credential_id: int) -> tuple:
        """
        Get VPN credentials for the specified ID or fqdn.

        Args:
            credential_id (str, optional):
                The unique identifier for the VPN credentials.
            fqdn (str, optional):
                The unique FQDN for the VPN credentials.

        Returns:
            :obj:`tuple`: The resource record for the requested VPN credentials.

        Examples:
            >>> pprint(zia.traffic.get_vpn_credential('97679391'))

            >>> pprint(zia.traffic.get_vpn_credential(fqdn='userid@fqdn'))

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /vpnCredentials/{credential_id}
            """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TrafficVPNCredentials)

        if error:
            return (None, response, error)

        try:
            result = TrafficVPNCredentials(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_vpn_credential(self, **kwargs) -> tuple:
        """
        Add new VPN credentials.

        Args:
            credential (dict):
                A dictionary representing the VPN credential to be created.
                It must include ``type`` (either ``IP`` or ``UFQDN``) and ``pre_shared_key``.

                For example::

                    {
                        "type": "UFQDN",
                        "fqdn": "example@domain.com",
                        "pre_shared_key": "my_key",
                        "comments": "Optional comments",
                        "location_id": 12345
                    }

        Returns:
            tuple:
                The newly created VPN credential resource record, accompanied by the response object and any error.

        Raises:
            ValueError:
                If required arguments are not provided or invalid.
        """
        # Validate the `type`
        valid_types = ["IP", "UFQDN"]
        if "type" not in kwargs or kwargs["type"] not in valid_types:
            return (None, None, ValueError(f"Invalid type. Must be one of {valid_types}."))

        # Validate the `pre_shared_key`
        if "pre_shared_key" not in kwargs:
            return (None, None, ValueError("Pre-shared key must be provided."))

        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /vpnCredentials
        """
        )

        # Prepare the request body from kwargs
        body = kwargs
        headers = {}

        request, error = self._request_executor.create_request(
            method=http_method, endpoint=api_url, body=body, headers=headers
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TrafficVPNCredentials)

        if error:
            return (None, response, error)

        try:
            result = TrafficVPNCredentials(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_vpn_credential(self, credential_id: int, **kwargs) -> tuple:
        """
        Update VPN credentials with the specified ID.

        Args:
            credential_id (int):
                The unique identifier for the credential that will be updated.
            credential (dict or VPNCredential object):
                The data for the VPN credential that is being updated.

        Returns:
            :obj:`tuple`: The newly updated VPN credential resource record.

        Raises:
            ValueError: If certain fields are invalid or attempted to be modified (i.e., type, fqdn, ipAddress).

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /vpnCredentials/{credential_id}
        """
        )

        # Retrieve the current VPN credential for validation
        current_credential, _, err = self.get_vpn_credential(credential_id)
        if err:
            return (None, None, err)

        # Validate that the `type` cannot be changed
        if "type" in kwargs and kwargs["type"] != current_credential.type:
            return (None, None, ValueError("The VPN credential type cannot be changed once created."))

        # Validate that the `fqdn` and `ipAddress` cannot be changed
        if current_credential.type == "UFQDN":
            if "fqdn" in kwargs and kwargs["fqdn"] != current_credential.fqdn:
                return (None, None, ValueError("The fqdn cannot be changed once created."))
        elif current_credential.type == "IP":
            if "ip_address" in kwargs and kwargs["ip_address"] != current_credential.ip_address:
                return (None, None, ValueError("The IP address cannot be changed once created."))

        # Prepare the request body from kwargs
        body = kwargs
        headers = {}

        # Create the request after passing validation
        request, error = self._request_executor.create_request(
            method=http_method, endpoint=api_url, body=body, headers=headers
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, TrafficVPNCredentials)

        if error:
            return (None, response, error)

        # Parse the response
        try:
            result = TrafficVPNCredentials(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def delete_vpn_credential(self, credential_id: int) -> tuple:
        """
        Delete VPN credentials for the specified ID.

        Args:
            credential_id (str):
                The unique identifier for the VPN credentials that will be deleted.

        Returns:
            :obj:`tuple`: Response code for the operation.

        Examples:
            >>> zia.traffic.delete_vpn_credential('97679391')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""{
            self._zia_base_endpoint}
            /vpnCredentials/{credential_id}
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

    def bulk_delete_vpn_credentials(self, credential_ids: list) -> tuple:
        """
        Bulk delete VPN credentials.

        Args:
            credential_ids (list): List containing IDs of each vpn credential that will be deleted.

        Returns:
            :obj:`tuple`: Response code for operation.

        Examples:
            >>> zia.traffic.bulk_delete_vpn_credentials(['94963984', '97679232'])

        """
        # Validate input before making the request
        if not credential_ids:
            return (None, ValueError("Empty credential_ids list provided"))

        if len(credential_ids) > 100:
            return (None, ValueError("Maximum 100 credential IDs allowed per bulk delete request"))

        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /vpnCredentials/bulkDelete
        """
        )

        payload = {"ids": credential_ids}

        request, error = self._request_executor.create_request(
            method=http_method, endpoint=api_url, body=payload, headers={}, params={}
        )
        if error:
            return (None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        # ✅ Return a 3-tuple, even if response is None (e.g., 204 No Content)
        return (None, response, None)
