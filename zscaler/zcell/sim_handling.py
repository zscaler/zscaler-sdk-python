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

from typing import List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zcell.models.sim_handling import (
    GetActivationCodeResponse,
    RefreshEsimState,
    SimData,
    SimDataResponse,
    SimDataSearchRequest,
    SimHandling,
    SimLockRequest,
    SimUpdateRequest,
)


class SimHandlingAPI(APIClient):

    _zcell_base_endpoint_customer = "/zcell/config/api/v1/customers"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def update_sims_assign_tag(self, id: str, **kwargs) -> APIResult[SimHandling]:
        """
        Assigns a tag to the sim.

        Args:
            id (str): Path parameter.
            **kwargs: Request body fields.

        Returns:
            tuple: (result, Response, error)

        Examples:
            >>> result, response, error = client.zcell.sim_handling.update_sims_assign_tag(id='...', name='example')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> print(result.as_dict())
        """
        http_method = "patch".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sims/assign/tag")

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SimHandling)
        if error:
            return (None, response, error)
        try:
            result = SimHandling(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_sims_details(self, id: str, query_params=None) -> APIResult[List[SimData]]:
        """
        Get sim details by iccId.

        Args:
            id (str): Path parameter.
            query_params (dict): Map of query parameters for the request.
                ``[query_params.icc_id]`` {str}: Required

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            >>> results, response, error = client.zcell.sim_handling.list_sims_details(id='...')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> for item in results:
            ...     print(item.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sims/details")

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
                result.append(SimData(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def create_sims_download(self, id: str, **kwargs) -> APIResult[SimDataSearchRequest]:
        """
        Sim data file download.

        Args:
            id (str): Path parameter.
            **kwargs: Request body fields.

        Returns:
            tuple: (result, Response, error)

        Examples:
            >>> result, response, error = client.zcell.sim_handling.create_sims_download(id='...', name='example')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> print(result.as_dict())
        """
        http_method = "post".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sims/download")

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SimDataSearchRequest)
        if error:
            return (None, response, error)
        try:
            result = SimDataSearchRequest(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_sims_lock(self, id: str, **kwargs) -> APIResult[SimLockRequest]:
        """
        Lock the sims for provided sim ids.

        Args:
            id (str): Path parameter.
            **kwargs: Request body fields.

        Returns:
            tuple: (result, Response, error)

        Examples:
            >>> result, response, error = client.zcell.sim_handling.update_sims_lock(id='...', name='example')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> print(result.as_dict())
        """
        http_method = "patch".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sims/lock")

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SimLockRequest)
        if error:
            return (None, response, error)
        try:
            result = SimLockRequest(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def create_sims_search(self, id: str, **kwargs) -> APIResult[SimDataResponse]:
        """
        Get all sims data with filter and pagination.

        Args:
            id (str): Path parameter.
            **kwargs: Request body fields.

        Returns:
            tuple: (result, Response, error)

        Examples:
            >>> result, response, error = client.zcell.sim_handling.create_sims_search(id='...', name='example')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> print(result.as_dict())
        """
        http_method = "post".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sims/search")

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SimDataResponse)
        if error:
            return (None, response, error)
        try:
            result = SimDataResponse(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_sims_status(self, id: str, **kwargs) -> APIResult[SimUpdateRequest]:
        """
        Update the sim status for provided sim ids.

        Args:
            id (str): Path parameter.
            **kwargs: Request body fields.

        Returns:
            tuple: (result, Response, error)

        Examples:
            >>> result, response, error = client.zcell.sim_handling.update_sims_status(id='...', name='example')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> print(result.as_dict())
        """
        http_method = "patch".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sims/status")

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SimUpdateRequest)
        if error:
            return (None, response, error)
        try:
            result = SimUpdateRequest(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_sims_assign(self, id: str, iccid: str, **kwargs) -> APIResult[GetActivationCodeResponse]:
        """
        Assigns an eSIM to the user email and gives back the activation code.

        Args:
            id (str): Path parameter.
            iccid (str): Path parameter.
            **kwargs: Request body fields.

        Returns:
            tuple: (result, Response, error)

        Examples:
            >>> result, response, error = client.zcell.sim_handling.update_sims_assign(
            ...     id='...',
            ...     iccid='...',
            ...     name='example',
            ... )
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> print(result.as_dict())
        """
        http_method = "patch".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sims/{iccid}/assign")

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, GetActivationCodeResponse)
        if error:
            return (None, response, error)
        try:
            result = GetActivationCodeResponse(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_sims_state(self, id: str, iccid: str, **kwargs) -> APIResult[RefreshEsimState]:
        """
        Fetch and Refresh Provider eSim State.

        Args:
            id (str): Path parameter.
            iccid (str): Path parameter.
            **kwargs: Request body fields.

        Returns:
            tuple: (result, Response, error)

        Examples:
            >>> result, response, error = client.zcell.sim_handling.update_sims_state(
            ...     id='...',
            ...     iccid='...',
            ...     name='example',
            ... )
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> print(result.as_dict())
        """
        http_method = "patch".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sims/{iccid}/state")

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, RefreshEsimState)
        if error:
            return (None, response, error)
        try:
            result = RefreshEsimState(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
