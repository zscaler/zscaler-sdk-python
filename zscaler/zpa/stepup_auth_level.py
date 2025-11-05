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
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.stepup_auth_level import StepUpAuthLevel
from zscaler.api_client import APIClient
from zscaler.utils import format_url
from zscaler.types import APIResult


class StepUpAuthLevelAPI(APIClient):
    """
    A Client object for the Step Up Auth Level resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def get_step_up_auth_levels(self, query_params: Optional[dict] = None) -> APIResult[List[StepUpAuthLevel]]:
        """
        Get step up authentication levels.

        This endpoint retrieves a list of step up authentication levels configured for the customer.
        Step up authentication levels define the authentication requirements for users based on risk factors.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            :obj:`Tuple`: A tuple containing (list of StepUpAuthLevel instances, Response, error).

        Examples:
            List all step up authentication levels:

            >>> auth_levels, _, err = client.zpa.stepup_auth_level.get_step_up_auth_levels()
            ... if err:
            ...     print(f"Error getting step up auth levels: {err}")
            ...     return
            ... print(f"Total step up auth levels found: {len(auth_levels)}")
            ... for level in auth_levels:
            ...     print(level.as_dict())

            List step up authentication levels with microtenant ID:

            >>> auth_levels, _, err = client.zpa.stepup_auth_level.get_step_up_auth_levels(
            ...     query_params={'microtenant_id': '1234567890'}
            ... )
            ... if err:
            ...     print(f"Error getting step up auth levels: {err}")
            ...     return
            ... print(f"Total step up auth levels found: {len(auth_levels)}")
            ... for level in auth_levels:
            ...     print(f"Name: {level.name}, Delta: {level.delta}, Description: {level.description}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /stepupauthlevel
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, StepUpAuthLevel)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(StepUpAuthLevel(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
