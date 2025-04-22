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
from zscaler.zpa.models.cbi_zpa_profile import ZPACBIProfile
from zscaler.utils import format_url


class CBIZPAProfileAPI(APIClient):
    """
    A Client object for the Cloud Browser Isolation ZPA Profile resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._cbi_base_endpoint = f"/zpa/cbiconfig/cbi/api/customers/{customer_id}"
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_cbi_zpa_profiles(self, query_params=None, **kwargs) -> tuple:
        """
        Returns a list of all cloud browser isolation ZPA profiles, with options to filter by disabled status and scope.

        Args:
            show_disabled (bool, optional): If set to True, the response includes disabled profiles.
            scope_id (str, optional): The unique identifier of the scope of the tenant to filter the profiles.

        Returns:
            :obj:`Tuple`: A tuple containing a list of `ZPAProfile` instances, response object, and error if any.

        Examples:
            >>> profile_list, _, err = client.zpa.cbi_zpa_profile.list_cbi_zpa_profiles()
            ... if err:
            ...     print(f"Error listing cbi profile: {err}")
            ...     return
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /zpaprofiles
        """
        )

        query_params = query_params or {}
        query_params.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body={}, headers={}, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ZPACBIProfile(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_isolation_profiles(self, query_params=None, **kwargs) -> tuple:
        """
        Returns a list of all cloud browser isolation ZPA profiles, with options to filter by disabled status and scope.

        Args:
            show_disabled (bool, optional): If set to True, the response includes disabled profiles.
            scope_id (str, optional): The unique identifier of the scope of the tenant to filter the profiles.

        Returns:
            :obj:`Tuple`: A tuple containing a list of `ZPAProfile` instances, response object, and error if any.

        Examples:
            >>> profile_list, _, err = client.zpa.cbi_zpa_profile.list_isolation_profiles()
            ... if err:
            ...     print(f"Error listing cbi profile: {err}")
            ...     return
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /isolation/profiles
        """
        )

        query_params = query_params or {}
        query_params.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body={}, headers={}, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ZPACBIProfile(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
