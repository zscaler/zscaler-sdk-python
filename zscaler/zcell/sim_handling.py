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

from datetime import datetime

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zcell.models.sim_handling import (
    GetActivationCodeResponse,
    RefreshEsimState,
    SimData,
    SimDataResponse,
    SimHandling,
    SimLockRequest,
    SimUpdateRequest,
)


class SimHandlingAPI(APIClient):

    _zcell_base_endpoint_customer = "/zcell/config/api/v1/customers"

    def __init__(self, request_executor: "RequestExecutor", config: dict = None) -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcell_customer_id = (config or {}).get("client", {}).get("zcellCustomerId")

    def list_sims_details(self, id: str = None, icc_id: str = None, query_params=None) -> APIResult[SimData]:
        """
        Get sim details by icc_id.

        This endpoint returns a single SIM resource (not a paginated list),
        matched by the required ``iccId`` query parameter.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
            icc_id (str): Required query parameter. The ICCID of the SIM to retrieve.
            query_params (dict): Map of query parameters for the request.
                ``[query_params.icc_id]`` {str}: Required. The ICCID (alternatively pass ``icc_id`` directly).

        Returns:
            tuple: (SimData, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection.

        Examples:
            >>> fetched_status, _, error = client.zcell.sim_handling.list_sims_details(
            ...     id='gi754cvqb07r0',
            ...     icc_id='89852350525020075842'
            ... )
            >>> if error:
            ...     print(f"Error fetching SIM details: {error}")
            ...     return
            >>> print(f"SIM details fetched successfully: {fetched_status.as_dict()}")
        """
        http_method = "get".upper()
        id = id or self._zcell_customer_id
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sims/details")

        query_params = query_params or {}
        if icc_id is not None:
            query_params["iccId"] = icc_id

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SimData)
        if error:
            return (None, response, error)
        try:
            result = SimData(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def create_sims_download(self, id: str = None, query_params=None, filename: str = None, **kwargs) -> str:
        """
        Downloads SIM data as a CSV file.

        This endpoint streams a CSV file directly to the response
        (``Content-Type: text/csv``). The response is a file download, not a
        JSON body, so this method writes the stream to disk and returns the
        path to the saved file.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
            query_params (dict, optional): Map of query parameters for the request.

                ``[query_params.sort_by]`` {str}: Field to sort by. Defaults to ``usage``.

                ``[query_params.sort_dir]`` {str}: Sort direction (``ASC`` or ``DESC``). Defaults to ``ASC``.

            filename (str, optional): Custom filename for the CSV file.
                Defaults to a timestamped name.

            **kwargs: Optional request body filters. Supported fields include:
                ``iccid`` (list[str]), ``status`` (str), ``network_status`` (str),
                ``ip_address`` (list[str]), ``location_country`` (str), ``tag`` (list[str]),
                ``device_type`` (str), ``brand_name`` (str), ``marketing_name`` (str),
                ``model_name`` (str), ``form_factor`` (str),
                ``imei_status`` (str: ``Locked``, ``Unlocked``, ``InProgress``).

        Returns:
            str: Path to the downloaded CSV file.

        Examples:
            Download SIM data as a CSV:

            >>> try:
            ...     # Invoke the create_sims_download method with correct parameters
            ...     filename = client.zcell.sim_handling.create_sims_download(
            ...         id='gi754cvqb07r0',
            ...         query_params={"sort_by": "usage", "sort_dir": "ASC"},
            ...         status="active",
            ...         filename="zcell_sims.csv",
            ...     )
            ...     print(f"SIM data downloaded successfully: {filename}")
            ... except Exception as e:
            ...     print(f"Error during download: {e}")
        """
        query_params = query_params or {}

        if not filename:
            filename = f"zcell-sims-{datetime.now().strftime('%Y%m%d-%H_%M_%S')}.csv"

        http_method = "post".upper()
        id = id or self._zcell_customer_id
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sims/download")

        body = kwargs
        headers = {"Accept": "*/*"}

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
            headers=headers,
            params=query_params,
        )
        if error:
            raise Exception("Error creating request for downloading SIM data.")

        response, error = self._request_executor.execute(request, return_raw_response=True)
        if error:
            raise error
        if response is None:
            raise Exception("No response received when downloading SIM data.")

        content_type = response.headers.get("Content-Type", "").lower()
        if not content_type.startswith("text/csv") and not content_type.startswith("application/octet-stream"):
            raise Exception("Invalid response content type or unexpected response format.")

        with open(filename, "wb") as f:
            f.write(response.content)

        return filename

    def update_sims_assign_tag(self, id: str = None, **kwargs) -> APIResult[SimHandling]:
        """
        Assigns a tag to the sim.

        This endpoint returns ``204 No Content`` on success (no response body),
        so ``result`` is ``None`` when the assignment succeeds. Use the returned
        ``response`` (e.g. ``response.get_status()``) to confirm success.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
            **kwargs: Request body fields.

                ``icc_id`` (str): The ICCID of the SIM to tag.

                ``tag_ids`` (list[str]): The tag IDs to assign to the SIM.

        Returns:
            tuple: (None, Response, error)

        Examples:
            >>> _, response, error = client.zcell.sim_handling.update_sims_assign_tag(
            ...     id='gi754cvqb07r0',
            ...     tag_ids=['1558'],
            ...     icc_id='89852350525020075842'
            ... )
            >>> if error:
            ...     print(f"Error updating SIM tag: {error}")
            ...     return
            >>> # This endpoint returns 204 No Content (no response body).
            >>> print(f"SIM tag assigned successfully (status {response.get_status()}).")
        """
        http_method = "patch".upper()
        id = id or self._zcell_customer_id
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

        # The API returns 204 No Content on success — there is no body to parse.
        if not response or not response.get_body():
            return (None, response, None)

        try:
            result = SimHandling(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_sims_lock(self, id: str = None, **kwargs) -> APIResult[SimLockRequest]:
        """
        Lock the sims for provided sim ids.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
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
        id = id or self._zcell_customer_id
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

        # The API returns 204 No Content on success — there is no body to parse.
        if not response or not response.get_body():
            return (None, response, None)

        try:
            result = SimLockRequest(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def create_sims_search(self, id: str = None, **kwargs) -> APIResult[SimDataResponse]:
        """
        Get all sims data with filter and pagination.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
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
        id = id or self._zcell_customer_id
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

    def update_sims_status(self, id: str = None, **kwargs) -> APIResult[SimUpdateRequest]:
        """
        Update the sim status for provided sim ids.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
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
        id = id or self._zcell_customer_id
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

        # The API returns 204 No Content on success — there is no body to parse.
        if not response or not response.get_body():
            return (None, response, None)

        try:
            result = SimUpdateRequest(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_sims_assign(self, id: str = None, iccid: str = None, **kwargs) -> APIResult[GetActivationCodeResponse]:
        """
        Assigns an eSIM to the user email and gives back the activation code.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
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
        id = id or self._zcell_customer_id
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

        # The API returns 204 No Content on success — there is no body to parse.
        if not response or not response.get_body():
            return (None, response, None)

        try:
            result = GetActivationCodeResponse(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_sims_state(self, id: str = None, iccid: str = None, **kwargs) -> APIResult[RefreshEsimState]:
        """
        Fetch and Refresh Provider eSim State.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
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
        id = id or self._zcell_customer_id
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

        # The API returns 204 No Content on success — there is no body to parse.
        if not response or not response.get_body():
            return (None, response, None)

        try:
            result = RefreshEsimState(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
