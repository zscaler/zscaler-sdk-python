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
from zscaler.utils import format_url
from zscaler.zcc.models.forwardingprofile import ForwardingProfile


class ForwardingProfileAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    def list_by_company(self, query_params=None) -> tuple:
        """
        Returns the list of Forwarding Profiles By Company ID in the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Specifies the page size.
                ``[query_params.search]`` {str}: The search string used to partially match.

        Returns:
            :obj:`list`: A list containing Forwarding Profiles By Company ID in the Client Connector Portal.

        Examples:
            List all Forwarding Profile:

            >>> profile_list, response, error = client.zcc.forwarding_profile.list_by_company()
            >>>     if error:
            ...         print(f"Error listing forwarding profiles: {error}")
            ...         return
            ...     for profile in profile_list:
            ...         print(profile.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /webForwardingProfile/listByCompany
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
                result.append(ForwardingProfile(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_forwarding_profile(self, **kwargs) -> tuple:
        """
       Updates a forwarding profile.

        Args:
            N/A

        Returns:
            tuple: A tuple containing the Create Forwarding Profile, response, and error.

        Examples:
           Updates a forwarding profile.

            >>> updated_profile, response, error = client.zcc.forwarding_profile.update_forwarding_profile(
            ...     name=ForwardingProfile01,
            ...     hostname='server.acme.com',
            ...     Resolved_ips_for_hostname='8.8.8.8',
            ... )
            >>> if error:
            ...     print(f"Error adding forwwarding profile: {error}")
            ...     return
            ... print(f"Forwwarding profile added successfully: {updated_profile.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /webForwardingProfile/edit
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ForwardingProfile)
        if error:
            return (None, response, error)

        try:
            result = ForwardingProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_forwarding_profile(self, profile_id: int) -> tuple:
        """
        Deletes the specified Forwarding Profile.

        Args:
            profile_id (str): The unique identifier of the Forwarding Profile.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete an existing Forwarding Profile:

            >>> _, _, error = client.zcc.forwarding_profile.delete_forwarding_profile('541244')
            >>> if error:
            ...     print(f"Error deleting Forwarding Profile: {error}")
            ...     return
            ... print(f"Forwarding Profile with ID '541244' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zcc_base_endpoint}
            /webForwardingProfile/{profile_id}/delete
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
